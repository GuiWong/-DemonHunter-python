
import sys
import os
import libtcodpy as libtcod
import weakref
import random

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

		self.random = libtcod.random_get_instance()



	def set_tileset(self,tileset):

		self.tileset=tileset

	def create_map(self):

		#TODO map generation
		pass

	def generate_level(self,branch,depth,max,min,minmin):

		self.map=Map.Map(40,40)
		self.map.empty(self.tileset)

		self.roomlist=list()

		self.create_main_room(max,min)

		self.spawn=None
		self.monster_spawn=None

		self.roomlist.append(self.main_room)

		a,b,c,d=self.main_room.get_area(minmin)
		#print area
		count=0
		branches=list()
		for i in range(1000):
			x,y,w,h=self.roll_room(a,b,c,d,minmin,min)
			r=Room(x,y,w,h,self.main_room)
			self.main_room.collide(r)
			if r.collide(self.main_room):
				count+=1
				col=make_room(self.map,self.tileset,0,1,x,y,w,h)
				#if not col:
					#print 'no passage here'
					#self.build_door(self.main_room,r)
 				branches.append([r])
				self.roomlist.append(r)


			if count>=branch:
				break

		count=0
		a=0
		for room in branches:
			count=0
			room=room[0]
			for i in range(1000):
				corner=room.get_outer_corner()
				right, bottom =room.outer_corner
				radius=minmin

				if right:

					dx=corner[0]-radius+2
					ddx=corner[0]-2
				else:
					dx=corner[0]-radius+2
					ddx=corner[0]+2

				if bottom:

					dy=corner[1]-radius+2
					ddy=corner[1]-2
				else:
					dy=corner[1]-radius+2
					ddy=corner[1]+2

				x,y,w,h=self.roll_room(dx,dy,ddx,ddy,minmin,min)
				new_room=Room(x,y,w,h,room)

				if new_room.collide(room):
					count+=1
					col=make_room(self.map,self.tileset,0,1,x,y,w,h)
					#if not col:
						#print 'no passage here'
						#self.build_door(self.main_room,r)
	 				branches[a].append(r)
					self.roomlist.append(r)
					room=r
				if count>=depth:
					break
				#a,b,c,d=room.get_area(minmin)
				#x,y,w,h=self.roll_room(a,b,c,d,minmin,min)
		#self.roomlist=self.roomlist+branches[a]
		a+=1


		#self.roomlist=list()
		#print branches

		print 'nbre de pieces: ' + str(len(self.roomlist))
		#self.set_player_room(branches[0])
		#self.set_monster_room(branches[1])
		#make_room(self.map,self.tileset,0,1,x,y,w,h)

		if self.set_spawns():
			return True
		else:
			return False


	def set_spawns(self):

		stop=False
		for i in range(200):
			self.randomize_spawn()
			for j in range(1000):
				self.randomize_monster_spawn()

				path=libtcod.path_new_using_map(self.map.pathdata,0)
				libtcod.path_compute(path,self.spawn[0],self.spawn[1],self.monster_spawn[0],self.monster_spawn[1])
				siz = libtcod.path_size(path)

				libtcod.path_delete(path)

				print siz
				if siz<16 or siz>40:
					break
				else:
					stop=True
					print siz
					break

			if stop:
				break

		print 'done?'

		if stop:
			return True
		else:
			return False

	def get_random_tile(self,x=0,y=0,w=40,h=40):

		x=int(libtcod.random_get_float(0,x,x+w-1))
		y=int(libtcod.random_get_float(0,y,y+h-1))
		return x,y

	def randomize_spawn(self):
			r=self.get_random_room()
			tx,ty=self.get_random_tile(r.x,r.y,r.w,r.h)

			self.place_spawn(tx,ty)
	def randomize_monster_spawn(self):
			r=self.get_random_room()
			tx,ty=self.get_random_tile(r.x,r.y,r.w,r.h)

			self.place_monster_spawn(tx,ty)

	def get_random_room(self):

		#a=random.randrange(0,len(self.roomlist))
		a=int(libtcod.random_get_float(0,0,len(self.roomlist)))
		return self.roomlist[a]

	def place_spawn(self,x,y):

		if self.spawn:
			tile=self.tileset.create_tile(0)
			self.map.set_tile(self.spawn[0],self.spawn[1],tile)
			libtcod.map_set_properties(self.map.pathdata,self.spawn[0],self.spawn[1],tile.view,tile.path)
		else:
			pass
		self.spawn=x,y
		tile=self.tileset.create_tile(4)
		self.map.set_tile(x,y,tile)
		libtcod.map_set_properties(self.map.pathdata,x,y,tile.view,tile.path)

	def place_monster_spawn(self,x,y):

		if self.monster_spawn:
			tile=self.tileset.create_tile(0)
			self.map.set_tile(self.monster_spawn[0],self.monster_spawn[1],tile)
			libtcod.map_set_properties(self.map.pathdata,self.monster_spawn[0],self.monster_spawn[1],tile.view,tile.path)
		else:
			pass
		self.monster_spawn=x,y
		tile=self.tileset.create_tile(5)
		self.map.set_tile(x,y,tile)
		libtcod.map_set_properties(self.map.pathdata,x,y,tile.view,tile.path)


	def set_monster_room(self,branch):
		rumm=branch[0]
		make_room(self.map,self.tileset,5,1,rumm.x,rumm.y,rumm.w,rumm.h)
	def set_player_room(self,branch):
		rumm=branch[0]
		make_room(self.map,self.tileset,4,1,rumm.x,rumm.y,rumm.w,rumm.h)
	#	self.place_spawn(rumm)
	def create_main_room(self,max,min):

		x,y,w,h=self.roll_main_room(10,max,min)

		make_room(self.map,self.tileset,0,1,x,y,w,h)

		self.main_room=Room(x,y,w,h)

	#def build_door(self,room1,room2):

	#	connex_wall=list()

	#	for wall in room1.get_walls():
	#		if room2.is_a_wall(wall):
	#			connex_wall.append(wall)

