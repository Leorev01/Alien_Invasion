import json

class GameStats:
	"""Track statistics for Alien Invasion"""

	def __init__(self, ai_game):
		"""Initialise statistics."""
		self.settings = ai_game.settings
		self.reset_stats()

		#Start game in inactive status
		self.game_active = False

		#High score should never be reset
		self.high_score = self.get_saved_high_score()

	def reset_stats(self):
		"""Initialise statistics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1

		self.settings.missed_shots = 0

	def get_saved_high_score(self):
		"""Gets high score from file if it exists"""
		try:
			with open('high_score.json') as f:
				return json.load(f)

		except FileNotFoundError:
			return 0
