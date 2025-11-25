import sys
from random import randint, choice

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from config import resource_path
from src.data import LearningWord
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.widgets.TestLevel import TestLevel


class TestLevel0(TestLevel):
    combo_answers = [None] * 4
    simple_translation = ("движение", "сила", "проект", "редкий", "случай", "щель")
    REWARD_IF = 2

    def load_ui(self):
        ui_file = resource_path("res/uis/test_level_0.ui")
        self.window = uic.loadUi(ui_file, self)

    def set_title(self, title):
        self.setWindowTitle(f"Тест уровень 0. Список - {title}")

    def show_word(self, learning_word: LearningWord):
        self.label_word.setText(
            f"{learning_word.word.name.__str__()}\n{learning_word.word.transcription}"
        )

    def set_setting_view_word(self):
        super().set_setting_view_word()
        self.fill_random_wrong_answers()
        if self.learning_words[self.current_position].isRight == True:
            for item, answer in enumerate(self.combo_answers):
                if self.learning_words[self.current_position].answer == answer:
                    self.combobox_answers.setCurrentIndex(item)

    def fill_random_wrong_answers(self):
        self.combobox_answers.clear()
        self.combo_answers.clear()
        self.combo_answers = [None] * 4
        right_answer_random_point = randint(0, 3)
        self.combo_answers[right_answer_random_point] = (
            self.learning_words[self.current_position]
            .word.path_of_speeches[0]
            .translations[0]
            .translation
        )

        for i in range(len(self.combo_answers)):
            if self.combo_answers[i] == None:
                if self.learning_words.__len__() > 2:
                    self.combo_answers[i] = (
                        self.learning_words[randint(0, len(self.learning_words) - 1)]
                        .word.path_of_speeches[0]
                        .translations[0]
                        .translation
                    )
                else:
                    self.combo_answers[i] = self.simple_translation[
                        randint(0, len(self.simple_translation) - 1)
                    ]

        self.fill_combobox_with_answers(right_answer_random_point)

    def fill_combobox_with_answers(self, right_answer_point):
        for item in range(4):
            self.combobox_answers.addItem(self.combo_answers[item])
            if right_answer_point == item:
                self.combobox_answers.setItemIcon(
                    item, QIcon(self.PATH_WAY_ICON_CHECKED)
                )
            else:
                self.combobox_answers.setItemIcon(item, QIcon(self.PATH_WAY_ICON_WRONG))

    def on_but_check_released(self):
        self.learning_words[self.current_position].answer = (
            self.combobox_answers.itemText(self.combobox_answers.currentIndex())
        )
        super().on_but_check_released()

    def on_combobox_answers_activated(self, index):
        if type(index) == int:
            self.learning_words[self.current_position].answer = (
                self.combobox_answers.itemText(index)
            )
            self.check_answer(self.learning_words[self.current_position].answer)
            self.on_but_check_released()

    def check_answer(self, answer):
        for p in self.learning_words[self.current_position].word.path_of_speeches:
            for t in p.translations:
                if (
                    t.translation.__str__().lower().strip()
                    == str(answer).lower().strip()
                ):
                    return True
        return False

    def set_right_answer(self):
        super().set_right_answer()
        self.combobox_answers.setEnabled(False)

    def set_wrong_answer(self):
        super().set_wrong_answer()
        self.combobox_answers.setEnabled(True)

    def set_default_answer(self):
        super().set_default_answer()
        self.combobox_answers.setEnabled(True)


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
