
import pygame.mixer

class Sound_Manager:

	def __init__(self):

		pygame.mixer.init(44100, -16, 2, 2048)
		print 'mixer initialized'

		pygame.mixer.set_reserved(0)

	def test_sound(self):

		file='data/Ressources/sound/system/win.m4a'
		file2='data/Ressources/sound/magic/magic1.ogg'
		sound=pygame.mixer.Sound(file2)

		#pygame.mixer.Channel(2).play(sound)
		sound.play()

	def load(self):

		path='data/Ressources/sound/'

		self.music1=pygame.mixer.Sound(path+'/music/music1.ogg')

		self.sword1=pygame.mixer.Sound(path+'/fight/sword1.ogg')
		self.sword2=pygame.mixer.Sound(path+'/fight/sword2.ogg')
		self.sword3=pygame.mixer.Sound(path+'/fight/sword3.ogg')
		#self.sword4=pygame.mixer.Sound(path+'/fight/sword4.ogg')

		self.punch1=pygame.mixer.Sound(path+'/fight/punch1.ogg')
		self.punch2=pygame.mixer.Sound(path+'/fight/punch2.ogg')
		self.punch3=pygame.mixer.Sound(path+'/fight/punch3.ogg')
		self.punch4=pygame.mixer.Sound(path+'/fight/punch4.ogg')

		self.magic1=pygame.mixer.Sound(path+'/magic/magic1.ogg')
		self.magic2=pygame.mixer.Sound(path+'/magic/magic2.ogg')

		self.sys1=pygame.mixer.Sound(path+'/system/validate.ogg')

	def start_music(self):

		pygame.mixer.Channel(0).play(self.music1,-1,0,3000)

	def pause_music(self):

		pygame.mixer.Channel(0).pause()

	def play_music(self):

		pygame.mixer.Channel(0).unpause()

	def toggle_music(self):

		if pygame.mixer.Channel(0).get_busy():
			self.pause_music()
		else:
			self.play_music()

	def stop_music(self):

		pygame.mixer.Channel(0).fadeout(3000)

	def play_sound(self,sound):

		chan=pygame.mixer.find_channel()
		chan.play(sound,0,0,0)

	def validate(self):

		chan=pygame.mixer.find_channel()
		print chan
		chan.play(self.sys1,0,0,0)
