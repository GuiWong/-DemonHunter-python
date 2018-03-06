
import sys
import os
import libtcodpy as libtcod
import copy


class TilesetListener:

	def __init__(self,tileset):

		self.tempData=[0 for i in range(7)]
		self.tileset=tileset

	def new_struct(self,str,name):

		if libtcod.struct_get_name(str)=='tile':
			self.tempdata=[0 for i in range(7)]
			self.tempdata[1]=name
			return True
		else:
			return False


	def new_flag(self,name):

		return False

	def new_property(self,name,type,value):

		if name=='id':
			self.tempdata[0]=value
		elif name=='chara':
			self.tempdata[2]=value
		elif name=='path':
			self.tempdata[3]=value
		elif name=='view':
			self.tempdata[4]=value

		elif name=='ccolor':
			self.tempdata[5]=(value.r,value.g,value.b)

		elif name=='bcgcolor':
			self.tempdata[6]=(value.r,value.g,value.b)

		else:
			return False

		#print name, value

		return True


	def end_struct(self,struct,name):

		#print self.tempdata
		self.tileset.tile_data[self.tempdata[0]]=copy.deepcopy(self.tempdata)

		return True


	def error(self,msg):

		print msg
		return True



	def __del__(self):

		print 'listener destroyed'


class Tile:

	def __init__(self,passable,viewable,char,color,bkgnd_color):

		self.path=passable
		self.view=viewable
		self.char=char
		self.color=color
		self.background=bkgnd_color

	def set_id(self,id):
		'''
		meant to be used by create_tile() in Tileset classe

		'''

		self.id=id

#-------addedfor 7drl-----------------------------------
	def set_bkg_color(self,color):

		self.background=color


#-------------------------------------------
class Tileset:
	"""
	class to handle tileset, load, store and access tiles properties

	"""

	def __init__(self,size):
		"""
		initialize Tileset object

		:param size: the numer of different tiles handled
		"""

		self.tile_data=[0 for i in range(size)]
		self.size=size


	def load(self,file):

		parser=libtcod.parser_new()
		tile_struc=libtcod.parser_new_struct(parser,"tile")
		libtcod.struct_add_property(tile_struc,"id",libtcod.TYPE_INT,True)
		libtcod.struct_add_property(tile_struc,"chara",libtcod.TYPE_CHAR,True)

		libtcod.struct_add_property(tile_struc,"path",libtcod.TYPE_BOOL,True)
		libtcod.struct_add_property(tile_struc,"view",libtcod.TYPE_BOOL,True)

		libtcod.struct_add_property(tile_struc,"ccolor",libtcod.TYPE_COLOR,True)
		libtcod.struct_add_property(tile_struc,"bcgcolor",libtcod.TYPE_COLOR,True)


		libtcod.parser_run(parser,file,TilesetListener(self))

		self.empty=0

		print "ended"

		libtcod.parser_delete(parser)

	def create_tile(self,id):


		a= Tile(self.tile_data[id][3],self.tile_data[id][4],self.tile_data[id][2],libtcod.Color(*self.tile_data[id][5]),libtcod.Color(*self.tile_data[id][6]))
		a.id=id
		return a


	def set_empty(self,id):
		self.empty=id
	def get_empty(self):
		return self.create_tile(self.empty)
class Map:

	def __init__(self,width,height):

		self.width=width
		self.height=height
		self.data=[[Tile(False,False,chr(219),libtcod.light_blue,libtcod.black) for X in range(width)] for Y in range(height)]

		self.pathdata=libtcod.map_new(width,height)
		#de-actived diagonal movement for pathfinding (7DRL)
		self.path=libtcod.path_new_using_map(self.pathdata,0)



		self.focusTile=False


	def empty(self,tileset):

		self.data=[[tileset.get_empty() for X in range(self.width)] for Y in range(self.height)]

	def get_tile(self,x,y):
		return self.data[y][x]

	def set_tile(self,x,y,tile):
		self.data[y][x]=tile

	def set_focus_tile(self,x,y):

		self.focusTile=(x,y)

	def save(self,name):


		new_fichier=open('Saves/'+name +'.txt','w')
		#:	;
		string=''
		string+=str(self.width)
		string+=':'
		string+=str(self.height)

		string+=';'

		for Y in range(self.height):
			for X in range(self.width):
				string += str(self.get_tile(X,Y).id)
				string += ':'
			string += ';'

		new_fichier.write(string)

		new_fichier.close()

	def load(self,name,tileset):

		fichier=open('Saves/'+name +'.txt','r')
		data=fichier.read()
		lines=data.split(';')
		prop=lines[0].split(':')

		self.width=int(prop[0])
		self.height=int(prop[1])

		for Y in range(self.height):
			cels=lines[Y+1].split(':')
			for X in range(self.width):

				tile=tileset.create_tile(int(cels[X]))
				self.set_tile(X,Y,tile)
				libtcod.map_set_properties(self.pathdata,X,Y,tile.view,tile.path)

		fichier.close()
	def __del__(self):

		print "Map deleted"
