




class Combat_Manager:

	def __init__(self):

		self.damage=None
		self.cost=None


	def type_win(self,type1,type2):

		if type1=='fight' and type2=='range':
			return True
		if type1=='range' and type2=='stealth':
			return True
		if type1=='stealth' and type2=='sage':
			return True
		if type1=='sage' and type2=='mage':
			return True
		if type1=='mage' and type2=='fight':
			return True
		else:
			return False


	def calc_issue(self,unit,skill,target):

		base = unit.get_skill(skill).get_power()

		if self.type_win(unit.get_type(),target.get_type()):
			base +=1

		print base

		self.damage=base
		self.cost=unit.get_skill(skill).cost

	def get_damage(self):

		return self.damage

	def get_cost(self):

		return self.cost
