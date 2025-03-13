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

async def encode_preview(in_file: str | bytes, 
                         start_time_str: str | None = None, 
                         end_time_str: str | None = None
                         ) -> bytes:
    return await _encode(in_file, preview=True)

async def encode_output(in_file: str | bytes, 
                        out_file: Optional[str], 
                        start_time_str: str | None = None, 
                        end_time_str: str | None = None
                        ) -> Optional[bytes]:
    return await _encode(in_file, out_file, preview=False)

async def _encode(in_file: str | bytes, 
                  out_file: Optional[str] = None, 
                  preview: bool = False,
                  start_time_str: str | None = None,
                  end_time_str: str | None = None
                  ) -> Optional[bytes]:
    # Preview should use format adts for .aac file format outout
    # Output should use format ogg for .ogg file format output
    
    # Set basic options
    cmd = [
        FFMPEG_CMD, # ffmpeg command
        '-hide_banner', # hide banner that shows compiler settings for current binary
        '-loglevel', 'quiet' # supress console output
        ]
    
    if(start_time_str):
        cmd.extend([
            '-ss', start_time_str # input seeking to specified time 
        ])
    
    # Input file option
    cmd.append('-i')
    stdin = None
    if type(in_file) == str:
        cmd.append(in_file)
    elif type(in_file) == bytes:
        cmd.append('-')
        stdin = asyncio.subprocess.PIPE
    else:
        raise TypeError('ffmpeg input file should be bytes or str')
    
    # Encoding options
    if end_time_str:
        cmd.extend([
            '-to', end_time_str # specify end of audio file time
        ])

    cmd.extend([
        '-vn', # Drop all video streams (including embedded images)
        '-ac', '1', # Downmix to mono for minecraft record format
        '-map_metadata', '-1', # drop all metadata from input
    ])

    if preview:
        cmd.extend([
            '-c:a', PREVIEW_ENCODER, # Set encoder to preview encoder
            ('-q:a' if USE_VBR else '-b:a'), PREVIEW_QUALITY, # set preview bitrate control mode and quality 
            '-f', 'adts' # 'adts' for '.aac' format file output for preview
        ])

    else:
        cmd.extend([
            '-c:a', OUTPUT_ENCODER, # Set encoder to output encoder
            '-q:a', OUTPUT_QUALITY, # Set output quality
            '-f', 'ogg' # 'ogg' for '.ogg' format
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

