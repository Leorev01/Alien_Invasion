import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to respresent a single alien in the fleet"""

	def __init__(self, ai_game):
		"""Initialise the alien and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#Load the alien image and set its rect attribute
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()

		#Start each new alien near the top left of the screen
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Store the aliens exact horizontal position
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def check_edges(self):
		"""Checks whetehr an alien is on either edge"""
		screen_rect = self.screen.get_rect()
		if self.rect.bottom >= screen_rect.bottom or self.rect.top <= screen_rect.top:
			return True

	def update(self):
		"""Move the alien up"""
		self.y += (self.settings.alien_speed * 
						self.settings.fleet_direction)
		self.rect.y = self.y