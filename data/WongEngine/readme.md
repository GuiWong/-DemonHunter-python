This is a "library"/API for libtcod python


author: Guillaume Maréchal




files:

	__init__.py
	Map.py
	Ui.py
	Window.py
	Wong.py





changelog:



	0.0.1:			-first commit:

					Classes to handle Window
					interface from Main class: MainWindow

					basic ui classes
					menus, text


	0.0.02:		(06.02.18)
							-Tileset Class, read tileData from txt file

							-Map class, create_tile method from tileset


	0.0.03		(07,02,18)
							-map saving and loading

	0.1.0			(08.02.18)
							-Mouse support
								method get_elem_by_mouse() in Main_Window
								chain to all Windows/Ui and return the Wui_elem
								or Window under the mouse cursor


							__ reserved methods to implement:

								.get_elem_by_mouse(self,x,y)
											-get elem under mousepos (relative to self)
											-chain method to that elem
											-return the result

	0.1.1			(09,02,18)

							-Game_Shower class in Ui
							handle map/entity Drawing

							-new methods in Wong_Game:
								add_entity(entity)
								game_move_map(dx,dy)
