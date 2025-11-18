import asyncio
from typing import List

import aiohttp
import requests
from bs4 import BeautifulSoup

from src.data.PathOfSpeech import PathOfSpeech
from src.data.Translation import Translation
from src.data.WordWithTranslations import WordWithTranslations


class TranslatorFromEnglishIntoRussian:

    def analiz_soup(self, soup) -> WordWithTranslations:
        return_word: WordWithTranslations = WordWithTranslations()
        cforms_result = soup.find_all("div", class_="cforms_result")
        if len(cforms_result):
            print("cforms_result")
            return_word.name = (
                cforms_result[0]
                .find("span", class_="ref_source")
                .find("span", class_="source_only sayWord")
                .text
            )
            response_path_of_speech_main = (
                cforms_result[0]
                .find("div", class_="cform")
                .find("span", class_="ref_psp")
                .text
            )
            try:
                return_word.transcription = (
                    cforms_result[0].find("span", class_="transcription").text
                )
            except:
                try:
                    return_word.transcription = (
                        cforms_result[1].find("span", class_="transcription").text
                    )
                except:
                    print(f"не найдена транскрипция: {return_word.name}")
                    return_word.transcription = ""
            for cf in cforms_result:
                print("cf")
                word_and_path_of_speech = PathOfSpeech(name="-")
                return_word.path_of_speeches.append(word_and_path_of_speech)
                word_and_path_of_speech.name = cf.find("span", class_="ref_psp").text
                if response_path_of_speech_main == word_and_path_of_speech.name:
                    word_and_path_of_speech.isMain = True

                response_translations = cf.find("div", class_="translations").find_all(
                    "div", "translation-item"
                )
                for t in response_translations:
                    translation = Translation(name="-")
                    word_and_path_of_speech.translations.append(translation)
                    translation.translation = t.find(
                        "span", class_="result_only sayWord"
                    ).text
        return return_word

    async def get_translations_async(self, session, word_name: WordWithTranslations):
        url = (
            f"https://www.translate.ru/перевод/английский-русский?text={word_name.name}"
        )
        word_with_translations: WordWithTranslations = WordWithTranslations()
        try:
            async with session.get(url) as response:
                response_text = await response.text()
                soup = BeautifulSoup(response_text, "lxml")
                word_with_translations = self.analiz_soup(soup)
        except:
            print(f"{word_name.name} : Нет результата")
            # return_word.path_of_speeches.append(PathOfSpeech(translations=[Translation()]))
        word_with_translations.name = word_name.name
        return word_with_translations

    def get_path_of_speech_with_translations(
        self, word_name: WordWithTranslations
    ) -> WordWithTranslations:
        url = (
            f"https://www.translate.ru/перевод/английский-русский?text={word_name.name}"
        )
        return_word: WordWithTranslations = WordWithTranslations()
        return_word.name = word_name.name
        try:
            response = requests.get(url)
            response_text = response.text
            soup = BeautifulSoup(response_text, "lxml")
            return_word = self.analiz_soup(soup)
        except:
            print(f"{word_name.name} : Нет результата")
            return_word.translations = [Translation()]
        return return_word

    async def gather_data(
        self, words_names: List[WordWithTranslations]
    ) -> List[WordWithTranslations]:
        words: List[WordWithTranslations] = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            c = 0
            for w in words_names:
                task = asyncio.create_task(self.get_translations_async(session, w))
                tasks.append(task)
                c += 1
            words = await asyncio.gather(*tasks)
        return words


def test_async_run_translations():
    words_names = [
        WordWithTranslations(name="elzebub"),  # without translation
        WordWithTranslations(name="leap"),
        WordWithTranslations(name="extralarge"),
    ]

    translator = TranslatorFromEnglishIntoRussian()
    words = asyncio.run(translator.gather_data(words_names))
    for w in words:
        print(f"{w.name} {w.transcription}")
        for p in w.path_of_speeches:
            print(f"\t{p.name}")
            for t in p.translations:
                print(f"\t\t{t.translation}")


def test_run_get_translation():
    translator = TranslatorFromEnglishIntoRussian()
    wordForSaving: WordWithTranslations = (
        translator.get_path_of_speech_with_translations(
            WordWithTranslations(name="break")
        )
    )
    print(f"{wordForSaving.name} {wordForSaving.transcription}")
    for p in wordForSaving.pathOfSpeeches:
        print(f"\t{p.name}")
        for t in p.translations:
            print(f"\t\t{t.translation}")


if __name__ == "__main__":
    test_async_run_translations()
