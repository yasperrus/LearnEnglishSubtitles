import os
import sys
from typing import List

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from config import ROOT_DIR
from src.data import LearnedWord
from src.improvements.Switch3 import (
    replace_checkbox_with_switch,
)
from src.repositories.learned_word_repository import LearnedWordRepository
from src.repositories.learning_word_repository import LearningWordRepository
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.ViewWord import ViewWord
from src.widgets.WidgetVerticalLayoutScroll import WidgetVerticalLayoutScroll


class WidgetVerticalLayoutScrollForWords(WidgetVerticalLayoutScroll):

    def __init__(self, items: List, learned_words: List[LearnedWord], user_id: int):
        self.user_id = user_id
        super().__init__(items, learned_words)

    def init_different(self):
        self.repo_learning_word = LearningWordRepository()
        self.learning_words = self.repo_learning_word.gets_by_user_id(self.user_id)
        ui_file = os.path.join(
            ROOT_DIR, "res", "uis", "widget_vertical_layout_scroll_for_words.ui"
        )
        self.window = uic.loadUi(ui_file, self)
        # uic.loadUi(ui_file, self)
        # self.but_is_filter.setChecked(False)
        self.but_is_filter.setChecked(True)
        self.widget_filter.setVisible(self.but_is_filter.isChecked())

        self.check_box_hide_learned_words = replace_checkbox_with_switch(
            self.check_box_hide_learned_words
        )
        self.check_box_hide_learned_words.toggled.connect(self.apply_filter)

        self.check_box_show_hard_words_only = replace_checkbox_with_switch(
            self.check_box_show_hard_words_only
        )
        self.check_box_show_hard_words_only.toggled.connect(self.apply_filter)

    def apply_filter(self):
        print(self.check_box_hide_learned_words.isChecked())
        if self.timer_filter:
            self.timer_filter.stop()
        text = self.line_edit_search.text().strip().lower()
        # self.filtered_items = (
        #     [item for item in self.items if text in item.name.lower()]
        #     if text
        #     else list(self.items)
        # )

        self.filtered_items = [
            item
            for item in self.items
            if (not text or text in item.name.lower())
            and (
                not self.check_box_hide_learned_words.isChecked()
                or item.id not in self.leaned_words_ids
            )
            and (
                not self.check_box_show_hard_words_only.isChecked()
                or item.id in self.leaned_hard_words_ids
            )
        ]
        if self.combo_box_sort.currentIndex():
            print("Sort list")
            reverse = self.combo_box_sort.currentIndex() - 1
            learning_dict = {
                lw.word_id: lw.quantity_correct_answer for lw in self.learning_words
            }
            sorted_words = sorted(
                self.filtered_items,
                key=lambda w: learning_dict.get(w.id, 0),
                reverse=reverse,
            )
            self.filtered_items = sorted_words

        self.offset = 0
        self.views = []
        self.clear_visible()
        self.load_more()

    def on_but_clear_filter_released(self):
        self.clear_filters()

    def on_combo_box_sort_currentIndexChanged(self, value):
        if type(value) == int:
            self.apply_filter()

    def update_count(self):
        self.label_count.setText(f"{self.offset}/{len(self.filtered_items)}")

    def clear_filters(self):
        self.check_box_hide_learned_words.blockSignals(True)
        self.check_box_show_hard_words_only.blockSignals(True)
        self.line_edit_search.blockSignals(True)
        self.combo_box_sort.blockSignals(True)

        self.check_box_hide_learned_words.setChecked(False)
        self.check_box_show_hard_words_only.setChecked(False)
        self.line_edit_search.setText("")
        self.combo_box_sort.setCurrentIndex(0)
        self.apply_filter()

        self.check_box_hide_learned_words.blockSignals(False)
        self.check_box_show_hard_words_only.blockSignals(False)
        self.line_edit_search.blockSignals(False)
        self.combo_box_sort.blockSignals(False)

    def get_create_widget(self, item):
        return ViewWord(item)

    def extend_words(self, words):
        self.items.extend(words)
        self.apply_filter()


def test_run():
    user_id = 1
    subtitle_list_id = 3
    subtitle_list_repo = SubtitleListRepository()
    repo_learned_word = LearnedWordRepository()

    subtitle_list_words = subtitle_list_repo.get_words_by_subtitle_list_id(
        subtitle_list_id
    )
    learned_word = repo_learned_word.gets_by_user_id(user_id)
    app = QApplication(sys.argv)
    win = WidgetVerticalLayoutScrollForWords(
        subtitle_list_words, learned_word, user_id=user_id
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
