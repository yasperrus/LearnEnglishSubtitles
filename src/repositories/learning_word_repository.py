from sqlalchemy import insert
from sqlalchemy import select

# если используешь диалект SQLite специально:
from sqlalchemy.dialects.sqlite import insert

from src.data import WordWithTranslations, SubtitleListAssociationWord, LearnedWord
from src.data.LearningWord import LearningWord
from src.db.session import SessionLocal


class LearningWordRepository:

    def adds_words_by_user_id(self, user_id, words: list[WordWithTranslations]):
        with SessionLocal() as s:

            learned_ids = s.query(LearnedWord.word_id).filter_by(user_id=user_id).all()
            learned_ids = {wid for (wid,) in learned_ids}

            new_words = [word for word in words if word.id not in learned_ids]
            if not new_words:
                return

            for i in range(0, len(new_words), 100):
                batch = new_words[i : i + 100]
                stmt = (
                    insert(LearningWord)
                    .prefix_with("OR IGNORE")
                    .values(
                        [{"user_id": user_id, "word_id": word.id} for word in batch]
                    )
                )
                s.execute(stmt)
            s.commit()

    def gets_by_user_id_subtitle_list_id(self, user_id: int, subtitle_list_id: int):
        with SessionLocal() as s:
            stmt = (
                select(LearningWord)
                .join(
                    WordWithTranslations,
                    LearningWord.word_id == WordWithTranslations.id,
                )
                .join(
                    SubtitleListAssociationWord,
                    SubtitleListAssociationWord.word_id == WordWithTranslations.id,
                )
                .where(
                    LearningWord.user_id == user_id,
                    SubtitleListAssociationWord.subtitle_list_id == subtitle_list_id,
                )
            )
            return s.scalars(stmt).all()

    def gets_by_user_id(self, user_id: int):
        with SessionLocal() as s:
            stmt = select(LearningWord).where(LearningWord.user_id == user_id)
            return s.scalars(stmt).all()
