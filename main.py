#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication

from src.core.auth import load_session, clear_session, save_session
from src.core.theme_manager import ThemeManager
from src.db.session import init_db
from src.repositories.theme_repository import ThemeRepository
from src.repositories.user_repository import UserRepository
from src.widgets.Login import Login
from src.widgets.Main import Main


def run():
    init_db()
    app = QApplication(sys.argv)

    session = load_session()
    user_info = None
    if session and session.get("token"):
        user_repo = UserRepository()
        user_info = user_repo.get_by_token(session["token"])

    main_window = None
    login_win = None

    def open_main(user):
        nonlocal main_window, login_win
        main_window = Main(user)

        # handle logout emitted from main_window
        def on_logout():
            clear_session()
            main_window.close()
            show_login()

        repo_theme = ThemeRepository()
        theme = repo_theme.get_by_user_id(user.id)
        ThemeManager().set_theme(theme)
        main_window.logout_requested.connect(on_logout)
        main_window.show()
        if login_win:
            login_win.close()
            login_win = None

    def show_login():
        nonlocal login_win, main_window
        login_win = Login()

        def on_logged(user):
            save_session({"token": user.session_token})
            open_main(user)

        login_win.logged_in.connect(on_logged)
        login_win.show()

    if user_info:
        open_main(user_info)
    else:
        show_login()

    sys.exit(app.exec_())


def apply_theme(self):
    """Применяем тему для пользователя, если он авторизован"""
    if self.theme_manager:
        self.theme_manager.apply_theme()


if __name__ == "__main__":
    run()
