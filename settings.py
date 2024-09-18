class Settings:
	"""A class to store all settings for alien invasion"""

	def __init__(self):
		"""Initialise the game's static settings"""
		#Bullet settings
		self.bullet_speed = 1.5
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_colour = (60,60,60)
		self.bullets_allowed = 3
		self.ss_bullet_width = 15
		self.ss_bullet_height = 3

		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_colour = (230,230,230)

		#Ship settings
		self.ship_speed = 1.5
		self.ship_limit = 3

		#Alien settings
		self.alien_speed = 1.0
		self.fleet_drop_speed = 10

		#How quickly the game speed's up
		self.speedup_scale = 1.1

		self.difficulty = "normal"

		#How quickly the alien point value increases
		self.score_scale = 1.5

		self.initialise_dynamic_settings()

				#Raindrop settings
		self.raindrop_speed = 1.5

		

	def initialise_dynamic_settings(self):
		if self.difficulty == 'easy':
			self.ship_limit = 5
			self.bullets_allowed = 10
			self.ship_speed = 1.5
			self.bullet_speed = 3.0
			self.alien_speed = 0.75

		elif self.difficulty == 'normal':
			self.ship_limit = 3
			self.bullets_allowed = 3
			self.ship_speed = 1.5
			self.bullet_speed = 3.0
			self.alien_speed = 1.0

		elif self.difficulty == 'hard':
			self.ship_limit = 2
			self.bullets_allowed = 3
			self.ship_speed = 3.0
			self.bullet_speed = 6.0
			self.alien_speed = 2.0

		# fleet direction of 1 represesnts right; -1 respresents left
		self.fleet_direction = 1

		#Scoring
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed settings and alien point values"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)

	def set_difficulty(self):
		"""Sets difficulty of game"""
		if dif == 'easy':
			print('easy')
		elif dif == 'normal':
			pass
		elif dif == 'hard':
			pass
		








