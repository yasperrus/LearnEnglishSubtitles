import sys

from PyQt5.QtWidgets import QApplication

from src.repositories.user_repository import UserRepository
from src.widgets.ViewWordWithDelete import ViewWordWithDelete
from src.widgets.WidgetVerticalLayoutScrollForWords import (
    WidgetVerticalLayoutScrollForWords,
)


class WidgetVerticalLayoutScrollForWordsWithDelete(WidgetVerticalLayoutScrollForWords):

    def get_create_widget(self, item):
        return ViewWordWithDelete(item)


def test_run():
    repo_user = UserRepository()
    user = repo_user.get_all_relationship_by_id(1)

    app = QApplication(sys.argv)
    win = WidgetVerticalLayoutScrollForWords(user.subtitle_lists[0].words)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    test_run()
