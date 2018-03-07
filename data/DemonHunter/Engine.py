import libtcodpy as libtcod
import os
from WongEngine import Wong, Window, Ui, Map, WongUtils
import ui
import Units
import Classes
import Level
import Color
import Input
import Ennemy
import Combat



class Demon_Hunter_Game(Wong.Wong_Game):

	def __init__(self):

		Wong.Wong_Game.__init__(self)

		#--------------------------------------
		self.level=None
		self.squad=None
		self.opponents=None

		self.selected_window=None



	#Ovveride from Wong_Game, to change game_shower to level_shower
	def set_game_window(self,window):

		self.game_screen=ui.Level_Shower(window,window.width-2,
										window.height-2,self)
		window.add_elem(self.game_screen)

	def initialize_game(self):

		self.game_w=self.window.create_window(49,42,0,0,"Map")
		self.menu_w=self.window.create_window(30,50,49,0,"Menu")

		#self.charamenu=self.ui.create_menu('simple',self.menu_w,28,10,'character')
		self.charamenu=ui.Soft_Menu(self.menu_w,28,48,'Menus')
		self.menu_w.add_elem(self.charamenu)



		self.selected_unit=None
		self.selected_tile=None	#not the same as focusTile

		self.selected_action= 0 #the id of the corrent selected action

		self.target=None
		self.potential_target=list()
		self.targeting=False

		self.reachable_tiles=list()

		self.in_move=False
		self.begin_pos=None



		self.init_ai()
		self.fight=Combat.Combat_Manager()


		self.other_unit=list()



		self.window.build()

	def create_squad(self):

		self.squad=Units.Squad(4)
		self.squad.add_unit(self.create_unit('Alice',Classes.Warrior()))
		self.squad.add_unit(self.create_unit('Bob',Classes.Sage()))
		self.squad.add_unit(self.create_unit('Cedric',Classes.Assasin()))
		self.squad.add_unit(self.create_unit('David',Classes.Archer()))

	def debug_start(self):


		#self.jauge=self.ui.create_cell_jauge(self.charamenu,self.get_A,self.get_B,libtcod.red)

		#self.test_icon=ui.State_Icon(self.charamenu,chr(35),Color.GREEN,Color.RED,chr(79),Color.LCYAN,Color.GREEN)
		#self.charamenu.add_elem(self.test_icon)



		#self.test_icon.switch()




		tileset=Map.Tileset(16)

		print os.path.abspath('..')
		#print os.path.dirname()
		tileset.load('data/Ressources/tileset1.cfg')

		tileset.set_empty(1)

		self.level=Level.Level()
		self.level.set_tileset(tileset)

		self.level.map=Level.create_test_map(tileset)

		self.path_map=None

		self.set_game_window(self.game_w)

		self.create_squad()
		self.squad.get_unit(1).set_pos(16,15)
		self.squad.get_unit(2).set_pos(18,15)
		self.squad.get_unit(3).set_pos(16,14)
		self.squad.get_unit(4).set_pos(17,14)


		for u in self.squad.get_units():
			self.heal_HP(u,10)
			self.heal_AP(u,10)


		libtcod.console_set_color_control(libtcod.COLCTRL_1,Color.RED,Color.BLACK)
		libtcod.console_set_color_control(libtcod.COLCTRL_2,Color.LBLUE,Color.BLACK)
		libtcod.console_set_color_control(libtcod.COLCTRL_2,Color.DBLUE,Color.BLACK)


		self.chara1_menu=ui.Unit_Info(self.charamenu,self.squad.get_unit(1))
		self.charamenu.add_elem(self.chara1_menu)

		self.chara2_menu=ui.Unit_Info(self.charamenu,self.squad.get_unit(2))
		self.charamenu.add_elem(self.chara2_menu)

		self.chara3_menu=ui.Unit_Info(self.charamenu,self.squad.get_unit(3))
		self.charamenu.add_elem(self.chara3_menu)

		self.chara4_menu=ui.Unit_Info(self.charamenu,self.squad.get_unit(4))
		self.charamenu.add_elem(self.chara4_menu)



		self.level.add_monster(self.create_monster(Classes.Demonito()))
		self.level.add_monster(self.create_monster(Classes.Runner()))
		self.level.monsters.get_unit(1).set_pos(20,16)
		self.level.monsters.get_unit(2).set_pos(21,15)



		self.set_state(1)

		self.initialize_path_map()
		self.path_place_unit()






		self.selected_window=None

		self.window.build()




	#	print self.squad.