#		print connex_wall
#
		#for elem in connex_wall:

	#		tile=self.tileset.create_tile(2)
		#	self.map.set_tile(elem[0],elem[1],tile)
		#	map.set_tile(X,Y,tile)



	def build_branch(self,room,max,min):
		pass

	def roll_room(self,x,y,xw,yh,min,max):

		#x=random.randrange(x,xw+1)
		#y=random.randrange(y,yh+1)
		x=int(libtcod.random_get_float(0,x,xw+1))
		y=int(libtcod.random_get_float(0,y,yh+1))
		print y

		w=int(libtcod.random_get_float(0,min,max+1))
		h=int(libtcod.random_get_float(0,min,max+1))
	#	w=random.randrange(min,max+1)
		#h=random.randrange(min,max+1)

		return x,y,w,h

	def roll_main_room(self,dist,max,min):

		x=random.randrange(dist,40-max-dist+1)
		y=random.randrange(dist,40-dist-max+1)

		w=random.randrange(min,max+1)
		h=random.randrange(min,max+1)

		return x,y,w,h

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


class Room:

	def __init__(self,x,y,w,h,parent=None):

		self.x=x
		self.y=y
		self.w=w
		self.h=h
		self.parent=parent

	def collide(self,room):

		s=0
		h=0
		corners_in=[False,False,False,False]#0,left,1:top,2:right,3:bottom
		if self.x>room.x and self.x<room.x+room.w-1:
			s+=1
			corners_in[0]=True
		if self.x+self.w-1>room.x and self.x+self.w<=room.x+room.w:
			s+=1
			corners_in[2]=True
		if self.y>room.y and self.y<room.y+room.h-1:
			h+=1
			corners_in[1]=True
		if self.y+self.h-1>room.y and self.y+self.h<=room.y+room.h:
			h+=1
			corners_in[3]=True

		count=0
		for val in corners_in:
			if val:
				count += 1

		if count>3:
		#	print '------------------------------------------------'
		#	print 'attention, cas non traite'
		#	print '------------------------------------------------'
			right,bottom=self.parent.outer_corner
		elif corners_in[0] and corners_in[2]:

			bottom=corners_in[1]
			if self.x+(self.x+self.w-1)/2 >= room.x+(room.x+room.w-1)/2:
				right=True
			else:
				right=False

		elif corners_in[1] and corners_in[3]:

			right=corners_in[0]
			if self.y+(self.y+self.h-1)/2 >= room.y+(room.y+room.h-1)/2:
				bottom=True
			else:
				bottom=False

		else:

			right=corners_in[0]
			bottom=corners_in[1]



		self.outer_corner=[right,bottom]


		if  s>0 and h>0:
			return True
		else:
			return False

	def get_outer_corner(self):

		if self.outer_corner[0]:
			cx=self.x+self.w-1
		else:
			cx=self.x

		if self.outer_corner[1]:
			cy=self.y+self.h-1
		else:
			cy=self.y

		return [cx,cy]

	def get_walls(self):

		result=list()

		for Y in range(self.y,self.y+self.h):#TODO: verify size
			result.append([self.x,Y])
			result.append([self.x+self.w+1,Y])
			for X in range(self.x+1,self.x+self.w):
				if Y==self.y or Y==self.y+self.h:
					result.append([X,Y])
				else:
					break

		return result

	def is_a_wall(self,tile):
		return tile[0]==self.x or tile[0]==self.x+self.w or tile[1]==self.y or tile[1]==self.y+self.h

	def get_area(self,min):
		x=self.x-min
		y=self.y-min
		xw=self.x+self.w-1
		yh=self.y+self.h-1

		return x,y,xw,yh

def make_room(map,tileset,id,idwall,x,y,w,h):
	collision=False
	for Y in range(y,y+h,1):
		for X in range(x,x+w,1):

			if X<0 or X>=40 or Y<0 or y>=40:

				print 'out of the map'
				break

			elif Y==y or Y==y+h-1 or X==x or X==x+w-1:
				if map.get_tile(X,Y).path:
					tile=tileset.create_tile(id)
					map.set_tile(X,Y,tile)
					#collision=True
				else:
					tile=tileset.create_tile(idwall)
					map.set_tile(X,Y,tile)
			else:
				if map.get_tile(X,Y).path:
					collision=True
				tile=tileset.create_tile(id)
				map.set_tile(X,Y,tile)
			libtcod.map_set_properties(map.pathdata,X,Y,tile.view,tile.path)
	return collision

def create_test_map(tileset):

	map=Map.Map(40,40)
	map.empty(tileset)
	make_room(map,tileset,0,12,12,16,12)
	make_room(map,tileset,0,7,7,7,7)
	make_room(map,tileset,0,27,10,6,6)
	return map
