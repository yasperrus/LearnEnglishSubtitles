from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.data.Base import Base

if TYPE_CHECKING:
    from .PathOfSpeech import PathOfSpeech


class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    translation: Mapped[str] = mapped_column(default="")
    isMain: Mapped[bool] = mapped_column(default=False)

    path_of_speech_id: Mapped[int] = mapped_column(
        ForeignKey("path_of_speeches.id", ondelete="CASCADE")
    )
    path_of_speech: Mapped["PathOfSpeech"] = relationship(
        "PathOfSpeech", back_populates="translations", lazy="joined"
    )
