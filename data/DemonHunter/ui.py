import libtcodpy as libtcod
import weakref

from WongEngine import  Window, Ui, WongUtils

import Color

class Value(Ui.W_Text):

	def __init__(self,parent,width,height,value_pointer,pos=False):

		Ui.W_Text.__init__(self,parent,width,height,value_pointer(),pos=False)

	def build(self,con):

		libtcod.console_print_ex(con,0,0,libtcod.BKGND_NONE,libtcod.LEFT,str(value_pointer))
		self.width=len(str(value_pointer))
		self.height=1

	def update(self):

		pos=self.calc_pos()
		libtcod.console_print_ex(self.parent().console,pos[0],pos[1],libtcod.BKGND_NONE,libtcod.LEFT,str(value_pointer))
		self.width=len(str(value_pointer))

#class Log(Ui.Wui_elem)


class Level_Shower(Ui.Game_Shower):

	def __init__(self,parent,width,height,game,pos=False):

		Ui.Game_Shower.__init__(self,parent,width,height,game,pos)

		self.selected=True
		self.move_range=True
		self.targetable=True

		self.range=False

		#self.reachable_tiles=list()	#Not sure to store it here

		self.blink_selected=False


	def get_elem_by_mouse(self,x,y):
		'''
		 method to get an elem by mouse position
		 set the x y coordinates on the map focus
		:param x : mouse x pos relative to top left corner
		:param y : mouse y pos relative to top left corner
		:return : self (default behavior)
		'''

		self.game.get_map().set_focus_tile(x+self.game.map_pos[0],y+self.game.map_pos[1])
		return self

	def update(self):
		'''
		this version draw the map stored in the level,
		may become obsolete when Game_Shower will be updated
		'''

		#TODO LATER: optimisation

		for Y in range(min(self.height,self.game.level.map.height)):
			for X in range(min(self.width,self.game.level.map.width)):


				libtcod.console_put_char_ex(self.parent().console,X+1,Y+1,
											self.game.level.map.get_tile(X,Y).char,
											self.game.level.map.get_tile(X,Y).color,
											self.game.level.map.get_tile(X,Y).background)




		for ent in self.game.get_entity():

			libtcod.console_put_char_ex(self.parent().console,ent.x+1,ent.y+1,
										ent.char,
										ent.get_color(),
										self.game.level.map.get_tile(ent.x,ent.y).background)

		self.ui_layer()
#----------------------------------------------------------

	def blink(self):
		if self.blink_selected:
			self.toggle_selected()
#-----------control for game related view-------------------

	def ui_layer(self):

		if self.move_range:
			for tile in self.game.get_reachable_list():
				libtcod.console_set_char_background(self.parent().console,
													tile[0]+1,
													tile[1]+1,
													Color.GREEN)


		if self.game.targeting:

			for unit in self.game.get_target_list():
				libtcod.console_set_char_background(self.parent().console,
													unit.get_pos()[0]+1,
													unit.get_pos()[1]+1,
													Color.RED)
			if self.game.selected_action > 0 and self.game.target:
				libtcod.console_set_char_background(self.parent().console,
													self.game.target.get_pos()[0]+1,
													self.game.target.get_pos()[1]+1,
													Color.LRED)
				libtcod.console_set_char_foreground(self.parent().console,
													self.game.target.get_pos()[0]+1,
													self.game.target.get_pos()[1]+1,
													Color.LCYAN)

		if self.selected:
			if self.game.selected_tile:
				libtcod.console_set_char_background(self.parent().console,
													self.game.get_select_tile()[0]+1,
													self.game.get_select_tile()[1]+1,
													Color.YELLOW)
			if self.game.selected_unit:
				libtcod.console_set_char_background(self.parent().console,
													self.game.selected_unit.get_pos()[0]+1,
													self.game.selected_unit.get_pos()[1]+1,
													Color.LCYAN)


	def show_selected(self):
		self.selected=True
	def hide_selected(self):
		self.selected=False
	def toggle_selected(self):
		if self.selected:
			self.hide_selected()
		else:
			self.show_selected()

	def toggle_blink_selected(self):
		if self.blink_selected:
			self.blink_selected=False
			self.selected=True
		else:
			self.blink_selected=True



	#def set_reachable_tiles(self,liste):

	#	self.reachable_tiles=list(liste)







