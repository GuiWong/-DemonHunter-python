import libtcodpy as libtcod

from WongEngine import  Window, Ui, WongUtils
import Color


class Target:

	def __init__(self):

		self.range=1
		self.radius=0

	def get_potential_target(self,x,y):

		pass


class CaC(Target):

	def __init__(self):

		Target.__init__(self)


	def get_potential_target(self,x,y):

		result=[[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
		return result

	def get_affected_tiles(self,x,y,cx,cy):

		return [[cx,xy]]
