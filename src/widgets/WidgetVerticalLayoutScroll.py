import os
import sys
from typing import TYPE_CHECKING, List

from PyQt5 import QtCore, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

from config import SUBLIST_PAGE_SIZE, ROOT_DIR, resource_path
from src.core.theme_manager import ThemeManager
from src.data import LearnedWord
from src.repositories.user_repository import UserRepository
from src.widgets.ThemeWidget import ThemeWidget

if TYPE_CHECKING:
    pass


class WidgetVerticalLayoutScroll(QWidget, ThemeWidget):

    def __init__(self, items: List, learned_words: List[LearnedWord]):
        QWidget.__init__(self)
        ThemeWidget.__init__(self)
        self.init_ui()
        current_theme = ThemeManager().get_theme()
        if current_theme:
            self.apply_theme(current_theme)

        # self.timer_add = QTimer()
        self.timer_filter = QTimer()
        self.items = items
        self.learned_words = learned_words
        self.leaned_words_ids = [lw.word_id for lw in self.learned_words]
        # при изменение learned_word на learning_word isHard и т.п. стали
        # self.leaned_hard_words_ids = [
        #     lw.word_id for lw in self.learned_words if lw.isHard == True
        # ]
        self.leaned_hard_words_ids = []
        self.views = []

        self.filtered_items = list(items)
        self.offset = 0
        self.load_more()

    def init_different(self):
        ui_file = resource_path("res/uis/widget_vertical_layout_scroll.ui")
        self.window = uic.loadUi(ui_file, self)
        # uic.loadUi(ui_file, self)
        self.setWindowTitle("Список")

    def init_ui(self):
        self.init_different()
        self.layout_scroll.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scroll_area.verticalScrollBar().valueChanged.connect(
            self.on_scroll_area_valueChanged
        )

    def on_line_edit_search_textEdited(self):  #  textChanged
        self.timer_filter = QTimer()
        self.timer_filter.timeout.connect(self.apply_filter)
        self.timer_filter.start(1000)

    def load_more(self):
        end = min(self.offset + SUBLIST_PAGE_SIZE, len(self.filtered_items))
        for i in range(self.offset, end):
            item = self.filtered_items[i]
            view = self.get_create_widget(item)
            self.layout_scroll.addWidget(view)
            self.views.append(view)
        self.offset = end
        self.update_count()

    # def load_more(self):
    #     end = min(self.offset + SUBLIST_PAGE_SIZE, len(self.filtered_items))
    #     self.smooth_index = self.offset
    #     self.smooth_end = end
    #
    #     self.timer_add.timeout.connect(self.add_next_item)
    #     self.timer_add.start(20)
    #     self.update_count()
    #
    # def add_next_item(self):
    #
    #     if self.smooth_index >= self.smooth_end:
    #         self.timer_add.stop()
    #         self.offset = self.smooth_end
    #         return
    #     item = self.filtered_items[self.smooth_index]
    #     view = self.get_create_widget(item)
    #     self.layout_scroll.addWidget(view)
    #     self.smooth_index += 1

    def get_create_widget(self, item):
        return QWidget()

    def apply_filter(self):
        if self.timer_filter:
            self.timer_filter.stop()
        text = self.line_edit_search.text().strip().lower()
        self.filtered_items = (
            [item for item in self.items if text in item.name.lower()]
            if text
            else list(self.items)
        )
        self.offset = 0
        self.views = []
        self.clear_visible()
        self.load_more()

    def update_count(self):
        self.label_count.setText(f"{self.offset}/{len(self.items)}")

    def clear_visible(self):
        for i in reversed(range(self.layout_scroll.count())):
            w = self.layout_scroll.itemAt(i).widget()
            if w:
                w.setParent(None)
                w.deleteLater()

    def clear_items(self):
        self.items = []
        self.clear_visible()
        self.update_count()

    def on_scroll_area_valueChanged(self, value: int):
        if (
            value == self.scroll_area.verticalScrollBar().maximum()
            and self.offset < len(self.filtered_items)
        ):
            self.load_more()

    def closeEvent(self, event):
        if self.timer_filter.isActive():
            self.timer_filter.stop()
        super().closeEvent(event)


def test_run():
    repo_user = UserRepository()
    user = repo_user.get_all_relationship_by_id(1)
    print(f"count list user: {len(user.subtitle_lists)}")
    app = QApplication(sys.argv)
    win = WidgetVerticalLayoutScroll(user.subtitle_lists)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
