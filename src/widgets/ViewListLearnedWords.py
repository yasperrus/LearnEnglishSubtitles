import os
import sys
from typing import List

from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from config import ROOT_DIR, resource_path
from src.data.LearnedWord import LearnedWord
from src.data.WordWithFrequency import WordWithFrequency
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal
from src.scripts.ConvertTextToWordsWithFrequency import ConvertTextToWordsWithFrequency
from src.widgets.ViewLearnedWord import ViewLearnWord
from src.widgets.ViewListKnownWords import ViewListKnownWords


class ViewListLearnedWords(ViewListKnownWords):

    def load_ui(self):
        ui_file = resource_path("res/uis/view_list_known_words.ui")
        self.window = uic.loadUi(ui_file, self)
        self.setWindowTitle("Изученные слова")
        self.settings = QSettings("LearnedWordsWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def create_widget(self, word: WordWithTranslations):
        card = ViewLearnWord(self.db, word)
        self.layout_scroll.addWidget(card)

    def get_known_words(self):
        return [w.name for w in self.db.query(LearnedWord).all()]


def get_words_from_subtitle(uri: str) -> List[WordWithTranslations]:
    words_with_frequency: List[WordWithFrequency] = ConvertTextToWordsWithFrequency(
        uri
    ).__call__()
    ws = []
    for ws_f in words_with_frequency:
        ws.append(WordWithTranslations(name=ws_f.name))
    ViewListLearnedWords(ws)
    return ws


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = SessionLocal()
    learned_words = db.query(LearnedWord).all()
    win = ViewListLearnedWords(db, learned_words)
    win.show()
    sys.exit(app.exec())
