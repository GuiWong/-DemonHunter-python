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

import SoundManager



class Demon_Hunter_Game(Wong.Wong_Game):

	def __init__(self):

		Wong.Wong_Game.__init__(self)

		#--------------------------------------
		self.level=None
		self.squad=None
		self.opponents=None

		self.selected_window=None

		self.sound_manager=SoundManager.Sound_Manager()

		self.loading()

	def loading(self):

		self.sound_manager.load()
		self.tileset=Map.Tileset(16)


		self.tileset.load('data/Ressources/tileset1.cfg')

		self.tileset.set_empty(3)
	#Ovveride from Wong_Game, to change game_shower to level_shower
	def set_game_window(self,window):

		self.game_screen=ui.Level_Shower(window,window.width-2,
										window.height-2,self)
		window.add_elem(self.game_screen)

	def initialize_game(self):

		#self.game_w=self.window.create_window(49,42,0,0,"Map")
		#self.menu_w=self.window.create_window(30,50,49,0,"Menu")

		#self.charamenu=self.ui.create_menu('simple',self.menu_w,28,10,'character')
		#self.charamenu=ui.Soft_Menu(self.menu_w,28,48,'Menus')
		#self.menu_w.add_elem(self.charamenu)



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

		self.path_map=None


		self.WUPOINT=60


		self.window.build()

	def create_squad(self):

		self.squad=Units.Squad(4)
		#self.squad.add_unit(self.create_unit('Alice',Classes.Warrior()))
		#self.squad.add_unit(self.create_unit('Bob',Classes.Sage()))
	#	self.squad.add_unit(self.create_unit('Cedric',Classes.Assasin()))
		#self.squad.add_unit(self.create_unit('David',Classes.Archer()))

	def debug_start(self):


		#self.jauge=self.ui.create_cell_jauge(self.charamenu,self.get_A,self.get_B,libtcod.red)

		#self.test_icon=ui.State_Icon(self.charamenu,chr(35),Color.GREEN,Color.RED,chr(79),Color.LCYAN,Color.GREEN)
		#self.charamenu.add_elem(self.test_icon)



		#self.test_icon.switch()


		#print os.path.abspath('..')
		#print os.path.dirname()



		#tileset=Map.Tileset(16)


		#tileset.load('data/Ressources/tileset1.cfg')

		#tileset.set_empty(1)

	#	self.level=Level.Level()
	#	self.level.set_tileset(tileset)

		#self.level.map=Level.create_test_map(tileset)



		#self.set_game_window(self.game_w)

	#	self.create_squad()
	#	self.squad.get_unit(1).set_pos(16,15)
	#	self.squad.get_unit(2).set_pos(18,15)
	#	self.squad.get_unit(3).set_pos(16,14)
	#	self.squad.get_unit(4).set_pos(17,14)


		for u in self.squad.get_units():
			self.heal_HP(u,10)
			self.heal_AP(u,10)


		libtcod.console_set_color_control(libtcod.COLCTRL_1,Color.RED,Color.BLACK)
		libtcod.console_set_color_control(libtcod.COLCTRL_2,Color.LBLUE,Color.BLACK)
		libtcod.console_set_color_control(libtcod.COLCTRL_2,Color.DBLUE,Color.BLACK)



		#self.squad_ui=ui.Squad_Ui(self.charamenu,self.squad,self)
		#self.charamenu.add_elem(self.squad_ui)


		self.level.add_monster(self.create_monster(Classes.Demonito()))
		self.level.add_monster(self.create_monster(Classes.Runner()))
		self.level.monsters.get_unit(1).set_pos(20,16)
		self.level.monsters.get_unit(2).set_pos(21,15)



		self.set_state(1)

		self.initialize_path_map()
		self.path_place_unit()



		self.log_w=self.window.create_window(50,8,0,42,'Log')
		self.log=ui.Log(self.log_w,48,6)
		self.log_w.add_elem(self.log)





		self.selected_window=None

		self.window.build()




	#	print self.squad.

