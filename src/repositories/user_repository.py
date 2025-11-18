from sqlalchemy.orm import joinedload, selectinload

from src.data.PathOfSpeech import PathOfSpeech
from src.data.SubtitleList import SubtitleList
from src.data.User import User
from src.data.UserAssociationSubtitleList import UserAssociationSubtitleList
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal
from src.repositories.subtitle_list_repository import SubtitleListRepository
from src.repositories.word_repository import WordRepository


class UserRepository:
    def create(self, user: User):
        with SessionLocal() as s:
            s.add(user)
            s.commit()
            s.refresh(user)
            return user

    def set_token_by_id(self, id: int, token: str):
        with SessionLocal() as s:
            user: User = s.query(User).filter(User.id == id).one_or_none()
            if user:
                user.session_token = token
                s.commit()

    def get_by_name(self, name: str):
        with SessionLocal() as s:
            user = s.query(User).filter(User.name == name).one_or_none()
            if not user:
                return None
            return user

    def get_by_id(self, id: int):
        with SessionLocal() as s:
            user: User = s.query(User).filter(User.id == id).one_or_none()
            if not user:
                return None
            return user

    def get_by_token(self, token: str):
        with SessionLocal() as s:
            user = s.query(User).filter(User.session_token == token).one_or_none()
            if not user:
                return None
            return user

    def get_all_relationship_by_id(self, id):
        with SessionLocal() as s:
            user: User = (
                s.query(User)
                .options(
                    selectinload(User.user_association)
                    .selectinload(UserAssociationSubtitleList.subtitle_list)
                    .selectinload(SubtitleList.words)
                    .selectinload(WordWithTranslations.path_of_speeches)
                    .selectinload(PathOfSpeech.translations)
                )
                .filter(User.id == id)
                .first()
            )
            if not user:
                return None
            return user

    def delete_all_subtitle_list_by_user_id(self, user_id: int):
        with SessionLocal() as s:
            user: User = (
                s.query(User)
                .options(joinedload(User.subtitle_lists))
                .filter(User.id == user_id)
                .one_or_none()
            )
            if user:
                user.subtitle_lists.clear()
                s.commit()

    def add_subtitle_list_by_user_id(self, id, subtitle_list: SubtitleList):
        with SessionLocal() as s:
            s.add(subtitle_list)
            user: User = s.query(User).filter(User.id == id).one_or_none()
            user.subtitle_lists.append(subtitle_list)
            s.commit()
            s.refresh(subtitle_list, attribute_names=["words_association"])
            # subtitle_list.words_association.__len__()
        return subtitle_list


def test_run_add_subtitle_list_by_user_id():
    subtitle_list = SubtitleList(name="ListTestName")
    word_repo = WordRepository()
    words = word_repo.get_words_by_list_word(["new", "old", "cool"])
    subtitle_list.words += words

    repo = UserRepository()
    repo.add_subtitle_list_by_user_id(1, subtitle_list)
    sub_repo = SubtitleListRepository()
    for i, w in enumerate(subtitle_list.words_association):
        w.frequency = 7 + i
        print(w.word.name)
    sub_repo.update_subtitle_list(subtitle_list)


def test_user_delete():
    repo = UserRepository()
    repo.delete_subtitle_list_by_user_id_and_subtitle_list_id(1, 1)


if __name__ == "__main__":

    test_user_delete()
