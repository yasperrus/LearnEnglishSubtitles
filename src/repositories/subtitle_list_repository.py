from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.data import UserAssociationSubtitleList, WordWithTranslations
from src.data.SubtitleList import SubtitleList
from src.data.SubtitleListAssociationWord import SubtitleListAssociationWord
from src.db.session import SessionLocal


class SubtitleListRepository:
    # def add_subtitle_list_by_user_id(self, user_id: int, subtitle_list: SubtitleList):
    #     with SessionLocal() as s:
    #         s.add(subtitle_list)
    #         user: User = (
    #             s.query(User)
    #             .options(joinedload(User.subtitle_lists))
    #             .filter(User.id == user_id)
    #             .one_or_none()
    #         )
    #         if user:
    #             user.subtitle_lists.append(subtitle_list)
    #             s.commit()
    #             s.refresh(subtitle_list)
    #             return subtitle_list
    #         return None

    def get_subtitle_lists_by_user_id(self, user_id: int):
        with SessionLocal() as s:
            subtitle_lists = (
                s.query(SubtitleList)
                .join(UserAssociationSubtitleList)
                .filter(UserAssociationSubtitleList.user_id == user_id)
                .order_by(SubtitleList.id.desc())
                .all()
            )
            return subtitle_lists

    def refresh_words(self, subtitle_list: SubtitleList):
        with SessionLocal() as session:
            subtitle_list = session.merge(subtitle_list)
            session.refresh(subtitle_list, ["words"])  # подгрузит только words
        return subtitle_list

    def get_words_by_subtitle_list_id(self, subtitle_list_id: int):
        with SessionLocal() as s:
            words = (
                s.query(WordWithTranslations)
                .join(SubtitleListAssociationWord)
                .filter(
                    SubtitleListAssociationWord.subtitle_list_id == subtitle_list_id
                )
                .all()
            )
            return words

    def get_subtitle_list_by_subtitle_list_id(self, subtitle_list_id: int):
        with SessionLocal() as s:
            # subtitle_list = (
            #     s.query(SubtitleList)
            #     .filter(
            #         SubtitleList.id == subtitle_list_id,
            #     )
            #     .one_or_none()
            # )
            stmt = (
                select(SubtitleList)
                .options(
                    selectinload(SubtitleList.words_association).joinedload(
                        SubtitleListAssociationWord.word
                    ),
                )
                .order_by(SubtitleList.id)
                .filter(SubtitleList.id == subtitle_list_id)
            )
            subtitle_list = s.scalars(stmt).one_or_none()

            if not subtitle_list:
                return None
            return subtitle_list

    def update_subtitle_list(self, subtitle_list: SubtitleList):
        with SessionLocal() as s:
            s.merge(subtitle_list)
            s.commit()

    def delete_subtitle_list_by_subtitle_list_id(self, subtitle_list_id: int):
        with SessionLocal() as s:
            subtitle_list = s.query(SubtitleList).get(subtitle_list_id)
            s.delete(subtitle_list)
            s.commit()


def test_delete_subtitle_list():
    repo_sub = SubtitleListRepository()
    repo_sub.delete_subtitle_list_by_subtitle_list_id(2)


def test_change_frequency_words():
    sub_repo = SubtitleListRepository()
    sub_list: SubtitleList = sub_repo.get_subtitle_list_by_subtitle_list_id(44)
    print(sub_list.id)
    # print(len(sub_list))
    # for s in sub_list:
    for w in sub_list.words_association:
        print(
            f"id_word: {w.word.id} | word_name: {w.word.name} | frequency: {w.frequency} | subtitle_list_id: {w.subtitle_list_id} | word_id: {w.word_id}"
        )
        w.frequency = 77
    sub_repo.update_subtitle_list(sub_list)


if __name__ == "__main__":

    test_delete_subtitle_list()
