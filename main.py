import discord
import discord.bot
import discord.ext

TOKEN = '' # TODO: some proper way to input token
CMDGRP = 'jextdc' # TODO: some proper way to configure the command group string

bot = discord.Bot()

cmdgrp = bot.create_group(CMDGRP)

@cmdgrp.command()
async def fromfile(ctx: discord.ApplicationContext,
                   file: discord.Attachment):
    '''
    Add a new song from file upload
    '''
    raise NotImplementedError

@cmdgrp.command()
async def fromurl(ctx: discord.ApplicationContext,
                  url: str):
    '''
    Add a file from a link
    '''
    raise NotImplementedError

@cmdgrp.command()
async def settitle(ctx: discord.ApplicationContext,
                   title: str):
    '''
    Edit title command
    '''
    raise NotImplementedError

@cmdgrp.command()
async def setartist(ctx: discord.ApplicationContext,
                    artist: str):
    '''
    edit artist command
    '''
    raise NotImplementedError

@cmdgrp.command()
async def setcover(ctx: discord.ApplicationContext,
                   cover: discord.Attachment):
    '''
    Set cover command
    '''
    raise NotImplementedError

@cmdgrp.command()
async def apply(ctx: discord.ApplicationContext):
    '''
    Apply pending tracks to server
    '''
    raise NotImplementedError

@cmdgrp.command()
async def pending(ctx: discord.ApplicationContext):
    '''
    Get a list of pending tracks (added to bot but not applied to server)
    '''
    raise NotImplementedError

@cmdgrp.command()
async def list(ctx: discord.ApplicationContext):
    '''
    Get a list of tracks that are on the server
    '''
    raise NotImplementedError