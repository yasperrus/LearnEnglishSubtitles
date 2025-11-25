import re
import time
from typing import List

import spacy
# from nltk import pos_tag, word_tokenize, FreqDist
# from nltk.stem import WordNetLemmatizer
from tabulate import tabulate

from config import resource_path
from src.data.WordWithFrequency import WordWithFrequency
from src.scripts.FileReader import FileReader

# nltk.download("words")
# nltk.download("omw-1.4")
model_path = resource_path("en_core_web_sm")

nlp = spacy.load(model_path, disable=["ner"])
from collections import Counter


class ConvertTextToWordsWithFrequency:

    words_with_frequency: List[WordWithFrequency] = []
    keep_pos = {"NOUN", "VERB", "ADJ"}
    min_len = 2

    def __init__(self, text):
        self.words_with_frequency = self.__convert_subtitle(text)

    def __iter__(self):
        return iter(self.words_with_frequency)

    def __len__(self):
        return len(self.words_with_frequency)

    def __getitem__(self, index):
        return self.words_with_frequency[index]

    def __convert_subtitle(self, text) -> List[WordWithFrequency]:
        cleared_text = self.clear_text(text)
        # return self.__frequencies(cleared_text)
        return self.__frequencies_n_process(cleared_text)

    # def __frequencies(self, text):
    #     lemmatizer = WordNetLemmatizer()
    #     tokenize_text = word_tokenize(text)
    #     i = 0
    #     for token, tag in pos_tag(tokenize_text):
    #         pos = tag[0].lower()
    #         if pos not in ["a", "r", "n", "v"]:
    #             pos = "n"
    #         tokenize_text[i] = lemmatizer.lemmatize(word=token, pos=pos)
    #         i += 1
    #     fd = FreqDist(token.lower() for token in tokenize_text)
    #
    #     wordsWithFrequency: List[WordWithFrequency] = []
    #     for f in fd.items():
    #         if len(f[0]) > 2:
    #             wordsWithFrequency.append(WordWithFrequency(name=f[0], frequency=f[1]))
    #     return wordsWithFrequency

    def __frequencies(self, text):
        clean_text = text
        doc = nlp(clean_text)
        words = []
        for token in doc:
            if token.is_stop or token.is_punct or token.is_space:
                continue
            if len(token.lemma_) < self.min_len:
                continue
            if self.keep_pos and token.pos_.upper() not in self.keep_pos:
                continue
            words.append(token.lemma_.lower())
        counter = Counter(words)
        return [WordWithFrequency(name=w, frequency=f) for w, f in counter.items()]

    def __frequencies_n_process(self, text):
        texts = self.split_text_by_words(text, 32)
        counters = []
        for doc in nlp.pipe(texts, n_process=1, batch_size=128):
            words = [
                token.lemma_.lower()
                for token in doc
                if not token.is_stop  # исключаем стоп-слова
                and not token.is_punct  # исключаем пунктуацию
                and not token.is_space  # исключаем пробелы
                and len(token.lemma_) >= self.min_len  # фильтр по минимальной длине
                and (
                    not self.keep_pos or token.pos_.upper() in self.keep_pos
                )  # фильтр по части речи
            ]
            counters.append(Counter(words))

        total_counter = sum(counters, Counter())
        list_words = [
            WordWithFrequency(name=w, frequency=f) for w, f in total_counter.items()
        ]
        return list_words

    def split_text_by_words(self, text: str, n_parts: int) -> List[str]:
        words = text.split()
        total_words = len(words)
        part_size = total_words // n_parts
        chunks = []

        for i in range(n_parts):
            start = i * part_size
            end = (i + 1) * part_size if i < n_parts - 1 else total_words
            chunk = " ".join(words[start:end])
            chunks.append(chunk)

        return chunks

    def clear_text(self, text):
        text = text.lower()
        text = re.sub(r"\d*:\d*:.*\n", "", text)
        text = re.sub(r"<[^>]*>", "", text)
        text = re.sub(r"\n+", " ", text)
        # text = re.sub(r"\{\\.*\}", "", text)
        text = re.sub(r"[0-9]", "", text)
        text = re.sub(r"'\w+", "", text)
        text = re.sub(
            r"[\"\'!#$%&()*+,-./:;<=>?@[\]^_`{|}~╗┐я\xa0«»\t—…♪―☯❃]", " ", text
        )
        return text.strip()

    def print_result_with_tabulate(self):
        data = []
        for w in self.words_with_frequency:
            try:
                data.append([w.name, w.frequency])
            except:
                print(f"Error {w.name}")
        table = tabulate(data, headers=["Name", "Frequency"], tablefmt="tsv")
        print(table)


def test_run():
    uri = "/home/chris/Videos/English/The big bang theory/Season 1/Episode 3/TheBigBangTheoryS1E3.vtt"
    # uri = (
    #     "/home/chris/Documents/subtitles/different/Wreck-It.Ralph.2012.WEB-DL.DSNP.srt"
    # )
    reader = FileReader(uri)
    text = reader.get_text()
    time_start = time.time()
    words_with_frequency = ConvertTextToWordsWithFrequency(text)
    time_end = time.time()
    # words_with_frequency.print_result_with_tabulate()
    print(f"Время выполнения конвертации субтитров в слова: {time_end - time_start}")
    print(len(words_with_frequency))


if __name__ == "__main__":
    test_run()
