import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os

class EMH(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	print("\033[92mLoading EMH Cog\033[0m")
	def isPrivateCommand():
		async def predicate(ctx):
			return ctx.guild.id == 714366654481694750
		return commands.check(predicate)
	
	@commands.command(help="Gets you the current key")
	@commands.cooldown(1, 120, commands.BucketType.user)
	@isPrivateCommand()
	async def getkey(self, ctx):
		async with ctx.typing():
			fetch = await ctx.send('`Fetching Key`')
			async with aiohttp.ClientSession() as session:
				async with session.get('https://whitelist.boogles.tech/demochecker.php?key=VSDQAV29XH') as resp:
					embed=discord.Embed()
					embed.color = 0xFFA500
					embed.add_field(name="Recieved Key", value="Use Key: `"+await resp.text()+"`", inline=True)
					embed.set_footer(text="Marmalade Bot - Designed by Boogle#4509")
					await ctx.author.send(embed=embed)	 
					await fetch.edit(content='`Check your DMs `'+ctx.author.mention)
	# ~ @commands.command(help='Gets you a link to the script')
	# ~ @isPrivateCommand()
	# ~ async def getscript(self, ctx):
		# ~ await ctx.send('`Get the script at: https://boogles.tech/EpicManHacks.lua`')
	@commands.command(help='Resets all the keys')
	@commands.has_permissions(administrator=True)
	@isPrivateCommand()
	async def getnewkeys(self, ctx, keylength: int=4):
		async with ctx.typing():
			fetch = await ctx.send('`Generating Keys`')
			async with aiohttp.ClientSession() as session:
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/randomkeysnotjam.php?key=yeetmybeet&length='+str(keylength)) as resp:
					await fetch.edit(content='`Keys were regenerated`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key1') as resp:
					await ctx.author.send('Monday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key2') as resp:
					await ctx.author.send('Tuesday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key3') as resp:
					await ctx.author.send('Wednesday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key4') as resp:
					await ctx.author.send('Thursday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key5') as resp:
					await ctx.author.send('Friday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key6') as resp:
					await ctx.author.send('Saturday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key7') as resp:
					await ctx.author.send('Sunday key: `' +await resp.text()+'`')
	@commands.command(help='Sends you all of the current keys')
	@commands.has_permissions(administrator=True)
	@isPrivateCommand()
	async def getallkeys(self, ctx):
		async with ctx.typing():
			await ctx.send('`Sending keys to '+ctx.author.name+'#'+ctx.author.discriminator+'`')
			async with aiohttp.ClientSession() as session:
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key1') as resp:
					await ctx.author.send('Monday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key2') as resp:
					await ctx.author.send('Tuesday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key3') as resp:
					await ctx.author.send('Wednesday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key4') as resp:
					await ctx.author.send('Thursday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key5') as resp:
					await ctx.author.send('Friday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key6') as resp:
					await ctx.author.send('Saturday key: `' +await resp.text()+'`')
				async with session.get('https://whitelist.boogles.tech/marmaladeisreallygoodontoastngl/pleasedonteatjam/key7') as resp:
					await ctx.author.send('Sunday key: `' +await resp.text()+'`')
		
		
def setup(bot):
	bot.add_cog(EMH(bot))
