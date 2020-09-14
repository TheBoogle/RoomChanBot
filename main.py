import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import tasks
from discord.ext.tasks import loop
import random
import asyncio
import aiohttp
import os

Bot = discord.Client(shard_count=1)
bot = commands.Bot(command_prefix='$')

async def update_status():
	statuses = ["RooM", 'RooM 2', 'Quake', 'DooM']
	status=0
	while True:
		if status == len(statuses)-1:
			status=0
		else:
			status=status+1
		sum = 0
		guilds = bot.guilds
		for guild in guilds:
			sum += len(guild.members)
		await bot.change_presence(status=discord.Status.idle, activity=discord.Game(statuses[status]))
		await asyncio.sleep(10)
		

@bot.event
async def on_ready():
	print('\033[92m{0.user} is online.'.format(bot)+"\033[0m")
	# ~ print('\033[92mConnected to proxy:{0.proxy}.'.format(Bot)+"\033[0m")
	print('\033[92m{0.shard_count} shards running\033[0m'.format(Bot))
	bot.loop.create_task(update_status())

	
@bot.command(aliases=['suggestion', 'sg'], help='Submit a suggestion to the developers. If the game is something other then Room 2, feel free to specify.')
@commands.cooldown(1, 120, commands.BucketType.user)
async def suggest(ctx, *, suggestion):
	suggestionChannelId = 754876657898094652
	suggestionChannel = bot.get_channel(suggestionChannelId)
	embed=discord.Embed(title="User Suggestion", description=suggestion)
	embed.set_author(name=ctx.author.name+'#'+ctx.author.discriminator, icon_url=ctx.author.avatar_url)
	msg = await suggestionChannel.send(embed=embed)

	await msg.add_reaction('👍')
	await msg.add_reaction('👎')
	await ctx.message.delete()
	await ctx.send('👍 Thank you for your suggestion, '+ctx.author.mention+'. Not all suggestions will it make it into the game, but the staff will vote on it.', delete_after=10)
@commands.has_permissions(manage_nicknames=True)
async def resetnicknames(ctx):
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
	

@bot.command()
async def membercount(ctx):
	await ctx.send("`"+str(len(ctx.guild.members))+"` member's")

@bot.event
async def on_command_error(ctx,error):
	embed=discord.Embed(color=0xf00a3a)
	embed.add_field(name="Error!", value=error, inline=True)
	await ctx.message.delete()
	await ctx.send(embed=embed, delete_after=3)
async def ban(guild, userid, reason):
	await guild.ban(discord.Object(id=userid), reason=reason)

@bot.event
async def on_message(ctx):
	author = ctx.author
	guild = ctx.guild
	if ctx.content.lower()[0:1] != '$' and ctx.author.bot != True:
		if 'tes' in ctx.content.lower() and 'room' in ctx.content.lower():
			await ctx.delete()
			await ctx.channel.send(author.mention+' Please refrain from talking about RooM 2 testing')
		elif 'can' in ctx.content.lower() and 'tes' in ctx.content.lower():
			await ctx.delete()
			await ctx.channel.send(author.mention+' Please refrain from talking about RooM 2 testing')
		elif 'want' in ctx.content.lower() and 'tes' in ctx.content.lower():
			await ctx.delete()
			await ctx.channel.send(author.mention+' Please refrain from talking about RooM 2 testing')
		elif 'sex' in ctx.content.lower():
			await ctx.delete()
			await ctx.channel.send(author.mention+' Please refrain from using that language')
		elif 'cum' in ctx.content.lower():
			await ctx.delete()
			await ctx.channel.send(author.mention+' Please refrain from using that language')
		elif 'secks' in ctx.content.lower():
			await ctx.delete()
			await ctx.channel.send(author.mention+' Please refrain from using that language')
	await bot.process_commands(ctx)
# @bot.event
# async def on_member_join(member):
# 	try:
# 		if member.bot == False:
# 			channel=None
# 			try:
# 				channel = discord.utils.get(member.guild.channels, name='notifications')
# 			except:
# 				channel = discord.utils.get(member.guild.channels, name='join leave')
# 			if channel == None:
# 				try:
# 					channel = discord.utils.get(member.guild.channels, name='welcome')
# 				except:
# 					channel = discord.utils.get(member.guild.channels, name='hello goodbye')
# 			embed = discord.Embed(title="Member Joined", description=member.mention+" joined the server", color=0x90EE90)
# 			embed.set_thumbnail(url=member.avatar_url)
# 			await channel.send(embed=embed)
# 	except:
# 		print("Attempted to send a join message but failed")

# @bot.event
# async def on_member_remove(member):
# 	try:
# 		if member.bot == False:
# 			channel=None
# 			try:
# 				channel = discord.utils.get(member.guild.channels, name='notifications')
# 			except:
# 				channel = discord.utils.get(member.guild.channels, name='join-leave')
# 			if channel == None:
# 				try:
# 					channel = discord.utils.get(member.guild.channels, name='welcome')
# 				except:
# 					channel = discord.utils.get(member.guild.channels, name='hello-goodbye')
				
# 			embed = discord.Embed(title="Member Left", description=member.mention+"("+member.display_name+"#"+member.discriminator+") left the server", color=0xA52A2A)
# 			embed.set_thumbnail(url=member.avatar_url)
# 			await channel.send(embed=embed)
# 	except:
# 		print("Attempted to send a removal message but failed")

# load cogs	
for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(help="Reloads the bot and all its commands", aliases=['r', 'rb'])
@commands.is_owner()
async def reloadbot(ctx):
	print('Reloading bot...')
	embed = discord.Embed(title="Reloading bot", color=0xFFA500)
	msg = await ctx.send(embed=embed)
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			bot.unload_extension(f'cogs.{filename[:-3]}')
			bot.load_extension(f'cogs.{filename[:-3]}')
			embed.add_field(name=f'{filename[:-3]}', value="Loaded")
			
			await msg.edit(embed=embed)
	embed.color=0x90EE90
	embed.title="Reload Complete!"
	await msg.edit(embed=embed)
	print("Reload Complete!")

f = open("token.txt", "r")
token = f.read()

bot.run(token)
