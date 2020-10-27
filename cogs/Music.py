from __future__ import unicode_literals
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os

import youtube_dl
import soundfile as sf

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '1'
    }],
    'prefer_ffmpeg': True,
    'keepvideo': False,
    'externaldownloader': 'aria2c'
}

vc = None
playlist = {
    "https://www.youtube.com/watch?v=1qN72LEQnaU"
}
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    print("\033[92mLoading Music Cog\033[0m")
   
   

    @commands.command(help='Begins RoomChan Radio Playback')
    async def radio(self, ctx):
        i = 0
        print(list(playlist)[i])
        while True:
            radio_channel = self.bot.get_channel(770719723851612170)

            try:    
                vc = await radio_channel.connect()
            except:
                await ctx.channel.send("A song is already playing")
                return


            for file in os.listdir("./"):
                if file.endswith(".wav"):
                    os.remove(file)
            
            await ctx.channel.send('Downloading & Converting file... This will take a few seconds.')
            
            try:
                
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                
                    ydl.download([list(playlist)[i]])
                    
                for file in os.listdir("./"):
                    if file.endswith(".wav"):
                        os.rename(file, 'song.wav')
                try:
                    vc.play(discord.FFmpegPCMAudio("song.wav"))
                    await ctx.channel.send('Playing.')
                   
                    f = sf.SoundFile('song.wav')
                    print(len(f) / f.samplerate)
                    await asyncio.sleep(len(f) / f.samplerate)
                    await vc.disconnect()
                
                except:
                    await ctx.channel.send("A song is already playing")
            except:
                await ctx.channel.send("This song can't be played due to DMCA")
                await vc.disconnect()
                
            
            
            i += 1
            if i > len(list(playlist)):
                i = 0
        
        
        
        
def setup(bot):
    bot.add_cog(Music(bot))