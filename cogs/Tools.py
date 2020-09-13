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
		
	
	
	@commands.command(help='Pings a random member')
	async def someone(self, ctx):
		members = ctx.guild.members
		await ctx.send(members[random.randint(0,len(members)-1)].mention)
	@commands.command(help='Donate to Boogle#4509')
	async def donate(self, ctx, amount: int=1):
		embed=discord.Embed(title="Click here to donate $"+str(amount)+".00 with PayPal", url="https://www.paypal.com/cgi-bin/webscr?&cmd=_xclick&business=tsrbuckley@gmail.com&currency_code=USD&amount="+str(amount)+"&item_name=Donation")
		embed.set_footer(text="<3 Thanks for helping me out.")
		# await ctx.author.send("https://www.paypal.com/cgi-bin/webscr?&cmd=_xclick&business=boogleisepic@gmail.com&currency_code=USD&amount="+str(amount)+"&item_name=Donation")
		if amount >= 1: 
			await ctx.author.send(embed=embed)
			await ctx.send("`Check your DMs` "+ctx.author.mention, delete_after=5)
		else:
			embed=discord.Embed(color=0xf00a3a)
			embed.add_field(name="Error!", value="Donation must be greater or equal to $1.00", inline=True)
			await ctx.send(embed=embed)
	@commands.command(help='Countsdown from desired time')
	async def countdown(self, ctx, seconds: int=10):
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
	@commands.command(help='Sends you a list of all the roles')
	async def getroles(self, ctx):
		async with ctx.typing():
			f = open("rolelist.txt","w")
			x = ctx.guild.roles
			for role in x:
				f.write("@"+role.name+"\n")
			f.close()
			await ctx.send("`Check your DMs` "+ctx.author.mention, delete_after=5)
			await ctx.author.send(file=discord.File('rolelist.txt'))
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
	@commands.command(help='Dumps all members of a role')
	async def dump(self, ctx, role: discord.Role=None):
		async with ctx.typing():
			f = open("dumped"+role.name+".txt","w")
			members = role.members
			for member in members:
				f.write(member.name+"#"+member.discriminator+"\n")
			f.close()
			if len(members) < 1:
				await ctx.send("There are no members with that role")
			else:
				await ctx.send("`Check your DMs` "+ctx.author.mention, delete_after=5)
				await ctx.author.send(file=discord.File("dumped"+role.name+".txt"))


		
	@commands.command(help='Sends you a list of all the banned members')
	async def bans(self, ctx):
		async with ctx.typing():
			f = open("bannedmembers.txt","w")
			bans = await ctx.guild.bans()
			for ban in bans:
				try:
					f.write(str(ban.user)+" reason: "+ban[0]+"\n")
				except:
					pass
			f.close()
			await ctx.send("`Check your DMs` "+ctx.author.mention, delete_after=5)
			await ctx.author.send(file=discord.File('bannedmembers.txt'))		
			
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
	@commands.command(help='Gets you info on the bot', aliases=['about','bot','invite'])
	async def botinfo(self, ctx):
		roles = [role for role in ctx.guild.roles]
		
		embed = discord.Embed(title="Click me for bot invite", url="https://discordapp.com/api/oauth2/authorize?client_id=688821496080367619&permissions=8&scope=bot", color = 0xFFA500, timestamp=ctx.message.created_at)
		
		embed.set_author(name=f"Bot Info - {self.bot.user}")
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
		
		embed.add_field(name="ID:", value=self.bot.user.id)
		embed.add_field(name="Name:", value=self.bot.user)
		embed.add_field(name="Created at:", value=self.bot.user.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
		
		sum = 0
		guilds = self.bot.guilds
		for guild in guilds:
			sum += len(guild.members)
		embed.add_field(name="Server Count:", value=len(guilds))
		embed.add_field(name="Member Count:", value=sum)
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
