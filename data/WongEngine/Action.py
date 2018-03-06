
import sys
import os
import libtcodpy as libtcod
import weakref

#TODO






class Action:

	def __init__(self,game):

		self.game=weakref.ref(game)

	def solve(self,actor,target,map):

		pass



class Move(Action):

	def __init__(self):

		Action.__init__(self)

	def solve(self,actor,target_pos,map):

		libtcod.path_compute(map.path,actor.x,actor.y,target_pos[0],target_pos[1])

		for i in range (libtcod.path_size(map.path)) :
    		actor.set_pos(libtcod.path_get(map.path,i))
			self.game().render()
