
import sys
import os
import libtcodpy as libtcod
import weakref

import DemonHunter as DH

class Wui_elem:

	def __init__(self,parent,width,height,pos=False):

		self.parent = weakref.ref(parent)
		self.width=width
		self.height=height
		self.pos=pos

		self.clickable=False

	def set_pos(self,x,y):
		'''called by parent when chainBuilduig
		set the relative position to parent
		'''
		self.pos=[x,y]

	def is_in(self,x,y):
		'''Return true if the x,y tile is in the elem
		note: elem store its x,y relative to parent
		'''

		if not self.pos:
			return False
		else:
			return(self.pos[0] <= x and
					self.pos[0] + self.width > x and
					self.pos[1] <= y and
					self.pos[1] +self.height > y)

	def get_elem_by_mouse(self,x,y):
		'''
		parent method to get an elem by mouse position
		:param x : mouse x pos relative to uiHolder
		:param y : mouse y pos relative to uiHolder
		:return : self (default behavior)
		'''
		return self

	#Added during 7DRL, chaining to window to get position

	def calc_pos(self,x=0,y=0):

		x+=self.pos[0]
		y+=self.pos[1]
		return self.parent().calc_pos(x,y)

	def get_window(self):

		return self.parent().get_window()




	def __del__(self):

		print "Wui object deleted"


		#TODO wrapping,colors, etc...


class Game_Shower(Wui_elem):

		#TODO: more multi-usage, by get_map in Game

	def __init__(self,parent,width,height,game,pos=False):

		Wui_elem.__init__(self,parent,width,height,pos)
		self.game=game

	def build(self,con):
		#TODO handle map bigger than window

		for Y in range(self.game.current_map.height):
			for X in range(self.game.current_map.width):
				libtcod.console_put_char_ex(con,X,Y,
											self.game.current_map.get_tile(X,Y).char,
											self.game.current_map.get_tile(X,Y).color,
											self.game.current_map.get_tile(X,Y).background)


	def update(self):

		for Y in range(min(self.game.current_map.height-self.game.map_pos[1],self.height)):
			for X in range(min(self.game.current_map.width-self.game.map_pos[0],self.width)):
				x=X+self.game.map_pos[0]
				y=Y+self.game.map_pos[1]
				libtcod.console_put_char_ex(self.parent().console,X+1,Y+1,
											self.game.current_map.get_tile(x,y).char,
											self.game.current_map.get_tile(x,y).color,
											self.game.current_map.get_tile(x,y).background)

		for ent in self.game.active_entities:
			if self.game.game_is_on_screen(ent.x,ent.y):

				libtcod.console_put_char_ex(self.parent().console,ent.x-self.game.map_pos[0],ent.y-self.game.map_pos[1],
											ent.char,
											ent.get_color(),
											ent.get_bcg_color())

	def get_elem_by_mouse(self,x,y):
		'''
		 method to get an elem by mouse position
		 set the x y coordinates on the map focus
		:param x : mouse x pos relative to top left corner
		:param y : mouse y pos relative to top left corner
		:return : self (default behavior)
		'''

		self.game.current_map.set_focus_tile(x+self.game.map_pos[0],y+self.game.map_pos[1])
		return self

class W_Text(Wui_elem):

	def __init__(self,parent,width,height,text,pos=False):

		Wui_elem.__init__(self,parent,width,height,pos)

		self.text=text

	def build(self,con):

		print 'and build here too'
		#libtcod.console_set_default_foreground(con,libtcod.blue)
		#libtcod.console_set_default_background(con,libtcod.red)
		libtcod.console_print_ex(con,0,0,libtcod.BKGND_NONE,libtcod.LEFT,self.text)
		self.width=len(self.text)
		self.height=1

		return 1

class W_Icon(Wui_elem):

	def __init__(self,parent,char,color,bcg_color,pos=False):

		Wui_elem.__init__(self,parent,1,1,pos)

		self.char=char
		self.color=color
		self.bcg_color=bcg_color


	def build(self,con):

		libtcod.console_put_char_ex(con,0,0,self.char,self.color,self.bcg_color)
		return 1

class W_Button():
	'''
	Parent(abstract) class for all buttons
	'''

	def __init__(self,color,bcg_color,action,args=None):

		self.selected=False
		self.clicked=False

		self.clickable=True

		self.action=action
		self.args=args

		self.base_color=color
		self.base_bcg_color=bcg_color

		self.hover_color=libtcod.Color(255,255,200)
		self.hover_bcg_color=libtcod.Color(0,0,128)

		self.clicked_color=libtcod.Color(0,0,255)
		self.clicked_bcg_color=libtcod.Color(255,255,0)

	def hover(self):

		pass

	def click(self):

		pass

	def leave(self):

		pass

	def activate(self):

		self.action(*self.args)


