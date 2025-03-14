import yt_dlp
import asyncio
import contextlib
import io
from typing import Optional

YDL_SETTINGS = {
    'quiet': True,
    'noplaylist': True,
    'format': 'bestaudio',
    'outtmpl': '-',
    'logtostderr': True
}


class ydl:
    def __init__(self) -> None:
        self._ydl = None

    async def __aenter__(self) -> None:
        self._ydl = yt_dlp.YoutubeDL(YDL_SETTINGS)

    async def __aexit__(self) -> None:
        self._ydl.close()
        self._ydl = None

    async def get_info(self, link: str) -> dict:
        await asyncio.to_thread(self._ydl.extract_info, link, download=False)
    
    async def download_audio(self, link: str) -> bytes:
        return await asyncio.to_thread(self._download_helper, link)
        
    def _download_helper(self, link: str) -> Optional[bytes]:
        if not self._ydl:
            return
        buffer = io.BytesIO()
        with contextlib.redirect_stdout(buffer):
            self._ydl.download(link)
        return buffer.getvalue()

        
