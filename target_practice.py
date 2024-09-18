import sys
from random import random
import pygame

from ss_settings import Settings
from game_stats import GameStats
from button import Button
from sideways_ship import Ship
from ssbullet import Bullet
from rectangle import Box

class TargetPractice:
	"""Initiates the game Target Practice"""
	def __init__(self):
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Target Practice")
		
		self.stats = GameStats(self)
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.box = Box(self)
		

		self.play_button = Button(self, "Play")

	def run_game(self):
		"""Starts main loop for game"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self.box.update()

			self._update_screen()

			pygame.display.flip()

	def _start_game(self):
		"""Start's game when command used"""
		self.stats.reset_stats()
		self.stats.game_active = True

		self.bullets.empty()

		self.ship._ship_center()
		self.box._box_center()

		pygame.mouse.set_visible(False)

	def _check_play_button(self, mouse_pos):
		"""Checks is person has presses the play button"""
		button_clicked = self.playbutton.rect.collidepointany(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.settings.initialise_dynamic_settings()
		else:
			self.stats.game_active = False
			pygame,mouse.set_visible(True)


	def _check_events(self):
		"""Check for keyboard and mouse activity"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()

	def _check_keydown_events(self, event):
		"""Checks for key presses"""
		if event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_p:
			self._start_game()

	def _check_keyup_events(self, event):
		"""Checks for key releases"""
		if event.key == pygame.K_UP:
			self.ship.moving_up = False
		if event.key == pygame.K_DOWN:
			self.ship.moving_down = False

	def _fire_bullet(self):
		"""Shoots bullets"""
		if len(self.bullets ) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Updates bullets"""
		self.bullets.update()

		for bullet in self.bullets.copy():
			if bullet.rect.left >= self.screen.get_rect().right:
				self.bullets.remove(bullet)
				self._increment_misses()

		self._check_bullet_box_collisions()

	def _check_bullet_box_collisions(self):
		"""Responds to bullet and box collision"""
		collisions = pygame.sprite.spritecollide(
				self.box, self.bullets, True)
		self.settings.increase_speed( )

	def _increment_misses(self):
		self.settings.missed_shots += 1
		if self.settings.missed_shots >= 3:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)


	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_colour)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		self.box.draw_box()

if __name__ == '__main__':
	tp = TargetPractice()
	tp.run_game()

	pygame.display.flip()