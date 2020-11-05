import discord
from discord.ext.commands import Bot
from discord.ext import commands
import random
import asyncio
import aiohttp
import os

class Tools(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	
	print("\033[92mLoading Tools Cog\033[0m")
	@commands.command(help='Pings the bots latency')
	async def ping(self, ctx):
		await ctx.send('`Pong! {0}ms`'.format(round(self.bot.latency, 2)))
		
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
	@commands.command(help='Outputs all server emojis')
	async def fetchemojis(self, ctx):
		emojis = await ctx.guild.fetch_emojis()
		message = ""
		for emoji in emojis:
			message = message + str(emoji)
		await ctx.send(message)
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
