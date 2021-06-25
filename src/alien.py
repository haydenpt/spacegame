import pygame, os
from pygame.sprite import Sprite


class Alien(Sprite):
    """Alien class of one single alien"""

    def __init__(self, game_settings, screen):
        """Initialize the alien and starting position"""
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load image
        self.image = pygame.image.load('Elements/alien.bmp')
        self.rect = self.image.get_rect()

        # Starting position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store exact position
        self.x = float(self.rect.x)

    def check_edge(self):
        """Return True if fleet hits the edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right."""
        self.x += self.game_settings.alien_speed * self.game_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """Draw alien on screen"""
        self.screen.blit(self.image, self.rect)
