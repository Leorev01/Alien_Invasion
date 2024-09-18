import pygame

class Ship:
	"""A class to manage the ship"""

	def __init__(self, tp_game):
		"""Initialise the ship and set its starting position"""
		self.screen = tp_game.screen
		self.settings = tp_game.settings
		self.screen_rect = tp_game.screen.get_rect()

		#Load the ship image and get its rect.
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.image = pygame.transform.rotate(self.image, 270)#Changed from 90 fro target practice game

		#Start each new ship at the bottom centre of the screen.
		#Changed from midright for target practice game
		self._ship_center()


		#Movement flag
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
		"""Update the ship's position based on the movement flag."""
		#Update the ships x value, not the rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed
		if self.moving_up and self.rect.top > 0:
			self.y -= self.settings.ship_speed
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.y += self.settings.ship_speed

		#Update rect object from self.x and self.y
		self.rect.x = self.x
		self.rect.y = self.y

	def _ship_center(self):
		"""Recenters the ship after being hit by an alien"""
		self.rect.midleft = self.screen_rect.midleft
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)
