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
		
		embed.add_field(name="Bot?", value=member.bot)
		
		await ctx.send(embed=embed)
	@commands.command(help='Sends a users avatar')
	async def avatar(self, ctx, member:discord.User=None):
		if member == None:
			member = ctx.author
		embed = discord.Embed(title=member.name+"#"+member.discriminator+"'s avatar")
		embed.set_image(url=member.avatar_url)
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
		await msg.add_reaction('❌')
def setup(bot):
	bot.add_cog(Tools(bot))
