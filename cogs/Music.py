from __future__ import unicode_literals
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os

import youtube_dl


ydl_opts = {
        'format': 'bestaudio/best',
        'external-downloader':'aria2',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '1024',
        }],
    }


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    print("\033[92mLoading Music Cog\033[0m")
    
   
    @commands.command(help='Begins RoomChan Radio Playback')
    async def radio(self, ctx):
        radio_channel = self.bot.get_channel(770719723851612170)
        try:    
            vc = await radio_channel.connect()
        except:
            pass
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v=6NTfCbfvwM8'])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        vc.play(discord.FFmpegPCMAudio("song.mp3"))
        
        
def setup(bot):
    bot.add_cog(Music(bot))