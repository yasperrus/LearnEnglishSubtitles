from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.data.Base import Base
from .LearnedWord import LearnedWord
from .LearningWord import LearningWord
from .SubtitleList import SubtitleList
from .UserAssociationSubtitleList import UserAssociationSubtitleList


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    session_token: Mapped[str] = mapped_column(nullable=True)
    quantity_entered: Mapped[int] = mapped_column(default=0, server_default="0")
    quantity_learned_words: Mapped[int] = mapped_column(default=0, server_default="0")
    quantity_known_words: Mapped[int] = mapped_column(default=0, server_default="0")
    created_time: Mapped[datetime] = mapped_column(
        default=datetime.now(), server_default=func.current_timestamp()
    )
    modified_time: Mapped[datetime] = mapped_column(
        default=datetime.now(), server_default=func.current_timestamp()
    )

    user_association: Mapped[List["UserAssociationSubtitleList"]] = relationship(
        "UserAssociationSubtitleList",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    subtitle_lists: Mapped[List["SubtitleList"]] = relationship(
        "SubtitleList",
        secondary="user_association_subtitle_list",
        back_populates="users",
        order_by="SubtitleList.id.desc()",
        overlaps="user_association,subtitle_list,user",
    )

    learning_words_association: Mapped[List["LearningWord"]] = relationship(
        "LearningWord",
        back_populates="user",
    )

    learned_words_association: Mapped[List["LearnedWord"]] = relationship(
        "LearnedWord",
        back_populates="user",
    )
