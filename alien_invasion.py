import sys
from time import sleep
import json

import pygame


from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Overall class to manage game assets and behaviour."""

	def __init__(self):
		"""Initialise the game, and create game resources."""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#Create an instance to store the game statistics,
		# and create a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		#Make the play button
		self.play_button = Button(self, "Play")

		self._make_difficulty_level()

	def _make_difficulty_level(self):
		"""Creates difficulty level buttons"""
		self.easy_button = Button(self, "Easy")
		self.normal_button = Button(self, "Normal")
		self.hard_button = Button(self, "Hard")

		self.easy_button.rect.top = (self.play_button.rect.top + 1.5* self.play_button.rect.height)
		self.easy_button.update_msg_position()

		self.normal_button.rect.top = (self.easy_button.rect.top + 1.5* self.easy_button.rect.height)
		self.normal_button.update_msg_position()

		self.hard_button.rect.top = (self.normal_button.rect.top + 1.5* self.normal_button.rect.height)
		self.hard_button.update_msg_position()


	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			
			self._update_screen()


	def _check_events(self):
		"""Respond to key presses and mouse events"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self._close_game()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
				self._check_difficulty_buttons(mouse_pos)

	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#Reset the game settings.
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			self._start_game()

	def _check_difficulty_buttons(self, mouse_pos):
		"""Checks the difficulty of button"""
		easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
		normal_button_clicked = self.normal_button.rect.collidepoint(mouse_pos)
		hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

		if easy_button_clicked:
			self.settings.difficulty = 'easy'
		elif normal_button_clicked:
			self.settings.difficulty = 'normal'
		elif hard_button_clicked:
			self.settings.difficulty = 'hard'


	def _start_game(self):
		"""Resets the game"""
		self.settings.initialise_dynamic_settings()

		self.stats.reset_stats()
		self.stats.game_active = True

		self.aliens.empty()
		self.bullets.empty()

		self._create_fleet()
		self.ship.center_ship()

		pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		"""Respond to keypresses"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			self._close_game()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()
		elif event.key == pygame.K_p and not self.stats.game_active:
			self._start_game()

	def _check_keyup_events(self, event):
		"""Respond to key releases"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

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

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions"""
		#Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(
				self.bullets, self.aliens, True, True)
		if collisions:
			for alien in collisions.values():
				self.stats.score += self.settings.alien_points * len(alien)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			#Destroy existing bullets and create new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#Increase level
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"""Check if the fleet is at an edge,
		the update the position of all aliens in the fleet"""
		self._check_fleet_edges()
		self.aliens.update()

		#Look for alien and ship collision
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()
		#Look for aliens hitting the bottom of the screen
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		"""Check if any aliens ahve reached the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#Treat this the same as if the ship gets hit
				self._ship_hit()
				break

	def _ship_hit(self):
		"""Responds to ship being hit by an alien"""
		if self.stats.ships_left > 0:
			#Decrement ships left, and update scorebaord
			self.stats.ships_left -=1
			self.sb.prep_ships()

			#Get rid of any remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#Pause
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _create_fleet(self):
		"""Create the fleet of aliens"""
		#Create an alien and find the number of aliens in a row.
		#Spacing between each alien is equal to one alien width
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		#Determine the numebr of rows of aliens that fit on the screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
								(3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		#Create the full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2* alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleets direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _close_game(self):
		"""Save high score and exit"""
		saved_high_score = self.stats.get_saved_high_score()
		if self.stats.high_score > saved_high_score:
			with open('high_score.json', 'w') as f:
				json.dump(self.stats.high_score, f)

		sys.exit()

	def _update_screen(self):
		"""Update images on the screen and flip to a new screen"""
		self.screen.fill(self.settings.bg_colour)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#Draw the scoreboard
		self.sb.show_score()

		#Draw the play button if the game is inactive
		if not self.stats.game_active:
			self.play_button.draw_button()
			self.easy_button.draw_button()
			self.normal_button.draw_button()
			self.hard_button.draw_button()

		pygame.display.flip()

if __name__ == '__main__':
	#Make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()