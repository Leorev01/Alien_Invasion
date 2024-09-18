import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship"""

	def __init__(self, tp_game):
		"""Create a bullet object at the ship's current position"""
		super().__init__()
		self.screen = tp_game.screen
		self.settings = tp_game.settings
		self.colour = self.settings.bullet_colour

		#Create a bullet rect at (0, 0) and then set current position
		self.rect = pygame.Rect(0, 0, self.settings.ss_bullet_width,
			self.settings.ss_bullet_height)
		self.rect.midright = tp_game.ship.rect.midright

		#Store the bullets position as a decimal value
		self.x = float(self.rect.x)

	def update(self):
		"""Move the bullet up the screen"""
		#Update the decimal position of the bullet.
		self.x += self.settings.ss_bullet_speed
		#Update the rect position
		self.rect.x = self.x

	def draw_bullet(self):
		"""Draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.colour, self.rect)