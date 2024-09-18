import pygame
from pygame.sprite import Sprite

class Box:
	"""Initiates the class for rectangle"""
	def __init__(self, tp_game):
		super().__init__()

		self.screen = tp_game.screen
		self.settings = tp_game.settings
		self.screen_rect = tp_game.screen.get_rect()
		self.colour = self.settings.box_colour

		self.rect = pygame.Rect(0,0, self.settings.box_width, self.settings.box_height)

		self._box_center()

		self.direction = 1

	def update(self):
		"""Move the rectangle upand down"""
		self.y += self.direction * self.settings.box_speed

		if self.rect.top < 0:
			self.rect.top = 0
			self.direction = 1
		elif self.rect.bottom > self.screen_rect.bottom:
			self.rect.bottom = self.screen_rect.bottom
			self.direction = -1

		self.rect.y = self.y

	def _box_center(self):
		self.rect.midright = self.screen_rect.midright

		self.y = float(self.rect.y)

	def draw_box(self):
		pygame.draw.rect(self.screen, self.colour, self.rect)