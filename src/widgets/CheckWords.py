import os
import sys
from pathlib import Path
from typing import List

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from sqlalchemy.orm import Session
from src.data.KnownWord import KnownWord

from config import ROOT_DIR
from src.data.WordWithTranslations import WordWithTranslations

scriptdir = Path(__file__).resolve().parents[0]
PATH_WAY_UI = os.path.join(scriptdir, "../uis/check_words.ui")


class CheckWords(QWidget):
    known_words = []
    words: List[WordWithTranslations]
    current_position = 0
    words_original: List[WordWithTranslations]

    def __init__(self, db: Session, words: List[WordWithTranslations]):
        super().__init__()
        self.db = db
        self.load_ui()
        self.known_words = self.db.query(KnownWord).all()
        self.words_original = words
        self.filter_word_and_show_word(self.words_original)

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "check_words.ui")
        self.window = uic.loadUi(ui_file, self)

    def filter_word_and_show_word(self, words: List[WordWithTranslations]):
        self.filter_word(words, 0)
        self.change_view_word()

    def filter_word(self, words: List[WordWithTranslations], correct_answer):
        self.words: List[WordWithTranslations] = []
        for o_w in self.words_original.words:
            if o_w.name not in self.known_words:
                self.words.words.append(o_w)
        if self.words.words.__len__() < 1:
            sys.exit()

    def change_view_word(self):
        self.next_word()
        self.show_word(self.words.words[self.current_position])
        self.label_count_list.setText(
            f"{self.current_position + 1}/{len(self.words.words)}"
        )

    def on_but_next_released(self):
        self.change_view_word()

    def on_but_back_released(self):
        self.change_view_word()

    def next_word(self):
        self.current_position += 1
        if self.current_position >= len(self.words.words):
            self.current_position = 0

    def show_word(
        self, word: WordWithTranslations = WordWithTranslations(name="Example")
    ):
        self.label_word.setText(f"{word.name.__str__()}")

    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if key == Qt.Key.Key_Up or key == 52:
            self.on_but_back_released()
        elif key == Qt.Key.Key_Down or key == 54:
            self.on_but_next_released()
        # event.accept()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = CheckWords(words)
    win.show()
    sys.exit(app.exec())
