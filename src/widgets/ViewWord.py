import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication

from config import ROOT_DIR
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal


class ViewWord(QWidget):
    def __init__(self, word: WordWithTranslations):
        super().__init__()
        self.init_ui()
        self.word = word
        self.label_word.setText(word.name)
        self.label_transcription.setText(word.transcription)

        self.insert_path_of_speech_to_combo_box()
        self.insert_translations_to_combo_box()

    def init_different(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "view_word.ui")
        self.window = uic.loadUi(ui_file, self)

    def init_ui(self):
        self.init_different()

    def on_combo_box_path_of_speeches_activated(self, index: int):
        if type(index) == int:
            self.clean_main_path_of_speeches()
            self.word.path_of_speeches[
                self.combo_box_path_of_speeches.currentIndex()
            ].isMain = True
            self.insert_translations_to_combo_box()
            self.combo_box_path_of_speeches.setCurrentIndex(index)

    def on_combo_box_translations_activated(self, index: int):
        if type(index) == int:
            self.clean_main_translations()
            self.word.path_of_speeches[
                self.combo_box_path_of_speeches.currentIndex()
            ].translations[index].isMain = True
            self.insert_translations_to_combo_box()

    def clean_main_path_of_speeches(self):
        for p in self.word.path_of_speeches:
            if p.isMain:
                p.isMain = False

    def clean_main_translations(self):
        for t in self.word.path_of_speeches[
            self.combo_box_path_of_speeches.currentIndex()
        ].translations:
            if t.isMain:
                t.isMain = False

    def insert_path_of_speech_to_combo_box(self):
        self.combo_box_path_of_speeches.clear()
        if self.word.path_of_speeches.__len__() > 0:
            for p in self.word.path_of_speeches:
                self.combo_box_path_of_speeches.addItem(p.name)
            self.combo_box_path_of_speeches.setCurrentIndex(
                self.get_main_index(self.word.path_of_speeches)
            )

    def insert_translations_to_combo_box(self):
        self.combo_box_translations.clear()
        if self.word.path_of_speeches.__len__() > 0:
            if (
                self.word.path_of_speeches[
                    self.combo_box_path_of_speeches.currentIndex()
                ].translations.__len__()
                > 0
            ):
                self.combo_box_translations.addItems(
                    [
                        t.translation
                        for t in self.word.path_of_speeches[
                            self.combo_box_path_of_speeches.currentIndex()
                        ].translations
                    ]
                )
                self.combo_box_translations.setCurrentIndex(
                    self.get_main_index(
                        self.word.path_of_speeches[
                            self.combo_box_path_of_speeches.currentIndex()
                        ].translations
                    )
                )

    def get_main_index(self, any_list: list):
        for i, l in enumerate(any_list):
            if l.isMain:
                return i
        return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = SessionLocal()
    word: WordWithTranslations = db.query(WordWithTranslations).get(12)

    win = ViewWord(word)
    win.show()
    sys.exit(app.exec())
