"""KAP HTTP istemci - session, rate limiting, cache."""

import json
import re
import time
from pathlib import Path
from typing import Any, Optional

import requests

from .models import KAP_BASE


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
}

DEFAULT_CACHE_DIR = Path.home() / ".bbb" / "cache" / "kap"
MIN_REQUEST_INTERVAL = 1.5  # saniye (normal islemler)
ARCHIVE_REQUEST_INTERVAL = 2.0  # saniye (arsivleme)


class KAPClient:
    """KAP.org.tr HTTP istemcisi. Session, rate-limit ve cache yonetimi."""

    def __init__(self, cache_dir: Path = None):
        self.cache_dir = cache_dir or DEFAULT_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._last_request_time: float = 0
        self._session: Optional[requests.Session] = None
        self._min_interval = MIN_REQUEST_INTERVAL

    @property
    def session(self) -> requests.Session:
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(HEADERS)
        return self._session

    def set_archive_mode(self, enabled: bool = True):
        """Arsivleme modunda rate limit'i artir."""
        self._min_interval = ARCHIVE_REQUEST_INTERVAL if enabled else MIN_REQUEST_INTERVAL

    # ── Rate Limiting ──

    def _rate_limit(self):
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()

    # ── HTTP ──

    def get(self, url: str, cache_key: str = None, cache_ttl: int = 300,
            timeout: int = 20) -> Optional[requests.Response]:
        """Rate-limited GET istegi. cache_key verilirse oncelikle cache'e bakar."""
        if cache_key:
            cached = self.cache_read(cache_key, max_age=cache_ttl)
            if cached is not None:
                return cached  # dict/list doner, Response degil

        self._rate_limit()
        try:
            resp = self.session.get(url, timeout=timeout)
            return resp
        except requests.RequestException as e:
            print(f"HTTP hata ({url}): {e}", file=__import__('sys').stderr)
            return None

    def get_json(self, url: str, cache_key: str = None, cache_ttl: int = 300,
                 timeout: int = 20) -> Optional[Any]:
        """GET istegi yap, JSON olarak dondur. Cache destekli."""
        if cache_key:
            cached = self.cache_read(cache_key, max_age=cache_ttl)
            if cached is not None:
                return cached

        resp = self.get(url, timeout=timeout)
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                if cache_key:
                    self.cache_write(cache_key, data)
                return data
            except ValueError:
                return None
        return None

    def get_html(self, url: str, cache_key: str = None, cache_ttl: int = 300,
                 timeout: int = 20) -> Optional[str]:
        """GET istegi yap, HTML text olarak dondur. Cache destekli."""
        if cache_key:
            cached = self.cache_read(cache_key, max_age=cache_ttl)
            if cached is not None:
                return cached

        resp = self.get(url, timeout=timeout)
        if resp and resp.status_code == 200:
            text = resp.text
            if cache_key:
                self.cache_write(cache_key, text)
            return text
        return None

    def download_file(self, url: str, dest_path: Path) -> bool:
        """Dosya indir (PDF, XLSX vb.) - streaming. Basarili ise True doner."""
        self._rate_limit()
        try:
            resp = self.session.get(url, timeout=30, stream=True)
            if resp.status_code != 200:
                return False

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            # KAP bazen dosyalari Java serialized byte array olarak sarmallar.
            # %PDF- imzasi offset 27'de baslar. Wrapper'i atla.
            if dest_path.suffix.lower() == '.pdf':
                with open(dest_path, 'rb') as f:
                    content = f.read()
                pdf_start = content.find(b'%PDF-')
                if pdf_start > 0:
                    # Java wrapper'i atla, saf PDF'i kaydet
                    with open(dest_path, 'wb') as f:
                        f.write(content[pdf_start:])
                elif pdf_start < 0:
                    # PDF degil, sil
                    dest_path.unlink(missing_ok=True)
                    return False
                # pdf_start == 0 ise zaten temiz PDF

            return True
        except Exception as e:
            # Partial download temizle
            if dest_path.exists():
                dest_path.unlink(missing_ok=True)
            print(f"Indirme hatasi ({url}): {e}", file=__import__('sys').stderr)
            return False

    # ── Cache ──

    def _cache_path(self, key: str) -> Path:
        safe = re.sub(r'[^\w\-]', '_', key)
        return self.cache_dir / f"{safe}.json"

    def cache_read(self, key: str, max_age: int = 300) -> Optional[Any]:
        """Cache oku. Suresi dolmussa None doner."""
        path = self._cache_path(key)
        if not path.exists():
            return None
        try:
            if time.time() - path.stat().st_mtime > max_age:
                return None
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def cache_write(self, key: str, data: Any):
        """Cache yaz."""
        try:
            with open(self._cache_path(key), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        except Exception:
            pass
