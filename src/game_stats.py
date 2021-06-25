import os

class GameStats():
    """Game Stats Report"""

    def __init__(self, game_settings):
        """Create stats"""
        self.game_settings = game_settings
        self.reset_stats()

        # Start in inactive state
        self.game_active = False

        # High score should never be reset
        if not os.path.isfile('highscore.txt'):
            self.high_score = 0
        else:
            high_score_file = open('highscore.txt', "r")
            self.high_score = int(high_score_file.read())
            high_score_file.close()

    def reset_stats(self):
        """Stats that change during the game."""
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1
