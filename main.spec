# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Путь к плагинам Qt
qt_plugins = r"C:/Users/Yasper/Documents/LearnEnglishSubtitles/.venv/lib/site-packages/PyQt5/Qt5/plugins"

# Путь к модели spaCy
spacy_model_path = r".venv/Lib/site-packages/en_core_web_sm"

# Включаем папки (источник → куда попадёт в сборке)
datas = [
    ('res', 'res'),
    (qt_plugins, 'PyQt5/Qt5/plugins'),
    ('en_core_web_sm', 'en_core_web_sm'),
]

hiddenimports = collect_submodules("PyQt5") + collect_submodules("spacy")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LearnEnglishSubtitles',
    debug=False,
    strip=False,
    upx=False,
    console=False,
)
