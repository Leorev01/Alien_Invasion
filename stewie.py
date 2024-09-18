import pygame

class Stewie:
	"""Creates class for Stewie"""
	def __init__(self, ai_game):
		#Initialise stewiw and starting position
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		#Load stewie image and get its rect
		self.image = pygame.image.load('images/stewie.bmp')
		self.rect = self.image.get_rect()		

		#Start Stewie at the center of the screen
		self.rect.center = self.screen_rect.center

	def blitme(self):
		"""Draw Stewie and it's current location"""
		self.screen.blit(self.image, self.rect)


