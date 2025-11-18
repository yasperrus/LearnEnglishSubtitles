import os
import sys
from typing import List

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QApplication
from sqlalchemy.orm import Session
from src.data.KnownWord import KnownWord

from config import ROOT_DIR
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal
from src.widgets.ViewKnownWord import ViewKnownWord


class ViewListKnownWords(QWidget):
    count_learned_words = 0

    def __init__(self, db: Session, words: List[WordWithTranslations]):
        super().__init__()
        self.load_ui()
        self.db = db
        self.words = words
        self.layout_scroll.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.count_learned_words = len(words)
        self.view_count_learned_words()
        for w in words:
            self.create_widget(w)

    def view_count_learned_words(self):
        self.label_count_words.setText(
            "Изученных слов: " + str(self.count_learned_words)
        )

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "view_list_known_words.ui")
        self.window = uic.loadUi(ui_file, self)
        self.setWindowTitle("Известные слова")
        self.settings = QSettings("KnownWordsWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def get_known_words(self):
        return [w.name for w in self.db.query(KnownWord).all()]

    def clear_layout_scroll(self):
        for i in range(self.layout_scroll.count()):
            self.layout_scroll.itemAt(i).widget().deleteLater()

    def create_widget(self, word: WordWithTranslations):
        card = ViewKnownWord(self.db, word)
        self.layout_scroll.addWidget(card)

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ws = []
    db = SessionLocal()
    for i in range(20):
        ws.append(WordWithTranslations(name="Example"))
    win = ViewListKnownWords(db, ws)
    win.show()
    sys.exit(app.exec())
