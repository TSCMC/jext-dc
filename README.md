Functionality requirements:
- Talk to the plugin using its [API](https://spartacus04.github.io/jext-reborn/docs/rest-api/)
- Periodically update the texture pack and upload new songs to the server while not breaking pre-existing songs (if you can't be bothered to deal with scheduled tasks you can make it a command behind some permissions for me to run manually)
- Can take input from an uploaded music file or download from something like youtube
- Automatically transcode the song into a format compatible with Minecraft (ogg vorbis 128kbps mono for records) and strip metadata tags while doing so
- generate custom art for the textures for records and shards (can be done with pillow)
- auto grab metadata (cover, title, artist) from supplied files but will prompt user to confirm and give user a chance to edit

Not requirements but nice-to-have:
- Make it with python 3.12 or above with pycord or discord.py as framework and manage dependencies with poetry
- write a dockerfile

In more human readable terms what needs to happen when someone wants to submit a new song:
1. The user triggers the bot to add a new song. The bot should take either a file upload or a link to some video service for this
2. The bot downloads the provided track and grabs metadata from it
3. The bot prompts the user to confirm the auto detected metadata and gives the user a chance to edit
4. The bot processes the input and adds the track to the resource pack, waiting to be uploaded to the server

Useful tools you might need
- pillow (python library) can generate the image
- ffmpeg can handle media related stuff
- mutagen can read metadata from music files (ffmpeg can also do this if you want)