class Icon_Button(W_Icon,W_Button):

	def __init__(self,parent,char,color,bcg_color,action,args=None,pos=False):

		W_Icon.__init__(self,parent,char,color,bcg_color,pos)
		W_Button.__init__(self,color,bcg_color,action,args)

	def hover(self):

		self.color=self.hover_color
		self.bcg_color=self.hover_bcg_color



class Ui_holder(Wui_elem):

	def __init__(self):

		self.content=list()

	def add_elem(self,elem):

		self.content.append(elem)


	def get_elem_by_mouse(self,x,y):
		'''
		parent method to get an elem by mouse position
		:param x : mouse x pos relative to uiHolder
		:param y : mouse y pos relative to uiHolder
		'''
		potential_elements=list()
		for elem in self.content:
			if elem.is_in(x,y):
				potential_elements.append(elem)

		#print len(potential_elements)
		if len(potential_elements)==1:
			candidate=potential_elements[0]
		elif len(potential_elements)==0:
			return self
		else:
			candidate=potential_elements[len(potential_elements)-1]

		result=candidate.get_elem_by_mouse(x-candidate.pos[0],y-candidate.pos[1])

		return result
	def __del__(self):

		print "ui holder object deleted"






class Simple_Menu(Ui_holder):

	def __init__(self,parent,width,height,name,id,pos=False):

		Ui_holder.__init__(self)
		Wui_elem.__init__(self,parent,width,height,pos)

		self.name=name
		self.id=id



	def build(self,con):

		#build the menu itself

		libtcod.console_print_ex(con,self.width/2,0,libtcod.BKGND_NONE,libtcod.CENTER,self.name)




		i=1

		temp=libtcod.console_new(self.width,self.height)


		for elem in self.content:

			print elem
			print "built"
			dh=elem.build(temp)
			dh=elem.height				#updated from dh
			libtcod.console_blit(temp,0,0,elem.width,dh,con,1,i)
			elem.set_pos(1,i)
			print 'elem placed at', elem.pos

			libtcod.console_clear(temp)
			libtcod.console_put_char_ex(con,0,i,chr(26),libtcod.white,libtcod.black)
		#	libtcod.console_set_char_background(con, 0, i, libtcod.blue)
			i+=dh

#---------------7Drl----------------------------------
		if self.height<i+1:	#Bricolage, to change later on
			self.height=i+1


class Line_Menu(Simple_Menu):

	def __init__(self,parent,width,height,name,id,pos=False):

		Simple_Menu.__init__(self,parent,width,height,name,id,pos)

	def build(self,con):

		i=0

		temp=libtcod.console_new(self.width,self.height)

		for elem in self.content:
			elem.build(temp)

			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,i,0)
			elem.set_pos(i,0)
			i+= elem.width

			libtcod.console_put_char_ex(con,i,0,chr(186),libtcod.white,libtcod.black)
			i+=1
			libtcod.console_clear(temp)



#Main Class, used for all ui manipulations, and constant keeping
class Ui:
	"""
	Main class of the Ui module
	used as interface to Create ui component

	"""

	def __init__(self,palette):
		"""

		"""

		self.color=palette

	def create_menu(self,type,window,width,height,name,pos=False):



		if type=='simple':			#TODO: change and automate this
			menu=Simple_Menu(window,width,height,name,42,pos)

		elif type=='line':
			menu = Line_Menu(window,width,height,name,42,pos)

		window.add_elem(menu)
		return menu

	def create_text(self,menu,text,pos=False):

		tex=W_Text(menu,1,1,text,pos)
		menu.add_elem(tex)
		return tex

	def create_icon(self,menu,char,color,bcg_color,pos=False):

		icon=W_Icon(menu,char,color,bcg_color,pos)
		menu.add_elem(icon)
		return icon

	def create_button(self,menu,text,color,bcg_color,action,args,pos=False):

		button=Icon_Button(menu,text,color,bcg_color,action,args,pos)
		menu.add_elem(button)
		return button

	#Methods added for 7DRL project: DemonHunter

	def create_cell_jauge(self,menu,max_pointer,val_pointer,color,pos=None):

		jauge=DH.ui.Cell_Jauge(menu,max_pointer,val_pointer,color,pos)
		menu.add_elem(jauge)
		return jauge
