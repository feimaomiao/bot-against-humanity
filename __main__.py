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


	@commands.Cog.listener()
	async def on_ready(self):
		self.games = {str(k.id) : None for k in self.bot.guilds}
		print("game online")

	@commands.command(name="create")
	async def create(self, client):
		if self.games[str(client.guild.id)] == None:
			self.games[str(client.guild.id)] = game(client)
		else:
			return await client.send("There is a game in progress!\nPlease wait until the current game is over!")
		await self._selfgame(client).initialise()
		self.

	# @commands.command(name="end")
	# async def endGame(self,client):
	# 	if self.games():
	# 		pass


# test func pls del later
	@commands.command(name="test")
	async def test(self, client):
		await client.send(self.games[str(client.guild.id)].players[0])
		await self.games[str(client.guild.id)].creator.send(self.games[str(client.guild.id)].tzar)
		await client.send(next(self._selfgame(client).tzar.next_q()))



bot.add_cog(cmds(bot))

bot.run(TOKEN)
