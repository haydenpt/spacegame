import pygame, os
from pygame.sprite import Sprite

class Ship(Sprite):
    # To manage most behaviors of the ship.

    def __init__(self, game_settings, screen):
        """Initialize the ship , starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('Elements/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()  # Store screen size that the class know the size to align.

        # Align ship position at bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Update the ship's position based on movement flag"""
        # Move the ship if movement flag is true.
        if self.moving_right and self.rect.right < self.screen_rect.right:  # Right
            self.x += self.game_settings.ship_speed

        if self.moving_left and self.rect.left > 0:  # Left
            self.x -= self.game_settings.ship_speed

        if self.moving_up and self.rect.top > (3*(self.screen_rect.bottom)/4):  # Up
            self.y -= self.game_settings.ship_speed

        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:  # Down
            self.y += self.game_settings.ship_speed

        self.rect.centerx = self.x
        self.rect.centery = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center ship"""
        self.center = self.screen_rect.centerx