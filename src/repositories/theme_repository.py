from src.data import Theme, User
from src.db.session import SessionLocal


class ThemeRepository:
    def get(self, id: int) -> Theme | None:
        with SessionLocal() as s:
            theme: Theme = s.query(Theme).filter(Theme.id == id).one_or_none()
            if not theme:
                return None
            return theme

        return session.query(Theme).filter_by(id=theme_id).first()

    def get_by_user_id(self, user_id: int) -> Theme | None:
        with SessionLocal() as session:
            return (
                session.query(Theme).join(User).filter(User.id == user_id).one_or_none()
            )

    def create_or_update_by_user_id(self, user_id: int, theme: Theme):
        with SessionLocal() as s:
            user_theme = self.get_by_user_id(user_id)
            s.merge(theme)
            if user_theme:
                user_theme.primary_bg = theme.primary_bg
                user_theme.secondary_bg = theme.secondary_bg
                user_theme.text_color = theme.text_color
            else:
                theme.user_id = user_id
                s.add(theme)
            s.commit()
            # s.refresh(theme)
            return theme
