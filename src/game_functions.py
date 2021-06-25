import sys, os
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, game_settings, screen, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # Move right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:  # Move left
        ship.moving_left = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:  # Move up
        ship.moving_up = True
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # Move down
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:  # Shoot
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # Stop moving right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:  # Stop moving left
        ship.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:  # Stop moving up
        ship.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # Stop moving down
        ship.moving_down = False


def check_events(game_settings, screen, stats, score, play_button, ship, aliens, bullets):
    """Respond to keyboard and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, score, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(game_settings, screen, stats, score, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when click Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset game
        game_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_active = True

        # Reset score
        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ship()

        # Empty aliens & bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(game_settings, screen, stats, score, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop.
    screen.fill(game_settings.bg_color)

    # Draw score information
    score.show_score()

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw button if game inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(game_settings, screen, stats, score, ship, aliens, bullets):
    """Remove old bullets"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Check for bullets that hit alien & remove both
    check_bullet_alien_collision(game_settings, screen, stats, score, ship, aliens, bullets)


def check_bullet_alien_collision(game_settings, screen, stats, score, ship, aliens, bullets):
    """Respond to bullet & alien collisions."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_settings.alien_points * len(aliens)
            score.prep_score()
        check_high_score(stats, score)

    if len(aliens) == 0:
        # If level is cleared, start new level
        bullets.empty()
        game_settings.increase_speed()
        start_new_level(game_settings, screen, stats, score, ship, aliens)

def start_new_level(game_settings, screen, stats, score, ship, aliens):
    """Next level"""
        # Increase level
    stats.level += 1
    score.prep_level()
    create_fleet(game_settings, screen, ship, aliens)


def fire_bullet(game_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def check_fleet_edge(game_settings, aliens):
    """Response when fleet hits edge of screen."""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """Drop fleet and change direction."""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def check_aliens_bottom(game_settings, stats, screen, score, ship, aliens, bullets):
    """Check if any alien hits bottom of screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, screen, score, ship, aliens, bullets)


def update_alien(game_settings, stats, screen, score, ship, aliens, bullets):
    """Update alien positions."""
    check_fleet_edge(game_settings, aliens)
    aliens.update()

    # End game if collide
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, score, ship, aliens, bullets)
        print("Ship hit!!!")

    # End if alien reaches bottom
    check_aliens_bottom(game_settings, stats, screen, score, ship, aliens, bullets)


def get_number_aliens_x(game_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = game_settings.screen_width - (2 * alien_width)  # Leave some space around the border
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 1 alien : 2 alien width -> ? aliens : avlbl width
    return number_aliens_x


def get_number_rows(game_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(game_settings, screen, aliens, alien_number, row_number):
    """Create an aliens and place it in a row."""
    alien = Alien(game_settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.x = alien.x  # rect x of the row
    alien.rect.y = (alien.rect.height * 2) + alien.rect.height * row_number  # rect y of the column
    aliens.add(alien)


def create_fleet(game_settings, screen, ship, aliens):
    """Create a row of alien."""
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Create first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def ship_hit(game_settings, stats, screen, score, ship, aliens, bullets):
    """Respond to ship hit"""
    if stats.ships_left > 0:
        # Decrease lives
        stats.ships_left -= 1

        # Update score board
        score.prep_ship()

        # Empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, score):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        high_score_file = open('highscore.txt', "w")
        high_score_file.write(str(stats.high_score))
        high_score_file.close()
        score.prep_high_score()

