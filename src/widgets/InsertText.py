import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, QSettings
from PyQt5.QtWidgets import QWidget, QApplication

from config import resource_path
from src.data.SubtitleList import SubtitleList
from src.db.session import SessionLocal


class InsertText(QWidget):

    changed_value = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setWindowTitle("Текст")

    def load_ui(self):
        ui_file = resource_path("res/uis/create_text.ui")
        self.window = uic.loadUi(ui_file, self)
        self.settings = QSettings("CreateTextWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def on_but_cancel_released(self):
        self.close()

    def on_but_save_released(self):
        self.changed_value.emit(self.plain_text_edit.toPlainText())
        self.close()

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = SessionLocal()
    subtitle_list: SubtitleList = db.query(SubtitleList).get(4)

    win = InsertText()
    win.show()
    sys.exit(app.exec())
