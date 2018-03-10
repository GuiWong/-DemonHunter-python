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

class Linked_Button(Linked_Text,Ui.W_Button):

	def __init__(self,parent,width,height,textpointer,action,args,pos=False):

		Linked_Text.__init__(self,parent,width,height,textpointer,pos)
		Ui.W_Button.__init__(self,Color.WHITE,Color.BLACK,action,args)

class Linked_value(Ui.Wui_elem):

	def __init__(self,parent,width,height,valuepointer,pos=False):

		Ui.Wui_elem.__init__(self,parent,width,height,pos)

		self.get_text=valuepointer
		self.color=Color.WHITE
		self.bkg_color=Color.BLACK

	def build(self,con):

		libtcod.console_set_default_background(con,self.bkg_color)
		libtcod.console_set_default_foreground(con,self.color)
		libtcod.console_print_ex(con,0,0,libtcod.BKGND_SET,libtcod.LEFT,str(self.get_text()))
		self.width=len(str(self.get_text()))
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
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,0,i)
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

class Upgrade_Controll(Control_Menu):



	def __init__(self,parent,game,pos=False):

		Control_Menu.__init__(self,parent,10,40,'upgrade',pos)
		self.selected=False
		self.elemid=None
		self.selected_unit=1
		self.get_game=weakref.ref(game)

		self.nubmer_of_point=Linked_Button(self,8,1,self.get_game().get_total_wupoint,WongUtils.idle,None)
		self.add_elem(self.nubmer_of_point)

		self.unit_name=Linked_Button(self,8,1,self.get_unit().get_name,WongUtils.idle,None)
		self.add_elem(self.unit_name)

		self.hp_button=Ui.Text_Button(self,8,1,'[' + str(self.get_game().get_upgrade_cost(self.get_unit(),'HP')) + ']',Color.WHITE,Color.BLACK,self.get_game().upgrade_unit,[self.get_unit(),'HP'])
		self.add_elem(self.hp_button)
		self.ap_button=Ui.Text_Button(self,8,1,'[' + str(self.get_game().get_upgrade_cost(self.get_unit(),'AP')) + ']',Color.WHITE,Color.BLACK,self.get_game().upgrade_unit,[self.get_unit(),'AP'])
		self.add_elem(self.ap_button)


		self.validation=Ui.Text_Button(self,8,1,'Next Level',Color.WHITE,Color.BLACK,self.get_game().next_level,None)
		self.add_elem(self.validation)


	def link_to_unit(self,unit):

		pass

	def get_unit(self):

		return self.get_game().squad.get_unit(self.selected_unit)

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

			i+=1

			libtcod.console_set_default_background(con,libtcod.black)
			libtcod.console_set_default_foreground(con,libtcod.white)


class upgrade_button(Linked_Button):

	def __init__(self,parent,width,height,textpointer,action,args,pos=False):
		Linked_Button.__init__(self,parent,width,height,textpointer,action,args,pos=False)



class Skill_Line(Line_Separator):#,Ui.W_Button):

	def __init__(self,parent,width,height,unit,skill_id,separator=':',pos=False):

		Line_Separator.__init__(self,parent,width,height,separator,pos)
	#	Ui.W_button.__init__(self,Color.WHITE,Color.BLACK,action,args=None))

		self.id=skill_id
		self.link_to_unit(unit)

	def link_to_unit(self,unit):

		self.get_unit=weakref.ref(unit)
		self.num=Ui.W_Text(self,1,1,str(self.id))
		self.add_elem(self.num)
		self.skill_name=Linked_Text(self,10,1,unit.get_skill(self.id).get_name)
		self.add_elem(self.skill_name)

class Squad_Ui(Ui.Ui_holder):

	def __init__(self,parent,squad,game,pos=False):

		Ui.Ui_holder.__init__(self)
		Ui.Wui_elem.__init__(self,parent,28,28,pos)


		for i in range(1,5,1):

			ui=Unit_Ui(self,squad.get_unit(i))
			self.add_elem(ui)

	def rebuild(self,squad):

		self.content=list()

		for i in range(1,5,1):

			ui=Unit_Ui(self,squad.get_unit(i))
			self.add_elem(ui)


	def build(self,con):

		i=0
		temp=libtcod.console_new(self.width,self.height)
		#print len(self.content)
		for elem in self.content:

			elem.build(temp)
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,0,i)
			elem.set_pos(0,i)
			#libtcod.console_put_char_ex(con,0,i,chr(26),libtcod.white,libtcod.black)
			libtcod.console_clear(temp)
			i+=elem.height-1

