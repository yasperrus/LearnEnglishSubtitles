from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.Base import Base

if TYPE_CHECKING:
    from src.data.WordWithTranslations import WordWithTranslations
    from src.data.User import User


class LearningWord(Base):
    __tablename__ = "learning_words"
    __allow_unmapped__ = True

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), primary_key=True
    )

    isHard: Mapped[bool] = mapped_column(default=False, server_default="False")
    quantity_correct_answer: Mapped[int] = mapped_column(default=0, server_default="0")
    quantity_showed: Mapped[int] = mapped_column(default=0, server_default="0")

    learned_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), server_default=func.current_timestamp()
    )

    user: Mapped["User"] = relationship(
        "User", back_populates="learning_words_association"
    )
    word: Mapped["WordWithTranslations"] = relationship(
        back_populates="learning_by_association"
    )

    __table_args__ = (
        Index("idx_learning_user_word", "user_id", "word_id"),
        Index("idx_learning_word_user", "word_id", "user_id"),
    )

    isAudio: bool = False
    isRight: bool = None
    answer: str = ""