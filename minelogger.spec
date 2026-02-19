# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

# Collect Flask's built-in static/template data files
from PyInstaller.utils.hooks import collect_data_files
flask_datas = collect_data_files("flask")
jinja2_datas = collect_data_files("jinja2")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=flask_datas + jinja2_datas + [
        ("minelogger/templates", "minelogger/templates"),
    ],
    hiddenimports=[
        "werkzeug.serving",
        "werkzeug.routing",
        "werkzeug.exceptions",
        "jinja2.ext",
        "markupsafe._speedups",
        "itsdangerous.url_safe",
        "itsdangerous.timed",
        "blinker.base",
        "colorama",
        "minelogger.cli",
        "minelogger.server",
        "minelogger.db",
        "minelogger.export",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,   # onedir mode
    name="minelogger",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,               # avoid AV false positives
    console=True,            # console suppressed via VBScript at OS level
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="minelogger",       # output: dist/minelogger/
)
