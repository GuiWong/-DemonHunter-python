
import sys
import os
import libtcodpy as libtcod
import weakref

'''
File For all Entity related classes

'''

class Entity:
	'''
	parent class for all Entity
	'''
	def __init__(self):

		self.x=0
		self.y=0

	def set_pos(self,x,y):

		self.x= x
		self.y= y

	def get_color(self):

		return libtcod.white

	def get_bcg_color(self):

		return libtcod.black

	def __del__(self):

		print 'entity deleted'




class Alive(Entity):
	'''
	parent class for "living" Entity
	'''

	def __init__(self):

		Entity.__init__(self)



	def move(self,dx,dy):

		self.pos=[pos[0]+dx,pos[1]+dy]

class Unit(Alive):

	def __init__(self,char):

		Alive.__init__(self)
		self.char=char
