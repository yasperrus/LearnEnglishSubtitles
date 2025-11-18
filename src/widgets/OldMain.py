import os
import sys

from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSlot, QSettings, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication

from config import ROOT_DIR
from src.data.LearnedWord import LearnedWord
from src.data.SubtitleList import SubtitleList
from src.data.User import User
from src.db.session import SessionLocal
from src.widgets.CreateListWords_2 import CreateListWords_2
from src.widgets.ViewList import ViewList
from src.widgets.ViewListKnownWords import ViewListKnownWords


# scrollArea
# widget_list
# layout_scroll
# page_lists
# layout_lists
class OldMain(QMainWindow):
    logout_requested = pyqtSignal()

    def __init__(self, user: User):
        super().__init__()
        self.db = SessionLocal()
        self.user = user
        self.subtitle_lists = user.subtitle_lists
        self.load_ui()
        self.setWindowTitle("Учить английские слова")

        for l in self.subtitle_lists:
            self.create_widget(l)
        self.view_known_words()

        self.layout_scroll.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # self.horizontalLayout_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.layout_scroll_hide_lists.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        # self.horizontalLayout_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "main.ui")
        self.window = uic.loadUi(ui_file, self)
        self.label_user_name.setText(self.user.name)
        self.settings = QSettings("MainWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def view_known_words(self):
        self.label_count_known_words.setText(self.user.quantity_learned_words.__str__())

    def on_but_create_list_released(self):
        view = CreateListWords_2(user_id=self.user.id)
        view.show()
        self.make_connection_create_list_words(view)

    def on_but_known_words_released(self):
        learned_words = self.db.query(LearnedWord).all()
        view = ViewListKnownWords(self.db, learned_words)
        view.show()

    def create_widget(self, subtitle_list):
        if not subtitle_list.is_hide:
            card = ViewList(self.db, subtitle_list)
            self.layout_scroll.addWidget(card)
        else:
            self.create_widget_hide_list(subtitle_list)

    def create_widget_hide_list(self, subtitle_list):
        card = ViewList(self.db, subtitle_list)
        self.layout_scroll_hide_lists.addWidget(card)

    @pyqtSlot(SubtitleList)
    def get_slider_value_create_list_words(self, subtitle_list: SubtitleList):
        self.subtitle_lists.append(subtitle_list)
        self.create_widget(subtitle_list)

    def make_connection_create_list_words(self, slider_object):
        slider_object.changed_value.connect(self.get_slider_value_create_list_words)

    def on_but_logout_released(self):
        self.logout_requested.emit()

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


def test_run():
    db = SessionLocal()

    app = QApplication(sys.argv)
    subtitle_lists = db.query(SubtitleList).all()
    win = OldMain(subtitle_lists)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
