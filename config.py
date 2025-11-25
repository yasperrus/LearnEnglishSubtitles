# Настройки приложения
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# config.py
import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


WORDS_PER_SUBLIST = 2000  # сколько слов создавать при первом открытии SubList
WORDS_PER_PAGE = 100  # сколько слов отображать за раз в WordListView
SUBLIST_PAGE_SIZE = 50  # сколько SubList отображать за раз в главном окне
