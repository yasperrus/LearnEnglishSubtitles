from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.data.Base import Base

if TYPE_CHECKING:
    from .LearnedWord import LearnedWord

from .SubtitleListAssociationWord import SubtitleListAssociationWord
from .PathOfSpeech import PathOfSpeech
from .Statuses import Statuses


class WordWithTranslations(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    transcription: Mapped[str] = mapped_column(
        String(30), default="", server_default=""
    )

    statuses: Mapped["Statuses"] = relationship(
        "Statuses", back_populates="word", uselist=False, lazy="selectin"
    )

    path_of_speeches: Mapped[List["PathOfSpeech"]] = relationship(
        "PathOfSpeech", back_populates="word", lazy="selectin"
    )

    subtitle_list_association: Mapped[List["SubtitleListAssociationWord"]] = (
        relationship(
            "SubtitleListAssociationWord",
            back_populates="word",
            lazy="selectin",
            cascade="all, delete-orphan",
        )
    )

    learned_by_association: Mapped[List["LearnedWord"]] = relationship(
        "LearnedWord", back_populates="word", lazy="selectin"
    )

    learning_by_association: Mapped[List["LearningWord"]] = relationship(
        "LearningWord", back_populates="word", lazy="selectin"
    )
