"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
import random

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
game_active = False  # Rechanged to video version
GROUND_Y = 300  # The Y-coordinate of the ground level
FLOAT_Y = 215
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
start_time = 0  # Reset to pygame.time.get_ticks() each time the game starts
score = 0
instance_score = 0
high_score = 0

# Load Font
game_font = pygame.font.Font("graphics/font/Minecraft.ttf", 48)
small_font = pygame.font.Font("graphics/font/Minecraft.ttf", 24)

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert_alpha()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert_alpha()

# Load sprite assets
player_walk = [
    pygame.image.load("graphics/player/player_walk_1.png").convert_alpha(),
    pygame.image.load("graphics/player/player_walk_2.png").convert_alpha(),
]
player_jump_surf = pygame.image.load("graphics/player/player_jump.png").convert_alpha()
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

egg_frames = [
    pygame.image.load("graphics/egg/egg_1.png").convert_alpha(),
    pygame.image.load("graphics/egg/egg_2.png").convert_alpha(),
]
egg_index = 0
egg_surf = egg_frames[egg_index]

level_up_surf = pygame.image.load("graphics/player/Level Up.png").convert_alpha()
level_up_rect = level_up_surf.get_rect(center=(400, 200))

# Load Menu Assets
title_surf = pygame.image.load("graphics/level/dino_game.png").convert_alpha()
title_surf = pygame.transform.scale_by(title_surf, 4)
title_rect = title_surf.get_rect(center=(400, 115))
sub_title_surf = game_font.render("Survive Extinction", False, "Black")
sub_title_rect = sub_title_surf.get_rect(center=(400, 180))
press_space_surf = pygame.image.load("graphics/level/press_space.png").convert_alpha()
press_space_surf = pygame.transform.scale_by(press_space_surf, 4)
prompt_rect = press_space_surf.get_rect(center=(400, 240))
retry_rect = press_space_surf.get_rect(center=(400, 260))
game_over_surf = game_font.render("GAME OVER", False, "Black")
game_over_rect = game_over_surf.get_rect(center=(400, 130))

obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)


# Videos way of displaying score instead of mine
def display_score():
    current_score = (pygame.time.get_ticks() - start_time) // 100
    score_surf = game_font.render(str(current_score), False, "Black")
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_score


def player_animation():
    global player_index, player_surf
    if player_rect.bottom < GROUND_Y:
        player_surf = player_jump_surf
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


def obstacle_movement(obstacle_list):
    global egg_index, egg_surf
    if obstacle_list:
        egg_index += 0.1
        if egg_index >= len(egg_frames):
            egg_index = 0
        egg_surf = egg_frames[int(egg_index)]
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8
            screen.blit(egg_surf, obstacle_rect)
        return [obstacle for obstacle in obstacle_list if obstacle.right > 0]
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        if game_active:
            if event.type == obstacle_timer:
                if random.randint(0, 2) == 0:
                    spawn_y = FLOAT_Y
                else:
                    spawn_y = GROUND_Y
                obstacle_rect_list.append(
                    egg_surf.get_rect(bottomleft=(random.randint(900, 1100), spawn_y))
                )
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and player_rect.bottom >= GROUND_Y:
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_rect.bottomleft = (25, GROUND_Y)
                players_gravity_speed = 0
                obstacle_rect_list = []
                start_time = pygame.time.get_ticks()  # Restarts Timer
                game_active = True

    if game_active:
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        score = display_score()

        players_gravity_speed += 1.75
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        player_animation()
        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Levels 'UP' the player once it reaches a threshold.
        if score % 25 == 0 and score != 0:
            screen.blit(level_up_surf, level_up_rect)

        if not collisions(player_rect, obstacle_rect_list):
            if score > high_score:
                high_score = score
            instance_score = score
            game_active = False

    else:
        # Remade Menu and Game Over Screen into combined one
        screen.fill("lightblue")
        screen.blit(GROUND_SURF, (0, GROUND_Y))

        if instance_score == 0:
            # First-time menu
            screen.blit(title_surf, title_rect)
            screen.blit(sub_title_surf, sub_title_rect)
            screen.blit(press_space_surf, prompt_rect)
        else:
            # Game-over view
            screen.blit(game_over_surf, game_over_rect)
            final_score_surf = small_font.render(
                f"Your Score: {instance_score}   Best: {high_score}",
                False, "Black",
            )
            final_score_rect = final_score_surf.get_rect(center=(400, 200))
            screen.blit(final_score_surf, final_score_rect)
            screen.blit(press_space_surf, retry_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
