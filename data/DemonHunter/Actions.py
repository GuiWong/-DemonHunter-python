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

		self.inflict_state=None
		self.state_bonus=None
		self.effect=None

	def get_power(self):

		return self.power

	def get_name(self):
		return self.name

class No_Skill(Skill):

	def __init__(self):

		self.name='-------'
		self.target=None	#the Target object who handle targetting
		self.power=0		#the damage/heal/power of the skill
		self.type='use'		# use/enemy/team/self
		self.cost=0


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

class Kick(Skill):

	def __init__(self):

		Skill.__init__(self)

		self.name='Kick'
		self.target=Target.CaC()	#the Target object who handle targetting
		self.power=1		#the damage/heal/power of the skill
		self.type='enemy'		# use/enemy/team/self
		self.cost=1			#the AP cost of the spell

		self.inflict_state=None
		self.state_bonus=None
		self.effect=['push',1]

class Lock(Skill):

	def __init__(self):

		Skill.__init__(self)

		self.name='Lock'
		self.target=Target.CaC()	#the Target object who handle targetting
		self.power=0	#the damage/heal/power of the skill
		self.type='enemy'		# use/enemy/team/self
		self.cost=1			#the AP cost of the spell

		self.inflict_state='locked'
		self.state_bonus=None


class Paralyse(Skill):

	def __init__(self):

		Skill.__init__(self)

		self.name='Paralyse'
		self.target=Target.Ranged(4,6)	#the Target object who handle targetting
		self.power=0		#the damage/heal/power of the skill
		self.type='enemy'		# use/enemy/team/self
		self.cost=0

		self.effect=['AP',-2]


class BackStab(Skill):

	def __init__(self):

		Skill.__init__(self)

		self.name='Backstab'
		self.target=Target.CaC()	#the Target object who handle targetting
		self.power=0	#the damage/heal/power of the skill
		self.type='enemy'		# use/enemy/team/self
		self.cost=0			#the AP cost of the spell

		self.state_bonus=['locked',2]
