import os

from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget

from config import ROOT_DIR
from src.data.SubtitleList import SubtitleList


class CreateListWords(QWidget):

    def __init__(self, user_id):
        super().__init__()
        self.load_ui()

        self.setWindowTitle("Создать список слов")

        self.subtitle_list = SubtitleList()

        self.update_count_words()

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "create_list_words.ui")
        self.window = uic.loadUi(ui_file, self)
        self.settings = QSettings("CreateListWordsWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def on_but_cancel_released(self):
        self.close()

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())
