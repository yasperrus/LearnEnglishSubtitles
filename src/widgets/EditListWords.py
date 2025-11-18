import os
import sys
from typing import List

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QWidget, QApplication

from config import ROOT_DIR
from src.data import LearnedWord
from src.data.SubtitleList import SubtitleList
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.WidgetVerticalLayoutScrollForWordsWithDelete import (
    WidgetVerticalLayoutScrollForWordsWithDelete,
)


class EditListWords(QWidget):
    changed_value = pyqtSignal(SubtitleList)

    def __init__(
        self,
        subtitle_list: SubtitleList,
        learned_words: List[LearnedWord],
        user_id: int,
        parent=None,
    ):
        super().__init__(parent)
        self.subtitle_list_repo = SubtitleListRepository()
        self.subtitle_list = subtitle_list
        self.learned_words = learned_words
        self.user_id = user_id
        self.init_ui()
        self.layout_scroll_for_words = WidgetVerticalLayoutScrollForWordsWithDelete(
            self.subtitle_list.words, self.learned_words, self.user_id
        )
        self.layout_words.addWidget(self.layout_scroll_for_words)

    def init_ui(self):
        self.init_different()
        self.line_edit_name_list.setText(self.subtitle_list.name)
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            print(f"Error settings window")

    def init_different(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "edit_list_words.ui")
        self.window = uic.loadUi(ui_file, self)
        self.setWindowTitle("Редактировать список")
        self.settings = QSettings("EditListWordsWindow", "LearnEnglish")

    def on_line_edit_name_list_textEdited(self, text):
        self.subtitle_list.name = text

    def on_but_save_released(self):
        self.subtitle_list_repo.update_subtitle_list(self.subtitle_list)
        self.changed_value.emit(self.subtitle_list)
        self.close()

    def on_but_cancel_released(self):
        self.close()

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


if __name__ == "__main__":

    sub_repo = SubtitleListRepository()
    subtitle_list: SubtitleList = sub_repo.get_subtitle_list_by_subtitle_list_id(1)

    app = QApplication(sys.argv)
    win = EditListWords(subtitle_list)
    win.show()
    sys.exit(app.exec())
