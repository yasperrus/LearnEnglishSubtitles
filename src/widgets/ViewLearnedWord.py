import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from sqlalchemy.orm import Session

from config import ROOT_DIR
from src.data.LearnedWord import LearnedWord
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal


class ViewLearnWord(QWidget):
    def __init__(self, db: Session, word: WordWithTranslations):
        super().__init__()
        self.load_ui()
        self.label_word.setText(f"{word.name}")

        self.db = db
        self.word = word

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "view_learned_word.ui")
        self.window = uic.loadUi(ui_file, self)

    def on_but_learned_released(self):
        self.db.add(LearnedWord(name=self.word.name))
        self.db.commit()
        self.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = SessionLocal()
    learned_word = db.query(LearnedWord).get(1).all()
    win = ViewLearnWord(db, learned_word)
    win.show()
    sys.exit(app.exec())
