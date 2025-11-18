import os
import sys
from typing import TYPE_CHECKING

from PyQt5 import uic
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from config import ROOT_DIR

if TYPE_CHECKING:
    pass
from src.services.auth_service import AuthService


class Registration(QWidget):

    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setWindowTitle("Регистрация")
        self.auth = AuthService()

    def load_ui(self):
        ui_file = os.path.join(ROOT_DIR, "res", "uis", "registration.ui")
        self.window = uic.loadUi(ui_file, self)
        self.settings = QSettings("RegistrationWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def on_but_registration_released(self):
        self.on_register()
        self.close()

    def on_register(self):
        name = self.line_edit_login.text().strip()
        password = self.line_edit_password.text()
        password_repeat = self.line_edit_password_repeat.text()
        if password != password_repeat:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        try:
            user = self.auth.register(name, password)
        except ValueError:
            QMessageBox.warning(
                self, "Validation", "Логин не пустой, пароль >= 4 символов"
            )
            return
        if user is None:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
        else:
            QMessageBox.information(self, "OK", "Пользователь создан")
            self.close()

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Registration()
    win.show()
    sys.exit(app.exec())
