from sqlalchemy import String, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.Base import Base


class Theme(Base):
    __tablename__ = "theme"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    user: Mapped["User"] = relationship(back_populates="theme")

    primary_bg: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
        default="#FFFFFFFF",
        server_default=text("'#FFFFFFFF'"),
    )
    secondary_bg: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
        default="#FFFFFFFF",
        server_default=text("'#FFFFFFFF'"),
    )
    text_color: Mapped[str] = mapped_column(
        String(9),
        nullable=False,
        default="#000000FF",
        server_default=text("'#000000FF'"),
    )