class Unit_Ui(Ui.Ui_holder):

	def __init__(self,parent,unit,pos=False):

		Ui.Ui_holder.__init__(self)
		Ui.Wui_elem.__init__(self,parent,28,7,pos)

		self.unit_info=Unit_Info(parent,unit)
		self.skill_info=Skill_Info(parent,unit)
		if unit.get_type()=='Not':
			self.empty=True
		else:
			self.empty=False

	def build(self,con):

		libtcod.console_print_frame(con,0,0,self.width,self.height,False,libtcod.BKGND_SET)
		libtcod.console_put_char_ex(con,13,0,chr(196),libtcod.white,libtcod.black)

		if self.empty:
			pass
		else:

			temp=libtcod.console_new(self.width,self.height)

			self.unit_info.build(temp)
			libtcod.console_blit(temp,0,0,self.unit_info.width,self.unit_info.height,con,1,1)
			self.unit_info.set_pos(1,1)
			libtcod.console_clear(temp)

			self.skill_info.build(temp)
			libtcod.console_blit(temp,0,0,self.skill_info.width,self.skill_info.height,con,15,1)
			self.skill_info.set_pos(16,1)
			#libtcod.console_put_char_ex(con,0,i,chr(26),libtcod.white,libtcod.black)
			libtcod.console_clear(temp)

			libtcod.console_put_char_ex(con,14,0,chr(194),libtcod.white,libtcod.black)
			libtcod.console_put_char_ex(con,14,self.height-1,chr(193),libtcod.white,libtcod.black)
			for i in range(1,self.height-1):
				libtcod.console_put_char_ex(con,14,i,chr(179),libtcod.white,libtcod.black)

class Skill_Info(Ui.Simple_Menu):

	def __init__(self,parent,unit,pos=False):

		#Ui.Ui_holder.__init__(self)
		#Ui.Wui_elem.__init__(self,parent,10,5,pos)
		Ui.Simple_Menu.__init__(self,parent,14,5,'notname','skills')

		self.skill1=Skill_Line(self,12,1,unit,1)
		self.skill2=Skill_Line(self,12,1,unit,2)
		self.skill3=Skill_Line(self,12,1,unit,3)
		self.skill4=Skill_Line(self,12,1,unit,4)

		self.add_elem(self.skill1)
		self.add_elem(self.skill2)
		self.add_elem(self.skill3)
		self.add_elem(self.skill4)





		self.link_to_unit(unit)

	def link_to_unit(self,unit):

		self.get_unit=weakref.ref(unit)


	def build(self,con):

		#if


		i=0
		temp=libtcod.console_new(self.width,self.height)
		#print len(self.content)
		for elem in self.content:

			elem.build(temp)
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,1,i)
			elem.set_pos(1,i)
			libtcod.console_put_char_ex(con,0,i,chr(26),libtcod.white,libtcod.black)
			libtcod.console_clear(temp)
			i+=1

class Attacker_Info(Ui.Ui_holder):

	def __init__(self,parent,unit,pos=False):

		Ui.Ui_holder.__init__(self)
		Ui.Wui_elem.__init__(self,parent,10,5,pos)

	def link(self,unit,fighter):

		self.unit_name=Linked_Text(self,10,1,unit.get_name)
		self.hp_damage=Linked_Value(self,2,1,fighter.get_attacker_damage)
		self.ap_damage=Linked_Value(self,2,1,fighter.get_cost)

	def build(self,con):

		temp=libtcod.console_new(self.width,self.height)

		self.unit_name.build(temp)
		libtcod.console_blit(temp,0,0,self.unit_name.width,self.unit_name.height,con,0,0)
		self.unit_name.set_pos(0,0)
		libtcod.console_clear(temp)

		self.hp_damage.build(temp)
		libtcod.console_blit(temp,0,0,self.hp_damage.width,self.hp_damage.height,con,8,1)
		self.hp_damage.set_pos(8,1)
		libtcod.console_clear(temp)

		self.ap_damage.build(temp)
		libtcod.console_blit(temp,0,0,self.ap_damage.width,self.ap_damage.height,con,8,2)
		self.ap_damage.set_pos(8,1)
		libtcod.console_clear(temp)


