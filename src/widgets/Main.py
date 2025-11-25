import sys

from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSettings, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication

from config import resource_path
from src.core.theme_manager import ThemeManager
from src.data.SubtitleList import SubtitleList
from src.data.User import User
from src.repositories.learned_word_repository import LearnedWordRepository
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.repositories.user_repository import UserRepository
from src.repositories.word_repository import WordRepository
from src.widgets.CreateListWords_2 import CreateListWords_2
from src.widgets.ThemeWidget import ThemeWidget
from src.widgets.ViewListWords import ViewListWords
from src.widgets.ViewSettings import ViewSettings
from src.widgets.WidgetVerticalLayoutScrollForSubtitleList import (
    WidgetVerticalLayoutScrollForSubtitleList,
)


# Нужно сохранить сколько выученных слов после обновления в базе данных
class Main(QMainWindow, ThemeWidget):
    logout_requested = pyqtSignal()

    def __init__(self, user: User):
        QMainWindow.__init__(self)
        ThemeWidget.__init__(self)
        self.user = user
        self.subtitle_list_repo = SubtitleListRepository()
        self.learned_words_repo = LearnedWordRepository()
        self.word_repo = WordRepository()

        self.subtitle_lists = self.subtitle_list_repo.get_subtitle_lists_by_user_id(
            self.user.id
        )
        self.learned_words = self.learned_words_repo.gets_by_user_id(self.user.id)
        self.words_learned = self.word_repo.get_words_learned_by_user_id(self.user.id)

        self.init_ui()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # делаем фон прозрачным
        current_theme = ThemeManager().get_theme()
        if current_theme:
            self.apply_theme(current_theme)
        self.setWindowTitle("Главная страница")

    def init_ui(self):
        ui_file = resource_path("res/uis/main.ui")
        uic.loadUi(ui_file, self)
        # uic.loadUi(ui_file, self)
        opened_subtitle_lists = [s for s in self.subtitle_lists if s.is_hide == False]
        hidden_subtitle_lists = [s for s in self.subtitle_lists if s.is_hide == True]
        self.window_scroll = WidgetVerticalLayoutScrollForSubtitleList(
            opened_subtitle_lists, self.learned_words, user_id=self.user.id
        )
        self.window_hide_scroll = WidgetVerticalLayoutScrollForSubtitleList(
            hidden_subtitle_lists, self.learned_words, user_id=self.user.id
        )
        self.layout_lists.addWidget(self.window_scroll)
        self.layout_hide_lists.addWidget(self.window_hide_scroll)

        self.window_scroll.hide_signal.connect(self.but_hide_clicked)
        self.window_hide_scroll.hide_signal.connect(self.but_hide_clicked)

        self.label_user_name.setText(self.user.name)
        self.show_quantity_learned_words()
        self.but_setting.setHidden(False)
        self.settings_ui()

    def but_hide_clicked(self, subtitle_list: SubtitleList):
        if subtitle_list.is_hide:
            self.window_hide_scroll.extend_subtitle_list([subtitle_list])
            self.window_scroll.pop_subtitle_list(subtitle_list)
        else:
            self.window_scroll.extend_subtitle_list([subtitle_list])
            self.window_hide_scroll.pop_subtitle_list(subtitle_list)

    def settings_ui(self):
        self.settings = QSettings("MainWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
            index = int(self.settings.value("tab_widget currentIndex", 0))
            self.tab_widget.setCurrentIndex(index)
        except:
            pass

    def on_but_setting_released(self):
        ui = ViewSettings(self.user)
        ui.show()

    def on_but_learned_words_released(self):
        view = ViewListWords(self.words_learned, self.learned_words, self.user.id)
        view.show()

    def show_quantity_learned_words(self):
        count = self.learned_words_repo.get_count_by_user_id(self.user.id)
        self.but_quantity_learned_words.setText(str(count))

    def on_but_create_list_released(self):
        view = CreateListWords_2(user_id=self.user.id, learned_words=self.learned_words)
        view.show()
        self.make_connection_create_list_words(view)

    @pyqtSlot(SubtitleList)
    def get_slider_value_create_list_words(self, subtitle_list: SubtitleList):
        self.subtitle_lists.append(subtitle_list)
        self.window_scroll.extend_subtitle_list([subtitle_list])

    def make_connection_create_list_words(self, slider_object):
        slider_object.changed_value.connect(self.get_slider_value_create_list_words)

    def on_but_logout_released(self):
        self.logout_requested.emit()

    def closeEvent(self, event):

        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())
        self.settings.setValue(
            "tab_widget currentIndex", self.tab_widget.currentIndex()
        )


def test_run():
    repo_user = UserRepository()
    user = repo_user.get(1)

    app = QApplication(sys.argv)
    win = Main(user)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