#--------------Main Methods------------------------------------------------


	def input(self):

		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,self.key,self.mouse)

			# SYSTEM INPUT -------------------------------------------------

		if self.key == Input.F11:#libtcod.KEY_ENTER and self.key.lalt:
	        #Alt+Enter: toggle fullscreen
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
		elif self.key == Input.F4:

			self.game_screen.toggle_blink_selected()

		elif self.key == Input.ALT_ESCAPE:
			self.state=0
			return

		elif self.key.vk == libtcod.KEY_SPACE:
			self.test_ai()
			print 'ai tested'

		elif self.key==Input.F12:

			print 'screenshot saved'
			libtcod.sys_save_screenshot('Ressources/screen.png')

	#MOUSE INPUT-------------------------------------------------------
		if self.mouse.rbutton_pressed:

			print self.window.get_elem_by_mouse()

		if self.mouse.lbutton_pressed:

			elem=self.window.get_elem_by_mouse()
			self.activate(elem)
	#Menu INPUT-----------------------------------------------------
		if self.selected_window:

			if self.key==Input.UP:
				print 'up!'
				self.selected_window.content.previous_elem()
				self.update_menu(self.selected_window)
			if self.key==Input.DOWN:
				print 'up!'
				self.selected_window.content.next_elem()
				self.update_menu(self.selected_window)
			elif self.key==Input.ESCAPE:
				print 'escape'
				#self.open_pause_menu()
			elif self.key==Input.ENTER:
				self.selected_window.content.activate_elem()





		#if self.key.vk==libtcod.KEY_CHAR:
		#	print self.key.c

	#Game INPUT----------------------------------------------------------

		elif not self.selected_window and self.state==1:

			if self.key==Input.ESCAPE:

				#self.open_pause_menu()
				#self.selected_unit=None	#temporary

				if self.selected_unit:


					if self.target:
						self.select_target(None)

					elif self.is_targeting() and len(self.get_target_list())>0:
						self.set_targeting(False)
						self.select_action(0)
						print 'stopped targeting'
					#	return		#Bad
					elif self.in_move:
						self.cancel_move()
						print 'move cancelled'
					#	return		#Bad
					else:
						self.select_unit(None)



			elif self.key==Input.ENTER:


				#if self.in_move and self.selected_action==0 and self.selected_tile==self.selected_unit.get_pos():

					#self.solve_move()
				#self.select()
					# solve_action
				if self.selected_unit and self.target:

					self.solve_action(self.selected_unit,self.selected_action,self.target)

				elif self.selected_tile:
					self.select()

					if self.selected_unit and self.target:

						self.solve_action(self.selected_unit,self.selected_action,self.target)

				else:
					print 'empty enter'



				if self.selected_unit:
					print 'what to do now'
				else:
					print "this enter input should'tbe"


			elif self.key==Input.TAB:

				if self.selected_unit and not self.target:
					if len(self.get_target_list())>0: #self.targeting:
						#print self.get_target_list()
						self.target=self.get_target_list()[0]
					else:
						self.next_unit()

				elif self.selected_unit and self.target:
					self.next_target()

				else:
					self.next_unit()




			elif self.key==Input.NUMBER:

				a=Input.NUMBER.get_value(self.key)
				print 'number input receveid: ', a

				if self.selected_unit:
					self.select_action(a)

				else:
					self.select_unit(self.squad.get_unit(a))

			elif self.key==Input.UP and not self.targeting:

				if self.selected_tile:

					self.set_selected_tile(self.selected_tile[0],self.selected_tile[1]-1)

			elif self.key==Input.DOWN and not self.targeting:

				if self.selected_tile:

					self.set_selected_tile(self.selected_tile[0],self.selected_tile[1]+1)

			elif self.key==Input.LEFT and not self.targeting:

				if self.selected_tile:

					self.set_selected_tile(self.selected_tile[0]-1,self.selected_tile[1])

			elif self.key==Input.RIGHT :

				if self.selected_tile and not self.targeting:

					self.set_selected_tile(self.selected_tile[0]+1,self.selected_tile[1])

				elif self.targeting:

					self.next_target()





	def activate(self,obj):

		if WongUtils.check_class(obj,'W_Button'):
			obj.activate()

		elif WongUtils.check_class(obj,'Game_Shower'):# or WongUtils.check_class(obj,'Level_Shower'):

			x,y= self.level.map.focusTile
			self.set_selected_tile(x,y)
			self.select()

			#if self.selected_unit:
				#TODO check if tile is reacheable
				#self.set_selected_tile(x,y)
				#self.solve_action(self.selected_unit,self.selected_action,self.selected_tile)

