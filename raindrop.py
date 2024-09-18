import pygame
from pygame.sprite import Sprite

class Raindrop(Sprite):
	"""Initiates the class for raindrop"""
	def __init__(self, rd_game, ):
		"""Initialise the raindrops"""
		super().__init__()
		self.screen = rd_game.screen
		self.settings = rd_game.settings

		#Load the raindrop image
		self.image = pygame.image.load('images/raindrop.png')
		self.rect = self.image.get_rect()
		self.image = pygame.transform.scale(self.image, (100,100))

		#Start each new raindrop at the top of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Store the raindrops position
		self.y = float(self.rect.y)

	def check_disappeared(self):
		"""Check if raindrops have disappeared"""
		if self.rect.top > self.screen.get_rect().bottom:
			return True
		else:
			False

	def update(self):
		"""Updates position of raindrops"""
		self.y += self.settings.raindrop_speed
		self.rect.y = self.y