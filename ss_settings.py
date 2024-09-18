class Settings:
	"""A class to store all settings for alien invasion"""

	def __init__(self):
		"""Initialise the game's settings"""
		#Bullet settings
		self.ss_bullet_speed = 3.0
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
		# fleet_direction of 1 represesnts right; -1 represents left
		self.fleet_direction = 1

		#Raindrop settings
		self.raindrop_speed = 1.5

		#Moving rectangle settings
		self.box_width = 150
		self.box_height = 450
		self.box_speed = 2.0
		self.box_direction = 1
		self.missed_shots = 0
		self.box_colour = (100,100,230)

		self.speedup_scale = 1.1

		self.initialiase_dynamic_settings()

	def initialiase_dynamic_settings(self):
		"""Initiates speed of all attributes of game"""
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0

	def increase_speed(self):
		"""Gradually increments speed to all atributes of game"""
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale