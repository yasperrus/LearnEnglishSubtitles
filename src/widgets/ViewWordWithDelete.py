import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from config import resource_path
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal
from src.widgets.ViewWord import ViewWord


class ViewWordWithDelete(ViewWord):

    def init_different(self):
        ui_file = resource_path("res/uis/view_word_with_delete.ui")
        self.window = uic.loadUi(ui_file, self)

    def on_but_delete_released(self):
        self.deleteLater()


if __name__ == "__main__":

    db = SessionLocal()
    word: WordWithTranslations = db.query(WordWithTranslations).get(12)

    app = QApplication(sys.argv)
    win = ViewWordWithDelete(word)
    win.show()
    sys.exit(app.exec())
