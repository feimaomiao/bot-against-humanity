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

	# when one joins the game
	def join(self, join_message):
		self.players.append(player(join_message.author, self))

	def set_Tzar(self, p):
		p.tzar= True

		def next_q():
			return get_cards(self.questions, 1)

		async def choose_winner():
			pass

		p.next_q = next_q
		p.choose_winner = choose_winner
		return p

	def playerlistEmbed(self):
		self.plEmbed = discordEmbed(title="Cards against humainty game")
		self.plEmbed.description = f"Host: {self.creator.display_name}"
		self.plEmbed.add_field(name="Players", value="\n".join(self.player_list))
		return self.plEmbed

	@property
	async def initEmbed(self):
		return await self.playerlistEmbed()
	

	@property
	def player_list(self):
		return [i.name for i in self.players]

	async def initialise(self):
		for p in self.players:
			if p.send_channel == None:
				p.send_channel = await p.user.create_dm()



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
		
	def __repr__(self):
		return self.name

