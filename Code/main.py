import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import tasks
from discord.ext.tasks import loop
from datetime import datetime, timedelta
import random
import asyncio
import aiohttp
import os
import mysql.connector
from autocorrect import Speller
from profanityfilter import ProfanityFilter
import pyjokes

pf = ProfanityFilter(custom_censor_list={'secks','sex', 'cum', 'nigga', 'nigger', 'coomer'})



minimum_age = 30
xp_per_level = 1000

bannedFileTypes = ['exe', 'dll', 'bat', 'zip', 'rar', 'img', 'iso', '7z','pdf', 'cmd', 'doc', 'docx', 'xlsx', 'Xls', 'xlsm', 'pif', 'jar', 'vbs', 'js', 'reg', 'poopfartnoah', 'py', 'lua', 'cs', 'c']

statuses = ["smh my head"]

mydb = mysql.connector.connect(
	host="localhost",
	user="boog",
	passwd="lol",
	database="RoomChan"

)

Bot = discord.Client()
bot = commands.Bot(command_prefix='$', shard_count = 1, intents = discord.Intents.all(), chunk_guilds_at_startup=True)

def generateXP():
	return random.randrange(25,50)

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

async def update_status():
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
		await asyncio.sleep(8)

@bot.event
async def on_member_join(member):
	channel = member.guild.get_channel(531310166662971422)

	if not channel:
		channel = member.guild.get_channel(782513121327317012)
	
	embed = discord.Embed(title="Member Joined", description=member.mention+" joined the server", color=0x90EE90)
	embed.set_thumbnail(url=member.avatar_url)
	
	age = datetime.now().timestamp() - member.created_at.timestamp()
	
	print(age)
	if age < minimum_age*86400:
		embed=discord.Embed(color=0xf00a3a)
		embed.add_field(name="You were kicked!", value=f"You have been kicked in {member.guild.name} for: `Your account must be {minimum_age} days or older to join.`", inline=True)
		await member.send(embed=embed)
		await member.guild.kick(member)
	else:
		await channel.send(embed=embed)
	
	await channel.edit(name = 'Member count: {}'.format(channel.guild.member_count))
@bot.event
async def on_member_remove(member):
	channel = member.guild.get_channel(531310166662971422)

	if not channel:
		channel = member.guild.get_channel(782513121327317012)



	embed = discord.Embed(title="Member Left", description=member.mention+" left the server", color=0xA52A2A)
	embed.set_thumbnail(url=member.avatar_url)
	await channel.send(embed=embed)
	await channel.edit(name = 'Member count: {}'.format(channel.guild.member_count))

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
	try:
		await ctx.message.delete()
	except:
		pass
	
	await ctx.send(embed=embed, delete_after=3)
	
async def ban(guild, userid, reason):
	await guild.ban(discord.Object(id=userid), reason=reason)

@bot.command()
@commands.is_owner()
async def resetlevels(ctx):
	command = "mysqldump -u boog -plol RoomChan > BACKUP.sql"

	import os; os.system(command)
	await asyncio.sleep(0.5)
	cursor = mydb.cursor()
	cursor.execute("UPDATE users SET user_xp = 0")
	mydb.commit()
	await ctx.send("Levels were reset!")

@bot.command()
@commands.is_owner()
async def savelevelbackup(ctx):
	command = "mysqldump -u boog -plol RoomChan > BACKUP.sql"

	import os; os.system(command)
	await ctx.send("Level backup was created.")
@bot.command()
@commands.is_owner()
async def loadlevelbackup(ctx):
	command = "mysql -u boog -plol RoomChan < BACKUP.sql"

	import os; os.system(command)
	await ctx.send("Level backup was loaded.")

