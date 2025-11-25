import sys

from PyQt5 import uic
from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from config import resource_path
from src.data.User import User
from src.services.auth_service import AuthService
from src.widgets.Registration import Registration


class Login(QWidget):
    logged_in = pyqtSignal(User)

    def __init__(self):
        super().__init__()
        self.load_ui()
        self.setWindowTitle("Авторизация")
        self.auth = AuthService()

    def load_ui(self):
        ui_file = resource_path("res/uis/login.ui")
        self.window = uic.loadUi(ui_file, self)
        self.settings = QSettings("LoginWindow", "LearnEnglish")
        try:
            self.resize(self.settings.value("window size"))
            self.move(self.settings.value("window position"))
        except:
            pass

    def on_but_registration_released(self):
        Registration().show()
        # self.close()

    def on_but_login_released(self):
        name = self.line_edit_login.text().strip()
        password = self.line_edit_password.text()
        if not name or not password:
            QMessageBox.warning(self, "Validation", "Введите логин и пароль")
            return
        user = self.auth.authenticate(name, password)
        if user is None:
            QMessageBox.warning(self, "Error", "Неверные учётные данные")
            return
        # emit id to main for opening main window
        self.logged_in.emit(user)

    def closeEvent(self, event):
        self.settings.setValue("window size", self.size())
        self.settings.setValue("window position", self.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Login()
    win.show()
    sys.exit(app.exec())
