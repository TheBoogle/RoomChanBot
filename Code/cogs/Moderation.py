import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import mysql.connector
import os
maxSpam = 20
maxPurge = 500

warning1 = 715331218186436679
warning2 = 715331294136893470
warning3 = 715331322385793137
logchannelId = 801880622187544576

mydb = mysql.connector.connect(
	host="localhost",
	user="boog",
	passwd="lol",
	database="RoomChan"
)

class Mod(commands.Cog, ):
	
	def __init__(self, bot):
		self.bot = bot
		
	print("\033[92mLoading Moderation Cog\033[0m")
	
	# @commands.command()
	# @commands.is_owner()
	# async def clearAllWarns(self, ctx):
	# 		for member in ctx.guild.get_role(warning1).members:
	# 			print("warning1 "+member.name)
	# 			try:
	# 				await member.remove_roles(ctx.guild.get_role(warning1))
	# 			except:
	# 				pass
	# 		for member in ctx.guild.get_role(warning2).members:
	# 			print("warning2 "+member.name)
	# 			try:
	# 				await member.remove_roles(ctx.guild.get_role(warning2))
	# 			except:
	# 				pass
	# 		for member in ctx.guild.get_role(warning3).members:
	# 			print("warning3 "+member.name)
	# 			try:
	# 				await member.remove_roles(ctx.guild.get_role(warning3))
	# 			except:
	# 				pass

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def warn(self, ctx, member:discord.Member=None, *, reason="No reason provided"):
		
		if member:
			logchannel = self.bot.get_channel(logchannelId)
			if member.bot == True:
				await ctx.send("You can't warn a bot!")
				return
			if ctx.author == member:
				await ctx.send("You can't warn yourself!")
				return

			
			cursor = mydb.cursor()
			cursor.execute(f"INSERT INTO warnings (UserId, Reason) VALUES({member.id}, '{reason}')")
			cursor.execute("SELECT LAST_INSERT_ID();")
			result = cursor.fetchall()
			result = result[0][0]

			await logchannel.send(f"Warned {member.mention}({member.id})! `Warning ID: {result}`")
			await ctx.channel.send(f"Warned {member.mention}! `Warning ID: {result}`")

			cursor.execute(f"SELECT * FROM warnings WHERE UserID={member.id}")
			result = cursor.fetchall()
			mydb.commit()

			try:
				await member.remove_roles(ctx.guild.get_role(warning1))
			except:
				pass
			try:
				await member.remove_roles(ctx.guild.get_role(warning2))
			except:
				pass
			try:
				await member.remove_roles(ctx.guild.get_role(warning3))
			except:
				pass

			if len(result) == 1:
				await member.add_roles(ctx.guild.get_role(warning1))
			elif len(result) == 2:
				await member.add_roles(ctx.guild.get_role(warning1))
				await member.add_roles(ctx.guild.get_role(warning2))
			elif len(result) == 3:
				await member.add_roles(ctx.guild.get_role(warning1))
				await member.add_roles(ctx.guild.get_role(warning2))
				await member.add_roles(ctx.guild.get_role(warning3))
			elif len(result) > 3:
				await ctx.channel.send(f"{member.mention} was banned for >3 warnings!")
				await ctx.guild.ban(member, reason=">3 Warnings")




	@commands.command(aliases=['deletewarn'])
	@commands.has_permissions(manage_roles=True)
	async def delwarn(self, ctx, warningID:int=None):
		logchannel = self.bot.get_channel(logchannelId)
		cursor = mydb.cursor()
		cursor.execute(f"DELETE FROM warnings WHERE warningID={warningID}")
		mydb.commit()
		await ctx.channel.send(f"Deleted warning with ID `{warningID}`")
		await logchannel.send(f"Deleted warning with ID `{warningID}`")

	@commands.command(aliases=['warnings'])
	@commands.has_permissions(manage_roles=True)
	async def warns(self, ctx, member:discord.User=None):
		cursor = mydb.cursor()
		cursor.execute(f"SELECT * FROM warnings WHERE UserID={member.id}")
		result = cursor.fetchall()
		mydb.commit()
		embed = discord.Embed(title=f"Warnings for {member.name}#{member.discriminator}")
		
		if len(result) == 0:
			embed.description = 'This user has no warnings.'
		else:
			for x in result:
				embed.add_field(name=f'Warning `ID:{x[2]}`', value=f'Reason: `{x[1]}`',inline=False)
		
		await ctx.send(embed=embed)

	@commands.command(hidden=True, help='Shutsdown the bot')
	@commands.is_owner()
	async def shutdown(self, ctx):
		await ctx.send("Shutting down...")
		print("Bot was manually shutdown")
		await self.bot.logout()
	
	@commands.command(hidden=True, help='Shutsdown the bot')
	@commands.is_owner()
	async def reboot(self, ctx):
		await ctx.send("Rebooting...")
		print("Bot was rebooted.")
		await self.bot.logout()
		os.system("cd ~/Desktop/RoomChanBot/ &&  sudo clear && python3 main.py")
		

	@commands.command(pass_context=True, help='Deletes messages in bulk')
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, amount: int=10):
		await ctx.message.delete()
		if amount > maxPurge:
			await ctx.send('`Amount must be less than or equal to '+str(maxPurge)+'`')
		else:
			await ctx.channel.purge(limit=amount+1)
			await ctx.send(content = 'Purged '+str(amount)+' messages', delete_after=2)
	
	@commands.command(help='Sends an embed')
	async def embed(self, ctx, title,  *, content):
		await ctx.channel.purge(limit=1)
		embed=discord.Embed()
		embed=discord.Embed(title=title, description=content, color=0xff5500)
		embed.set_author(name=ctx.author.name+"#"+ctx.author.discriminator, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	@commands.command(help='Bans a member')
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member, *, reason=None):
		try:
			print(member.id)
		except:
			member = await self.bot.fetch_user(int(member))

		if member == None or member == ctx.message.author:
			await ctx.channel.send("You cannot ban yourself")
			return
		
		if reason == None:
			reason = "No reason provided..."
		logchannel = self.bot.get_channel(logchannelId)
		embed=discord.Embed(color=0xf00a3a)
		embed.add_field(name="You were banned!", value=f"You have been banned from {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} for: `{reason}`", inline=True)
		try:
			await member.send(embed=embed)
		except:
			pass
		
		await ctx.guild.ban(member, reason=reason)
		embed=discord.Embed(color=0xf00a3a)
		embed.add_field(name="Member was banned!", value=f"{member.name}#{member.discriminator} has been banned by {ctx.author.name}#{ctx.author.discriminator} for: `{reason}`", inline=True)
		await ctx.send(embed=embed)
		await logchannel.send(embed=embed)
	@commands.command(help='Assigns a role to member, or removes it if they have it already.')
	@commands.has_permissions(manage_roles=True)
	async def role(self, ctx, member:discord.Member=None, role:discord.Role=None):
		if member == None:
			await ctx.channel.send("Please specify a member")
			return
		roles = [role for role in member.roles]
		i=0
		found=False
		while i < len(roles):
			currentrole=roles[i]

			if role.id == currentrole.id:
				embed=discord.Embed(color=0x90EE90)
				embed.add_field(name="Role removed!", value=f"The {role.mention} was removed from {member.name}#{member.discriminator} by {ctx.author.name}#{ctx.author.discriminator}", inline=True)
				await member.remove_roles(role)
				await ctx.send(embed=embed)
				found=True
				return
			i=i+1
		if found == False:
			embed=discord.Embed(color=0x90EE90)
			embed.add_field(name="Role added!", value=f"The {role.mention} was added to {member.name}#{member.discriminator} by {ctx.author.name}#{ctx.author.discriminator}", inline=True)
			await member.add_roles(role)
			await ctx.send(embed=embed) 
		
			

	@commands.command(help='Kicks a member')
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member:discord.User=None, *, reason=None):
		if member == None or member == ctx.message.author:
			await ctx.channel.send("You cannot kick yourself")
			return
		if reason == None:
			reason = "No reason provided..."
		logchannel = self.bot.get_channel(logchannelId)
		embed=discord.Embed(color=0xf00a3a)
		embed.add_field(name="You were kicked!", value=f"You have were kicked in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} for: `{reason}`", inline=True)
		try:
			await member.send(embed=embed)
		except:
			pass
		
		await ctx.guild.kick(member, reason=reason)
		embed=discord.Embed(color=0xf00a3a)
		embed.add_field(name="Member was kicked!", value=f"{member.name}#{member.discriminator} has been kicked by {ctx.author.name}#{ctx.author.discriminator} for: `{reason}`", inline=True)
		await ctx.send(embed=embed)
		await logchannel.send(embed=embed)
def setup(bot):
	bot.add_cog(Mod(bot))
