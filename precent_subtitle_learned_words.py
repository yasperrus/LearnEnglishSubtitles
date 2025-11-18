
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.data.LearnedWord import LearnedWord


def test_run():
    engine = create_engine("sqlite:///res/db/myTestDB.db", echo=False)
    session = Session(autoflush=False, bind=engine)
    learned_words: LearnedWord = session.query(LearnedWord).all()

    with open('../AnalizSubtitlesFrequency/learned_words.txt', 'w', encoding="utf-8") as file:
        for item in learned_words:
            file.write(str(item.name) + "\n")

#find ./subtitles -type f -exec cp {} ./subs \;
if __name__ == "__main__":
    test_run()
