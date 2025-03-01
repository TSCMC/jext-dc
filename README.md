# jext-dc

discord bot for managing jukebox extended reborn

> [!CAUTION]
> This thing is in very early stages. Please do not attempt to use this right now unless you know exactly what you are doing

Functionality requirements:
[ ] Talk to the plugin using its [API](https://spartacus04.github.io/jext-reborn/docs/rest-api/)
[ ] Periodically update the texture pack and upload new songs to the server (command to trigger manually is also fine)
[ ] don't break pre-existing songs when updating
[ ] only update when there are actually new songs added
[ ] Can take input from an uploaded music file or download from something like youtube
[ ] Automatically transcode the song into a format compatible with Minecraft (ogg vorbis 128kbps mono for records) and strip metadata tags while doing so
[ ] generate custom art for the textures for records and shards (can be done with pillow)
[ ] auto grab metadata (cover, title, artist) from supplied files but will prompt user to confirm and give user a chance to edit

Not requirements but nice-to-have:
[ ] Make it with python 3.12 or above with pycord or discord.py as framework and manage dependencies with poetry
[ ] write a dockerfile

In more human readable terms what needs to happen when someone wants to submit a new song:
1. The user triggers the bot to add a new song. The bot should take either a file upload or a link to some video service for this
2. The bot downloads the provided track and grabs metadata from it
3. The bot prompts the user to confirm the auto detected metadata and gives the user a chance to edit
4. The bot processes the input and adds the track to the resource pack, waiting to be uploaded to the server

