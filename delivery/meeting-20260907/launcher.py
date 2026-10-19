"""Meeting executable entrypoint. Uses real product UI and explicitly preview mode."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TAG = 'crossgen-agi-mu:meeting-20260907'
EXPECTED = {
    'CrossGen-core-Q4_K_M.gguf': '60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463',
    'CrossGen-v13-e3-LoRA.gguf': '2963b2e99d2df37f1393f3d8f16fde8cbeca37469620865ee721997b601c643e',
}


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(4 * 1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def main():
    # Run pipe-capable speech helpers before Qt, Ollama, or the task engine.
    for flag in ('--voice-worker', '--asr-worker'):
        if flag in sys.argv:
            sys.argv.remove(flag)
            for stream in (sys.stdin, sys.stdout, sys.stderr):
                if stream is not None:
                    stream.reconfigure(encoding='utf8')
            if flag == '--voice-worker':
                from desktop_ui.voice_worker import main as worker_main
            else:
                from desktop_ui.asr_worker import main as worker_main
            worker_main()
            return 0
    root = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
    os.chdir(root)
    os.environ.update(GHOST_WORKSPACE=str(root / '展示工作區'), GHOST_PLANNER_MODELS=TAG,
        GHOST_VISION_MODELS='', GHOST_ENABLE_VOICE='0', GHOST_USE_MICRO_HINT='0',
        GHOST_ALLOW_SHELL='0', GHOST_ALLOW_OUTSIDE_WORKSPACE='0', GHOST_AUTO_APPROVE_HIGH_RISK='0',
        GHOST_CONTEXT_CLIPBOARD='0', GHOST_NUM_CTX='12288')
    if '--self-check' in sys.argv:
        import run_daemon
        import product_tools
        import desktop_session
        import explicit_reply
        import ollama
        import psutil
        import numpy
        import pyperclip
        import pynput
        from PySide6.QtCore import qVersion
        from playwright.sync_api import sync_playwright
        report = {'frozen': bool(getattr(sys, 'frozen', False)), 'qt': qVersion(),
            'runtime_import_ok': True, 'qml_exists': (root / 'desktop_ui/Main.qml').is_file(),
            'model_required': TAG, 'target_hardware_tested': False, 'release_approved': False}
        (root / 'EXE_SELF_CHECK.json').write_text(json.dumps(report, indent=2), encoding='utf8')
        if not report['qml_exists']: raise RuntimeError('Missing product QML')
        return 0
    # Frozen speech subprocesses need a dedicated entrypoint before calling Qt.
    # This package does not silently fall back to a different voice engine.
    if '--install-model' in sys.argv:
        exe = shutil.which('ollama')
        if not exe: raise RuntimeError('請先安裝並開啟 Ollama：https://ollama.com/download/windows')
        for name, digest in EXPECTED.items():
            path = root / 'models' / name
            if not path.is_file() or sha(path) != digest:
                raise RuntimeError('模型缺失或SHA256不符：' + name)
        subprocess.run([exe, 'create', TAG, '-f', str(root / 'Modelfile')], check=True)
        return 0
    if '--render' not in sys.argv:
        import urllib.request
        try:
            host = os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434').rstrip('/')
            if not host.startswith(('http://', 'https://')): host = 'http://' + host
            with urllib.request.urlopen(host + '/api/tags', timeout=5) as response:
                tags = json.load(response)['models']
            if not any(item['name'] == TAG for item in tags): raise RuntimeError('模型尚未匯入')
        except Exception as exc:
            ctypes.windll.user32.MessageBoxW(None,
                '請先安裝並開啟 Ollama，將兩個 GGUF 放入 models 資料夾，再執行「首次匯入模型.cmd」。\n\n' + str(exc),
                'CrossGen-AGI-μ｜展示準備', 0x10)
            return 1
    import desktop_ui.app as ui
    ui.ROOT = root
    if '--development' not in sys.argv: sys.argv.append('--development')
    return ui.main()


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        root = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
        (root / 'STARTUP_ERROR.txt').write_text(str(exc), encoding='utf8')
        if sys.platform == 'win32' and Path(sys.executable).stem != 'CrossGen-Voice' and not any(a in sys.argv for a in ['--self-check', '--render']):
            ctypes.windll.user32.MessageBoxW(None, str(exc), 'CrossGen-AGI-μ', 0x10)
        raise
