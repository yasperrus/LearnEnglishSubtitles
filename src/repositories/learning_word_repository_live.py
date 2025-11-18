from sqlalchemy.orm import selectinload

from src.data import (
    SubtitleListAssociationWord,
    LearnedWord,
    PathOfSpeech,
)
from src.data.LearningWord import LearningWord
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal


class LearningWordRepositoryLive:
    def __init__(self, session):
        self.session = session

    def gets_by_user_id_subtitle_list_id(
        self, user_id: int, subtitle_list_id: int, limit: int = 20
    ) -> list[LearningWord]:
        learning_words = (
            self.session.query(LearningWord)
            .join(WordWithTranslations, LearningWord.word_id == WordWithTranslations.id)
            .join(
                SubtitleListAssociationWord,
                WordWithTranslations.id == SubtitleListAssociationWord.word_id,
            )
            .outerjoin(
                LearnedWord,
                (LearnedWord.word_id == WordWithTranslations.id)
                & (LearnedWord.user_id == user_id),
            )
            .filter(
                LearningWord.user_id == user_id,
                SubtitleListAssociationWord.subtitle_list_id == subtitle_list_id,
                LearnedWord.word_id == None,  # исключаем выученные
            )
            .options(
                selectinload(LearningWord.word)
                .selectinload(WordWithTranslations.path_of_speeches)
                .selectinload(PathOfSpeech.translations)
            )
            .order_by(
                LearningWord.quantity_showed.asc(),
                LearningWord.quantity_correct_answer.asc(),
            )
            .limit(limit)
            .all()
        )
        return learning_words

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


def test_run():
    session = SessionLocal()
    learning_word_repo = LearningWordRepositoryLive(session)

    learning_words = learning_word_repo.gets_by_user_id_subtitle_list_id(1, 3)
    for w in learning_words:
        print(w.word.name)
    print(len(learning_words))


if __name__ == "__main__":
    test_run()
