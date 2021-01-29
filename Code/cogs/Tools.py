from __future__ import print_function
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os
from pyspectator.computer import Computer
from pyspectator.processor import Cpu
from gpiozero import CPUTemperature
from py_expression_eval import Parser
import math
import psutil
import datetime
import matplotlib.pyplot as plt
import numpy as np

import requests


parser = Parser()
	

def lvl(xp):
	return xp / 1000

parser.functions['level'] = lvl
parser.functions['len'] = len
parser.functions['str'] = str
parser.functions['int'] = int


variables = {'X':datetime.datetime.now().timestamp(),'x':datetime.datetime.now().timestamp()}

class Tools(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		

	print("\033[92mLoading Tools Cog\033[0m")
	
	@commands.command(help="Report's a player for whatever it is you want. Please don't abuse or you will be punished. Please make sure to attach video evidence/screenshots.")
	async def report(self, ctx, Username, *, Reason):

		Attach = ctx.message.attachments

		toSend = []

		for attachment in Attach:
			toSend.insert(len(toSend), await attachment.to_file())

		await ctx.message.delete()

		await ctx.channel.send(content = "Thanks for your report! Our staff will investigate the issue. " + ctx.author.mention, delete_after=4)

		

		

		Channel = ctx.guild.get_channel(783633385917513728)

		r = requests.get(f"https://users.roblox.com/v1/users/search?keyword={Username}&limit=10")

		r = r.json()

		userId = r['data'][0]['id']

		b = requests.get(f"https://users.roblox.com/v1/users/{userId}")

		b = b.json()

		embed = discord.Embed(title = 'User Report', description = f"The user `{ b['name'] }` was reported." )

		embed.add_field(name='Reported User', value = f"`{ b['name'] }`")

		embed.add_field(name='User Reporting', value = f"{ctx.author.mention}({ctx.author.id})")

		embed.add_field(name='Reason', value = f"`{Reason}`")

		embed.url = f"https://www.roblox.com/users/{userId}/profile"

		

	

		AvatarUrl = requests.get(f'https://www.roblox.com/headshot-thumbnail/json?userId={userId}&width=420&height=420')

		AvatarUrl = AvatarUrl.json()

		AvatarUrl = AvatarUrl['Url']

		embed.set_thumbnail(url=str(AvatarUrl))

		creationDate = datetime.datetime.strptime(b['created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%m/%d/%y")

		embed.add_field(name='Creation Date', value = creationDate, inline=False)

		


		await Channel.send(embed = embed, content = None, files = toSend)
		
	@commands.command(help="Report's a player for whatever it is you want. Please don't abuse or you will be punished.")
	async def search(self, ctx, Username):
		r = requests.get(f"https://users.roblox.com/v1/users/search?keyword={Username}&limit=10")

		r = r.json()

		userId = r['data'][0]['id']

		embed = discord.Embed()

		embed.url = f"https://www.roblox.com/users/{userId}/profile"

		b = requests.get(f"https://users.roblox.com/v1/users/{userId}")

		b = b.json()

		embed.title = f"{b['name']} ({userId})"

		creationDate = datetime.datetime.strptime(b['created'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%m/%d/%y")

		string = ""

		if len(r['data'][0]['previousUsernames']) > 0:
			for name in r['data'][0]['previousUsernames']:
				string = string + name + ", "
			
		embed.add_field(name='Username(userId)', value=f"{b['name']}({userId})", inline=False)
		if len(string) > 0:
			embed.add_field(name='Previous Usernames', value = string, inline=True)
		else:
			embed.add_field(name='Previous Usernames', value ='N/A', inline=True)

		embed.add_field(name='Creation Date', value = creationDate, inline=False)

		


		
		if b['description']:
			embed.add_field(name='User Description', value = b['description'], inline=False)
		else:
			embed.add_field(name='User Description', value = 'N/A', inline=False)

		embed.add_field(name='Is Banned?', value = b['isBanned'], inline=False)

		r = requests.get(f"https://users.roblox.com/v1/users/{userId}/status")

		r = r.json()

		if r['status']:
			embed.add_field(name='Status', value = r['status'], inline=False)
		else:
			embed.add_field(name='Status', value = 'N/A', inline=False)

		


		AvatarUrl = requests.get(f'https://www.roblox.com/headshot-thumbnail/json?userId={userId}&width=420&height=420')

		AvatarUrl = AvatarUrl.json()

		AvatarUrl = AvatarUrl['Url']

		embed.set_thumbnail(url=str(AvatarUrl))

		await ctx.channel.send(embed = embed, content = None)




	@commands.command(help='Calculates a math expression, X = current time')
	async def calculate(self, ctx, *, expression: str="2+2"):
		msg = await ctx.channel.send("Calculating...")
		variables['X'] = datetime.datetime.now().timestamp()
		variables['x'] = datetime.datetime.now().timestamp()
	
		output = parser.parse(expression).evaluate(variables)

		embed = discord.Embed(title='Calculation')
		embed.add_field(name='Input', value = f"`{expression}`")
		embed.add_field(name='Output', value = f"`{output}`")
		if len(embed) >= 6000:
			f = open("output.txt","w")
			f.write(f'Input: {expression}' + "\n")
			f.write(f'Output: {output}')
			f.close()
			await ctx.channel.send(content='Length of output was too long, changed to .txt file instead', file=discord.File('output.txt'))
		else:
			await msg.edit(content = None, embed=embed)
		
	
	@commands.command(help='Simplifies a math expression, X = current time')
	async def simplify(self, ctx, *, expression: str="2+2"):
		variables['X'] = datetime.datetime.now().timestamp()
		variables['x'] = datetime.datetime.now().timestamp()
	
		output = parser.parse(expression).simplify(variables).toString()
		embed = discord.Embed(title='Simplified')
		embed.add_field(name='Input', value = f"`{expression}`")
		embed.add_field(name='Output', value = f"`{output}`")
		await ctx.send(embed=embed)
	
	@commands.command(help='Defines a variable for usage with $calculate', aliases=['define', 'int'])
	async def integer(self, ctx, varName, value):
		variables[varName] = int(value)
		await ctx.send(f"Defined int(`{varName}`) to the global variables dictionary with a value of `{value}`")

	@commands.command(help='Defines a string variable for usage with $calculate', aliases=['strdefine', 'str'])
	async def string(self, ctx, varName, *, value):
		variables[varName] = value
		await ctx.send(f"Defined str(`{varName}`) to the global variables dictionary with a value of `{value}`")
	
	
	@commands.command(help='Returns a variable list', aliases=['vars'])
	async def variables(self, ctx):
		embed = discord.Embed()
		
		for var in variables:
			embed.add_field(name=var, value = variables[var], inline=False)
		await ctx.send(embed=embed)
			
	
	@commands.command(help='Gets Room Chan Information')
	async def botstats(self, ctx):
		async with ctx.channel.typing():
			computer = Computer()
			embed = embed=discord.Embed(title='Bot Stats', description='Information on the Room Chan Bots computer', color=0xff5500)
			embed.add_field(name="Operating System", value=computer.os)
			embed.add_field(name="Python Version", value=computer.python_version)
			embed.add_field(name="Computer Uptime", value=computer.uptime)
			embed.add_field(name="Processor Name", value=computer.processor.name)
			cpu = Cpu(monitoring_latency=1)
			await asyncio.sleep(1.1)
			with cpu:
				embed.add_field(name='CPU Usage', value = str(cpu.load)+"%")
			cpu = CPUTemperature()
			embed.add_field(name='CPU Temperature', value = f"{cpu.temperature}°C / {(cpu.temperature * (9/5)) + 32}°F")
			embed.add_field(name='RAM Usage', value = str(psutil.virtual_memory().percent)+"%")
			
			await ctx.send(embed=embed)
			
	@commands.command(help='Outputs all server emojis')
	@commands.cooldown(1,240, commands.BucketType.guild)
	async def fetchemojis(self, ctx):
	
		emojis = await ctx.guild.fetch_emojis()
		message = ""
		
		for emoji in emojis:
			message = message + str(emoji)
			
			if len(message) > 1500:
				await ctx.send(message)
				message = ""
		await ctx.send(message)
		
	@commands.command(help='Sends you a list of all the members')
	async def getmembers(self, ctx):
		async with ctx.typing():
			f = open("memberlist.txt","w")
			x = ctx.guild.members
			for member in x:
				f.write(member.name+"#"+member.discriminator+"\n")
			f.close()
			await ctx.send("`Check your DMs` "+ctx.author.mention, delete_after=5)
			await ctx.author.send(file=discord.File('memberlist.txt'))
	@commands.command(help='Pings the bots latency')
	async def ping(self, ctx):
		await ctx.send(f'Pong! {self.bot.latency}')
		
	@commands.command(help='Countsdown from desired time')
	@commands.cooldown(1,120, commands.BucketType.guild)
	async def countdown(self, ctx, seconds: int=10):
		if seconds >= 120:
			await ctx.channel.send("Countdown time must be less then 120 seconds")
			return

		embed=discord.Embed(title="Countdown", description=str(seconds)+" seconds remaining...")
		msg = await ctx.send(embed=embed)
		i=0
		while i < seconds:
			seconds=seconds-1
			embed.description=str(seconds)+" seconds remaining..."
			await msg.edit(embed=embed)
			await asyncio.sleep(1)
		embed.description="Countdown Complete!"
		await msg.edit(embed=embed, delete_after=5)
	@commands.command()
	@commands.is_owner()
	async def savelevelbackup(self, ctx):
		command = "mysqldump -u boog -plol RoomChan > BACKUP.sql"

		import os; os.system(command)
		await ctx.send("Level backup was created.")
	@commands.command()
	@commands.is_owner()
	async def loadlevelbackup(self, ctx):
		command = "mysql -u boog -plol RoomChan < BACKUP.sql"

		import os; os.system(command)
		await ctx.send("Level backup was loaded.")

	@commands.has_permissions(manage_nicknames=True)
	async def resetnicknames(self, ctx):
		members = ctx.guild.members
		for member in members:
			try:
				if member.nick != None:
					await member.edit(nick=None)
					print('changed '+member.name+"#"+member.discriminator)
			except:
				print('error changing '+member.name+"#"+member.discriminator)
		print("Nickname reset complete")
		await ctx.send("Nickname reset complete")


	@commands.command()
	async def membercount(self, ctx):
		await ctx.send("`"+str(len(ctx.guild.members))+"` member's")

	@commands.command(aliases=['suggestion', 'sg'], help='Submit a suggestion to the developers. If the game is something other then Room 2, feel free to specify.')
	@commands.cooldown(1, 120, commands.BucketType.user)
	async def suggest(self, ctx, *, suggestion : str):
		suggestionChannelId = 754876657898094652
		suggestionChannel = self.bot.get_channel(suggestionChannelId)
		embed=discord.Embed(title="User Suggestion", description=suggestion)
		embed.set_author(name=ctx.author.name+'#'+ctx.author.discriminator, icon_url=ctx.author.avatar_url)
		msg = await suggestionChannel.send(embed=embed)

		await msg.add_reaction('👍')
		await msg.add_reaction('👎')
		await ctx.message.delete()
		await ctx.send('👍 Thank you for your suggestion, '+ctx.author.mention+'. Not all suggestions will it make it into the game, but the staff will vote on it.', delete_after=10)
	@commands.command()
	async def rbxavatar(self, ctx, Username):
		r = requests.get(f"https://users.roblox.com/v1/users/search?keyword={Username}&limit=10")

		r = r.json()

		if len(r) > 25:
			id = r['data'][0]['id']
			b = requests.get(f"https://users.roblox.com/v1/users/{id}")

			b = b.json()
			Username = b['name']

			embed = discord.Embed(title = f"{Username}'s avatar", description = "Avatar From Roblox API")
			embed.set_image(url=f"https://www.roblox.com/bust-thumbnail/image?userId={id}&width=420&height=420&format=png")
			await ctx.send(embed=embed)
		await ctx.send(f"Error with finding {Username}'s account.")



	@commands.command(help='Gets you info on a member', aliases=['whois', 'whodat', 'who', 'view', 'profile'])
	async def info(self, ctx, member: discord.Member=None):
	
		member = ctx.author if not member else member
		roles = [role for role in member.roles]
		
		embed = discord.Embed(color = member.color, timestamp=ctx.message.created_at)
		
		embed.set_author(name=f"User Info - {member}")
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		
		embed.add_field(name="ID:", value=member.id)
		embed.add_field(name="Display name:", value=member.display_name)
		
		embed.add_field(name="Created at:", value=member.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
		embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
		
		embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
		embed.add_field(name="Top role:", value=member.top_role.mention)
		
		embed.add_field(name="Mention", value=member.mention)

		embed.add_field(name="Bot?", value=member.bot)
		
		await ctx.send(embed=embed)
	@commands.command(help='Sends a users avatar')
	async def avatar(self, ctx, member:discord.User=None):
		if member == None:
			member = ctx.author
		embed = discord.Embed(title=member.name+"#"+member.discriminator+"'s avatar")
		embed.set_image(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member))
		await ctx.send(embed=embed)
	
	@commands.command(help='Gets you info on a server', aliases=['aboutserver'])
	async def serverinfo(self, ctx):
		roles = [role for role in ctx.guild.roles]
		
		embed = discord.Embed(color = 0xFFA500, timestamp=ctx.message.created_at)
		
		embed.set_author(name=f"Server Info - {ctx.guild.name}")
		embed.set_thumbnail(url=ctx.guild.icon_url)
		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		
		embed.add_field(name="ID:", value=ctx.guild.id)
		embed.add_field(name="Name:", value=ctx.guild.name)
		
		embed.add_field(name="Created at:", value=ctx.guild.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
		
		embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
		
		await ctx.send(embed=embed)
	@commands.command(help='Creates a poll people can react to')
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def poll(self, ctx, *, message):
		await ctx.channel.purge(limit=1)
		embed = discord.Embed(title=ctx.author.name+"#"+ctx.author.discriminator+" asks...", description=message )
		msg = await ctx.send(embed=embed)
		await msg.add_reaction('✅')
		#await msg.add_reaction("<:maybe:794705956507222026>")
		await msg.add_reaction('❌')
def setup(bot):
	bot.add_cog(Tools(bot))
