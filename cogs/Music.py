import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os

class Tools(commands.Cog):

    def __init__(self, bot):
		self.bot = bot
        
    print("\033[92mLoading Music Cog\033[0m")
        
def setup(bot):
	bot.add_cog(Tools(bot))