import os
import re
import sys
from typing import List

from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal, QSettings, QTimer
from PyQt5.QtWidgets import QWidget, QApplication

from config import ROOT_DIR
from src.data.SubtitleList import SubtitleList
from src.data.WordWithTranslations import WordWithTranslations
from src.repositories.learned_word_repository import LearnedWordRepository
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.ViewWord import ViewWord


class EditListWords(QWidget):
    changed_value = pyqtSignal(SubtitleList)

    numbers_items = []
    time_click = 0

    def __init__(self, subtitle_list: SubtitleList):
        super().__init__()
        self.load_ui()
        self.sub_repo = SubtitleListRepository()
        self.subtitle_list = subtitle_list
        self.setWindowTitle("Редактировать список")
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.filter_words_by_request)
        self.timer.stop()

        self.line_edit_name_list.setText(self.subtitle_list.name)
        self.layout_scroll.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.view_all_words(self.subtitle_list.words)
        self.update_count()

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "edit_list_words.ui")
        self.window = uic.loadUi(ui_file, self)
        self.settings = QSettings("EditListWordsWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def update_count(self):
        self.label_count_words.setText(
            f"Количество слов: {self.subtitle_list.quantity_words}"
        )
        self.label_count_learned_words.setText(
            f"Выученных слов: {self.subtitle_list.quantity_learned_words}"
        )

    def on_line_edit_name_list_textEdited(self, text):
        self.subtitle_list.name = text
        # print(f"Change name list : {text}")

    def on_line_edit_search_textEdited(self, text):
        if type(text):
            self.start_timer()

    def on_line_edit_search_editingFinished(self):
        self.timer.stop()

    def start_timer(self):
        self.timer.start(1000)

    def filter_words_by_request(self):
        view_words: List[WordWithTranslations] = self.subtitle_list.words.copy()
        self.clear_layout_scroll()
        if self.line_edit_search.text():
            i = 0
            while i < len(view_words):
                if not re.match(self.line_edit_search.text(), view_words[i].name):
                    view_words.pop(i)
                else:
                    i += 1
        print(f"check {self.check_box_remove_learned_words.checkState()}")
        if self.check_box_remove_learned_words.checkState():
            print("check_box_remove_learned_words")
            view_words = self.remove_learned_words(view_words)
        self.view_all_words(view_words)

    def on_check_box_remove_learned_words_stateChanged(self, value):
        if type(value) == int:
            self.filter_words_by_request()

    def remove_learned_words(self, words: List[WordWithTranslations]):
        learned_words = self.get_learned_words()
        i = 0
        while i < len(words):
            if words[i].name in learned_words:
                words.pop(i)
            else:
                i += 1
        return words

    def clear_layout_scroll(self):
        for i in range(self.layout_scroll.count()):
            self.layout_scroll.itemAt(i).widget().deleteLater()

    def get_learned_words(self):
        learned_repository = LearnedWordRepository()
        return [w.name for w in learned_repository.get_learned_words()]

    def view_all_words(self, words: List[WordWithTranslations]):
        self.numbers_items = []
        for i, w in enumerate(words):
            self.numbers_items.append(w.name)
            self.create_widget(w)

    def create_widget(self, word_with_translations: WordWithTranslations):
        card = ViewWord(word_with_translations)
        self.layout_scroll.addWidget(card)

    def on_but_save_released(self):
        self.sub_repo.update_subtitle_list(self.subtitle_list)
        self.changed_value.emit(self.subtitle_list)
        self.close()

    def on_but_cancel_released(self):
        self.close()

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    sub_repo = SubtitleListRepository()
    subtitle_list: SubtitleList = sub_repo.get_subtitle_list_by_subtitle_list_id(1)

    win = EditListWords(subtitle_list)
    win.show()
    sys.exit(app.exec())