@bot.event
async def on_message(ctx):
	author = ctx.author
	guild = ctx.guild

	attach = ctx.attachments
	staffChannel = await bot.fetch_channel(722148701753311332)
	
	if len(attach) > 0:
		for attachment in attach:
			for banned in bannedFileTypes:
				if attachment.filename.lower().endswith('.'+banned.lower()):
					await ctx.delete()
					await ctx.channel.send(f"{ctx.author.mention} no {banned.upper()} file types allowed!")
					await staffChannel.send(ctx.author.mention + f" sent a {banned.upper()} File")
				
	
	if not ctx.guild and not author.bot:
		user = await bot.fetch_user(643491766926049318)
		await user.send(str(ctx.author) + ": " + ctx.content)
		return
	if ctx.channel.id == 762540670836670504:
		if ctx.content != 'Caleb':
			await ctx.delete()
			await ctx.author.send('Are you stupid!? You can only say `Caleb` in #caleb >:(')
	if pf.is_profane(ctx.content.lower()) == True:
		await ctx.delete()
		await ctx.channel.send(author.mention+' Please refrain from using that language `'+pf.censor(ctx.content)+'`', delete_after=6)
    
	if ctx.author.bot == False and ctx.content[0:1] != "$" and len(ctx.content) > 1:
		xp = generateXP()
		cursor = mydb.cursor()
		cursor.execute("SELECT user_xp FROM users WHERE client_id = "+str(ctx.author.id))
		result = cursor.fetchall()
		if len(result) == 0:
			cursor.execute("INSERT INTO users VALUES(" + str(ctx.author.id) + "," + str(xp) + ')')
		else:
			currentXP = result[0][0] + xp
			
			if currentXP >= 100 * xp_per_level and ctx.guild.id == 460932049394728990:
				
				role = ctx.guild.get_role(460944551130169346)
				
				member = ctx.author
				roles = [role for role in member.roles]
				i=0
				found=False
				while i < len(roles):
					currentrole=roles[i]

					if role.id == currentrole.id:
						found=True
						
					i=i+1
				
				
				if not found:
					role = ctx.guild.get_role(460944551130169346)
					await ctx.author.add_roles(role)
					await ctx.channel.send(f"Congragulations {member.mention} on hitting level 100! Enjoy the Advanced AGM members role")

			if currentXP >= 200 * xp_per_level and ctx.guild.id == 460932049394728990:
				
				role = ctx.guild.get_role(787042501780701225)
				
				member = ctx.author
				roles = [role for role in member.roles]
				i=0
				found=False
				while i < len(roles):
					currentrole=roles[i]

					if role.id == currentrole.id:
						found=True
						
					i=i+1
				
				
				if not found:
					role = ctx.guild.get_role(787042501780701225)
					await ctx.author.add_roles(role)
					await ctx.channel.send(f"Congragulations {member.mention} on hitting level 200! Enjoy the Mega-Advanced AGM members role")

			cursor.execute("UPDATE users SET user_xp = "+ str(currentXP)+" WHERE client_id = " +str(ctx.author.id))
		mydb.commit()
        
	await bot.process_commands(ctx)

@bot.command(aliases=['lvl','xp','exp', 'rank'])
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
		cursor.execute('SET @row_number=0')
		cursor.execute("SELECT (@row_number:=@row_number + 1) AS num, client_id, user_xp FROM users ORDER BY user_xp DESC")
		result3 = cursor.fetchall()
		i=0
		found=False
		while i < len(result3):

			if result3[i][1] == user.id:
				
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
@bot.command(aliases=["top", "leader"])
async def leaderboard(ctx, lines:int=10, start:int=0):
	if lines:
		lines = int(lines)
	if start:
		start = int(start)
	else:
		start = 0
	cursor = mydb.cursor()
	cursor.execute("SELECT user_xp from users ORDER BY user_xp DESC")
	result = cursor.fetchall()
	cursor.execute("SELECT client_id from users ORDER BY user_xp DESC")
	result2 = cursor.fetchall()
	embed = discord.Embed(title="Global Leaderboard",color=0xFFFF00)
	if lines == None:
		lines = len(result)
		if lines > 10:
			lines = 10
	
	lines = lines + start

	i=start
	if i < 0: 
		i=0
	runs=1+start
	if lines > len(result):
		lines = len(result)

	async with ctx.channel.typing():
		while i < lines:

			
			member = ctx.guild.get_member(result2[i][0])

			if member == None:
				pass
			else:
				embed.add_field(name="@"+str(member)+" RANK: #"+str(runs), inline=False, value="**Level**: "+str(result[i][0]//xp_per_level)+" **Total XP**: "+str(result[i][0]))
				runs=runs+1
			i=i+1

	cursor.execute("SET @row_number = 0")
	cursor.execute("SELECT (@row_number:=@row_number + 1) AS num, client_id, user_xp FROM users ORDER BY user_xp DESC")
	result3 = cursor.fetchall()
	i=0
	found=False
	while i < len(result3):
		if result3[i][1] == ctx.author.id:
			embed.set_footer(text="@"+ctx.author.name+"#"+ctx.author.discriminator+" is rank #"+str(result3[i][0])+" / "+str(len(result3)))
			found=True
			break
		i=i+1
	await ctx.send(embed=embed)

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
			try:
				try:
					bot.unload_extension(f'cogs.{filename[:-3]}')
				except:
					pass
				bot.load_extension(f'cogs.{filename[:-3]}')
				embed.add_field(name=f'{filename[:-3]}', value="Loaded")
			except:
				embed.add_field(name=f'{filename[:-3]}', value="Failed to Load")
			
			await msg.edit(embed=embed)
	embed.color=0x90EE90
	embed.title="Reload Complete!"
	await msg.edit(embed=embed)
	print("Reload Complete!")

f = open("token.txt", "r")
token = f.read()

bot.run(token)
