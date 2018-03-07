

import Units


class Leader_Ai:

	def __init__(self,game):

		self.game=game
		self.move_list=None


	def start_turn(self):

		pass

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
							tar=b
							a=i

				val+=dam


				potential.append([val,a,tar])

		max=0
		choice=0

		print potential

		for i in range(len(potential)):

			if max < potential[i][0]:
				print 'wait a minute'
				max=potential[i][0]


	def move_unit(self,unit):

		pass
