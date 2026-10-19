"""CrossGen per-user installation wizard and one-click shutdown control center."""
import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import threading
import webbrowser
from engine import Installer, Job, Cancelled
from auth import Auth

ASSETS=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent))


def shortcuts(root, installer):
    root=Path(root);target=root/'CrossGen-Setup.exe'
    if getattr(sys,'frozen',False) and Path(sys.executable).resolve()!=target.resolve():shutil.copy2(sys.executable,target)
    if not target.exists():return
    def quoted(value):return "'"+str(value).replace("'","''")+"'"
    script=root/'create-shortcuts.ps1'
    script.write_text("$shell = New-Object -ComObject WScript.Shell\n"
        "$places = @($shell.SpecialFolders.Item('Desktop'), $shell.SpecialFolders.Item('Programs'))\n"
        "foreach ($place in $places) {\n"
        "  $link = $shell.CreateShortcut((Join-Path $place 'CrossGen-AGI-μ.lnk'))\n"
        "  $link.TargetPath = "+quoted(target)+"\n"
        "  $link.Arguments = '--launch --root '+[char]34+"+quoted(root)+"+[char]34\n"
        "  $link.WorkingDirectory = "+quoted(root)+"\n"
        "  $link.IconLocation = "+quoted(str(root/'app/desktop_ui/assets/crossgen.ico')+',0')+"\n"
        "  $link.Save()\n}\n",encoding='utf-8-sig')
    installer.run(['powershell.exe','-NoProfile','-NonInteractive','-ExecutionPolicy','Bypass','-File',str(script)],timeout=30)
    script.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path)
    parser.add_argument('--launch',action='store_true');parser.add_argument('--render',type=Path)
    parser.add_argument('--shutdown-check',action='store_true')
    args=parser.parse_args()
    if args.shutdown_check and not args.render:parser.error('--shutdown-check requires --render')
    os.environ['QT_QUICK_CONTROLS_STYLE']='Basic'
    if args.render:os.environ.update(QT_QPA_PLATFORM='offscreen',QT_QUICK_BACKEND='software')
    from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QTimer
    from PySide6.QtGui import QGuiApplication,QIcon,QFontDatabase
    from PySide6.QtQml import QQmlApplicationEngine
    from PySide6.QtQuick import QQuickWindow
    app=QGuiApplication(sys.argv[:1]);app.setWindowIcon(QIcon(str(ASSETS/'crossgen.ico')))
    app.setApplicationName('CrossGen 安裝與控制台')
    for name in ['msjh.ttc','msjhbd.ttc','segoeui.ttf']:
        path=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'/name
        if path.is_file():QFontDatabase.addApplicationFont(str(path))
    default=Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'CrossGen-AGI-mu'
    config=json.loads((ASSETS/'release.json').read_text(encoding='utf8'))

    class Bridge(QObject):
        changed=Signal();event=Signal(str,object)
        def __init__(self):
            super().__init__();self.root=(args.root or default).resolve();self.root.mkdir(parents=True,exist_ok=True)
            self._status='準備就緒';self._detail='從 GitHub 公開下載並校驗程式、模型、語音與瀏覽器元件。'
            self._progress=0.0;self._busy=False;self._ready=(self.root/'installed.json').exists()
            self._code='';self._url='';self._worker=None;self._closing=False;self._job=None;self._installer=None
            self._allowExit=bool(args.render)
            self._probe=None
            self._auth=Auth();self.event.connect(self.receive)
        @Property(str,notify=changed)
        def installPath(self):return str(self.root)
        @Property(str,notify=changed)
        def status(self):return self._status
        @Property(str,notify=changed)
        def detail(self):return self._detail
        @Property(float,notify=changed)
        def progress(self):return self._progress
        @Property(bool,notify=changed)
        def busy(self):return self._busy
        @Property(bool,notify=changed)
        def ready(self):return self._ready
        @Property(str,notify=changed)
        def authCode(self):return self._code
        @Property(bool,notify=changed)
        def canExit(self):return self._allowExit
        def make_installer(self):
            if self._job and not self._job.closed:return self._installer
            self._cancel=threading.Event();self._job=Job()
            self._installer=Installer(self.root,config,self.event.emit,self._cancel,self._job,self._auth.token)
            return self._installer
        @Slot(str,object)
        def receive(self,kind,value):
            if self._closing and kind!='closed':return
            if kind=='status':self._status=value;self._detail='請保持網路連線，下載可中斷續傳。';self._progress=0
            elif kind=='progress':
                n,total=value;self._progress=n/max(total,1);self._detail=f'{n/1_000_000:,.1f} / {total/1_000_000:,.1f} MB'
            elif kind=='auth':
                self._code=value['code'];self._url=value['url'];self._status='請在瀏覽器完成登入授權'
                self._detail='使用可存取 CrossGen 私有模型的 Hugging Face 帳號；授權後會自動繼續。'
                webbrowser.open(self._url)
            elif kind=='done':
                self._busy=False;self._ready=True;self._code='';self._progress=1;self._status='CrossGen 已啟動'
                self._detail='控制台管理本次模型服務；使用「一鍵全部關閉」可一併退出。'
                self._auth.forget()
            elif kind=='error':self._busy=False;self._code='';self._status='尚未完成';self._detail=value
            elif kind=='closed':
                if args.shutdown_check:
                    passed=self._probe is not None and self._probe.poll() is not None
                    args.render.with_suffix('.shutdown.json').write_text(json.dumps({'button_clicked':True,'owned_process_exited':passed,'passed':passed}),encoding='utf8')
                self._allowExit=True;app.quit()
            self.changed.emit()
        def work(self,install):
            if self._busy or self._closing:return
            self._busy=True;self._status='正在準備';self.changed.emit()
            worker=self.make_installer()
            def execute():
                try:
                    if install:
                        self._code=''
                        worker.install();shortcuts(self.root,worker)
                    worker.launch();self.event.emit('done',None)
                except Cancelled as exc:self.event.emit('error',str(exc))
                except Exception as exc:
                    # Do not expose tokens, signed download URLs, or raw authentication exceptions.
                    text=str(exc)
                    if 'http' in text or 'hf_' in text or 'Bearer' in text:text='連線或安裝未完成，請重新嘗試。'
                    self.event.emit('error',text[-1600:])
            self._worker=threading.Thread(target=execute,daemon=True);self._worker.start()
        @Slot()
        def install(self):self.work(True)
        @Slot()
        def launch(self):self.work(False)
        @Slot()
        def openAuth(self):
            if self._url:webbrowser.open(self._url)
        @Slot()
        def microphoneSettings(self):webbrowser.open('ms-settings:privacy-microphone')
        @Slot()
        def closeAll(self):
            if self._closing:return
            self._closing=True;self._status='正在關閉 CrossGen 與所有背景工作';self._detail='停止錄音與下載，釋放模型資源。';self.changed.emit()
            def stop():
                if self._installer:self._installer.close_all()
                if self._worker:self._worker.join(22)
                self._auth.forget();self.event.emit('closed',None)
            threading.Thread(target=stop,daemon=True).start()
    mutex=None
    if not args.render:
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateMutexW.argtypes=[ctypes.c_void_p,wintypes.BOOL,wintypes.LPCWSTR];kernel.CreateMutexW.restype=wintypes.HANDLE
        name='Local\\CrossGenSetup-'+hashlib.sha256(str((args.root or default).resolve()).casefold().encode()).hexdigest()[:20]
        mutex=kernel.CreateMutexW(None,False,name)
        if ctypes.get_last_error()==183:
            window=ctypes.windll.user32.FindWindowW(None,'CrossGen-AGI-μ｜安裝與控制台')
            if window:ctypes.windll.user32.ShowWindow(window,9);ctypes.windll.user32.SetForegroundWindow(window)
            return 0
    bridge=Bridge();engine=QQmlApplicationEngine();engine.rootContext().setContextProperty('setup',bridge)
    errors=[];engine.warnings.connect(lambda warnings:errors.extend(w.toString() for w in warnings))
    engine.load(QUrl.fromLocalFile(str(ASSETS/'Setup.qml')))
    if not engine.rootObjects():raise RuntimeError(str(errors))
    window=engine.rootObjects()[0]
    if args.render:
        def render():
            try:
                assert not errors, errors
                args.render.parent.mkdir(parents=True,exist_ok=True)
                assert window.grabWindow().save(str(args.render))
                args.render.with_suffix('.json').write_text(json.dumps({'qml_warnings':errors,'frozen':bool(getattr(sys,'frozen',False)),'microphone_opened':False,'installation_started':False}),encoding='utf8')
                if args.shutdown_check:
                    from PySide6.QtCore import Qt
                    from PySide6.QtTest import QTest
                    worker=bridge.make_installer()
                    bridge._probe=worker.job.start(['powershell.exe','-NoProfile','-NonInteractive','-Command','Start-Sleep -Seconds 30'])
                    button=window.findChild(QObject,'closeAllButton');assert button is not None
                    button.forceActiveFocus();QTest.keyClick(window,Qt.Key_Space)
                else:app.quit()
            except Exception as exc:
                args.render.with_suffix('.error.txt').write_text(str(exc),encoding='utf8');app.exit(1)
        QTimer.singleShot(700,render)
    elif args.launch and bridge._ready:QTimer.singleShot(150,bridge.launch)
    try:return app.exec()
    finally:
        if bridge._job:bridge._job.close()
        if mutex:
            kernel.CloseHandle.argtypes=[wintypes.HANDLE];kernel.CloseHandle(mutex)


if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        if sys.platform=='win32' and '--render' not in sys.argv:ctypes.windll.user32.MessageBoxW(None,'安裝精靈無法啟動：'+str(exc),'CrossGen',0x10)
        raise
