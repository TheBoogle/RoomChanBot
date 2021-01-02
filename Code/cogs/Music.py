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


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	print("\033[92mLoading Music Cog\033[0m")

	@commands.command()
	async def play(self, ctx, url : str):
		await ctx.send("Downloading song... this will take time as this bot is slow as hell on a Raspberry Pi 3, stop bitching about it.")
		song_there = os.path.isfile("song.wav")
		try:
			if song_there:
				os.remove("song.wav")
		except PermissionError:
			await ctx.send("Wait for the current playing music to end or use the 'stop' command")
			return

		try:
			voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='The Boiler Room In Hell')
			await voiceChannel.connect()
			voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
		except:
			pass

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
		for file in os.listdir("./"):
			if file.endswith(".wav"):
				os.rename(file, "song.wav")
		await ctx.send("Song has been downloaded.")
		voice.play(discord.FFmpegPCMAudio("song.wav"))

def setup(bot):
	bot.add_cog(Music(bot))