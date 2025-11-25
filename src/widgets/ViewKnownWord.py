import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from sqlalchemy.orm import Session
from src.data.KnownWord import KnownWord

from config import resource_path
from src.db.session import SessionLocal


class ViewKnownWord(QWidget):
    def __init__(self, db: Session, word: KnownWord):
        super().__init__()
        self.load_ui()
        self.label_word.setText(word.name)

        self.db = db
        self.word = word

    def load_ui(self):
        ui_file = resource_path("res/uis/view_known_word.ui")
        self.window = uic.loadUi(ui_file, self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = SessionLocal()
    learned_word = db.query(KnownWord).get(1).all()
    win = ViewKnownWord(db, learned_word)
    win.show()
    sys.exit(app.exec())
