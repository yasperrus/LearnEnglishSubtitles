from dataclasses import dataclass

from sqlalchemy.orm import Mapped, mapped_column


@dataclass
class WordWithFrequency:
    name: Mapped[str] = mapped_column(default="")
    frequency: Mapped[int] = mapped_column(default=0)
