import sys
from random import choice

from PyQt5.QtWidgets import QApplication

from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.TestLevel0 import TestLevel0


class TestLevel0_2(TestLevel0):
    combo_answers = [None] * 4
    REWARD_IF = 3

    def set_title(self, title):
        self.setWindowTitle(f"Тест уровень 0.2. Список - {title}")

    def fill_combobox_with_answers(self, right_answer_point):
        for item in range(4):
            self.combobox_answers.addItem(self.combo_answers[item])


def test_run():
    user_id = 1
    sub_repo = SubtitleListRepository()
    subtitle_lists = sub_repo.get_subtitle_lists_by_user_id(user_id)
    random_subtitle_list = choice(subtitle_lists)

    app = QApplication(sys.argv)
    win = TestLevel0_2(
        user_id=user_id,
        subtitle_list_id=random_subtitle_list.id,
        title=random_subtitle_list.name,
    )
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
