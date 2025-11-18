from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.data.Base import Base
from .SubtitleListAssociationWord import SubtitleListAssociationWord

if TYPE_CHECKING:
    from .User import User
from .UserAssociationSubtitleList import UserAssociationSubtitleList
from .WordWithTranslations import WordWithTranslations


class SubtitleList(Base):
    __tablename__ = "subtitle_lists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(default="", server_default="")
    is_open_menu: Mapped[bool] = mapped_column(default=False, server_default="False")
    is_hide: Mapped[bool] = mapped_column(default=False, server_default="False")
    quantity_words: Mapped[int] = mapped_column(default=0, server_default="0")
    quantity_words_frequencies: Mapped[int] = mapped_column(
        default=0, server_default="0"
    )
    quantity_learned_words: Mapped[int] = mapped_column(default=0, server_default="0")
    quantity_learned_words_frequencies: Mapped[int] = mapped_column(
        default=0, server_default="0"
    )

    created_time: Mapped[datetime] = mapped_column(
        default=datetime.now(), server_default=func.current_timestamp()
    )
    modified_time: Mapped[datetime] = mapped_column(
        default=datetime.now(), server_default=func.current_timestamp()
    )

    user_association: Mapped[List["UserAssociationSubtitleList"]] = relationship(
        "UserAssociationSubtitleList",
        back_populates="subtitle_list",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_association_subtitle_list",
        back_populates="subtitle_lists",
        viewonly=True,
    )

    words: Mapped[List["WordWithTranslations"]] = relationship(
        "WordWithTranslations",
        secondary="subtitle_list_words_association",
        uselist=True,
        overlaps="subtitle_list_association,word",
        passive_deletes=False,
    )

    words_association: Mapped[List["SubtitleListAssociationWord"]] = relationship(
        "SubtitleListAssociationWord",
        back_populates="subtitle_list",
        cascade="all, delete-orphan",
        passive_deletes=True,
        overlaps="words",
    )
