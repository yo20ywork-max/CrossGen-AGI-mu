from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

root = Path(SPECPATH).resolve().parents[1]
data = collect_data_files('opencc') + collect_data_files('faster_whisper')
a = Analysis([str(Path(SPECPATH) / 'launcher.py')], pathex=[str(root)],
    binaries=collect_dynamic_libs('ctranslate2'), datas=data,
    hiddenimports=['run_daemon', 'product_tools', 'desktop_session', 'explicit_reply',
                   'pynput.keyboard._win32', 'pynput.mouse._win32', 'PySide6.QtQuick', 'PySide6.QtTest',
                   'desktop_ui.voice_worker', 'desktop_ui.asr_worker'],
    excludes=['torch', 'torchaudio', 'funasr', 'transformers', 'scipy', 'pandas', 'matplotlib',
              'IPython', 'notebook', 'pytest'],
    noarchive=False)
# Qt on Windows 11 uses the Windows ICU API. A Poppler directory in the build
# host PATH contains a different ICU with version-suffixed exports. Do not ship
# that unrelated same-named DLL; let Windows resolve its own ICU implementation.
a.binaries = [entry for entry in a.binaries if not (
    Path(entry[0]).name.lower().startswith('icu') and 'codex-runtimes' in entry[1].lower())]
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='CrossGen-AGI-mu',
    console=False, debug=False, strip=False, upx=False, contents_directory='_internal', icon=str(root / 'desktop_ui/assets/crossgen.ico'))
voice = EXE(pyz, a.scripts, [], exclude_binaries=True, name='CrossGen-Voice',
    console=True, debug=False, strip=False, upx=False, contents_directory='_internal', icon=str(root / 'desktop_ui/assets/crossgen.ico'))
coll = COLLECT(exe, voice, a.binaries, a.datas, name='CrossGen-AGI-mu', strip=False, upx=False)
