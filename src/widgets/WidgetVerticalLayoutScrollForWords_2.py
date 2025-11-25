import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from config import ROOT_DIR, resource_path
from src.repositories.user_repository import UserRepository
from src.widgets.ViewWord import ViewWord
from src.widgets.WidgetVerticalLayoutScroll import WidgetVerticalLayoutScroll


class WidgetVerticalLayoutScrollForWords_2(WidgetVerticalLayoutScroll):

    def init_different(self):
        ui_file = resource_path("res/uis/widget_vertical_layout_scroll_for_words.ui")
        self.window = uic.loadUi(ui_file, self)
        self.but_is_filter.setChecked(False)
        self.widget_filter.setVisible(self.but_is_filter.isChecked())

    def get_create_widget(self, item):
        return ViewWord(item)

    def extend_words(self, words):
        self.items.extend(words)
        self.apply_filter("")


def test_run():
    repo_user = UserRepository()
    user = repo_user.get_all_relationship_by_id(1)

    app = QApplication(sys.argv)
    win = WidgetVerticalLayoutScrollForWords_2(user.subtitle_lists[0].words)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
