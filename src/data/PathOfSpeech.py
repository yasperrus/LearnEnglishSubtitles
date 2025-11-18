from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.Base import Base

if TYPE_CHECKING:
    from src.data.WordWithTranslations import WordWithTranslations
from src.data.Translation import Translation


class PathOfSpeech(Base):
    __tablename__ = "path_of_speeches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    isMain: Mapped[bool] = mapped_column(default=False)

    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"))
    word: Mapped["WordWithTranslations"] = relationship(
        "WordWithTranslations",
        back_populates="path_of_speeches",
        # lazy="joined"
    )

    translations: Mapped[List["Translation"]] = relationship(
        "Translation", back_populates="path_of_speech", uselist=True, lazy="selectin"
    )
