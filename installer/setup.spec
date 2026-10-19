from pathlib import Path
root=Path(SPECPATH)
a=Analysis([str(root/'setup.py')],pathex=[str(root)],binaries=[],
    datas=[(str(root/name),'.') for name in ['Setup.qml','release.json','company-mark.png','crossgen.ico']],
    hiddenimports=['PySide6.QtQuick'],excludes=['torch','torchaudio','funasr','numpy','pandas','scipy','matplotlib','transformers','IPython','pytest'],noarchive=False)
a.binaries=[e for e in a.binaries if not (Path(e[0]).name.lower().startswith('icu') and 'codex-runtimes' in e[1].lower())]
pyz=PYZ(a.pure)
exe=EXE(pyz,a.scripts,a.binaries,a.datas,[],name='CrossGen-Setup',console=False,debug=False,
    strip=False,upx=False,icon=str(root/'crossgen.ico'))
