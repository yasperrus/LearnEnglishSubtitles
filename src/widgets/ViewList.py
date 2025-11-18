import os
import sys
from typing import List

from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy
from sqlalchemy import inspect

from config import ROOT_DIR
from src.data.LearnedWord import LearnedWord
from src.data.SubtitleList import SubtitleList
from src.db.session import SessionLocal
from src.improvements import RoundProgressBar
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.EditListWords import EditListWords
from src.widgets.TestLevel import TestLevel
from src.widgets.TestLevel0_2 import TestLevel0_2
from src.widgets.TestLevel1 import TestLevel1
from src.widgets.TestLevel2 import TestLevel2
from src.widgets.TestLevel2_2 import TestLevel2_2
from src.widgets.ViewListWords import ViewListWords


class ViewList(QWidget):
    hide_signal = pyqtSignal(SubtitleList)
    delete_signal = pyqtSignal(SubtitleList)

    PATH_WAY_ICON_HIDE = os.path.join(ROOT_DIR, "res", "icons", "hidden.png")
    PATH_WAY_ICON_VISIBLE = os.path.join(ROOT_DIR, "res", "icons", "visible.png")

    def __init__(
        self,
        subtitle_list: SubtitleList,
        learned_words: List[LearnedWord],
        user_id: int,
    ):
        super().__init__()

        self.subtitle_list_repo = SubtitleListRepository()
        self.init_ui()
        self.user_id = user_id
        self.db = SessionLocal()
        self.subtitle_list = subtitle_list
        self.learned_words = learned_words

        self.update_count_learned_words()

        if self.subtitle_list.is_open_menu is not None:
            self.widget_buttons.setVisible(self.subtitle_list.is_open_menu)

        self.update_icon_hide_status()

        self.rpb = RoundProgressBar.roundProgressBar()
        self.rpb.rpb_setBarStyle("Donet")
        self.rpb.rpb_setLineColor((33, 33, 33))
        self.rpb.rpb_setTextColor((33, 33, 33))
        self.rpb.rpb_setTextWidth(10)
        self.rpb.rpb_setMaximumSize(150, 150)
        self.rpb.rpb_setMinimumSize(90, 90)
        self.rpb.rpb_setMaximum(100)
        self.set_view_learned_words()
        self.rpb.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        # self.rpb.setMaximumSize(self.rpb.sizeHint())

        self.layout_info.addWidget(self.rpb)
        self.layout_info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rpb.mousePressEvent = self.clicked_progress_bar

    def init_different(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "view_list.ui")
        self.window = uic.loadUi(ui_file, self)
        # uic.loadUi(ui_file, self)

    def init_ui(self):
        self.init_different()

    def clicked_progress_bar(self, event):
        self.update_progress_bar()

    def update_icon_hide_status(self):
        if not self.subtitle_list.is_hide:
            icon_hide_status = QIcon(self.PATH_WAY_ICON_HIDE)
        else:
            icon_hide_status = QIcon(self.PATH_WAY_ICON_VISIBLE)
        self.but_hide.setIcon(icon_hide_status)

    def update_progress_bar(self):
        print("обновление приостановлено иза ошибок с частотами и т.п.")
        print(
            f"number_learned_words_frequency: {self.number_learned_words_frequency()}"
        )
        # self.subtitle_list.number_learned = self.number_learned_word()
        # self.subtitle_list.number_learned_all = self.number_learned_words_frequency()
        # print(f"{self.subtitle_list.name} :\n\twords len: {len(self.subtitle_list.words)} | "
        #       f"learned len: {self.subtitle_list.number_learned} | "
        #       f"learned all len: {self.subtitle_list.number_learned_all} | "
        #       f"all len {self.subtitle_list.number_all}")
        # self.set_view_learned_words()
        # self.db.commit()

    def number_learned_word(self):
        number = 0
        learned_words = self.db.query(LearnedWord).all()
        list_learned_words = [l_w.name for l_w in learned_words]
        for w in self.subtitle_list.words:
            if w.name in list_learned_words:
                number += 1
        return number

    def number_learned_words_frequency(self):
        learned_words = self.db.query(LearnedWord).all()
        list_learned_words = [l_w.name for l_w in learned_words]
        count_learned_frequency = 0
        count_know = 0
        for w in self.subtitle_list.words_association:
            if w.word.name in list_learned_words:
                count_learned_frequency += w.frequency
            if w.word.name == "know":
                count_know += w.frequency
        return count_learned_frequency

    def set_view_learned_words(self):
        self.label_counts.setText(
            f"{self.subtitle_list.quantity_learned_words}/{self.subtitle_list.quantity_words}"
        )
        if self.subtitle_list.quantity_learned_words_frequencies > 0:
            self.rpb.rpb_setValue(
                (self.subtitle_list.quantity_learned_words_frequencies * 100)
                / self.subtitle_list.quantity_words_frequencies
            )
        else:
            self.rpb.rpb_setValue(0)

    def on_but_open_menu_released(self):
        self.change_open_menu_state()

    def on_but_hide_released(self):
        self.change_hide_status()
        self.hide_signal.emit(self.subtitle_list)
        self.deleteLater()

    def change_hide_status(self):
        if self.subtitle_list.is_hide:
            self.subtitle_list.is_hide = False
        else:
            self.subtitle_list.is_hide = True
        self.update_icon_hide_status()
        self.subtitle_list_repo.update_subtitle_list(self.subtitle_list)

    def change_open_menu_state(self):
        if self.subtitle_list.is_open_menu:
            self.subtitle_list.is_open_menu = False
        else:
            self.subtitle_list.is_open_menu = True
        self.widget_buttons.setVisible(self.subtitle_list.is_open_menu)
        self.subtitle_list_repo.update_subtitle_list(self.subtitle_list)

    def on_but_view_list_released(self):
        # words.words.sort(key=lambda Word: Word.correct_answer)

        # view = ViewListLearnedWords(self.db, self.subtitle_list.words)
        self.refresh_words()
        view = ViewListWords(self.subtitle_list.words, self.learned_words, self.user_id)
        view.show()

    def refresh_words(self):
        if "words" in inspect(self.subtitle_list).unloaded:
            self.subtitle_list = self.subtitle_list_repo.refresh_words(
                self.subtitle_list
            )

    def on_but_test_0_released(self):
        view = TestLevel(user_id=self.user_id, subtitle_list_id=self.subtitle_list.id)
        view.show()

    def on_but_edit_released(self):
        self.refresh_words()
        view = EditListWords(self.subtitle_list, self.learned_words, self.user_id)
        self.make_connection_edit_list_words(view)
        view.show()

    def get_known_words(self):
        return [w.name for w in self.db.query(LearnedWord).all()]

    def on_but_test_0_2_released(self):
        view = TestLevel0_2(
            user_id=self.user_id, subtitle_list_id=self.subtitle_list.id
        )
        view.show()

    def on_but_test_1_released(self):
        view = TestLevel1(user_id=self.user_id, subtitle_list_id=self.subtitle_list.id)
        view.show()

    def get_correct_words(self):
        learned_words = [w.name for w in self.db.query(LearnedWord).all()]
        copy_learned_words_subtitle_list = filter(
            lambda x: x.name not in learned_words, self.subtitle_list.words.copy()
        )
        sorted_copy_learned_words_subtitle_list = sorted(
            copy_learned_words_subtitle_list,
            key=lambda w: (w.statuses.correct_answer, w.statuses.showed),
        )
        return sorted_copy_learned_words_subtitle_list

    def on_but_test_2_released(self):
        view = TestLevel2(user_id=self.user_id, subtitle_list_id=self.subtitle_list.id)
        view.show()

    def on_but_test_2_2_released(self):
        view = TestLevel2_2(
            user_id=self.user_id, subtitle_list_id=self.subtitle_list.id
        )
        view.show()

    def on_but_delete_released(self):
        self.subtitle_list_repo.delete_subtitle_list_by_subtitle_list_id(
            self.subtitle_list.id
        )
        self.delete_signal.emit(self.subtitle_list)
        self.deleteLater()

    @pyqtSlot(SubtitleList)
    def get_slider_value_edit_list_words(self, subtitle_list: SubtitleList):
        self.update_count_learned_words()
        # self.__init__(self.db, self.subtitle_list)

    def make_connection_edit_list_words(self, slider_object):
        slider_object.changed_value.connect(self.get_slider_value_edit_list_words)

    def update_count_learned_words(self):
        self.label_name_list.setText(self.subtitle_list.name)
        self.label_counts.setText(
            f"{self.subtitle_list.quantity_learned_words}/{self.subtitle_list.quantity_words}"
        )


def test_run():
    app = QApplication(sys.argv)

    db = SessionLocal()

    subtitle_list: SubtitleList = db.query(SubtitleList).get(4)

    win = ViewList(subtitle_list)
    win.show()
    sys.exit(app.exec())


# def load_words(db):
#
#     results = db.execute(
#         text("""SELECT W.id AS word_id, W.name AS name_word, P.name AS path_name,
#         P.isMain AS path_is_main, T.isMain AS translation_is_main, translation
#         FROM words W
#             JOIN subtitle_list_words_association SWA ON W.id = SWA.word_id
#             JOIN subtitle_lists S ON S.id = SWA.subtitle_list_id
#             JOIN path_of_speeches P ON P.word_id = W.id
#             JOIN translations T ON T.path_of_speech_id = P.id
#                 WHERE S.id = 2;"""
#         )
#     ).fetchall()
#     for row in enumerate(results):
#         w = WordWithTranslations(
#             id=row[0],
#             name=row[1]
#         )
#         print(f"{row[0]} {row[1]}")

if __name__ == "__main__":
    test_run()
