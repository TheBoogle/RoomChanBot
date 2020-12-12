import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import random
import asyncio
import aiohttp
import os
import json
import soundfile as sf
bernieBomb = 5
bernieNuke = 30
class Fun(commands.Cog):
	
	def __init__(self, bot):
		self.bot = bot
	
	print("\033[92mLoading Fun Cog\033[0m")
	
	@commands.command(help='Command is exclusive to Ciba')
	async def ciba(self, ctx):
		if int(ctx.author.id) == 516713042558320664:
			await ctx.send(":point_down: Gay :flushed: :point_down:")
		else:
			await ctx.send(":point_up: Gay :flushed: :point_up:")
	@commands.command(help='Tells CanyonJack roomchan loves him')
	@commands.cooldown(1, 1000, commands.BucketType.guild)
	async def dmcanyon(self, ctx):
		user = await self.bot.fetch_user(524686319004155924)
		try:
			await user.send('I love you CanyonJack ♥')
			await ctx.channel.send("Your love message was sent!")
		except:
			await ctx.channel.send("An error occured while sending this message, he may have blocked Room Chan")
	@commands.command(help='Tells PoptartNoahh "poopfartnoahh" ')
	@commands.cooldown(1, 1000, commands.BucketType.guild)
	async def dmpoptartnoahh(self, ctx):
		user = await self.bot.fetch_user(281922284216909824)
		try:
			await user.send('poopfartnoahh xd')
			await ctx.channel.send("Your hate message was sent!")
		except:
			await ctx.channel.send("An error occured while sending this message, he may have blocked Room Chan")
	@commands.command(help='I love me some bread')
	async def baguette(self, ctx, member:discord.User=None):
		if member == None:
			member = ctx.author
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/imagegen?type=baguette&url='+str(member.avatar_url)) as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Baguette")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)	
		
	@commands.command(help="Get Weather For Location")
	async def weather(self, ctx, lat: str="10", lon: str="10"):
		async with aiohttp.ClientSession() as session:
				async with session.get('https://api.openweathermap.org/data/2.5/onecall?lat={0}&lon={1}&units=imperial&part=current&appid=1db40d6e610ba7e7cf22ef2ce45df6e8'.format(lat, lon)) as resp:
					data = json.loads(str(await resp.text()))
		try:			
			embed = discord.Embed(title="Weather for lat:{0} | lon:{1}".format(lat, lon))
			embed.set_thumbnail(url="http://openweathermap.org/img/wn/{0}@2x.png".format(data['current']['weather'][0]['icon']))
			embed.add_field(name="Timezone", value = data['timezone'])
			embed.add_field(name="Weather", value=data['current']['weather'][0]['description'])
			embed.add_field(name="Cloudiness", value=str(data['current']['clouds'])+"%")
			f = int(data['current']['temp'])
			c = int( (f - 32) * 5/9)
			embed.add_field(name="Temperature", value=str(f)+" F / " + str(c) + " C")
			await ctx.send(embed=embed)
		except:
			await ctx.send("That location could not be found.")
					
	@commands.command(help='Trap card kekw')
	async def trap(self, ctx, member:discord.User=None):
		if member == None:
			member = ctx.author
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/imagegen?type=trap&name='+str(member.name)+'&author='+str(ctx.author.name)+'&image='+str(member.avatar_url)) as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Trap")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)	
	@commands.command(help='Weeb shit bro')
	async def awooify(self, ctx, member:discord.User=None):
		if member == None:
			member = ctx.author
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/imagegen?type=awooify&url='+str(member.avatar_url)) as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Awooify")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)	
	@commands.command(help='Deep frys an image')
	async def deepfry(self, ctx, member:discord.User=None):
		if member == None:
			member = ctx.author
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/imagegen?type=deepfry&image='+str(member.avatar_url)) as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Deepfried")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command(help='More weeb shit')
	async def trash(self, ctx, member:discord.User=None):
		if member == None:
			member = ctx.author
		async with aiohttp.ClientSession() as session:
				async with session.get('https://nekobot.xyz/api/imagegen?type=trash&url='+str(member.avatar_url)) as resp:
					data = json.loads(str(await resp.text()))
		print(data['message'])
		embed = discord.Embed(title="Trash")
		embed.set_image(url=data['message'])
		await ctx.send(embed=embed)
	@commands.command(help='Calls you a twat')
	async def twat(self, ctx):
		await ctx.send(ctx.author.name+'#'+ctx.author.discriminator+' is a twat.')
	@commands.command(name='8ball', aliases=["eightball"],help='Predicts the future')
	async def eightball(self, ctx):
		eightballanswers=["Yes","Probably","No","Probably Not","idk"]
		await ctx.send(random.choice(eightballanswers))
	@commands.command(aliases=["fc"], help='Flips a coin, 50/50 chance')
	async def flipcoin(self, ctx):
		coin=["It landed tails", "It landed heads"]
		await ctx.send(random.choice(coin))
	@commands.command(aliases=["pp"], help='Measures your PP')
	async def ppsize(self, ctx, member: discord.User=None):
		sizes=["8)","8=)", "8==)", "8===)", "8====)","8=====)","8======)","8=======)", "8========)", "8=========)", "8==========)", "8=================)"]
		if member == None:
			member = ctx.author
		if int(member.id) == 643491766926049318:
			await ctx.send(member.mention+"'s pp: "+sizes[len(sizes)-1])
		elif int(member.id) == 748287469643890719:
			await ctx.send(member.mention+"'s pp: {(.)}")
		# ~ elif int(member.id) == 460040394999332885:
			# ~ await ctx.send(member.display_name+"'s pp: () something about thats not right...")
			
		else:
			random.seed(a=member.id)
			await ctx.send(member.mention+"'s pp: "+random.choice(sizes))
			random.seed(a=None)
	@commands.command(aliases=["rr"], help='Hidden rickroll in an embed')
	async def rickroll(self,ctx,*,message):
		await ctx.channel.purge(limit=1)
		embed=discord.Embed(title="Breaking News! Click me!", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",description=message)
		await ctx.send(embed=embed)
	# ~ @commands.command(aliases=["p"], help='Play in the million dollar lottery')
	# ~ async def lottery(self, ctx):
		# ~ luck = random.randint(0,500)
		# ~ if luck == 500:
			# ~ await ctx.send("Congragulations, "+ctx.author.mention+"! You won the lottery of :dollar:1,000,000 DM Boogle#4509 to claim your prize.")
		# ~ else:
			# ~ await ctx.send("Better luck next time. " + str(luck) +"/500")
def setup(bot):
	bot.add_cog(Fun(bot))

