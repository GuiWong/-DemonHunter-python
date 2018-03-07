import libtcodpy as libtcod

from WongEngine import  Window, Ui, WongUtils
import Target, Actions


class Classe:

	def __init__(self):

		self.name=None
		self.base_skills=list()
		self.learn_skills=list()
		self.type=None




class Warrior(Classe):

	def __init__(self):

		Classe.__init__(self)
		self.name="Warrior"

		self.baseAP=3
		self.baseHP=4
		self.char=chr(82)

		self.type='fight'

		self.base_skills.append(Actions.Attack())

class Assasin(Classe):

	def __init__(self):

		Classe.__init__(self)
		self.name="Assasin"

		self.baseAP=4
		self.baseHP=3
		self.char=chr(105)
		self.type='stealth'

		self.base_skills.append(Actions.Attack())

class Archer(Classe):

	def __init__(self):

		Classe.__init__(self)
		self.name="Ranger"

		self.baseAP=3
		self.baseHP=3
		self.char=chr(68)
		self.type='range'

		self.base_skills.append(Actions.RangeAttack())

class Sage(Classe):

	def __init__(self):

		Classe.__init__(self)
		self.name="Sage"

		self.baseAP=3
		self.baseHP=3
		self.char=chr(55)
		self.type='sage'

		self.base_skills.append(Actions.Attack())

class Demonito(Classe):

	def __init__(self):

		Classe.__init__(self)
		self.name="Demonito"

		self.baseAP=2
		self.baseHP=2
		self.char=chr(235)

		self.base_skills.append(Actions.Attack())

class Runner(Classe):

	def __init__(self):

		Classe.__init__(self)
		self.name="Runner"

		self.baseAP=2
		self.baseHP=2
		self.char=chr(224)
		self.type='stealth'

		self.base_skills.append(Actions.Attack())
