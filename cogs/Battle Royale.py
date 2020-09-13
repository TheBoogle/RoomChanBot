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

mydb = mysql.connector.connect(
	host="localhost",
	user="pi",
	passwd=None,
	database="userlevels"
)
weapons = ["AKM", "HK416", "Kar98K", "Mosin", "Duck Spine", "MP5K", "S12K", "Pump shotgun", "Double-Barrel shotgun", "Desert Eagle", "Fists", "Knife", "Lamp", "Rat", "No U", "Soda Can", "Gaming computer", "Beans"]
locations = ["Shelter", "Quarry", "Basecamp", "Airfield", "Millitary Base", "Big City 1", "Big City 2", "Village", "Qlyhen Mountain", "Llama Fields", "The Factory", "The Beach", "Middle of no where"]
joinable = False
class BattleRoyale(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(pass_Context=True)
	async def join(self, ctx):
		global joinable
		global players
		msg = ctx.message
		if joinable == True:
			await ctx.send(f"{ctx.author.mention} Joined!")
			await msg.delete()
			players.append(ctx.author)
		else:
			await ctx.send("Game is in progress/No game started/Game uses all members")
		
		
		
	@commands.command(pass_Context=True)
	@commands.has_permissions(administrator=True)
	async def br(self, ctx, waittime: int=30, maxplayers: int=None):
		global joinable
		global players
		ranonce=False
		loser = None
		embed = discord.Embed(title="A BR is starting...", description=f"Will start in {waittime} seconds")
		await ctx.send(embed=embed)
		if maxplayers != None:
			players=ctx.guild.members
		else:
			joinable=True
			players=[]
		playersweapons=[]
		playerslocations=[]
		playerkills=[]
		await asyncio.sleep(waittime-3)
		msg = await ctx.send("**FINAL WARNING!** Game starting in 3 seconds")
		await asyncio.sleep(1)
		await msg.edit(content="**FINAL WARNING!** Game starting in 2 seconds")
		await asyncio.sleep(1)
		await msg.edit(content="**FINAL WARNING!** Game starting in 1 seconds", delete_after=3)
		await asyncio.sleep(1)
		joinable = False
		if len(players) > 1:
			pass
		else:
			await ctx.send("Not enough players joined :(")
			return
		mostplayers=len(players)
		random.shuffle(players)
		random.shuffle(playersweapons)
		random.shuffle(playerslocations)
		if maxplayers != None:
			if len(players) > maxplayers:
				print(len(players))
				del players[:len(players)-maxplayers]
				del playersweapons[:len(players)-maxplayers]
				del playerslocations[:len(players)-maxplayers]
				del playerkills[:len(players)-maxplayers]
			# ~ i=0
			# ~ while i < len(players):
				# ~ if players[i].bot:
					# ~ del players[i]
					# ~ del playersweapons[i]
					# ~ del playerslocations[i]
					# ~ del playerkills[i]
				# ~ i=i+1
		embed = discord.Embed(title=f"There are {len(players)} players playing today.", color=0xFFC0CB)
		msg = await ctx.send(embed=embed)
		await asyncio.sleep(2)
		for member in players:
			playersweapons.append(random.choice(weapons))
			playerslocations.append(random.choice(locations))
			playerkills.append(0)
			await asyncio.sleep(0.01)
		
		i=0
		if len(players) <  50:
			for member in players:
				embed = discord.Embed(title="Player #"+str(i+1), color=member.top_role.color, description = member.name+"#"+member.discriminator+f" | Weapon: **{playersweapons[i]}** | Drop Location: **{playerslocations[i]}**")
				embed.set_thumbnail(url=member.avatar_url)
				await msg.edit(content=None, embed=embed)
				await asyncio.sleep(1.50)
				i=i+1
		await asyncio.sleep(1)
		await msg.delete()
		embed = discord.Embed(title="Lets get to it..", color=0x90EE90)
		await ctx.send(embed=embed)
		async def checkLocations():
			# ~ print("Checking locations")
			i=-1
			ranonce=True
			if len(players) == 1:
				return
			while i < len(playerslocations):
				i=i+1
				# ~ print("Finding")
				# ~ print(i)
				# ~ print(len(playerslocations))
				try:
					if playerslocations[i] == playerslocations[i+1]:
						# ~ await ctx.send(f"{players[i].mention} and {players[i+1].mention} are in the same location")
						fighter1 = i
						fighter2 = i+1
						break
				except IndexError:
					pass
				try:
					if playerslocations[i] == playerslocations[i-1]:
						# ~ await ctx.send(f"{players[i].mention} and {players[i-1].mention} are in the same location")
						fighter1 = i
						fighter2 = i-1
						break
				except IndexError:
					pass
				fighter1 = None
				fighter2 = None
				loser = None
			
			
			if fighter1 != None and fighter2 != None:
				await asyncio.sleep(2)
				embed = discord.Embed(color=0xA52A2A)
				embed.title=(f"{players[fighter1].name}#{players[fighter1].discriminator} and {players[fighter2].name}#{players[fighter2].discriminator} are fighting in {playerslocations[fighter1]}!")
				if random.randint(1,3) == 1:
					playerkills[fighter1] += 1
					embed.description=(f"`{players[fighter1].name}#{players[fighter1].discriminator}` killed `{players[fighter2].name}#{players[fighter2].discriminator}` with `{playersweapons[fighter1]}`.  They now have `{playerkills[fighter1]}` kills")
					
					loser = fighter2
					embed.set_thumbnail(url=players[fighter1].avatar_url)
				else:
					playerkills[fighter2] += 1
					embed.description=(f"`{players[fighter2].name}#{players[fighter2].discriminator}` killed `{players[fighter1].name}#{players[fighter1].discriminator}` with `{playersweapons[fighter2]}`. They now have `{playerkills[fighter2]}` kills")
					loser = fighter1
					embed.set_thumbnail(url=players[fighter2].avatar_url)
			else:
				# ~ await ctx.send("No one is in the same location, all players moved.")
				i=0
				while i < len(players):
					playerslocations[i] = random.choice(locations)
					i=i+1
				if len(players) == 2:
					playerslocations[0] = locations[0]
					playerslocations[1] = locations[0]
			if loser != None:
				# ~ print("deleting")
				del players[loser]
				del playersweapons[loser]
				del playerslocations[loser]
				del playerkills[loser]
				embed.set_footer(text="Players Remaining: " + str(len(players)))
				await ctx.send(embed=embed)
			await asyncio.sleep(1)
			await checkLocations()
		if ranonce == False:
			await checkLocations()
		winner = players[0]
		embed = discord.Embed(Title="WINNER", description=f"{winner.mention}({winner.name}#{winner.discriminator}) won the game with `{playerkills[0]}` kills!")
		embed.set_thumbnail(url=winner.avatar_url)
		embed.color = winner.color
		await ctx.send(embed=embed)
		if mostplayers >= 32:
			xp = 5000
		else:
			xp = 100
		cursor = mydb.cursor()
		cursor.execute("SELECT user_xp FROM users WHERE client_id = "+str(winner.id))
		result = cursor.fetchall()
		if len(result) == 0:
			print("\033[93mUser is not in DB, adding...\033[0m")
			if len(winner.name) > 10:
				cursor.execute("INSERT INTO users VALUES(" + str(winner.id) + "," + str(xp) + ',"' + str(winner.name)[0:10]+'")')
			else:
				cursor.execute("INSERT INTO users VALUES(" + str(winner.id) + "," + str(xp) + ',"' + str(winner.name)+'")')
			mydb.commit()
			print("\033[92minserted data\033[0m")
		else:
			currentXP = result[0][0] + xp
			print("\033[92mNew xp:" + str(currentXP)+"\033[0m")
			cursor.execute("UPDATE users SET user_xp = "+ str(currentXP)+" WHERE client_id = " +str(winner.id))
			mydb.commit()
			print("\033[92mUpdated...\033[0m")
def setup(bot):
	bot.add_cog(BattleRoyale(bot))
