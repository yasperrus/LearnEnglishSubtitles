import os
import sys

from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QApplication, QColorDialog

from config import ROOT_DIR
from src.core.theme_manager import ThemeManager
from src.data import User
from src.repositories.theme_repository import ThemeRepository
from src.repositories.user_repository import UserRepository


class ViewSettings(QWidget):
    def __init__(self, user: User):
        super().__init__()

        self.user = user
        self.repo = ThemeRepository()

        self.load_user_theme()

        self.init_ui()

        self.manager = ThemeManager()
        self.manager.subscribe(self)
        current_theme = self.manager.get_theme()
        if current_theme:
            self.apply_theme(current_theme)

    def apply_theme(self, theme):
        if not theme:
            return

        self.main_widget.setVisible(True)
        self.main_widget.setStyleSheet(
            f"""#main_widget {{
                     background: qlineargradient(
                        spread:pad,
                        x1:0, y1:1, x2:1, y2:1,
                        stop:0 {theme.primary_bg},
                        stop:1 {theme.secondary_bg}
                    )
                 }}
                 QWidget, QLabel, QPushButton {{
                    color: {theme.text_color};
                 }}
                 """
        )

        self.but_primary_bg.setStyleSheet(f"background: {theme.primary_bg};")
        self.but_secondary_bg.setStyleSheet(f"background: {theme.secondary_bg};")
        self.but_text_bg.setStyleSheet(f"background: {theme.text_color};")

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
        self.manager.set_theme(self.theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    repo_user = UserRepository()
    user = repo_user.get(1)
    win = ViewSettings(user)
    win.show()
    sys.exit(app.exec())
