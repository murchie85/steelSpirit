import pygame

class music():
	def __init__(self, tunePath=None,state='stopped'):
		self.tunePath  = tunePath
		self.state = state

	def play(self,tunePath,pos=None):
		self.tunePath = tunePath
		print('playing ' + str(tunePath))
		if(self.state=='playing'):
			self.stop()
			return()
		if(self.state=='stopped'):
			pygame.mixer.init()
			pygame.mixer.music.load(tunePath)
			pygame.mixer.music.play()
			if(pos):
				pygame.mixer.music.pause()
				pygame.mixer.music.set_pos(pos)
				pygame.mixer.music.unpause()
			self.state = 'playing'
	def stop(self):
		if(self.state=='playing'):
			pygame.mixer.music.stop()
			self.state= 'stopped'