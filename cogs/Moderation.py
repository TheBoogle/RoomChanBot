import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os
maxSpam = 20
maxPurge = 1000
class Mod(commands.Cog, ):
	
	def __init__(self, bot):
		self.bot = bot
	print("\033[92mLoading Moderation Cog\033[0m")
	
	@commands.command(hidden=True, help='Shutsdown the bot')
	@commands.is_owner()
	async def shutdown(self, ctx):
		await ctx.send("Shutting down")
		print("Bot was manually shutdown")
		await self.bot.logout()
	
	@commands.command(pass_context=True, help='Deletes messages in bulk')
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, amount: int=10):
		if amount > maxPurge:
			await ctx.send('`Amount must be less than or equal to '+str(maxPurge)+'`')
		else:
			await ctx.channel.purge(limit=amount+1)
			purged = await ctx.send('Purged '+str(amount)+' messages')
			await asyncio.sleep(2)
			await purged.edit(content="a", delete_after=0)
	@commands.command(help='Spams messages')
	@commands.has_permissions(administrator=True)
	async def spam(self, ctx, amount: int=5, *, phrase,):
		if amount <= maxSpam:
			for x in range(0,amount):
					await ctx.send(phrase)
		else:
			await ctx.send('`Amount must be less than or equal to '+str(maxSpam)+'`')
	@commands.command('Sends an embed')
	async def embed(self, ctx, title,  *, content):
		await ctx.channel.purge(limit=1)
		embed=discord.Embed()
		embed=discord.Embed(title=title, description=content, color=0xff5500)
		embed.set_author(name=ctx.author.name+"#"+ctx.author.discriminator, icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	@commands.command(help='Bans a member')
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member:discord.User=None, *, reason=None):
		if member == None or member == ctx.message.author:
			await ctx.channel.send("You cannot ban yourself")
			return
		if reason == None:
			reason = "No reason provided..."
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
def setup(bot):
	bot.add_cog(Mod(bot))
