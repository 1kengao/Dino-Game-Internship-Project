"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
game_state = STATE_MENU
# Used to show high scores, when done instead of just menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
start_time = pygame.time.get_ticks() # returns time since start
score = 0 # initializes the score
high_score = 0 

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
small_font = pygame.font.Font(pygame.font.get_default_font(), 24)
score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))

# Load sprite assets
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))

#Load Menu Assets
title_surf = pygame.image.load("graphics/level/dino_game.png").convert_alpha()
title_surf = pygame.transform.scale_by(title_surf, 4)
title_rect = title_surf.get_rect(center=(400, 130))
press_space_surf = pygame.image.load("graphics/level/press_space.png").convert_alpha()
press_space_surf = pygame.transform.scale_by(press_space_surf, 4)
prompt_rect = press_space_surf.get_rect(center=(400, 240))
retry_rect = press_space_surf.get_rect(center=(400, 260))
game_over_surf = game_font.render("GAME OVER", False, "Black")
game_over_rect = game_over_surf.get_rect(center=(400, 130))



while running:
    # Gets the score based off time survived and renders it center top
    score = (pygame.time.get_ticks() - start_time) // 10
    score_surf = game_font.render(str(score), False, "Black")
    score_rect = score_surf.get_rect(center=(400, 50))
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False
            continue

        if game_state == STATE_PLAYING:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                egg_rect.left = 800
                player_rect.bottomleft = (25, GROUND_Y)
                start_time = pygame.time.get_ticks() # Restarts Timer
                game_state = STATE_PLAYING
    if game_state == STATE_PLAYING:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        pygame.draw.rect(screen, "#c0e8ec", score_rect)
        pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        screen.blit(score_surf, score_rect)

        # Adjust egg's horizontal location then blit it
        egg_rect.x -= 5
        if egg_rect.right <= 0:
            egg_rect.left = 800
        screen.blit(egg_surf, egg_rect)

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        screen.blit(player_surf, player_rect)

        # When player collides with enemy, game ends
        if egg_rect.colliderect(player_rect):
            if score > high_score:
                high_score = score
            game_state = STATE_GAME_OVER
    
    # If game just initialized, shows menu.
    elif game_state == STATE_MENU:
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        screen.blit(player_surf, player_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(press_space_surf, prompt_rect)
    
    # When game is over, display game over message
    else:
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        screen.blit(game_over_surf, game_over_rect)
        final_score_surf = small_font.render(
            f"Score: {score}    Best: {high_score}", False, "Black"
        )
        final_score_rect = final_score_surf.get_rect(center=(400, 200))
        screen.blit(final_score_surf, final_score_rect)
        screen.blit(press_space_surf, retry_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
