from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.data.Base import Base

if TYPE_CHECKING:
    from .User import User
    from .SubtitleList import SubtitleList


class UserAssociationSubtitleList(Base):
    __tablename__ = "user_association_subtitle_list"

    # id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    subtitle_list_id: Mapped[int] = mapped_column(
        ForeignKey("subtitle_lists.id", ondelete="CASCADE"), primary_key=True
    )
    user: Mapped["User"] = relationship("User", back_populates="user_association")
    subtitle_list: Mapped["SubtitleList"] = relationship(
        "SubtitleList", back_populates="user_association"
    )
