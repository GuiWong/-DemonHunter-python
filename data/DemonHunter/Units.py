import libtcodpy as libtcod

from WongEngine import  Window, Ui, WongUtils
import Color, Actions


class Entity:

	def __init__(self,player=True):#TODO

		self.char='@'
		if player:
			self.color=Color.LBLUE
		else:
			self.color=Color.LRED
		self.name='default'

		self.x=0
		self.y=0

	def set_pos(self,x,y):

		self.x=x
		self.y=y


	def get_color(self):
		return self.color
	def set_color(self,color):
		self.color=color
	def set_char(self,char):
		self.char=char




class Unit:

	def __init__(self,player=True):

		self.level=0
		self.entity=Entity(player)
		self.classe=None
		self.skills=list()

		self.skills.append(Actions.Move())
		self.AP=0
		self.AP_max=2

		self.HP=1
		self.HP_max=1

		self.ready=True

		self.player=player


	def set_class(self,classe):

		self.classe=classe


	def learn_skill(self,skill):

		self.skills.append(skill)


	def build_from_class(self):

		self.AP_max=self.classe.baseAP
		self.HP_max=self.classe.baseHP

		self.AP=self.classe.baseAP
		self.HP=self.classe.baseHP

		self.entity.set_char(self.classe.char)

		for skil in self.classe.base_skills:

			self.learn_skill(skil)





	#-----getter (used for jaugues)-------------
	def get_name(self):

		return self.entity.name

	def set_name(self,name):

		self.entity.name=name

	def get_class_name(self):

		return self.classe.name


	def get_HP(self):
		return self.HP
	def get_HP_max(self):
		return self.HP_max
	def change_HP(self,val):
		self.HP+=val
		if self.HP>self.HP_max:
			self.HP=self.HP_max
		elif self.HP<=0:
			print 'Dead'
	def change_AP(self,val):
		self.AP+=val
		if self.AP>self.AP_max:
			self.AP=self.AP_max
	def get_AP(self):
		return self.AP
	def get_AP_max(self):
		return self.AP_max

	def is_ready(self):
		return self.ready
	def end_turn(self):
		self.ready=False
	def set_ready(self):
		self.ready=True

	def get_entity(self):
		return self.entity

	def get_pos(self):
		return self.get_entity().x, self.get_entity().y
	def set_pos(self,x,y):
		self.get_entity().x=x
		self.get_entity().y=y

	def get_skill(self,id):

		return self.skills[id]

	def get_type(self):

		return self.classe.type


	def __del__(self):

		print self.get_name(), ' revoved from memory'



class Squad:

	def __init__(self,size):

		self.units=list()
		self.max=size

	def get_unit_by_name(self,name):

		result=None
		for unit in self.units:

			if unit.get_name()==name:

				result=unit

		return result

	def get_unit(self,id):

		return self.units[id-1]

	def add_unit(self,unit):

		self.units.append(unit)


	def get_entities(self):

		ret=list()
		for unit in self.units:
			ret.append(unit.get_entity())
		return ret

	def get_units(self):

		return self.units

	def remove_unit(self,unit):

		for elem in self.units:

			if elem == unit:
				self.units.remove(unit)
				break






class Corpse(Unit):

	def __init__(self):

		Unit.__init__(self,False)

	def is_ready(self):
		return self.ready

	def build_from_unit(self,unit):

		self.set_name(unit.get_name()+' Body')
		self.entity.set_char(chr(37))
		self.entity.set_color(Color.BLACK)

		self.AP_max=0
		self.HP_max=0

		self.AP=0
		self.HP=0

		self.set_pos(unit.get_pos()[0],unit.get_pos()[1])

	def get_type(self):

		return 'Corpse'
