import pygame.font

class Difficulty:
	"""Initiates a class that allows user to select difficulty before starting game"""
	def __init__(self, ai_game, msg):
		"""Initialise difficulty button attributes"""
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()

		#Set dimensions and properties of the buttons
		self.width, self.height = 150, 37.5
		