class Combat_Info(Ui.Ui_holder):

	def __init__(self,parent,unit,pos=False):

		Ui.Ui_holder.__init__(self)
		Ui.Wui_elem.__init__(self,parent,28,7,pos)

class Log_Entry(Ui.Wui_elem):

	def __init__(self,parent,width,height,type,text,pos=False):

		Ui.Wui_elem.__init__(self,parent,width,height,pos)

		self.entry = '['+type+']'+' - '+text

		self.type=type

		if type=='COMBAT':
			self.color=Color.RED
			self.bkg_color=libtcod.Color(0,128,128)

		elif type=='TEAM':
			self.color=Color.GREEN
			self.bkg_color=Color.BLACK

		else:
			self.color=Color.WHITE
			self.bkg_color=Color.BLACK

	def build(self,con):

		libtcod.console_set_default_background(con,self.bkg_color)
		libtcod.console_set_default_foreground(con,self.color)
		libtcod.console_print_rect_ex(con, 0, 0, self.width, 0, libtcod.BKGND_NONE, libtcod.LEFT, self.entry)
		self.height=libtcod.console_get_height_rect(con, 0, 0, self.width, 0, self.entry)

class Log(Ui.Ui_holder):

	def __init__(self,parent,width,height,pos=False):

		Ui.Ui_holder.__init__(self)
		Ui.Wui_elem.__init__(self,parent,width,height,pos)

	def print_entry(self,type,text):

		self.content.insert(0,Log_Entry(self,self.width,1,type,text))

	def build(self,con):

		i=self.height-1
		temp=libtcod.console_new(self.width,self.height)
		#print len(self.content)
		for elem in self.content:

			elem.build(temp)
			h=i+1-elem.height
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,1,h)
			elem.set_pos(1,h)
			libtcod.console_put_char_ex(con,0,h,chr(26),libtcod.white,libtcod.black)
			libtcod.console_clear(temp)
			i=h-1

			if h<=0:
				break


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


class Character_File(Ui.Ui_holder):

	def __init__(self,parent,unit,pos=False):
		Ui.Ui_holder.__init__(self)
		Ui.Wui_elem.__init__(self,parent,14,15,pos)

		self.link_to_unit(unit)

	def link_to_unit(self,unit):


		self.get_unit=weakref.ref(unit)
		self.name_slot=Linked_Text(self,11,1,unit.get_name)
		self.classe_slot=Linked_Text(self,11,1,unit.get_class_name)
		self.health_bar=Cell_Jauge(self,unit.get_HP_max,unit.get_HP,Color.RED)
		self.action_bar=Cell_Jauge(self,unit.get_AP_max,unit.get_AP,Color.GREEN)

		self.skill1=Skill_Line(self,12,1,unit,1)
		self.skill2=Skill_Line(self,12,1,unit,2)
		self.skill3=Skill_Line(self,12,1,unit,3)
		self.skill4=Skill_Line(self,12,1,unit,4)


		self.add_elem(self.classe_slot)
		self.add_elem(self.name_slot)
		self.add_elem(self.health_bar)
		self.add_elem(self.action_bar)

		self.add_elem(self.skill1)
		self.add_elem(self.skill2)
		self.add_elem(self.skill3)
		self.add_elem(self.skill4)


	def build(self,con):


		i=0
		temp=libtcod.console_new(self.width,self.height)
		print len(self.content)
		for elem in self.content:

			elem.build(temp)
			libtcod.console_blit(temp,0,0,elem.width,elem.height,con,1,i)
			elem.set_pos(1,i)
			libtcod.console_put_char_ex(con,0,i,chr(26),libtcod.white,libtcod.black)
			libtcod.console_clear(temp)
			i+=2

class Name_Entry(Ui.W_Text):

	def __init__(self,parent,pos=False):


		self.text=''
		Ui.W_Text.__init__(self,parent,10,1,'',pos)

		self.text=''

	def get_text(self):

		return self.text

	def add_letter(self,char):

		self.text+=char

	def del_letter(self):

		self.text=self.text[:len(self.text)-1]




	def select_elem(self,id):

		pass

	def unselect_elem(self,id):

		pass

	def select(self):

		self.selected=True


	def unselect(self):

		self.selected=False

	def next_elem(self):


		pass

	def previous_elem(self):

		pass

	def activate_elem(self):

		print 'yeah!'
