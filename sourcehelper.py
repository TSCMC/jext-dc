import mutagen
import mutagen.flac
import mutagen.id3
import mutagen.m4a
import mutagen.ogg
import mutagen.mp4
from typing import Optional

class trackInfo:
    def __init__(self, title: Optional[str] = None, 
                 artist: Optional[str] = None,
                 cover: Optional[bytes] = None):
        self.title = title
        self.artist = artist
        self.cover = cover
    
    def has_title(self):
        return bool(self.title)
    
    def has_artist(self):
        return bool(self.artist)
    
    def has_cover(self):
        return bool(self.cover)

def get_metadata_from_file(file_bytes: bytes) -> trackInfo:
    file = mutagen.File(file_bytes)
    
    info = trackInfo()

    if isinstance(file, mutagen.id3.ID3FileType):
        # file with ID3 tags
        pass
    elif isinstance(file, (mutagen.flac.FLAC, mutagen.ogg.OggFileType)):
        # VorbisComment
        pass
    elif isinstance(file, (mutagen.m4a.M4A, mutagen.mp4.MP4)):
        # MP4
        pass
