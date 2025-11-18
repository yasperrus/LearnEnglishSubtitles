import random
import sys

from PyQt5.QtWidgets import QApplication

from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.TestLevel2 import TestLevel2


class TestLevel2_2(TestLevel2):
    REWARD_IF = 7

    def set_title(self, title):
        self.setWindowTitle(f"Тест уровень 2.2. Список - {title}")

    def get_edit_hint_word(self, text_word: str):
        list_text_word = list(text_word)
        count = int(list_text_word.__len__() / 1.5)
        list_letter_numbers = random.sample(
            range(0, list_text_word.__len__() - 1), count
        )
        for i in list_letter_numbers:
            list_text_word[i] = " _"
        return "".join(list_text_word)

    def reward(self):
        super().reward()
        if self.learning_words[self.current_position].quantity_correct_answer < 5:
            self.learning_words[self.current_position].quantity_correct_answer = 4


def test_run():
    user_id = 1
    sub_repo = SubtitleListRepository()
    subtitle_lists = sub_repo.get_subtitle_lists_by_user_id(user_id)
    random_subtitle_list = random.choice(subtitle_lists)

    app = QApplication(sys.argv)
    win = TestLevel2_2(
        user_id=user_id,
        subtitle_list_id=random_subtitle_list.id,
        title=random_subtitle_list.name,
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
