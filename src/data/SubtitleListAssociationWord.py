from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.data.Base import Base

if TYPE_CHECKING:
    from .SubtitleList import SubtitleList
    from .WordWithTranslations import WordWithTranslations


class SubtitleListAssociationWord(Base):
    __tablename__ = "subtitle_list_words_association"

    # id: Mapped[int] = mapped_column(primary_key=True)
    word_id: Mapped[int] = mapped_column(
        ForeignKey("words.id", ondelete="CASCADE"), primary_key=True
    )
    subtitle_list_id: Mapped[int] = mapped_column(
        ForeignKey("subtitle_lists.id", ondelete="CASCADE"), primary_key=True
    )

    frequency: Mapped[int] = mapped_column(default=1, server_default="1")

    word: Mapped["WordWithTranslations"] = relationship(
        "WordWithTranslations",
        back_populates="subtitle_list_association",
        lazy="joined",
    )
    subtitle_list: Mapped["SubtitleList"] = relationship(
        "SubtitleList", back_populates="words_association", overlaps="words"
    )
