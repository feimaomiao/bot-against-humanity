import asyncio
import json
import random
from copy import deepcopy as copyof
from time import time as time
from types import MethodType
from discord import Embed as discordEmbed

random.seed(time())

with open("cah.json") as f:
	js = json.load(f)
	questions = js["questions"]
	answers = js["answers"]

# iterable of a elements from c 
# also pops item from c when yields item
def get_cards(c, a):
	for i in range(a):
		random.shuffle(c)
		yield c.pop()

class game:
	def __init__(self, host_message):

		# pre-define list of players
		self.players = []

		# each game object has its own copy of questions and answers 
		# allows the possibility of multiple games occuring at the same time.
		self.questions = copyof(questions)
		self.answers = copyof(answers)

		# shuffle the questions and answers 
		random.shuffle(self.questions)
		random.shuffle(self.answers)

		# pre-define host
		self.tzar = self.set_Tzar(player(host_message.author, self))

		# static creator
		self.creator = host_message.author
		# end is used to define if the game has ended -> check the game auto ends.
		self.end = False
		self.players.append(self.tzar)

		self.plEmbed=None
		self.playerMsg = None


	# when one joins the game
	async def join(self, join_message):
		# Check if player is already registered in the game.
		if player(join_message.author, self) not in self.players:
			# adds player to list
			self.players.append(player(join_message.author, self))

			# creates discord embed object of a list of players
			self.createPlayerEmbed()
			return await self.playerMsg.edit(embed=self.plEmbed)
		msg = await join_message.send("You have already joined the game!")
		await asyncio.sleep(5)
		return await msg.delete()


	def set_Tzar(self, p):
		p.tzar= True

		def next_q():
			return get_cards(self.questions, 1)

		async def choose_winner():
			pass

		p.next_q = next_q
		p.choose_winner = choose_winner
		return p

	def createPlayerEmbed(self):
		ptrStr = []
		for i in range(len(self.player_list)):
			ptrStr.append(f"{i+1}. {self.player_list[i]}\n")
		self.plEmbed = None
		self.plEmbed = discordEmbed(title="Cards against humainty game")
		self.plEmbed.description = f"Host: {self.creator.mention}"
		self.plEmbed = self.fit1024(ptrStr, self.plEmbed)
		return self.plEmbed

	def fit1024(strArr, embed):
		length = 0
		index = 0
		ret = [""]
		for i in range(len(strArr)):
			if length + len(strArr[i]) < 1024:
				ret[index] += strArr[i]
				length += len(strArr[i])
			else:
				length = 0
				index += 1
				ret.append("")
				ret[index] += strArr[i]
				length += len(strArr[i])
		for i in ret:
			embed.add_field(name="Players",values=i)
		return embed

	@property
	def player_list(self):
		return [i.mention for i in self.players]

	# Initialise game with parameteers
	async def initialise(self, client):
		for p in self.players:
			if p.send_channel == None:
				p.send_channel = await p.user.create_dm()
		self.createPlayerEmbed()
		self.playerMsg = await client.send(embed=self.plEmbed)
		return 

	# deletes all the previous game messages
	# todo at the end: show points???
	async def end(self):
		await self.playerMsg.delete()

# player class takes one input, the discord-user object of the player
class player:
	def __init__(self, userobj, game):
		# user is just an easier way to access other values of the discord user, such as dms and 
		self.user = userobj
		self.name = self.user.display_name
		self.mention = self.user.mention
		self.score = 0
		self.game = game

		self.tzar = False

		# assign cards.
		self.cards = get_cards(self.game.answers, 10)
		self.send_channel = self.user.dm_channel
		
	# assign print(self) values
	def __repr__(self):
		return self.name

	# compare values, used in function game.join
	def __eq__(self, other):
		return self.user == other.user
