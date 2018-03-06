import libtcodpy as libtcod

from WongEngine import  Window, Ui, WongUtils




data=[(0,0,0),(0,0,128),(0,128,0),(0,128,128),(128,0,0),(128,0,128),(128,128,0),(192,192,192),(128,128,128),(0,0,255),(0,255,0),(0,255,255),(255,0,0),(255,0,255),(255,255,0),(255,255,255)]

BLACK=libtcod.Color(*data[0])
BLUE=libtcod.Color(*data[1])
GREEN=libtcod.Color(*data[2])
CYAN=libtcod.Color(*data[3])
RED=libtcod.Color(*data[4])
MAGENTA=libtcod.Color(*data[5])
BROWN=libtcod.Color(*data[6])
LGREY=libtcod.Color(*data[7])
DGREY=libtcod.Color(*data[8])
LBLUE=libtcod.Color(*data[9])
LGREEN=libtcod.Color(*data[10])
LCYAN=libtcod.Color(*data[11])
LRED=libtcod.Color(*data[12])
LMAGENTA=libtcod.Color(*data[13])
YELLOW=libtcod.Color(*data[14])
WHITE=libtcod.Color(*data[15])

DBLUE=libtcod.Color(0,0,80)

def setPalette(data=None):

	if not data:
		data=[(0,0,0),(0,0,128),(0,128,0),(0,128,128),(128,0,0),(128,0,128),(128,128,0),(192,192,192),(128,128,128),(0,0,255),(0,255,0),(0,255,255),(255,0,0),(255,0,255),(255,255,0),(255,255,255)]
		print data[0]

	BLACK=libtcod.Color(*data[0])
	BLUE=libtcod.Color(*data[1])
	GREEN=libtcod.Color(*data[2])
	CYAN=libtcod.Color(*data[3])
	RED=libtcod.Color(*data[4])
	MAGENTA=libtcod.Color(*data[5])
	BROWN=libtcod.Color(*data[6])
	LGREY=libtcod.Color(*data[7])
	DGREY=libtcod.Color(*data[8])
	LBLUE=libtcod.Color(*data[9])
	LGREEN=libtcod.Color(*data[10])
	LCYAN=libtcod.Color(*data[11])
	LRED=libtcod.Color(*data[12])
	LMAGENTA=libtcod.Color(*data[13])
	YELLOW=libtcod.Color(*data[14])
	WHITE=libtcod.Color(*data[15])