#COPY PASTE IS BAD, I KNOW. TODO: SOLVE THAT
			if self.selected_unit and self.target:

				self.solve_action(self.selected_unit,self.selected_action,self.target)

			elif self.selected_unit:
				print 'what to do now'



				#t=self.level.map.get_tile(x,y)

				#temporary, will have to handle others ent. types







		elif WongUtils.check_class(obj,'Wui_elem'):
			print obj.__class__.__name__

	def render(self):

		self.window.render()



	def run(self):

		while self.state!=0:

			if self.state==1:
				self.render()
				self.input()
				self.turn_iterate()
			if self.state==2:
				self.render()
				self.input()

	def turn_iterate(self):

		self.turner+=1

		if self.turner%10 ==0 and self.game_screen and self.state==1:
			self.game_screen.update()
		if self.turner%50==0:
			self.game_screen.blink()
		if self.turner==1000:
			self.turner=0

	#Bigger Scope Methods-------------------------------------------------------------


	def main_menu(self):
		'''
		handle the main menu
		'''
		main_menu_w=self.window.create_window(20,20,30,20,'Demon Hunter')


		menu=ui.Control_Menu(main_menu_w,18,18,'Main menu')
		main_menu_w.add_elem(menu)

		button1=Ui.Text_Button(menu,15,1,'New Game',Color.WHITE,Color.BLACK,self.new_game,None)
		menu.add_elem(button1)


		button3=Ui.Text_Button(menu,15,1,'controls',Color.WHITE,Color.BLACK,WongUtils.idle,None)
		menu.add_elem(button3)

		button4=Ui.Text_Button(menu,15,1,'options',Color.WHITE,Color.BLACK,WongUtils.idle,None)
		menu.add_elem(button4)

		button2=Ui.Text_Button(menu,15,1,'quit',Color.WHITE,Color.BLACK,self.set_state,[0])
		menu.add_elem(button2)

		self.select_window(main_menu_w)

		self.state=2
		self.window.build()

	def new_game(self):

		wind=self.window.get_window_by_id('Demon Hunter')
		if wind:
			self.window.close_window(wind)

		self.initialize_game()

		#TODO
		self.debug_start()

#	def build


	#Combat Methods--------------------------------

	def get_fight_issue(self):

		assert self.target

		self.fight.calc_issue(self.selected_unit,self.selected_action,self.target)

	def kill_unit(self,unit):

		corp=Units.Corpse()
		corp.build_from_unit(unit)
		self.other_unit.append(corp)

		if unit.player:

			self.squad.remove_unit(unit)

		else:

			self.level.monsters.remove_unit(unit)

	#Base_Monster_Methodes--------------------------

	def init_ai(self):

		self.ia=Ennemy.Leader_Ai(self)

	def test_ai(self):

		unit=self.level.get_monsters()[1]
		self.ia.get_all_targets(unit)
		print '-----------------------------'
		self.ia.choose_target(unit)


	#-----getters-------------------------------

	def get_entity(self):

		result=list()

		for ent in self.squad.get_entities():

			result.append(ent)

		for ent in self.level.get_entities():

			result.append(ent)

		for u in self.other_unit:

			result.append(u.get_entity())

		return result

	def get_all_unit(self):

		result=list()
		for u in self.squad.get_units():
			result.append(u)
		for u in self.level.get_monsters():
			result.append(u)

		for u in self.other_unit:
			result.append(u)


		return result

	def get_map(self):

		return self.level.map

	def get_select_tile(self):

		return self.selected_tile

	def get_select_unit(self):

		return self.selected_unit


	def get_tile_occupant(self,x,y):

			#for ent in self.get_entity():
				#if ent.x==x and ent.y==y:
				#	return ent

			for unit in self.get_all_unit():
				if unit.get_entity().x==x and unit.get_entity().y==y:
					return unit

			return None

	def set_reachable_tiles(self,liste):

		self.reachable_tiles=liste

	def get_reachable_list(self):

		return self.reachable_tiles

	def set_potential_target(self,liste):

		self.potential_target=liste

	def get_target_list(self):
		return self.potential_target

	def is_targeting(self):
		return self.targeting
	def set_targeting(self,mode=True):
		self.targeting=mode
