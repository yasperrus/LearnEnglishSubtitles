from src.data import Theme
from src.repositories.theme_repository import ThemeRepository


class UserService:
    def __init__(self):
        self.theme_repo = ThemeRepository()

    def create_or_update_theme(self, user_id: int, theme: Theme) -> Theme:
        """Создаём или обновляем тему для пользователя"""
        return self.theme_repo.create_or_update_by_user_id(user_id, theme)
