import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from score import Score
from button import Button
from pygame.sprite import Group


class Alien_Invasion():
    """The main class of the game"""


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption(game_settings.screen_caption)

    # Create Play button.
    play_button = Button(game_settings, screen, "Start")

    # Create instance to store game stats and score
    stats = GameStats(game_settings)
    score = Score(game_settings, screen, stats)

    # Background color
    bg_color = game_settings.bg_color

    # Create ship
    ship = Ship(game_settings, screen)
    # Make a group to store bullets in
    bullets = Group()
    aliens = Group()

    # Create fleet of aliens.
    gf.create_fleet(game_settings, screen, ship, aliens)

    # Start the main loop for the game
    while True:
        gf.check_events(game_settings, screen, stats, score, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(game_settings, screen, stats, score, ship, aliens, bullets)
            gf.update_alien(game_settings, stats, screen, score, ship, aliens, bullets)

        gf.update_screen(game_settings, screen, stats, score, ship, aliens, bullets, play_button)


run_game()
