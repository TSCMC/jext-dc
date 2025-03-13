import asyncio
import subprocess
from typing import Optional, Iterable

# TODO: Make FFMPEG_CMD, OUTPUT_QUALITY, PREVIEW_ENCODER, PREVIEW_QUALITY, USE_VBR options 
# user-configurable (except force USE_VBR = False if PREVIEW_ENCODER is 'aac')
# OUTPUT_ENCODER should be hard-coded 'libvorbis' because other codecs won't work for minecraft,
# and 'vorbis' encoder for ffmpeg is experimental
# PREVIEW_ENCODER should also have limits to ensure compatibility accross all platforms
# AAC has best compatibility currently, opus and mp3 might also be fine, Vorbis is asking for trouble
# Lossless codecs for preview = whoever runs the server has too much upload bandwidth

FFMPEG_CMD = "ffmpeg"
OUTPUT_ENCODER = 'libvorbis'
OUTPUT_QUALITY = '3'

'''
Get info about ffmpeg codecs
'''

has_vorbis = False
has_libfdk = False
has_at = False
info_cmd = [FFMPEG_CMD, '-encoders', '-hide_banner']
info_res = subprocess.run(info_cmd, stdout=subprocess.PIPE)
for i in info_res.stdout.splitlines():
    i = str(i)
    if 'libvorbis' in i:
        has_vorbis = True

    elif 'libfdk_aac' in i:
        has_libfdk = True
    
    elif 'aac_at' in i:
        has_at = True

if has_at:
    PREVIEW_ENCODER = 'aac_at'
    PREVIEW_QUALITY = '11'

elif has_libfdk:
    PREVIEW_ENCODER = 'libfdk_aac'
    PREVIEW_QUALITY = '4'

else:
    PREVIEW_ENCODER = 'aac'
    PREVIEW_QUALITY = '80k'

USE_VBR = has_at or has_libfdk

async def encode_preview(in_file: str | bytes) -> bytes:
    return await _encode(in_file, preview=True)

async def encode_output(in_file: str | bytes, out_file: Optional[str]) -> Optional[bytes]:
    return await _encode(in_file, out_file, preview=False)

async def _encode(in_file: str | bytes, out_file: Optional[str] = None, preview: bool = False) -> Optional[bytes]:
    # Preview should use format adts for .aac file format outout
    # Output should use format ogg for .ogg file format output
    
    # Set basic options
    cmd = [FFMPEG_CMD, '-hide_banner', '-loglevel', 'quiet', '-i']
    
    # Input file option
    stdin = None
    if type(in_file) == str:
        cmd.append(in_file)
    elif type(in_file) == bytes:
        cmd.append('-')
        stdin = asyncio.subprocess.PIPE
    else:
        raise TypeError('ffmpeg input file should be bytes or str')
    
    # Encoding options
    cmd.extend([
        '-vn', # Drop all video streams (including embedded images)
        '-ac', '1', # Downmix to mono for minecraft record format
        '-c:a', (PREVIEW_ENCODER if preview else OUTPUT_ENCODER), # set encoder to use
        ('-b:a' if preview and not USE_VBR else '-q:a'), # set bitrate control mode
        (PREVIEW_QUALITY if preview else OUTPUT_QUALITY), # set bitrate / quality setting
        '-map_metadata', '-1', # drop all metadata from input
        '-f', ('adts' if preview else 'ogg') # set output container format
    ])

    # Output options
    stdout = None
    if out_file is None:
        cmd.append('-')
        stdout = asyncio.subprocess.PIPE
    else:
        cmd.append(out_file)
    
    proc = await asyncio.create_subprocess_exec(*cmd, stdin=stdin, stdout=stdout)
    if stdin:
        stdout, stderr = await proc.communicate(in_file)
    
    return stdout