class Cell_Jauge(Ui.Wui_elem):

	def __init__(self,parent,maxvalue,currentvalue,color,pos=None):

		self.max=maxvalue	#a method
		self.value=currentvalue
		Ui.Wui_elem.__init__(self,parent,self.max(),1,pos)

		self.color=color


		self.full_cell=chr(4)
		self.empty_cell=chr(42)

	def get_max(self):

		return self.max()

	def get_value(self):


			return self.value()


	def get_color(self,i):

		if i < self.value():
			return self.color
		else:
			return Color.DGREY
	def get_char(self,i):

		if i < self.value():
			return self.full_cell
		else:

			return self.empty_cell

	def build(self,con):

		for i in range(self.max()):

			libtcod.console_put_char_ex(con,i,0,self.get_char(i),self.get_color(i),libtcod.black)
			self.width=self.max()

class Linked_Text(Ui.Wui_elem):

	def __init__(self,parent,width,height,textpointer,pos=False):

		Ui.Wui_elem.__init__(self,parent,width,height,pos)

		self.get_text=textpointer
		self.color=Color.WHITE
		self.bkg_color=Color.BLACK

	def build(self,con):

		libtcod.console_set_default_background(con,self.bkg_color)
		libtcod.console_set_default_foreground(con,self.color)
		libtcod.console_print_ex(con,0,0,libtcod.BKGND_SET,libtcod.LEFT,self.get_text())
		self.width=len(self.get_text())
		self.height=1

	def set_color(self,color):
		self.color=color
	def set_bkg_color(self,color):
		self.bkg_color=color


class State_Icon(Ui.Wui_elem):

	def __init__(self,parent,char,color,bcgcolor,sec_char=None,sec_color=None,sec_bcgcolor=None,pos=False):

		Ui.Wui_elem.__init__(self,parent,1,1,pos)

		self.char=char
		self.color=color
		self.bkg_color=bcgcolor

		self.on=False

		if sec_char:
			self.sec_char=sec_char
		else:
			self.sec_char=char
		if sec_color:
			self.sec_color=sec_color
		else:
			self.sec_color=color
		if sec_bcgcolor:
			self.sec_bkg_color=sec_bcgcolor
		else:
			self.sec_bkg_color=bcgcolor
	def build(self,con):

		if self.on:
			char=self.char
			col=self.color
			bkg=self.bkg_color
		else:
			char=self.sec_char
			col=self.sec_color
			bkg=self.sec_bkg_color
		libtcod.console_put_char_ex(con,0,0,char,col,bkg)

	def switch(self):

		if self.on:
			self.on=False
		else:
			self.on=True

class Line_Separator(Ui.Line_Menu):

	def __init__(self,parent,width,height,separator=':',pos=False):

		Ui.Line_Menu.__init__(self,parent,width,height,'noname',0,pos)
		self.separator=separator

	def build(self,con):

		i=0

		temp=libtcod.console_new(self.width,self.height)

		for elem in self.content:
			elem.build(temp)

			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,i,0)
			elem.set_pos(i,0)
			i+= elem.width

			libtcod.console_put_char_ex(con,i,0,self.separator,libtcod.white,libtcod.black)
			i+=1
			libtcod.console_clear(temp)

class Soft_Menu(Ui.Simple_Menu):

	def __init__(self,parent,width,height,name,pos=False):

		Ui.Simple_Menu.__init__(self,parent,width,height,name,0,pos)

	def build(self,con):

		i=0
		temp=libtcod.console_new(self.width,self.height)
		for elem in self.content:
			for c in range(self.width):
				libtcod.console_put_char_ex(con,c,i,chr(196),libtcod.white,libtcod.black)
			i+=1
			elem.build(temp)
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,1,i)
			elem.set_pos(1,i)
			libtcod.console_clear(temp)
			i+=elem.height

