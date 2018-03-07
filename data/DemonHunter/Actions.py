import libtcodpy as libtcod

from WongEngine import  Window, Ui, WongUtils
import Target


class Skill:

	def __init__(self):

		self.name='default'
		self.target=None	#the Target object who handle targetting
		self.power=0		#the damage/heal/power of the skill
		self.type='use'		# use/enemy/team/self
		self.cost=0			#the AP cost of the spell

class Move(Skill):

	def __init__(self):

		self.name='move'
		self.target=None	#the Target object who handle targetting
		self.power=0		#the damage/heal/power of the skill
		self.type='use'		# use/enemy/team/self
		self.cost=0



class Attack(Skill):

	def __init__(self):

		Skill.__init__(self)

		self.name='attack'
		self.target=Target.CaC()	#the Target object who handle targetting
		self.power=1		#the damage/heal/power of the skill
		self.type='enemy'		# use/enemy/team/self
		self.cost=0

class RangeAttack(Skill):

	def __init__(self):

		Skill.__init__(self)

		self.name='attack'
		self.target=Target.Ranged(1,3)	#the Target object who handle targetting
		self.power=1		#the damage/heal/power of the skill
		self.type='enemy'		# use/enemy/team/self
		self.cost=0
