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

class Ranged(Target):

	def __init__(self,min,max):

		Target.__init__(self)
		self.min_range=min
		self.max_range=max

	def get_potential_target(self,X,Y):

		radius=self.max_range
		result=list()

		print 'looking for targetable tiles'

		b=-1
		h=-1
		grow=True

		for y in range(2*radius+1):
			if grow:
				b+=1
				h+=2
			else:
				b-=1
				h-=2
			if y==radius:
				grow=False
			for x in range(h):

				#print tile
				tile=[X-b+x,Y-radius+y]
				if abs(tile[0]-X)+abs(tile[1]-Y)>=self.min_range:

					result.append(tile)

		return result
