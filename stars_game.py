import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from stars import Star
from random import randint

class StarsGame:
	"""Overall class to manage game assets and behaviour."""

	def __init__(self):
		"""Initialise the game, and create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.stars = pygame.sprite.Group()

		self._create_fleet()

	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()

			#Make the most recently drawn screen visible.
			pygame.display.flip()

	def _check_events(self):
		"""Respond to key presses and mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		"""Respond to keypresses"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Respond to key releases"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		elif event.key == pygame.K_q:
			sys.exit()

	def _fire_bullet(self):
		"""Create a new bullet and add it to the bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		#Update bullet positions
		self.bullets.update()

		#Get rid of bullets that have disappeared
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

	def _create_fleet(self):
		"""Create the fleet of stars"""
		#Create a star and find the number of stars in a row.
		#Spacing between each star is equal to one star width
		star = Star(self)
		star_width, star_height = star.rect.size
		available_space_x = randint(0, 10)
		number_stars_x = randint(0, 10)

		#Determine the number of rows of stars that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
								(2 * star_height) - ship_height)
		number_rows = available_space_y // (2 * star_height)

		#Create the full fleet of aliens.
		for row_number in range(randint(0, 10)):
			for star_number in range(randint(0, 10)):
				self._create_stars(star_number, row_number)

	def _create_stars(self, star_number, row_number):
		"""Create an alien and place it in the row"""
		star = Star(self)
		star_width, star_height = star.rect.size
		star.x = star_width + 2 * star_width * star_number
		star.rect.x = star.x
		star.rect.y = star.rect.height + 2 * star.rect.height * row_number
		self.stars.add(star)

	def _update_screen(self):
		"""Update images on the screen and flip to a new screen"""
		self.screen.fill(self.settings.bg_colour)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.stars.draw(self.screen)

if __name__ == '__main__':
	#Make a game instance and run the game.
	sg = StarsGame()
	sg.run_game()