#----------Utility Methods----------------------------------------



	def create_unit(self,name,classe):

		unit=Units.Unit()
		unit.set_class(classe)
		unit.set_name(name)
		unit.build_from_class()
		return unit

	def create_monster(self,classe):

		unit=Units.Unit(False)
		unit.set_class(classe)
		unit.set_name(classe.name)
		unit.build_from_class()
		return unit

	def select_unit(self,unit):

		if self.in_move:
			self.cancel_move()

		self.selected_unit=unit

		#
	#	self.select_action(0)
		self.select_target(None)
		self.set_potential_target(list())
		self.set_targeting(False)

		#temporary:
		if unit:
			self.get_reachable_tile(unit,True)
			self.select_action(0)
		else:
			self.set_reachable_tiles(list())


	def set_selected_tile(self,x,y):

		self.selected_tile=[x,y]

	def select_window(self,window):

		self.selected_window=window
		window.content.select()

	def select_action(self,id):

		self.selected_action=id
		if self.selected_unit.get_skill(id).type=='enemy':
			self.set_targeting()
		elif self.selected_unit.get_skill(id).type=='use':
			self.set_targeting(False)

	def select_target(self,target):


		self.target=target
		if target and type(target).__name__ != 'list':
			self.get_fight_issue()

	def is_targetable(self,target,player=True):

		#TODO: use action to know targettable propriety
		if player:											#temporary, will have to more checks
			if self.in_move and self.selected_unit==target: #and not self.targeting:
				return True

			if not target.player and self.selected_action >0:

				print 'this is a monster'
				return True
		else:

			if target.player:
				return True





		return False

	def is_selectable(self,unit):
		print 'checking selectability of ',unit.get_name()
		for elem in self.squad.get_units():
			print elem
			if unit==elem and unit.is_ready():
				print 'it can!'
				return True
			else:
				pass
		return False

	def can_reach(self):


		return self.selected_unit.get_AP() >= self.get_move_cost(self.selected_unit.get_pos(),self.selected_tile)

		#radius = self.selected_unit.get_AP()
		#pa= self.selected_unit.get_pos()
		#pb=self.selected_tile
		#dist=abs(pa[0]-pb[0])+abs(pa[1]-pb[1])
		#if dist <= radius:
		#	return True
		#else:
		#	return False

	def get_move_cost(self,pos1,pos2):

		path=libtcod.path_new_using_map(self.path_map,0)
		libtcod.path_compute(path,pos1[0],pos1[1],pos2[0],pos2[1])
		return libtcod.path_size(path)


	def select(self):

		assert self.selected_tile
		x,y = self.selected_tile
		unit=self.get_tile_occupant(x,y)
		if unit:
			if self.is_targetable(unit):
				self.select_target(unit)
			elif self.is_selectable(unit):
				self.select_unit(unit)
		else:
			if self.selected_unit and self.can_reach() and self.selected_action==0:
				self.select_target(self.selected_tile)



	def open_pause_menu(self):

		if self.state != 2:

			pausemenu=self.window.create_window(30,30,10,10,"Pause")
			self.select_window(pausemenu)
			self.set_state(2)
			self.window.build()

		else:

			self.set_state(1)
			print 'pause ended'
			self.window.close_window_by_id("Pause")
			self.select_window(None)
			self.window.build()

	def update_menu(self,windowsup=None):

		#self.
			#temporary

		if windowsup:
			windowsup.build()
		else:
			self.menu_w.build()

	def debug(self):

		self.test_icon.switch()
		self.menu_w.build()


	def next_unit(self):

		if self.selected_unit:
			#self.select_unit(WongUtils.get_next(self.squad.get_units(),self.selected_unit))

			a=WongUtils.get_next(self.squad.get_units(),self.selected_unit)
		else:
			a=self.squad.get_unit(1)

		t=0
		while not a.is_ready():
			a=WongUtils.get_next(self.squad.get_units(),a)
			t+=1
			if t>5:
				self.select_unit(None)
				return
		self.select_unit(a)



	def next_target(self):


		if not len(self.potential_target)>=1:
			return

		if self.target:
			self.select_target(WongUtils.get_next(self.potential_target,self.target))
		else:
			self.select_target(self.get_target_list()[0])

	def heal_HP(self,unit,value):

		unit.change_HP(value)

		if unit.get_HP()<=0:

			print 'a unit is dead'
			self.kill_unit(unit)

	def heal_AP(self,unit,value):

		unit.change_AP(value)


	def get_reachable_tile(self,unit,send=False):

		X,Y= unit.get_pos()
		radius=unit.get_AP()
		result=list()

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

				tile=[X-b+x,Y-radius+y]
				if (self.get_move_cost([X,Y],tile) <= radius and
						libtcod.map_is_walkable(self.path_map,tile[0],tile[1])):

					result.append(tile)

		if send:
			self.set_reachable_tiles(result)
		return result




	def get_potential_target(self,send=False):

		assert self.selected_action>0

		pot=list()
		reachable=self.selected_unit.get_skill(self.selected_action).target.get_potential_target(self.selected_unit.get_pos()[0],self.selected_unit.get_pos()[1])
		print reachable
		for coord in reachable:
			unit=self.get_tile_occupant(coord[0],coord[1])
			if unit:
				print unit
				if self.is_targetable(unit):
					pot.append(unit)



		print pot
		if send:
			self.set_potential_target(pot)

		if len(pot)>=1:
			return pot
		else:
			return None

	def get_all_potential_target(self,unit,x,y):

		atks=len(unit.skills)

		pot=list()
		pot.append('thingy')

		num_target=0

		for a in range(1,atks):

			pot.append(list())
			reachable=unit.get_skill(a).target.get_potential_target(x,y)

			for coord in reachable:
				target=self.get_tile_occupant(coord[0],coord[1])
				if target:
					if self.is_targetable(target,False):
						pot[a].append(target)
						num_target+=1

		pot[0]=num_target
		return pot





	def initialize_path_map(self):

		assert self.level

		self.path_map=self.level.map.pathdata

	def path_place_unit(self):

		assert self.path_map
		for unit in self.get_all_unit():

			libtcod.map_set_properties(self.path_map,unit.get_pos()[0],unit.get_pos()[1],True,False)

	def update_path_map(self,beginpos,unit):

		libtcod.map_set_properties(self.path_map,beginpos[0],beginpos[1],True,True)

		libtcod.map_set_properties(self.path_map,unit.get_pos()[0],unit.get_pos()[1],True,False)


	def solve_action(self,unit,id,target):

		if id==0:
			self.solve_move(unit,target)
		elif self.in_move and unit == target:
			self.solve_move(unit,target)

		else:
			#print unit.get_name(),',the ',unit.get_class_name()
			#print 'attacked the ',target.get_class_name(), ' Ennemy'
			self.solve_fight(unit,id,target)

			self.end_unit_turn()

	def solve_fight(self,unit,id,target):

		self.fight.calc_issue(unit,id,target)#not necessary
		self.heal_HP(target,-1*self.fight.get_damage())
		self.heal_AP(unit,-1*self.fight.get_cost())





	def cancel_move(self):

		assert self.in_move
		self.selected_unit.set_pos(self.begin_pos[0],self.begin_pos[1])
		self.in_move=False
		self.select_unit(self.selected_unit)


	def solve_move(self,unit,target):

		#unit.get_entity().set_pos(target[0],target[1])
		if self.in_move:
			dist=self.get_move_cost(self.begin_pos,unit.get_pos())
			#dist=WongUtils.tile_distance(unit.get_pos(),self.begin_pos)
			self.heal_AP(unit,dist*(-1))
			self.in_move=False

			if target != 'pass':
				self.end_unit_turn()
			#self.select_unit(None)

			self.update_path_map(self.begin_pos,unit)
			#self.set_targeting(False)
			self.update_menu()
		else:
			self.begin_pos=list(unit.get_pos())
			print self.begin_pos
			unit.set_pos(target[0],target[1])
			print unit.get_pos()
			self.in_move=True

			self.select_action(1)
			self.get_potential_target(True)
			self.select_target(None)
			self.set_targeting()

			self.set_reachable_tiles(list())
			#self.set_potential_target()


	def end_unit_turn(self):

		self.selected_unit.end_turn()
		self.selected_unit.get_entity().set_color(Color.DBLUE)

		if self.in_move:

			self.solve_move(self.selected_unit,'pass')

		self.set_targeting(False)
		self.select_target(None)
		self.next_unit()