class Control_Menu(Ui.Simple_Menu):

	def __init__(self,parent,width,height,name,pos=False):

		Ui.Simple_Menu.__init__(self,parent,width,height,name,0,pos)
		self.selected=False
		self.elemid=None

	def build(self,con):

		i=0
		w=1
		temp=libtcod.console_new(self.width,self.height)
		for elem in self.content:

			#i+=1
			elem.build(temp)
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,w,i)
			elem.set_pos(w,i)
			libtcod.console_clear(temp)
			i+=elem.height

			libtcod.console_set_default_background(con,libtcod.black)
			libtcod.console_set_default_foreground(con,libtcod.white)


	def select_elem(self,id):

		self.content[id].hover()

	def unselect_elem(self,id):

		self.content[id].leave()

	def select(self):

		self.selected=True
		if self.elemid>=0:
			self.select_elem(self.elemid)

		else:
			self.select_elem(0)
			self.elemid=0


	def unselect(self):

		self.selected=False

	def next_elem(self):


		if self.elemid < len(self.content)-1 and self.elemid>=0:
			self.unselect_elem(self.elemid)
			self.elemid+=1
			self.select_elem(self.elemid)

	def previous_elem(self):

		if self.elemid > 0:
			self.unselect_elem(self.elemid)
			self.elemid-=1
			self.select_elem(self.elemid)

	def activate_elem(self):

		self.content[self.elemid].activate()

class Unit_Info(Ui.Ui_holder):

	def __init__(self,parent,unit,pos=False):

		Ui.Ui_holder.__init__(self)
		Ui.Wui_elem.__init__(self,parent,14,5,pos)


		self.hp_zone=Line_Separator(self,13,1)
		self.ap_zone=Line_Separator(self,13,1)

		self.link_to_unit(unit)

		#self.name_slot=Linked_Text(self,11,1,unit.get_name)
		self.add_elem(self.name_slot)

		#self.classe_slot=Linked_Text(self,11,1,unit.get_class_name)
		self.add_elem(self.classe_slot)

		#self.state_slot=Ui.W_Text(self,1,1,'still to do')
		self.add_elem(self.state_slot)



		self.hp_zone.add_elem(Ui.W_Text(self.hp_zone,2,1,'HP'))

		#self.health_bar=Cell_Jauge(self.hp_zone,unit.get_HP_max,unit.get_HP,Color.RED)
		self.hp_zone.add_elem(self.health_bar)



		self.ap_zone.add_elem(Ui.W_Text(self.ap_zone,2,1,'AP'))

		#self.action_bar=Cell_Jauge(self.ap_zone,unit.get_AP_max,unit.get_AP,Color.GREEN)
		self.ap_zone.add_elem(self.action_bar)

		self.add_elem(self.hp_zone)
		self.add_elem(self.ap_zone)


		self.selected=False

	def link_to_unit(self,unit):

		self.get_unit=weakref.ref(unit)
		self.name_slot=Linked_Text(self,11,1,unit.get_name)
		self.classe_slot=Linked_Text(self,11,1,unit.get_class_name)
		self.state_slot=Ui.W_Text(self,1,1,'still to do')
		self.health_bar=Cell_Jauge(self.hp_zone,unit.get_HP_max,unit.get_HP,Color.RED)
		self.action_bar=Cell_Jauge(self.ap_zone,unit.get_AP_max,unit.get_AP,Color.GREEN)

	def set_selected(self,elem):

		elem.set_color(Color.LBLUE)
		elem.set_bkg_color(Color.WHITE)

	def set_used(self,elem):

		elem.set_color(Color.LGREY)
		elem.set_bkg_color(Color.DBLUE)

	def set_idle(self,elem):

		elem.set_color(Color.WHITE)
		elem.set_bkg_color(Color.LBLUE)




	def build(self,con):

		if self.get_unit().is_ready():

			self.set_idle(self.name_slot)

		else:

			self.set_used(self.name_slot)

	#	if self.

		i=0
		temp=libtcod.console_new(self.width,self.height)
		print len(self.content)
		for elem in self.content:

			elem.build(temp)
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,1,i)
			elem.set_pos(1,i)
			libtcod.console_put_char_ex(con,0,i,chr(26),libtcod.white,libtcod.black)
			libtcod.console_clear(temp)
			i+=1
