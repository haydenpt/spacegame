import pygame.font


class Button():

    def __init__(self, game_settings, screen, msg):
        """Create button"""
        self.game_settings = game_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Button size
        self.width, self.height = 200, 50
        self.button_color = (0, 100, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('C:/Windows/Fonts/BAUHS93.TTF', 40)

        # Create button rect and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn message into image and center on button."""
        self.msg_imgage = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_imgage_rect = self.msg_imgage.get_rect()
        self.msg_imgage_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_imgage, self.msg_imgage_rect)
