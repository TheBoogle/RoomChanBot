import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    print("\033[92mLoading Music Cog\033[0m")
    
   
    @commands.command(help='Begins RoomChan Radio Playback')
    async def radio(self, ctx):
        radio_channel = self.bot.get_channel(770719723851612170)
        vc = await radio_channel.connect()
        
        vc.play(discord.FFmpegPCMAudio("test.mp3"))
        
        
def setup(bot):
    bot.add_cog(Music(bot))