#--------------Main Methods------------------------------------------------


	def input(self):

		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE,self.key,self.mouse)

			# SYSTEM INPUT -------------------------------------------------

		if libtcod.console_is_window_closed():
			self.set_state(0)
		if self.key == Input.F11:#libtcod.KEY_ENTER and self.key.lalt:
	        #Alt+Enter: toggle fullscreen
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
		elif self.key == Input.F4:

			self.game_screen.toggle_blink_selected()

		elif self.key == Input.F2:

			#self.test_log()
			#self.sound_manager.toggle_music()
			#self.sound_manager.play_sound(self.sound_manager.sword2)
			self.kill_all_ennemy()

		elif self.key == Input.ALT_ESCAPE:
			self.state=0
			return

		elif self.key.vk == libtcod.KEY_SPACE:
			#self.test_ai()
			#print 'ai tested'
			pass

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

	#keyboard input--------------------------------------------------------

		if self.state==4 or self.state==5 :

			if self.key.vk==libtcod.KEY_CHAR:

				print chr(self.key.c)
				self.print_letter(chr(self.key.c))

			elif self.key==Input.BACKSPACE:

				self.del_letter()

			elif self.key==Input.ENTER:

				self.validate_character()#temporary

			elif self.key==Input.SPACE:

				self.validate_team()

		elif self.state==6:

			if self.key==Input.SPACE:

				self.new_level()

			elif self.key==Input.TAB:

				self.level.set_spawns()

			elif self.key==Input.ENTER:

				self.launch_level()

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

			elif self.key==Input.SPACE:

				self.next_turn()

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
			if self.state==2 or self.state == 4 or self.state == 5 or self.state == 7:
				self.render()
				self.input()

			if self.state==3 or self.state == 6:

				self.render()
				self.input()
				self.turn_iterate()

	def turn_iterate(self):

		self.turner+=1

		if self.turner%10 ==0 and self.game_screen and (self.state==1 or self.state==3 or self.state==6):
			self.game_screen.update()
		if self.turner%50==0:
			self.game_screen.blink()
		if self.turner==1000:
			self.turner=0

		if self.state==3 and self.turner%100==0:

			self.ia.step_ahead()

	#Bigger Scope Methods-------------------------------------------------------------


	def main_menu(self):
		'''
		handle the main menu
		'''
		main_menu_w=self.window.create_window(20,20,30,20,'Demon Hunter')


		menu=ui.Control_Menu(main_menu_w,18,18,'Main menu')
		main_menu_w.add_elem(menu)

		button1=Ui.Text_Button(menu,15,1,'New Game',Color.WHITE,Color.BLACK,self.team_screen,None)#self.new_game,None)
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


		self.sound_manager.start_music()

	def new_game(self):

		wind=self.window.get_window_by_id('Demon Hunter')
		if wind:
			self.window.close_window(wind)

		self.initialize_game()

		#TODO
		self.debug_start()


	def next_turn(self,confirm=True):

		can_still_act=False
		for u in self.get_all_unit():

			if u.player and u.is_ready():

				can_still_act=True

		if can_still_act and confirm:
			print 'message davertisement'
			return
		else:

			self.ia.start_turn()
			self.set_state(3)	#3:ennemy turn
			#self.ia.do_a_move()
			for u in self.squad.get_units():
				u.set_ready()

		self.print_log('GAME',"Ennemy turn")

	def new_turn(self):

		for u in self.squad.get_units():
			u.set_ready()
			self.heal_AP(u,10)

		for m in self.level.get_monsters():
			m.set_ready()

		self.state=1

		self.print_log('GAME',"it's your turn")

	def team_screen(self):


		self.window.close_window(self.selected_window)

		self.class_window=self.window.create_window(15,30,0,5,'select your team')

		self.log_w=self.window.create_window(50,8,0,42,'Log')
		self.log=ui.Log(self.log_w,48,6)
		self.log_w.add_elem(self.log)


		menu=ui.Control_Menu(self.class_window,13,28,'classes')
		self.class_window.add_elem(menu)


		self.create_squad()


		warrior=Ui.Text_Button(menu,10,1,'warrior',Color.WHITE,Color.BLACK,self.select_class,[Classes.Warrior()])
		menu.add_elem(warrior)

		archer=Ui.Text_Button(menu,10,1,'archer',Color.WHITE,Color.BLACK,self.select_class,[Classes.Archer()])
		menu.add_elem(archer)

		assasin=Ui.Text_Button(menu,10,1,'assasin',Color.WHITE,Color.BLACK,self.select_class,[Classes.Assasin()])
		menu.add_elem(assasin)

		sage=Ui.Text_Button(menu,10,1,'sage',Color.WHITE,Color.BLACK,self.select_class,[Classes.Sage()])
		menu.add_elem(sage)

		mage=Ui.Text_Button(menu,10,1,'mage',Color.WHITE,Color.BLACK,self.select_class,[Classes.Mage()])
		menu.add_elem(mage)

		start=Ui.Text_Button(menu,10,1,'Begin',Color.LBLUE,Color.GREEN,self.validate_team,None)
		menu.add_elem(start)

		self.set_state(2)	#4: selection_screen


		self.menu_w=self.window.create_window(30,50,49,0,"Menu")
		self.charamenu=ui.Soft_Menu(self.menu_w,28,48,'Menus')
		self.menu_w.add_elem(self.charamenu)
		self.squad_ui=ui.Squad_Ui(self.charamenu,self.squad,self)
		self.charamenu.add_elem(self.squad_ui)

		self.select_window(self.class_window)

		self.window.build('erase')


	def select_class(self,classe):

		self.team_window=self.window.create_window(20,30,15,5,'class info')

		unit=self.create_unit('name',classe)

		for u in range(1,5):
			if self.squad.get_unit(u).get_type()=='Not':
				break
		self.squad.set_unit(u,unit)

		self.selected_unit=unit

		unit_file=ui.Character_File(self.team_window,unit)
		self.team_window.add_elem(unit_file)

		name_w=self.window.create_window(15,5,35,5,'enter name ')
		self.entry=ui.Name_Entry(name_w)
		name_w.add_elem(self.entry)
		self.select_window(name_w)

		self.name_w=name_w

		self.set_state(4)


		self.squad_ui.rebuild(self.squad)

		self.window.build('erase')


	def open_upgrade_menu(self):

		self.set_state(7)
		self.upgrade_window=self.window.create_window(80,50,0,0,'upgrade')

		unit1_w=self.window.create_window(17,40,0,0,'unit1')
		unit1_m=ui.Character_File(unit1_w,self.squad.get_unit(1))
		unit1_w.add_elem(unit1_m)

		unit2_w=self.window.create_window(17,40,17,0,'unit2')
		unit2_m=ui.Character_File(unit1_w,self.squad.get_unit(2))
		unit2_w.add_elem(unit2_m)

		unit3_w=self.window.create_window(17,40,34,0,'unit3')
		unit3_m=ui.Character_File(unit1_w,self.squad.get_unit(3))
		unit3_w.add_elem(unit3_m)

		unit4_w=self.window.create_window(17,40,51,0,'unit4')
		unit4_m=ui.Character_File(unit1_w,self.squad.get_unit(4))
		unit4_w.add_elem(unit4_m)

		controll_w=self.window.create_window(12,40,68,0,'upgrade')
		controll=ui.Upgrade_Controll(controll_w,self)
		controll_w.add_elem(controll)

		self.team_window.add_elem(unit1_w)
		self.team_window.add_elem(unit2_w)
		self.team_window.add_elem(unit3_w)
		self.team_window.add_elem(unit4_w)
		self.team_window.add_elem(controll_w)

		self.select_window(controll_w)

		self.window.build()

	def kill_all_ennemy(self):

		while len(self.level.get_monsters())>=1:
			self.heal_HP(self.level.monsters.get_unit(0),-10)

	def print_letter(self,char):

		self.entry.add_letter(char)
		self.name_w.build()

	def del_letter(self):

		self.entry.del_letter()

	def validate_character(self):

		if len(self.entry.get_text())<2:
			return
		self.selected_unit.set_name(self.entry.get_text())
		print 'valided'
		self.select_window(self.class_window)
		self.window.close_window(self.team_window)
		self.window.close_window(self.name_w)
		self.set_state(2)

		print self.squad.get_units()
		self.squad_ui.rebuild(self.squad)
		print 'squad ui rebuilt'

		self.print_log('TEAM',self.selected_unit.get_name()+ ' the '+ self.selected_unit.get_class_name() + ' has joined the team')


		if self.squad.get_unit(4).get_type() !='Not':

			self.print_log('TEAM','Your team is ready, press [space] to begin your adventure')
			self.set_state(5)#temporary




		self.window.build('erase')
		#self.menu_w.build()

	def validate_team(self):

		if self.squad.get_unit(4).get_type() =='Not':
			self.print_log('WARNING',"you don't have your full team yet")
		else:
			self.print_log('INFO',"launching game...")
			self.sound_manager.validate()
			self.select_window(None)
			self.prepare_game()



	def prepare_game(self):

		self.print_log('SYSTEM',"cleaning windows")
		self.window.close_window(self.class_window)
		#self.window.close_window(self.team_window)
	#	self.window.close_window(self.name_w)
	#	self.window.close_window(self.team_window)
		#self.window.close_window(

		self.print_log('SYSTEM',"done")
		self.set_state(2)

		self.game_w=self.window.create_window(49,42,0,0,"Map")

		self.window.build('erase')





		self.initialize_game()
		self.new_level()


	def new_level(self):

		self.print_log('SYSTEM',"generating level")
		self.level=Level.Level()
		self.level.set_tileset(self.tileset)

		while not self.level.generate_level(2,5,18,11,6):
			print 'retrying level generation'

		self.set_game_window(self.game_w)


		self.print_log('GAME','press [enter] to start playing')
		self.set_state(6)


	def launch_level(self):

		print 'launching_level'
		self.initialize_path_map()

		print self.level.spawn
		for u in self.squad.get_units():
			while not self.place_to(u,self.level.spawn):
				pass

		self.generate_monsters()

		for m in self.level.get_monsters():
			while not self.place_to(m,self.level.monster_spawn):
				pass

		self.new_turn()


	def end_level(self):

		self.print_log('GAME','level finished')

		#gain_point

		self.open_upgrade_menu()


	def upgrade_unit(self,unit,upgrade):

		self.WUPOINT-=self.get_upgrade_cost(unit,upgrade)
		if upgrade=='HP':
			unit.levelup()
			unit.HP_max=unit.HP_max+1
			self.heal_HP(unit,1)

		if upgrade=='AP':
			unit.levelup()
			unit.AP_max=unit.AP_max+1



		print 'upgraded'
		self.window.build()


	def get_upgrade_cost(self,unit,upgrade):

		return 30

	def place_to(self,unit,tile):


		result=False
		if libtcod.map_is_walkable(self.path_map,tile[0],tile[1]):

			unit.set_pos(tile[0],tile[1])
			result = True

		else:
			a=0
			while a<5:

				if libtcod.map_is_walkable(self.path_map,tile[0]+1+a,tile[1]):

					unit.set_pos(tile[0]+1+a,tile[1])
					result= True

				if libtcod.map_is_walkable(self.path_map,tile[0]-1-a,tile[1]):

					unit.set_pos(tile[0]-1-a,tile[1])
					result= True

				if libtcod.map_is_walkable(self.path_map,tile[0],tile[1]+1+a):

					unit.set_pos(tile[0],tile[1]+1+a)
					result= True

				if libtcod.map_is_walkable(self.path_map,tile[0],tile[1]-1-a):

					unit.set_pos(tile[0],tile[1]-1-a)
					result= True

				else:
					pass

				a+=1
				if result:
					break



		self.path_place_unit()

		return result


	def game_over(self):

		self.main_menu()
		self.window.build('erase')
	#Combat Methods--------------------------------

	def generate_monsters(self):

		if self.level<3:

			self.level.add_monster(self.create_monster(Classes.Demonito()))
			self.level.add_monster(self.create_monster(Classes.Runner()))
			#-----------------
			self.level.add_monster(self.create_monster(Classes.Runner()))
			self.level.add_monster(self.create_monster(Classes.Runner()))


	def get_fight_issue(self):

		assert self.target or self.state>2

		self.fight.calc_issue(self.selected_unit,self.selected_action,self.target)

	def kill_unit(self,unit):

		corp=Units.Corpse()
		corp.build_from_unit(unit)
		self.other_unit.append(corp)

		if unit.player:

			self.squad.remove_unit(unit)
			if len(self.squad.get_units())<1:
				self.game_over()

		else:

			self.level.monsters.remove_unit(unit)
			if len(self.level.get_monsters())<1:
				self.end_level()

		self.print_log('COMBAT',unit.get_name() + ' Died!')

	#Base_Monster_Methodes--------------------------

	def init_ai(self):

		self.ia=Ennemy.Leader_Ai(self)

	def test_ai(self):

		self.ia.start_turn()
		self.ia.calc_move()
		#unit=self.level.get_monsters()[1]
		#self.ia.get_all_targets(unit)
		#print '-----------------------------'
		#self.ia.choose_target(unit)

	def solve_ennemy_move(self,unit,move):

		bginpos=unit.get_pos()
		#self.update_path_map(unit.get_pos(),move)
		unit.set_pos(move[0],move[1])
		self.update_path_map(bginpos,unit)


	#-----------log-------------------------------

	def print_log(self,type,text):

		self.log.print_entry(type,text)
		self.log_w.build()

	def test_log(self):

		self.print_log('DEBUG','Ceci est un message test')

	#------------music--------------------------

	def play_combat_sound(self,unit,action):

		print 'sound incomming'

		if unit.get_class_name()=='Warrior':

			if action==1:

				self.sound_manager.play_sound(self.sound_manager.sword2)

		elif unit.get_class_name()=='Assasin':

			if action==1:

				self.sound_manager.play_sound(self.sound_manager.punch3)

		elif unit.get_class_name()=='Archer':

			if action==1:

				self.sound_manager.play_sound(self.sound_manager.punch4)

		elif unit.get_class_name()=='Sage':

			if action==1:

				self.sound_manager.play_sound(self.sound_manager.punch1)

		elif unit.get_class_name()=='Mage':

			if action==1:

				self.sound_manager.play_sound(self.sound_manager.magic2)

		elif unit.get_class_name()=='Demonito':

			if action==1:

				self.sound_manager.play_sound(self.sound_manager.sword1)

		elif unit.get_class_name()=='Runner':

			if action==1:

				self.sound_manager.play_sound(self.sound_manager.punch2)


	#-----getters-------------------------------

	def get_total_wupoint(self,num=False):

		if num:
			return self.WUPOINT
		else:
			return str(self.WUPOINT)

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

			self.print_log('GAME',unit.get_name() + ' selected')
		else:
			self.set_reachable_tiles(list())





	def set_selected_tile(self,x,y):

		self.selected_tile=[x,y]

	def select_window(self,window):

		self.selected_window=window
		if window:
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
			if target != self.selected_unit:
				self.print_log('GAME',target.get_name() + ' targeted - ' + str(self.fight.get_damage()) + ' damages if you attack')

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
		siz = libtcod.path_size(path)

		libtcod.path_delete(path)

		return siz

	def get_path_pos(self,pos1,pos2,dist):

		chemin=libtcod.path_new_using_map(self.path_map,0)
		print pos1,pos2
		libtcod.path_compute(chemin,pos1[0],pos1[1],pos2[0],pos2[1])
		print libtcod.path_is_empty(chemin)

		x,y=libtcod.path_get(chemin,dist)

	#	for i in range(dist):
	#		x,y=libtcod.path_walk(path,False)
	#	print x,y
		libtcod.path_delete(chemin)
		return [x,y]

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
				if libtcod.map_is_walkable(self.path_map,x,y):
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

	def set_path_map(self,x,y,path):

		libtcod.map_set_properties(self.path_map,x,y,True,path)

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


		print unit.get_class_name(), id
		self.play_combat_sound(unit,id)

		self.fight.calc_issue(unit,id,target)#not necessary

		log=unit.get_name() + ' attacked ' + target.get_name() + ' for ' + str(self.fight.get_damage()) + ' damage'

		self.print_log('COMBAT',log)


		self.heal_HP(target,-1*self.fight.get_damage())
		self.heal_AP(unit,-1*self.fight.get_cost())


		self.menu_w.build()



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
