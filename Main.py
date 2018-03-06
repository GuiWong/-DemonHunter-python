import sys
sys.path.insert(0,'data/DemonHunter')
sys.path.insert(0,'data')
import libtcodpy as libtcod

from WongEngine import Wong, Window, Ui, Map, WongUtils

from DemonHunter.Engine import  *
from DemonHunter.ui import *	#temporary





game=Demon_Hunter_Game()

libtcod.console_set_custom_font('data/Ressources/terminal16x16_gs_ro.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW,16,16)
libtcod.console_init_root(80,50,"DemonHunter")

libtcod.sys_set_fps(100)

game.initialize_game()



game.debug_start()

print 'launching game'

game.run()
