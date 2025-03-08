from typing import Optional
import uuid

class soundtrack:
    '''
    Represents a soundtrack
    '''
    def __init__(self, 
                 id: Optional[str] = None, 
                 title: Optional[str] = None,
                 artist: Optional[str] = None,
                 disc_texture: Optional[bytes] = None,
                 frag_texture: Optional[bytes] = None,
                 raw_audio: Optional[bytes] = None,
                 processed_audio: Optional[bytes] = None
                 ) -> None:
        '''
        This class is not intended to be called directly. Use one of the helper functions below instead.
        '''
        self.id = id if id is not None else uuid.uuid4()
        self.title = title
        self.artist = artist
        self.disc_texture = disc_texture
        self.frag_texture = frag_texture
        self.raw_audio = raw_audio
        self.processed_audio = processed_audio


    @staticmethod
    def fromFile(file: bytes) -> soundtrack: # type: ignore
        '''
        Creates a new soundtrack object from an audio file using embedded metadata
        '''
        raise NotImplementedError

    @staticmethod
    def fromLink(link: str) -> soundtrack: # type: ignore
        '''
        Creates a new soundtrack object from a streaming link supported by yt-dlp
        '''
        raise NotImplementedError

    @staticmethod
    def fromResourcePack():
        raise NotImplementedError