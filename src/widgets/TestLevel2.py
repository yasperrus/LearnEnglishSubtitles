import random
import sys

from PyQt5.QtWidgets import QApplication

from src.data import LearningWord
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.TestLevel1 import TestLevel1


class TestLevel2(TestLevel1):

    REWARD_IF = 6

    def set_title(self, title):
        self.setWindowTitle(f"Тест уровень 2. Список - {title}")

    def show_word(self, learning_word: LearningWord):
        self.label_word.setText(f"{self.get_translation_from_word(learning_word)}")

    def set_setting_view_word(self):
        super().set_setting_view_word()
        self.line_edit_translate.setPlaceholderText(
            self.get_edit_hint_word(
                self.learning_words[self.current_position].word.name
            )
        )

    def get_edit_hint_word(self, text_word: str):
        list_text_word = list(text_word)
        count = int(list_text_word.__len__() / 2)
        list_letter_numbers = random.sample(
            range(0, list_text_word.__len__() - 1), count
        )
        for i in list_letter_numbers:
            list_text_word[i] = " _"
        return "".join(list_text_word)

    def reward(self):
        super().reward()
        if self.learning_words[self.current_position].quantity_correct_answer < 4:
            self.learning_words[self.current_position].quantity_correct_answer = 3

    def check_answer(self, answer):
        if (
            self.learning_words[self.current_position]
            .word.name.__str__()
            .lower()
            .strip()
            == str(answer).lower().strip()
        ):
            return True
        return False


def test_run():
    user_id = 1
    sub_repo = SubtitleListRepository()
    subtitle_lists = sub_repo.get_subtitle_lists_by_user_id(user_id)
    random_subtitle_list = random.choice(subtitle_lists)

    app = QApplication(sys.argv)
    win = TestLevel2(
        user_id=user_id,
        subtitle_list_id=random_subtitle_list.id,
        title=random_subtitle_list.name,
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
