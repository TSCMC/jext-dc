import mutagen
import mutagen.flac
import mutagen.id3
import mutagen.m4a
import mutagen.ogg
import mutagen.mp4
from typing import Optional
import io

class trackData:
    def __init__(self, title: Optional[str] = None, 
                 artist: Optional[str] = None,
                 cover: Optional[bytes] = None,
                 audio: Optional[bytes] = None):
        '''
        Represents metadata obtained from source, can optionally contain an audio stream
        '''
        self.title = title
        self.artist = artist
        self.cover = cover
        self.audio = audio
    
    def has_title(self):
        return bool(self.title)
    
    def has_artist(self):
        return bool(self.artist)
    
    def has_cover(self):
        return bool(self.cover)
    
    def has_audio(self):
        return bool(self.audio)

def get_metadata_from_file(file_bytes: bytes) -> trackData:
    file_bytes = io.BytesIO(file_bytes)
    file = mutagen.File(file_bytes)
    
    data = trackData()

    if isinstance(file, mutagen.id3.ID3FileType):
        # file with ID3 tags
        data.title = file.get('TIT2')
        data.artist = file.get('TPE1')
        data.cover = file.get('APIC:')
        if data.cover is not None:
            data.cover = data.cover.data

    elif isinstance(file, (mutagen.flac.FLAC, mutagen.ogg.OggFileType)):
        # VorbisComment
        data.title = file.get('title')
        data.artist = file.get('artist')

        if data.title:
            data.title = str(data.title)
        if data.artist:
            data.artist = str(data.artist)

        for i in file.pictures:
            if i.type == 3:
                data.cover = i.data
                break

    elif isinstance(file, (mutagen.m4a.M4A, mutagen.mp4.MP4)):
        # MP4
        data.title = file.get('\xa9nam')[0]
        data.artist = ','.join(file.get('\xa9ART'))
        if 'covr' in file.keys():
            data.cover = bytes(file.get('covr')[0])
                    

    return data

if __name__ == "__main__":
    from PIL import Image
    from sys import argv

    if len(argv) > 1:
        file = argv[1]
        print(file)
        with open(file, 'rb') as fileobj:
            filebytes = fileobj.read()
        
        trackdata = get_metadata_from_file(filebytes)
        print(f'Title:  {trackdata.title}')
        print(f'Artist: {trackdata.artist}')
        if trackdata.cover:
            img = Image.open(io.BytesIO(trackdata.cover))
            img.show()
        else:
            print('There is no cover image on this track.')

    else:
        print('No Input Provided!')