from src.data import User, LearnedWord
from src.data.WordWithTranslations import WordWithTranslations
from src.db.session import SessionLocal


def get_words_by_list_word(session, list_word: list, chunk_size: int = 900):

    results = []
    for i in range(0, len(list_word), chunk_size):
        chunk = list_word[i : i + chunk_size]
        results.extend(
            session.query(WordWithTranslations)
            .filter(WordWithTranslations.name.in_(chunk))
            .all()
        )
    return results


def add_learned_words_from_file(session, user_id: int, file_path: str):

    user = session.get(User, user_id)
    if not user:
        raise ValueError(f"User {user_id} не найден")

    with open(file_path, "r", encoding="utf-8") as f:
        words_text = [line.strip() for line in f if line.strip()]

    if not words_text:
        return

    # Получаем все слова из базы, которые есть в списке
    words = get_words_by_list_word(session, words_text)
    print(f"{len(words)}")

    for word in words:
        exists = any(
            assoc.word_id == word.id for assoc in user.learned_words_association
        )
        if not exists:
            assoc = LearnedWord(user=user, word=word)
            session.add(assoc)

    session.commit()


def run_test():
    uri = "../../learned_words.txt"
    db = SessionLocal()
    add_learned_words_from_file(session=db, user_id=1, file_path=uri)


if __name__ == "__main__":
    run_test()
