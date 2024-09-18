import pygame
from pygame.sprite import Sprite

class Star(Sprite):
	"""Initiates the class for each star"""
	def __init__(self, s_game):
		"""Initialise star and set it to its starting position"""
		super().__init__()
		self.screen = s_game.screen

		#Load stars image and set its rect attribute
		self.image = pygame.image.load('images/star.bmp')
		self.image = pygame.transform.scale(self.image, (100,100))
		self.rect = self.image.get_rect()

		#Start each star from the top left corner
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Store the star's exact horizontal position
		self.x = float(self.rect.x)