from typing import List

from sqlalchemy import select, insert

from src.data import LearningWord
from src.data.LearnedWord import LearnedWord
from src.db.session import SessionLocal


class LearnedWordRepository:
    def create(self, learned_word: LearnedWord):
        with SessionLocal() as s:
            s.add(learned_word)
            s.commit()
            s.refresh(learned_word)
            return learned_word

    def adds(self, learned_words: List[LearnedWord]):
        with SessionLocal() as s:
            print("LearnedWordRepository Start adds")
            for i in range(0, len(learned_words), 100):
                batch = learned_words[i : i + 100]
                stmt = (
                    insert(LearningWord)
                    .prefix_with("OR IGNORE")
                    .values(
                        [
                            {"user_id": word.user_id, "word_id": word.word_id}
                            for word in batch
                        ]
                    )
                )
                print(
                    f"LearnedWordRepository Start adds create query {learned_words[0].word_id}"
                )
                s.execute(stmt)
            s.commit()
            print("LearnedWordRepository Start adds create query commit")

    def gets_by_user_id(self, user_id: int):
        with SessionLocal() as s:
            stmt = select(LearnedWord).where(LearnedWord.user_id == user_id)
            return s.scalars(stmt).all()

    def get_count_by_user_id(self, user_id: int):
        with SessionLocal() as s:
            return s.query(LearnedWord).filter_by(user_id = user_id).count()



def test_run():
    learned_repository = LearnedWordRepository()
    # learned_words: List[LearnedWord] = learned_repository.gets_by_user_id(1)
    count: int = learned_repository.get_count_by_user_id(1)
    print(count)


if __name__ == "__main__":
    test_run()
