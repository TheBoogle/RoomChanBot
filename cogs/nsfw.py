import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os
import json


class NSFW(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	print("\033[92mLoading NSFW Cog\033[0m")
	@commands.command(aliases=["vagina", "not pp"])
	@commands.is_nsfw()
	async def pussy(self, ctx):
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/image?type=pussy') as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Pussy")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command()
	@commands.is_nsfw()
	async def anal(self, ctx):
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/image?type=anal') as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Anal")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command()
	@commands.is_nsfw()
	async def hentai(self, ctx):
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/image?type=hentai') as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Hentai")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command(aliases=["butt", "butts"])
	@commands.is_nsfw()
	async def ass(self, ctx):
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/image?type=ass') as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Ass")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command()
	@commands.is_nsfw()
	async def thigh(self, ctx):
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/image?type=thigh') as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Thigh")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command()
	@commands.is_nsfw()
	async def gif(self, ctx):
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/image?type=pgif') as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="GIF")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command()
	@commands.is_nsfw()
	async def search(self, ctx, option):
		options=['hass','hmidriff','pgif','4k','hentai','holo','hneko','neko','hkitsune','kemonomimi','anal','hanal','gonewild','kanna','ass','pussy','thigh','hthigh','gah','coffee','food']
		found=False
		i=0
		while i < len(options):
			if option == options[i]:
				msg = await ctx.send('`Fetching Image`')
				found=True
			i=i+1
		if found == False:
			embed=discord.Embed(color=0xf00a3a)
			embed.add_field(name="Error!", value="Invalid option, please choose from this list: `hass, hmidriff, pgif, 4k, hentai, holo, hneko, neko, hkitsune, kemonomimi, anal, hanal, gonewild, kanna, ass, pussy, thigh, hthigh, gah, coffee, food`", inline=True)
			await ctx.send(embed=embed)
			return
			
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/image?type='+str(option)) as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Option: "+str(option))
		embed.set_image(url=data['message'])
		await msg.edit(embed=embed)
def setup(bot):
	bot.add_cog(NSFW(bot))
