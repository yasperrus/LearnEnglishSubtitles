from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.Base import Base

if TYPE_CHECKING:
    from src.data.WordWithTranslations import WordWithTranslations
    from src.data.User import User


class LearnedWord(Base):
    __tablename__ = "learned_words"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), primary_key=True
    )

    learned_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), server_default=func.current_timestamp()
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="learned_words_association"
    )
    word: Mapped["WordWithTranslations"] = relationship(
        back_populates="learned_by_association"
    )

    __table_args__ = (
        Index("idx_learned_user_word", "user_id", "word_id"),
        Index("idx_learned_word_user", "word_id", "user_id"),
    )
