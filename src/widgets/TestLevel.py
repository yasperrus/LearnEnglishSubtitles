import fnmatch
import os
import sys
from datetime import datetime
from random import choice
from threading import Timer

import pygame
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication

from config import ROOT_DIR
from src.data import LearningWord
from src.db.session import SessionLocal
from src.repositories.learning_word_repository_live import LearningWordRepositoryLive
from src.repositories.subtitle_list_repository import SubtitleListRepository


class TestLevel(QWidget):
    REWARD_COST = 1
    REWARD_IF = 1

    current_position = 0
    quantity_correct_answer = 0

    PATH_WAY_ICON_CHECKED = os.path.join(ROOT_DIR, "res", "icons", "checked.png")
    PATH_WAY_ICON_WRONG = os.path.join(ROOT_DIR, "res", "icons", "wrong.png")
    PATH_WAY_ICON_EASY = os.path.join(ROOT_DIR, "res", "icons", "easy.png")
    PATH_WAY_ICON_HARD = os.path.join(ROOT_DIR, "res", "icons", "hard_3.png")

    def __init__(
        self,
        user_id: int,
        subtitle_list_id: int,
        title: str = "",
    ):
        super().__init__()
        self.user_id = user_id
        self.subtitle_list_id = subtitle_list_id
        session = SessionLocal()
        self.learning_word_repo = LearningWordRepositoryLive(session)
        self.learning_words = self.learning_word_repo.gets_by_user_id_subtitle_list_id(
            self.user_id, self.subtitle_list_id
        )

        self.words_original = self.learning_words
        self.load_ui()
        self.set_title(title)
        self.settings = QSettings("TestWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

        pygame.mixer.init()
        self.label_check.setHidden(True)
        print(f"{len(self.learning_words)} {self.current_position}")
        self.change_view_word(self.learning_words[self.current_position])

    def set_title(self, title):
        self.setWindowTitle(f"Тест уровень 0. Список - {title}")

    def load_ui(self):
        ui_file = os.path.join(base_path(), "res", "uis", "test_level.ui")
        self.window = uic.loadUi(ui_file, self)

    def set_setting_view_word(self):
        self.view_correct_word_status()
        self.view_but_icon_hard_status()

    def view_correct_word_status(self):
        if self.learning_words[self.current_position].isRight:
            self.set_right_answer()
        elif self.learning_words[self.current_position].isRight == None:
            self.set_default_answer()
        else:
            self.set_wrong_answer()

    def set_right_answer(self):
        pixmap = QPixmap(self.PATH_WAY_ICON_CHECKED)
        self.label_right.setPixmap(pixmap)
        self.but_check.setEnabled(False)
        self.label_right.setHidden(False)

    def set_wrong_answer(self):
        pixmap = QPixmap(self.PATH_WAY_ICON_WRONG)
        self.label_right.setPixmap(pixmap)
        self.but_check.setEnabled(True)
        self.label_right.setHidden(False)

    def set_default_answer(self):
        pixmap = QPixmap()
        self.label_right.setPixmap(pixmap)
        self.but_check.setEnabled(True)
        self.label_right.setHidden(True)

    def change_view_word(self, learning_word: LearningWord):
        self.show_word(learning_word)
        self.label_count_list.setText(
            f"{self.current_position + 1}/{len(self.learning_words)}"
        )
        self.set_setting_view_word()
        self.load_audio(learning_word.word.name)

    def show_word(self, learning_word: LearningWord):
        learning_word.quantity_showed += 1
        translation = self.get_translation_from_word(learning_word)
        self.label_word.setText(
            f"{learning_word.word.name}\n{learning_word.word.transcription}"
            f"\n{translation}"
        )

    def get_translation_from_word(self, learning_word: LearningWord):
        if learning_word.word.path_of_speeches.__len__() > 0:
            for p in learning_word.word.path_of_speeches:
                if p.isMain:
                    for t in p.translations:
                        if t.isMain:
                            return t.translation
                    return p.translations[0].translation
            return learning_word.word.path_of_speeches[0].translations[0].translation
        return ""

    def load_audio(self, word_name: str):
        self.but_speak.setEnabled(False)
        if os.path.exists(os.path.join(base_path(), "res", "audios", word_name)):
            if (
                len(
                    fnmatch.filter(
                        os.listdir(
                            os.path.join(base_path(), "res", "audios", word_name)
                        ),
                        "*.mp3",
                    )
                )
                > 0
            ):
                self.learning_words[self.current_position].isAudio = True
                self.but_speak.setEnabled(True)
                random_filename = choice(
                    os.listdir(os.path.join(base_path(), "res", "audios", word_name))
                )
                pygame.mixer.music.load(
                    os.path.join(base_path(), "res", "audios", word_name)
                    + "/"
                    + random_filename
                )

    def on_but_speak_released(self):
        if self.learning_words[self.current_position].isAudio:
            pygame.mixer.music.play()

    def on_but_hard_released(self):
        if self.learning_words[self.current_position].isHard:
            self.learning_words[self.current_position].isHard = False
        else:
            self.learning_words[self.current_position].isHard = True
        self.view_but_icon_hard_status()

    def view_but_icon_hard_status(self):
        if self.learning_words[self.current_position].isHard:
            icon_hard_word = QIcon(self.PATH_WAY_ICON_HARD)
        else:
            icon_hard_word = QIcon(self.PATH_WAY_ICON_EASY)
        self.but_hard.setIcon(icon_hard_word)

    def on_but_next_released(self):
        self.next_current_position()
        word = self.learning_words[self.current_position]
        self.change_view_word(word)

    def next_current_position(self):
        self.current_position += 1
        if self.current_position >= len(self.learning_words):
            self.current_position = 0

    def on_but_back_released(self):
        self.back_current_position()
        word = self.learning_words[self.current_position]
        self.change_view_word(word)

    def back_current_position(self):
        self.current_position -= 1
        if self.current_position < 0:
            self.current_position = len(self.learning_words) - 1

    def on_but_check_released(self):
        if self.check_answer(self.learning_words[self.current_position].answer):
            self.task_right_answer()
        else:
            self.task_wrong_answer()
        self.show_label_check_per_second()
        self.on_but_next_released()

    def task_right_answer(self):
        self.quantity_correct_answer += 1
        self.learning_words[self.current_position].learned_at = datetime.now()
        self.reward()
        self.label_quantity_correct_answer.setText(
            self.quantity_correct_answer.__str__()
        )
        self.learning_words[self.current_position].isRight = True
        pixmap = QPixmap(self.PATH_WAY_ICON_CHECKED)
        self.label_check.setPixmap(pixmap)

    def show_label_check_per_second(self):
        hide_label_timer = Timer(1.0, self.hide_label_check).start()
        self.label_check.setHidden(False)

    def hide_label_check(self):
        self.label_check.setHidden(True)

    def reward(self):
        if (
            self.learning_words[self.current_position].quantity_correct_answer
            < self.REWARD_IF
        ):
            self.learning_words[
                self.current_position
            ].quantity_correct_answer += self.REWARD_COST

    def task_wrong_answer(self):
        self.learning_words[self.current_position].isRight = False
        pixmap = QPixmap(self.PATH_WAY_ICON_WRONG)
        self.label_check.setPixmap(pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Up or key == 16777249:
            self.on_but_back_released()
        elif key == Qt.Key.Key_Down or key == 16777251:
            self.on_but_next_released()
        elif key == 16777220:
            self.on_but_check_released()
        event.accept()

    def check_answer(self, answer):
        return True

    def closeEvent(self, event):
        self.learning_word_repo.commit()
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


def test_run():
    user_id = 1
    sub_repo = SubtitleListRepository()
    subtitle_lists = sub_repo.get_subtitle_lists_by_user_id(user_id)
    random_subtitle_list = choice(subtitle_lists)

    app = QApplication(sys.argv)
    win = TestLevel(
        user_id=user_id,
        subtitle_list_id=random_subtitle_list.id,
        title=random_subtitle_list.name,
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
