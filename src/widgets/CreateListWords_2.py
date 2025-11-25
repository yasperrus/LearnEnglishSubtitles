import sys
from typing import List

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal, QFileInfo, QSettings, pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication

from config import resource_path
from src.core.theme_manager import ThemeManager
from src.data.LearnedWord import LearnedWord
from src.data.SubtitleList import SubtitleList
from src.data.WordWithFrequency import WordWithFrequency
from src.data.WordWithTranslations import WordWithTranslations
from src.repositories.learned_word_repository import LearnedWordRepository
from src.repositories.learning_word_repository import LearningWordRepository
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.repositories.user_repository import UserRepository
from src.repositories.word_repository import WordRepository
from src.scripts.ConvertTextToWordsWithFrequency import ConvertTextToWordsWithFrequency
from src.scripts.FileReader import FileReader
from src.widgets.InsertText import InsertText
from src.widgets.ThemeWidget import ThemeWidget
from src.widgets.WidgetVerticalLayoutScrollForWordsWithDelete import (
    WidgetVerticalLayoutScrollForWordsWithDelete,
)


# удаление слова из списка не возвращает и не удаляет его из subtitle_list
# нужно чтоб порядок слов был по проядку суббтитра, чтоб каждое новое слово шло как в себбтитрах
class CreateListWords_2(QWidget, ThemeWidget):
    changed_value = pyqtSignal(SubtitleList)

    def __init__(self, user_id: int, learned_words: List[LearnedWord]):
        QWidget.__init__(self)
        ThemeWidget.__init__(self)

        # self.layout_scroll.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.user_id = user_id
        self.subtitle_list = SubtitleList()
        self.learned_words = learned_words
        self.learned_words_idx = [
            learned_word.word_id for learned_word in learned_words
        ]
        self.init_ui()
        current_theme = ThemeManager().get_theme()
        if current_theme:
            self.apply_theme(current_theme)

        self.update_count_words()
        self.setWindowTitle("Создать список слов")

    def init_ui(self):
        ui_file = resource_path("res/uis/create_list_words.ui")
        self.window = uic.loadUi(ui_file, self)
        self.settings = QSettings("CreateListWordsWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

        self.layout_scroll_for_words = WidgetVerticalLayoutScrollForWordsWithDelete(
            items=[], learned_words=self.learned_words, user_id=self.user_id
        )
        self.layout_words.addWidget(self.layout_scroll_for_words)

    def on_but_clear_released(self):
        self.clear_list()

    def clear_list(self):
        self.layout_scroll_for_words.clear_items()
        self.subtitle_list = SubtitleList()
        self.update_count_words()

    def clear_layout_scroll(self):
        for i in range(self.layout_scroll.count()):
            self.layout_scroll.itemAt(i).widget().deleteLater()

    def get_words_by_list_word(self, list_word: list, chunk_size: int = 900):
        word_repository = WordRepository()
        results = []
        for i in range(0, len(list_word), chunk_size):
            chunk = list_word[i : i + chunk_size]
            results.extend(word_repository.get_words_by_list_word(chunk))
        return results

    def translate_words_create_widgets(self, list_word: List[str]):
        exist_words_with_translations: List[WordWithTranslations] = (
            self.get_words_by_list_word(list_word)
        )
        self.subtitle_list.words += exist_words_with_translations
        # self.create_list_widget(exist_words_with_translations)
        self.layout_scroll_for_words.extend_words(exist_words_with_translations)
        self.update_count_words()

    def on_but_file_dialog_released(self):
        path_file = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выбрать файл",
            "~/",
            "Text files (*.srt *.sub *.ssa *.smi *.vtt *.ttml *.idx)",
        )[0]
        if path_file:
            self.file_name = QFileInfo(path_file).fileName()
            if len(self.line_name_list.text()) < 1:
                self.line_name_list.setText(self.file_name)

            self.line_uri.setText(path_file)
            reader = FileReader(path_file)
            text = reader.get_text()
            self.create_list_words_by_text(text)

    def create_list_words_by_text(self, text: str):
        self.words_with_frequency: List[WordWithFrequency] = (
            ConvertTextToWordsWithFrequency(text)
        )
        list_words_name = [word.name for word in self.words_with_frequency]
        self.translate_words_create_widgets(list_words_name)

    def count_words_frequencies(self):
        count_learned_all = 0
        for w in self.subtitle_list.words_association:
            count_learned_all += w.frequency
        return count_learned_all

    def count_learned_words(self):
        quantity = 0
        if self.subtitle_list.words:
            for w in self.subtitle_list.words:
                if w.id in self.learned_words_idx:
                    quantity += 1
        return quantity

    def count_learned_words_frequencies(self):
        quantity_learned_frequency = 0
        for w in self.subtitle_list.words_association:
            if w.word.id in self.learned_words_idx:
                quantity_learned_frequency += w.frequency
        return quantity_learned_frequency

    def update_count_words(self):
        self.subtitle_list.quantity_words = len(self.subtitle_list.words)
        self.subtitle_list.quantity_learned_words = self.count_learned_words()
        # self.label_count_words.setText(
        #     f"Количество слов: {self.subtitle_list.number_words}"
        # )
        # self.label_count_learned_words.setText(
        #     f"Выученных слов: {self.subtitle_list.number_learned_words}"
        # )

    # def create_list_widget(self, words: List[WordWithTranslations]):
    #     for w in words:
    #         self.create_widget(w)

    def on_but_insert_text_released(self):
        view = InsertText()
        view.show()
        self.make_connection_insert_text(view)

    def get_id_by_match(self, list_words: list, name):
        for i, w in enumerate(list_words):
            if w.name == name:
                return i
        return -1

    # def create_widget(self, word_with_translations: WordWithTranslations):
    #     card = ViewWord(word_with_translations)
    #     self.layout_scroll.addWidget(card)

    @pyqtSlot(str)
    def get_slider_value_insert_text(self, text: str):
        self.create_list_words_by_text(text)

    def make_connection_insert_text(self, slider_object):
        slider_object.changed_value.connect(self.get_slider_value_insert_text)

    def on_but_save_released(self):
        if self.validate_list():
            learning_word_repo = LearningWordRepository()
            learning_word_repo.adds_words_by_user_id(
                self.user_id, self.subtitle_list.words
            )

            self.subtitle_list.name = self.line_name_list.text()
            user_repo = UserRepository()
            user_repo.add_subtitle_list_by_user_id(self.user_id, self.subtitle_list)

            for w in self.subtitle_list.words_association:
                id = self.get_id_by_match(self.words_with_frequency, w.word.name)
                if id != -1:
                    w.frequency = self.words_with_frequency[id].frequency
            self.subtitle_list.quantity_words_frequencies = (
                self.count_words_frequencies()
            )
            self.subtitle_list.quantity_learned_words_frequencies = (
                self.count_learned_words_frequencies()
            )
            subtitle_list_repo = SubtitleListRepository()
            subtitle_list_repo.update_subtitle_list(self.subtitle_list)
            self.changed_value.emit(
                subtitle_list_repo.get_subtitle_list_by_subtitle_list_id(
                    self.subtitle_list.id
                )
            )
            self.close()

    def validate_list(self) -> bool:
        if self.subtitle_list.words.__len__() > 0:
            if len(self.line_name_list.text()) > 0:
                return True
        return False

    def on_but_cancel_released(self):
        self.close()

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


def test_run():
    user_id = 1
    learned_words_repo = LearnedWordRepository()
    learned_words = learned_words_repo.gets_by_user_id(user_id=user_id)

    app = QApplication(sys.argv)
    win = CreateListWords_2(user_id, learned_words)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()

    # word_repo = WordRepository()
    # words = word_repo.get_words_by_list_word(["new", "old", "cool"])
    # s = SubtitleList()
    # s.words += words
    #
    # for w in s.words:
    #     w.subtitle_list_association.frequency = 2
