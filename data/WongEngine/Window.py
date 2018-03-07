
import sys
import os
import libtcodpy as libtcod
import weakref


#TODO handle more colors, easier acces
class Palette:

	def __init__(self,data=None):

		if not data:
			data=[(0,0,0),(0,0,128),(0,128,0),(0,128,128),(128,0,0),(128,0,128),(128,128,0),(192,192,192),(128,128,128),(0,0,255),(0,255,0),(0,255,255),(255,0,0),(255,0,255),(255,255,0),(255,255,255)]
			print data[0]

		self.BLACK=libtcod.Color(*data[0])
		self.BLUE=libtcod.Color(*data[1])
		self.GREEN=libtcod.Color(*data[2])
		self.CYAN=libtcod.Color(*data[3])
		self.RED=libtcod.Color(*data[4])
		self.MAGENTA=libtcod.Color(*data[5])
		self.BROWN=libtcod.Color(*data[6])
		self.LGREY=libtcod.Color(*data[7])
		self.DGREY=libtcod.Color(*data[8])

		self.LBLUE=libtcod.Color(*data[9])

		self.LGREEN=libtcod.Color(*data[10])

		self.LCYAN=libtcod.Color(*data[11])

		self.LRED=libtcod.Color(*data[12])

		self.LMAGENTA=libtcod.Color(*data[13])

		self.YELLOW=libtcod.Color(*data[14])

		self.WHITE=libtcod.Color(*data[15])






class W_Window:

	def __init__(self,parent,width,height):

		self.parent = weakref.ref(parent)
		self.width=width
		self.height=height
		self.console=libtcod.console_new(width,height)

	def get_palette(self):

		pal=self.parent().get_palette()
		return pal

#-------added during 7DRL --------------------------
	def calc_pos(self,x,y):

		return x, y

	def get_window(self):

		return self

	def __del__(self):

		print 'window deleted'


class Main_Window(W_Window):

	def __init__(self,parent,width,height,palette=False):

		W_Window.__init__(self,parent,width,height)

		#self.window=libtcod.console_new(width,height)
		self.sub_windows=list()

		if not palette:
			palette=Palette()

		self.color=palette

	def get_palette(self):

		return self.color

	def create_complex_window(self,width,height,rx,ry,id):

		wind=Configurable_Window(self,width,height,rx,ry,id)
		self.sub_windows.append(wind)
		return wind


	def create_window(self,width,height,rx,ry,id):

		wind=Simple_Window(self,width,height,rx,ry,id)
		self.sub_windows.append(wind)
		return wind

	#------7DRL------------------------------------------------------------
	def close_window(self,window):

		self.sub_windows.remove(window)

	def close_window_by_id(self,id):

		self.sub_windows.remove(self.get_window_by_id(id))


	def get_window_by_id(self,id):

		candidate=None
		for wind in self.sub_windows:
			if wind.id==id:
				candidate=wind
		return candidate
	#------7DRL------------------------------------------------------------

	def build(self):

		for window in self.sub_windows:
			window.build()


	def get_elem_by_mouse(self):
		'''
		return the Wui_elem/Window under the mouse
		'''

		potList=list()
		x=self.parent().mouse.cx
		y=self.parent().mouse.cy
		for window in self.sub_windows:
			if window.is_in(x,y):
				potList.append(window)

		if len(potList) > 1:
			print 'Unimplemented yet, see Z-Levels for windows'
			target=potList[len(potList)-1]
	#Bug corrected for 7DRL project
		elif len(potList) < 1:
			return self
		else:
			target=potList[0]

		result=target.get_elem_by_mouse(x-target.rx,y-target.ry)


		return result


	def render(self):

		for window in self.sub_windows:
			#window.render()
			libtcod.console_blit(window.console,0,0,window.width,window.height,self.console,window.rx,window.ry)

		libtcod.console_blit(self.console,0,0,self.width,self.height,0,0,0)
		libtcod.console_flush()


class Sub_Window(W_Window):

	def __init__(self,parent,width,height,rx,ry,id):

		W_Window.__init__(self,parent,width,height)

		self.rx=rx
		self.ry=ry
		self.id=id

		self.bk_color=False
		self.color=False

	def get_elem_by_mouse(self,x,y):
		'''
		parent method to get an elem by mouse position
		:param x : mouse x pos relative to window
		:param y : mouse y pos relative to window
		'''

		return self

	def set_bk_color(self,color):

		self.bk_color=color

	def set_color(self,color):

		self.color=color

	def get_bk_color(self):

		if self.bk_color:
			return self.bk_color
		else:
			return self.get_palette().DGREY

	def get_color(self):

		if self.color:
			return self.color
		else:
			return self.get_palette().BLUE


	def is_in(self,x,y):
		'''Return true if the x,y tile is in the window
		note: window store its x,y relative to parent
		'''

		return (self.rx <= x and
				self.rx + self.width > x and
				self.ry <= y and
				self.ry +self.height > y)




