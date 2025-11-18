import sys
from typing import List

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from config import SUBLIST_PAGE_SIZE
from src.data import LearnedWord
from src.data.SubtitleList import SubtitleList
from src.repositories.learned_word_repository import LearnedWordRepository
from src.repositories.user_repository import UserRepository
from src.widgets.ViewList import ViewList
from src.widgets.WidgetVerticalLayoutScroll import WidgetVerticalLayoutScroll


class WidgetVerticalLayoutScrollForSubtitleList(WidgetVerticalLayoutScroll):
    hide_signal = pyqtSignal(SubtitleList)
    delete_signal = pyqtSignal(SubtitleList)

    def __init__(self, items: List, learned_words: List[LearnedWord], user_id: int):
        self.user_id = user_id
        super().__init__(items, learned_words)

    def get_create_widget(self, item):
        return ViewList(item, self.learned_words, user_id=self.user_id)

    def extend_subtitle_list(self, words):
        self.items = words + self.items
        self.apply_filter()

    def load_more(self):
        end = min(self.offset + SUBLIST_PAGE_SIZE, len(self.filtered_items))
        for i in range(self.offset, end):
            item = self.filtered_items[i]
            view = self.get_create_widget(item)
            self.layout_scroll.addWidget(view)
            view.hide_signal.connect(self.on_view_hide)
            view.delete_signal.connect(self.pop_subtitle_list)
            self.views.append(view)
        self.offset = end
        self.update_count()

    def on_view_hide(self, subtitle_list):
        self.hide_signal.emit(subtitle_list)

    def pop_subtitle_list(self, item):
        if item in self.items:
            idx = self.items.index(item)
            self.views.pop(idx)
            self.items.pop(idx)
        else:
            print("not item in layout")


def test_run():
    user_repo = UserRepository()
    user = user_repo.get_all_relationship_by_id(1)
    learned_word_repo = LearnedWordRepository()
    learned_words = learned_word_repo.gets_by_user_id(1)

    app = QApplication(sys.argv)
    win = WidgetVerticalLayoutScrollForSubtitleList(
        user.subtitle_lists, learned_words, user_id=1
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
