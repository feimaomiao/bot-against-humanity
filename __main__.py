import asyncio
import datetime
import json

import discord
import requests
from discord import Embed as discordembed
from discord.ext import commands, tasks

from exec import *

TOKEN = open(".env").read()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("cah "))
bot.remove_command("help")

class cmds(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.games = {}
		self.initMessage = None

	# returns the game the client is running.
	def _selfgame(self, client):
		return self.games[str(client.guild.id)]

	# initialize bot, tells me when the bot is online.
	@commands.Cog.listener()
	async def on_ready(self):
		self.games = {str(k.id) : None for k in self.bot.guilds}
		print("game online")

	# Creates game with parameters
	@commands.command(name="create")
	async def create(self, client):
		await client.message.delete()
		# Checks if the guild is running a game currently
		if self._selfgame(client) == None:
			self.games[str(client.guild.id)] = game(client)
		else:
			msg = await client.send("There is a game in progress!\nPlease wait until the current game is over!")
			await asyncio.sleep(5)
			return await msg.delete()
		await self._selfgame(client).initialise(client)
		return

	# Ends game
	@commands.command(name="end")
	async def endGame(self,client):
		await client.message.delete()
		# Checks if there is a game running on the server
		if self._selfgame(client) == None:
			message = await client.send("There is no game associated to this server!")
		# Check if the sender is the game creator
		elif not client.author == self._selfgame(client).creator:
			message = await client.send("You have to be the game creator to end the game!\nIf the game creator went afk, please wait 10 minutes for the game to auto-end!")
		# deletes the game
		else: 
			await self._selfgame(client).end()
			self.games[str(client.guild.id)] = None
			return
		await asyncio.sleep(5)
		return await message.delete()

	# Joins game with parameters.
	@commands.command(name="join")
	async def joinGame(self, client):
		await client.message.delete()
		if not self._selfgame(client):
			msg = await client.send("There is no game currently assigned to your server!\nYou can create a game with the command cah create")
			await asyncio.sleep(5)
			return await msg.delete()
		return await self._selfgame(client).join(client)



# test func pls del later
	@commands.command(name="test")
	async def test(self, client):
		await client.message.delete()
		await client.send(self.games[str(client.guild.id)].players[0])
		if self._selfgame(client) != None:
			await self.games[str(client.guild.id)].creator.send(self.games[str(client.guild.id)].tzar)
			await client.send(next(self._selfgame(client).tzar.next_q()))


@bot.command(name="dc")
async def bot_logout(client):
	await bot.logout()
	
bot.add_cog(cmds(bot))

bot.run(TOKEN)
