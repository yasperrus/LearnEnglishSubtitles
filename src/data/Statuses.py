from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.data.Base import Base


class Statuses(Base):
    __tablename__ = "statues_words"
    __allow_unmapped__ = True

    isHard: Mapped[bool] = mapped_column(default=False, server_default="False")
    correct_answer: Mapped[int] = mapped_column(default=0, server_default="0")
    showed: Mapped[int] = mapped_column(default=0, server_default="0")

    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), primary_key=True
    )

    # <-- исправлено здесь:
    word: Mapped["WordWithTranslations"] = relationship(
        "WordWithTranslations", back_populates="statuses", single_parent=True
    )

    isAudio: bool = False
    isRight: bool = None
    answer: str = ""
