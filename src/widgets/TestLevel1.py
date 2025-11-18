import os
import sys
from random import choice

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

from config import ROOT_DIR
from src.data import LearningWord
from src.data.LearnedWord import LearnedWord
from src.repositories.learned_word_repository import LearnedWordRepository
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.TestLevel import TestLevel


class TestLevel1(TestLevel):
    REWARD_IF = 4
    REWARD_COST = 2

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "test_level_1.ui")
        self.window = uic.loadUi(ui_file, self)

    def set_title(self, title):
        self.setWindowTitle(f"Тест уровень 1. Список - {title}")

    def show_word(self, learning_word: LearningWord):
        self.learning_words[self.current_position].quantity_showed += 1
        self.label_word.setText(
            f"{learning_word.word.name.__str__()}\n{learning_word.word.transcription}"
        )

    def set_setting_view_word(self):
        super().set_setting_view_word()
        self.line_edit_translate.setText(
            self.learning_words[self.current_position].answer
        )
        self.line_edit_translate.setFocus()

    def set_right_answer(self):
        super().set_right_answer()
        self.line_edit_translate.setEnabled(False)

    def set_wrong_answer(self):
        super().set_wrong_answer()
        self.line_edit_translate.setEnabled(True)

    def set_default_answer(self):
        super().set_default_answer()
        self.line_edit_translate.setEnabled(True)

    def on_but_check_released(self):
        if self.line_edit_translate.text():
            self.learning_words[self.current_position].answer = (
                self.line_edit_translate.text()
            )
            super().on_but_check_released()
        else:
            self.on_but_next_released()

    def reward(self):
        super().reward()
        repo_learned = LearnedWordRepository()
        repo_learned.adds(
            learned_words=[
                LearnedWord(
                    user_id=self.user_id,
                    word_id=self.learning_words[self.current_position].word_id,
                )
            ]
        )

    def check_answer(self, answer):
        for p in self.learning_words[self.current_position].word.path_of_speeches:
            for t in p.translations:
                if (
                    t.translation.__str__().lower().strip()
                    == str(answer).lower().strip()
                ):
                    return True
        return False


def test_run():
    user_id = 1
    sub_repo = SubtitleListRepository()
    subtitle_lists = sub_repo.get_subtitle_lists_by_user_id(user_id)
    random_subtitle_list = choice(subtitle_lists)

    app = QApplication(sys.argv)
    win = TestLevel1(
        user_id=user_id,
        subtitle_list_id=random_subtitle_list.id,
        title=random_subtitle_list.name,
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
