import sys
from time import sleep
import pygame
from sideways_ship import Ship
from settings import Settings
from ssbullet import Bullet
from sideways_aliens import Alien
from ss_game_stats import GameStats

class SidewaysShooter:
	"""Creates a class for sideways shooter"""
	def __init__(self):
		"""Initialise the game and create the game resources"""
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Sideways Shooter")

		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

	def run_game(self):
		"""Start main loop for the game"""
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()

			#Make most recent drawn screen visisble
			pygame.display.flip()

	def _check_events(self):
		"""Responds to keypresses or mous movements in game"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		"""Responds to keypresses"""
		if event.key == pygame.K_UP:
			self.ship.moving_up = True
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = True
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		"""Responds to release of keys"""
		if event.key == pygame.K_UP:
			self.ship.moving_up = False
		elif event.key == pygame.K_DOWN:
			self.ship.moving_down = False
		elif event.key == pygame.K_q:
			sys.exit()

	def _fire_bullet(self):
		"""Fires bullets from the ship"""
		if len(self.bullets) <= self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets"""
		self.bullets.update()

		#Get rid of bullets that have disappeared
		for bullet in self.bullets.copy():
			if bullet.rect.left <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collision()

	def _check_bullet_alien_collision(self):
		"""Checks if bullet has collided with alien and removes them both"""
		collisions = pygame.sprite.groupcollide(
				self.bullets, self.aliens, True, True)

		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()

	def _update_aliens(self):
		"""Updates position of aliens"""
		self._check_fleet_edges()
		self.aliens.update()

		#Look for ship collision
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

	def _create_fleet(self):
		"""Creates a fleet of aliens"""
		alien = Alien(self)
		self.aliens.add(alien)
		alien_width,alien_height = alien.rect.size
		available_space_y = self.settings.screen_height - (2 * alien_height)
		number_aliens_y = available_space_y // (2 * alien_height)
		
		ship_length = self.ship.rect.width
		available_space_x = (self.settings.screen_width - (5 * alien_width) - ship_length)
		number_rows = available_space_x // (2 * alien_width)

		for row_number in range(number_rows):
			for alien_number in range(number_aliens_y):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		"""Creates aliens"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.rect.x = alien.rect.width + 2 * alien.rect.width * row_number
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * alien_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Checks to see if any aliens are touching edge of screen"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Changes direction of fleet when it touches either edge of screen"""
		for alien in self.aliens.sprites():
			alien.rect.x += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _ship_hit(self):
		"""When ship collides with alien resets the fleet and remove ship life"""
		if self.stats.ships_left > 0:

			self.stats.ships_left -=1

			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship._ship_center()

			sleep(0.5)
		else:
			self.stats.game_active = False

	def _update_screen(self):
		"""Updates the screen"""
		self.screen.fill(self.settings.bg_colour)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

if __name__ == '__main__':
	#Make a game instance and run the game
	ss = SidewaysShooter()
	ss.run_game()