class Simple_Window(Sub_Window):

	def __init__(self,parent,width,height,rx,ry,id):

		Sub_Window.__init__(self,parent,width,height,rx,ry,id)
		self.content=None



	def set_content(self,elem):

		self.content=elem

	def add_elem(self,elem):

		self.set_content(elem)





	def get_elem_by_mouse(self,x,y):
		'''
		method to get an elem by mouse position
		chain to content
		:param x : mouse x pos relative to window
		:param y : mouse y pos relative to window
		'''
		if not self.content:
			ret= self
		else:
			ret= self.content.get_elem_by_mouse(x-1,y-1)

		return ret

	def build(self):


		print 'built!'
		libtcod.console_set_default_foreground(self.console,self.get_color())
		libtcod.console_set_default_background(self.console,self.get_bk_color())
		libtcod.console_print_frame(self.console,0,0,self.width,self.height,True,libtcod.BKGND_SET,self.id)

		temp=libtcod.console_new(self.width-2,self.height-2)
		y=1
		if not self.content:
			print 'fenetre vide'
		else:
			#TODO: redo this, exeptions
			self.content.build(temp)
			libtcod.console_blit(temp,0,0,self.content.width,self.content.height,self.console,1,y)


class Folding_Window(Sub_Window):

	def __init__(self,parent,width,height,rx,ry,id):

		Sub_Window.__init__(self,parent,width,height,rx,ry,id)
		self.content=list()

		#self.mode=

	def add_elem(self,elem):

		self.content.append(elem)

	def build(self):


		print 'built!'
		libtcod.console_set_default_foreground(self.console,self.get_palette().LBLUE)
		libtcod.console_set_default_background(self.console,self.get_palette().DGREY)
		libtcod.console_print_frame(self.console,0,0,self.width,self.height,True,libtcod.BKGND_SET,'fenetre1')

		temp=libtcod.console_new(self.width-2,self.height-2)

		libtcod.console_set_default_foreground(temp,self.get_palette().LBLUE)
		libtcod.console_set_default_background(temp,self.get_palette().DGREY)
		y=1

		for elem in self.content:
			libtcod.console_clear(temp)
			height=elem.build(temp)

			libtcod.console_blit(temp,0,0,elem.width,elem.height,self.console,1,y)

			y+=height



	def render(self):

		pass



class Configurable_Window(Sub_Window):

	def __init__(self,parent,width,height,rx,ry,id):

		Sub_Window.__init__(self,parent,width,height,rx,ry,id)

		self.border_v=chr(179)
		self.border_h=chr(196)
		self.fixed=True
		self.arrows=False
		self.reduce=False
		self.close=False
		self.vertical=True

		self.size_v=height-2
		self.size_h=width-2

		self.content=list()
		self.controls=list()

	def configure(self,mode):

		if mode == "simple":

			print "simple"

	def add_elem(self,elem):

		self.content.append(elem)


	def get_elem_by_mouse(self,x,y):
		'''
		method to get an elem by mouse position
		chain to content
		:param x : mouse x pos relative to window
		:param y : mouse y pos relative to window
		'''

		ret= self



		for elem in self.content:
			print x-1, y-1
			if elem.is_in(x-1,y-1):
				print elem
				ret=elem.get_elem_by_mouse(x+elem.x+1,y+elem.y+1)

		return ret


	def build(self):


		print 'built!'
		libtcod.console_set_default_foreground(self.console,self.get_color())
		libtcod.console_set_default_background(self.console,self.get_bk_color())
		libtcod.console_print_frame(self.console,0,0,self.width,self.height,True,libtcod.BKGND_SET,self.id)

		temp=libtcod.console_new(self.width-2,self.height-2)
		y=1

		if self.vertical:
			for elem in self.content:
				libtcod.console_clear(temp)
				elem.build(temp)
				height=elem.height

				libtcod.console_blit(temp,0,0,elem.width,elem.height,self.console,1,y)

				y+=height
