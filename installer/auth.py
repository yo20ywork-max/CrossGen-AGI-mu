"""Hugging Face public CLI device login; credentials live in memory only.

Protocol/client registration: huggingface_hub/utils/_oauth_device.py and constants.py
(Hugging Face, Apache-2.0). No account credential or client secret is bundled.
"""
import json
import os
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from engine import check

CLIENT_ID = '26be6b09-91c5-47da-9861-d2d2bb7a7e36'  # Public Hugging Face CLI client.


def post(endpoint, data):
    request=urllib.request.Request('https://huggingface.co/oauth/'+endpoint,
        data=urllib.parse.urlencode(data).encode(),headers={'Content-Type':'application/x-www-form-urlencoded'})
    try:
        with urllib.request.urlopen(request,timeout=10) as response:return json.load(response)
    except urllib.error.HTTPError as exc:
        try:return json.load(exc)
        except ValueError:raise RuntimeError('登入服務暫時無法使用，請重試。') from None


class Auth:
    def __init__(self):self.access='';self.refresh='';self.expires=0

    def token(self):
        if self.refresh and time.monotonic()>self.expires-60:
            self.accept(post('token',{'grant_type':'refresh_token','refresh_token':self.refresh,'client_id':CLIENT_ID}))
        return self.access

    def accept(self, data):
        if not data.get('access_token'):raise RuntimeError('授權已失效，請重新登入。')
        self.access=data['access_token'];self.refresh=data.get('refresh_token',self.refresh)
        self.expires=time.monotonic()+int(data.get('expires_in',3600))

    def existing(self):
        # Only standard HF credential locations; never enumerate browser profiles.
        token=os.environ.get('HF_TOKEN') or os.environ.get('HUGGING_FACE_HUB_TOKEN')
        path=Path(os.environ.get('HF_TOKEN_PATH',str(Path(os.environ.get('HF_HOME',str(Path.home()/'.cache/huggingface')))/'token')))
        if not token and path.is_file():token=path.read_text(encoding='utf8').strip()
        if token:self.access=token
        return bool(token)

    def login(self,cancel,notify):
        check(cancel)
        data=post('device',{'client_id':CLIENT_ID,'scope':'read-repos'})
        if not data.get('device_code'):raise RuntimeError('無法啟動瀏覽器登入，請重試。')
        url=data.get('verification_uri_complete') or data['verification_uri']
        if urllib.parse.urlparse(url).hostname!='huggingface.co':raise RuntimeError('登入網址驗證失敗。')
        notify('auth',{'url':url,'code':data['user_code']})
        interval=max(1,int(data.get('interval',5)));deadline=time.monotonic()+min(int(data.get('expires_in',900)),900)
        while time.monotonic()<deadline:
            if cancel.wait(interval):check(cancel)
            try:response=post('token',{'grant_type':'urn:ietf:params:oauth:grant-type:device_code',
                'device_code':data['device_code'],'client_id':CLIENT_ID})
            except (OSError,ValueError):continue
            check(cancel)
            if response.get('access_token'):self.accept(response);return
            error=response.get('error')
            if error=='slow_down':interval+=5
            elif error in ('access_denied','expired_token'):raise RuntimeError('登入未授權或已逾時，請按自動安裝重試。')
            elif error not in (None,'authorization_pending'):raise RuntimeError('登入失敗，請重試。')
        raise RuntimeError('登入時間已到，請重新開始。')

    def validate(self,url):
        if urllib.parse.urlparse(url).hostname!='huggingface.co':raise ValueError('Credential destination must be Hugging Face')
        request=urllib.request.Request(url,method='HEAD',headers={'Authorization':'Bearer '+self.token()})
        from engine import SafeRedirect
        try:
            with urllib.request.build_opener(SafeRedirect()).open(request,timeout=15):return True
        except (OSError,ValueError):return False

    def forget(self):self.access='';self.refresh='';self.expires=0
