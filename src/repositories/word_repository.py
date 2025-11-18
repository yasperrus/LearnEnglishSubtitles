from typing import List

from sqlalchemy import select

from src.data import LearnedWord
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal


class WordRepository:

    def get_words_learned_by_user_id(self, user_id: int):
        with SessionLocal() as s:
            stmt = (
                select(WordWithTranslations)
                .join(LearnedWord)
                .where(
                    LearnedWord.user_id == user_id,
                )
            )
            return s.scalars(stmt).all()

    def get_words_by_list_word(
        self, list_word: List[str]
    ) -> List[WordWithTranslations]:
        with SessionLocal() as s:
            words_with_translations = (
                s.query(WordWithTranslations)
                .filter(WordWithTranslations.name.in_(list_word))
                .all()
            )
            s.close()
            return words_with_translations

    def update_word(self, word: WordWithTranslations):
        with SessionLocal() as s:
            s.merge(word)
            s.commit()

    def update_words(self, words: List[WordWithTranslations]):
        with SessionLocal() as s:
            for w in words:
                s.merge(w)
            s.commit()


list_word = ["name", "new", "cool", "sdfsdfsd"]


def test_run():
    w_repo = WordRepository()
    result_repo: List[WordWithTranslations] = w_repo.get_words_by_list_word(list_word)
    print(len(result_repo))
    if result_repo:
        for w in result_repo:
            print(w.name)
            print("\t" + w.transcription)


if __name__ == "__main__":
    test_run()
