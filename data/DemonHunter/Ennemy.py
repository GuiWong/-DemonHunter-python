

import Units


class Leader_Ai:

	def __init__(self,game):

		self.game=game
		self.move_list=None
		self.pull_list=list()
		self.step=0
		self.active=None
		self.move=None


	def start_turn(self):

		self.pull_list=list(self.game.level.get_monsters())
		for m in self.pull_list:
			m.set_ready()


	def calc_move(self):

		unit=self.pull_list[0]#no target
		print unit
		self.get_all_targets(unit)
		move=self.choose_target(unit)

		print move
		self.step=1
		self.active=unit
		self.move=move

		self.pull_list.remove(unit)


		#was do_a_move befor, bug expected
	def step_ahead(self):

		if self.step==0 and len(self.pull_list)>=1:
			self.calc_move()

		elif self.step==1:
			self.do_a_move()

		elif self.step==2:
			self.do_an_attack()

		else:

			self.game.new_turn()

	def do_a_move(self):

		self.step=2
		n=len(self.move)-1
		self.active.set_pos(self.move[n][0],self.move[n][1])

	def do_an_attack(self):

		self.step=0

		self.game.solve_fight(self.active,self.move[1],self.move[2])

		self.active.end_turn()




	def get_all_targets(self,unit):

		reach=self.game.get_reachable_tile(unit)
		print reach
		targets=list()

		targets.append(self.game.get_all_potential_target(unit,unit.get_pos()[0],unit.get_pos()[1]))
		targets[0].append([unit.get_pos()[0],unit.get_pos()[1]])

		for i in range(len(reach)):

			targets.append(self.game.get_all_potential_target(unit,reach[i][0],reach[i][1]))
			targets[i+1].append(reach[i])
		print targets
		self.move_list=targets

	def choose_target(self,unit):


		potential=list()

		for move in self.move_list:
			val=0
			if move[0]==0:
				pass
			else:
				if move[0]==1:
					val+=2
				else:
					val+=1

				atk=len(move)-2
				a=1
				dam=0
				tar=0
				for i in range(1,atk+1):



					for b in range(move[0]):


						self.game.fight.calc_issue(unit,i,move[i][b])
						damage=self.game.fight.get_damage()
						#bonus for moves? todo maybe
						if damage>dam:
							dam=damage
							tar=move[i][b]
							a=i

				val+=dam


				potential.append([val,a,tar,move[atk+1]])

		max=0
		choice=0

		print potential

		for i in range(len(potential)):

			if max < potential[i][0]:
				print 'wait a minute'
				max=potential[i][0]
				choice=i

		if max==0:

			print 'no target'

		else:

			return potential[choice]



	def move_unit(self,unit):

		pass
