import os
import sys

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QApplication, QColorDialog

from config import ROOT_DIR
from src.core.theme_manager import ThemeManager
from src.data import User
from src.repositories.theme_repository import ThemeRepository
from src.repositories.user_repository import UserRepository
from src.widgets.ThemeWidget import ThemeWidget


class ViewSettings(QWidget, ThemeWidget):
    def __init__(self, user: User):
        QWidget.__init__(self)
        ThemeWidget.__init__(self)

        self.user = user
        self.repo = ThemeRepository()

        self.load_user_theme()

        self.init_ui()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # делаем фон прозрачным
        current_theme = ThemeManager().get_theme()
        if current_theme:
            self.apply_theme(current_theme)
        # self.manager = ThemeManager()
        # self.manager.subscribe(self)
        # current_theme = self.manager.get_theme()
        # if current_theme:
        #     self.apply_theme(current_theme)

    def init_different(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "view_settings.ui")
        self.window = uic.loadUi(ui_file, self)

    def init_ui(self):
        self.init_different()

    def load_user_theme(self):
        self.theme = self.repo.get_by_user_id(self.user.id)

    def on_but_primary_bg_released(self):
        color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
        if not color.isValid():
            return
        self.theme.primary_bg = color.name(QColor.HexArgb)
        # self.but_primary_bg.setStyleSheet(f"background: {QColor.HexArgb};")
        print(f"primary_bg: {self.theme.primary_bg}")
        self.save_and_apply()

    def on_but_secondary_bg_released(self):
        color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
        if not color.isValid():
            return
        self.theme.secondary_bg = color.name(QColor.HexArgb)
        # self.but_secondary_bg.setStyleSheet(f"background: {QColor.HexArgb};")
        print(f"secondary_bg: {self.theme.secondary_bg}")
        self.save_and_apply()

    def on_but_text_bg_released(self):
        color = QColorDialog.getColor(options=QColorDialog.ShowAlphaChannel)
        if not color.isValid():
            return
        self.theme.text_color = color.name(QColor.HexArgb)
        print(f"text_color: {self.theme.text_color}")
        self.save_and_apply()

    def save_and_apply(self):
        self.repo.create_or_update_by_user_id(user_id=self.user.id, theme=self.theme)
        ThemeManager().set_theme(self.theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    repo_user = UserRepository()
    user = repo_user.get(1)
    win = ViewSettings(user)
    win.show()
    sys.exit(app.exec())
