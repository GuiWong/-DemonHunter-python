import libtcodpy as libtcod

from WongEngine import  Window, Ui, WongUtils
import Color



class Input:

	def __init__(self,inputs,chars=None,modif=False):

		self.inputs=inputs
		self.char=chars
		self.modif=modif

	def __eq__(self,other):

		same=False

		if self.modif=='lalt':

			if not other.lalt:
				return False
		elif self.modif=='ralt':
			if not other.ralt:
				return False

		for i in self.inputs:

			if other.vk==i:
				return True

		if self.char:
			for char in self.char:
				if other.c==char:
					return True

		return same

class Num_Input(Input):

	def __init__(self,inputs,chars=None,modif=False):

		Input.__init__(self,inputs,chars,modif)

	def get_value(self,other):

		for i in range(len(self.inputs)):

			if self.inputs[i]==other.vk:
				return i




UP=Input([libtcod.KEY_UP])
DOWN=Input([libtcod.KEY_DOWN])
LEFT=Input([libtcod.KEY_LEFT])
RIGHT=Input([libtcod.KEY_RIGHT])

PLUS=0
MINUS=0

CROSS=0
SLASH=0

NUMBER=Num_Input([libtcod.KEY_0,libtcod.KEY_1,libtcod.KEY_2,libtcod.KEY_3,
		libtcod.KEY_4,libtcod.KEY_5,libtcod.KEY_6,libtcod.KEY_7,
		libtcod.KEY_8,libtcod.KEY_9])

N0=([libtcod.KEY_0])
N1=([libtcod.KEY_1])
N2=([libtcod.KEY_2])
N3=([libtcod.KEY_3])
N4=([libtcod.KEY_4])
N5=([libtcod.KEY_5])
N6=([libtcod.KEY_6])
N7=([libtcod.KEY_7])
N8=([libtcod.KEY_8])
N9=([libtcod.KEY_9])

F4=Input([libtcod.KEY_F4])

F11=Input([libtcod.KEY_F11])
F12=Input([libtcod.KEY_F12])

ENTER=Input([libtcod.KEY_ENTER])
TAB=Input([libtcod.KEY_TAB])
SPACE=Input([libtcod.KEY_SPACE])
BACK=0









ESCAPE=Input([libtcod.KEY_ESCAPE],[113])
ALT_ESCAPE=Input([libtcod.KEY_ESCAPE],None,'lalt')
