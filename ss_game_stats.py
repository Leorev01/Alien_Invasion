class GameStats:
	"""Track statistics for Sideways Shooter"""
	def __init__(self, ss_game):

		self.settings = ss_game.settings
		self.reset_stats()

		#Stops the game after loss of all ships
		self.game_active = True

	def reset_stats(self):
		self.ships_left = self.settings.ship_limit