
import sys
import os
import libtcodpy as libtcod
import weakref

from WongEngine import  Map, WongUtils

import Units


class Level:
	'''
	class who contain a map,
	and all its objects
	'''
	def __init__(self):

		self.map=Map.Map(10,10)
		self.monsters=Units.Squad(10)
		self.tileset=None


	def set_tileset(self,tileset):

		self.tileset=tileset

	def create_map(self):

		#TODO map generation
		pass

	def load_map(self,name,tileset=None):

		if not tileset:
			if not self.tileset:
				print "Error! Must give tileset to load"
				#TODO make exeptions
			else:
				tileset=self.tileset

		self.map.load(name,tileset)

	def get_path_map(self):

		return self.map



	def set_squad(self,squad):

		self.monsters=squad

	def add_monster(self,monster):

		self.monsters.add_unit(monster)

	def get_monsters(self):

		return self.monsters.get_units()

	def get_entities(self):

		return self.monsters.get_entities()


def make_room(map,tileset,id,x,y,w,h):

	for Y in range(y,y+h,1):
		for X in range(x,x+w,1):
			tile=tileset.create_tile(id)
			map.set_tile(X,Y,tile)
			libtcod.map_set_properties(map.pathdata,X,Y,tile.view,tile.path)

def create_test_map(tileset):

	map=Map.Map(40,40)
	map.empty(tileset)
	make_room(map,tileset,0,12,12,16,12)
	make_room(map,tileset,0,7,7,7,7)
	make_room(map,tileset,0,27,10,6,6)
	return map
