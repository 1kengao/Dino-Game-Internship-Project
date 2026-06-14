"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
"""

import pygame
import random # Imported for spawn logic
import math

# Initialize Pygame and create a window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 400), pygame.SCALED)
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
game_active = False  # Rechanged to video version
GROUND_Y = 300  # The Y-coordinate of the ground level
FLOAT_Y = 215  # Y- Coordinate for High Level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
start_time = 0  # Reset to pygame.time.get_ticks() each time the game starts
score = 0
instance_score = 0
high_score = 0

# Load Difficulty Scaler
LEVEL_INTERVAL = 50 # The Amount needed to level up
STARTING_OBSTACLE_SPEED = 8 # Starting speed of objects
STARTING_SPAWN_INTERVAL = 1400 # Starting rate the Objects spawn 
SPEED_INCREASE = 1 # Interval that speed increases when leveling up
SPAWN_DECREASE = 100 # Interval Spawn rate decreases by when leveling up
MIN_SPAWN_INTERVAL = 600 # limit for spawn rate
LEVEL_UP_DISPLAY = 500 # How long Level Up png is shown
level = 1
obstacle_speed = STARTING_OBSTACLE_SPEED
spawn_interval = STARTING_SPAWN_INTERVAL
level_up_time = 0

# Boss Variables
BOSS_LEVEL = 4
BOSS_DURATION = 20000
BOSS_SPAWN_INTERVAL = 750
BOSS_OBSTACLE_SPEED = 10
boss_active = False
boss_start_time = 0
boss_defeated_time = 0
level_offset = 0

# Load Font
game_font = pygame.font.Font("graphics/font/Minecraft.ttf", 48)
small_font = pygame.font.Font("graphics/font/Minecraft.ttf", 24)

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert_alpha()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert_alpha()
FOREST_SURF = pygame.transform.scale(pygame.image.load("graphics/level/forest.png").convert_alpha(), (800, 300))
FOREST_GROUND_SURF = pygame.image.load("graphics/level/forest_ground.png").convert_alpha()
SUNSET_SURF = pygame.transform.scale(pygame.image.load("graphics/level/sunset.png").convert_alpha(), (800, 300))
SUNSET_GROUND_SURF = pygame.image.load("graphics/level/sunset_ground.png").convert_alpha()
BOSS_BACKGROUND_SURF = pygame.transform.scale(pygame.image.load("graphics/level/boss_background.png").convert_alpha(), (800, 400))
BOSS_BACKGROUND_BOTTOM_SURF = pygame.image.load("graphics/level/boss_background_bottom.png").convert_alpha()

# Load sprite assets - New Assets Added for Animation
player_walk = [
    pygame.image.load("graphics/player/level_1_walk_1.png").convert_alpha(),
    pygame.image.load("graphics/player/level_1_walk_2.png").convert_alpha(),
]
player_jump_surf = pygame.image.load("graphics/player/level_1_jump.png").convert_alpha()
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))

# Load Enemy assets - Also Added Animations 
egg_frames = [
    pygame.image.load("graphics/enemy/egg_1.png").convert_alpha(),
    pygame.image.load("graphics/enemy/egg_2.png").convert_alpha(),
]
egg_index = 0
egg_surf = egg_frames[egg_index]

# Originals for resetting on restart
LEVEL_1_WALK = player_walk
LEVEL_1_JUMP_SURF = player_jump_surf
DEFAULT_ENEMY_FRAMES = egg_frames

# Cat Used for Level 2 Animations
LEVEL_2_SIZE = (64, 64)
LEVEL_2_WALK = [
    pygame.transform.scale(pygame.image.load("graphics/player/level_2_walk_1.png").convert_alpha(), LEVEL_2_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/player/level_2_walk_2.png").convert_alpha(), LEVEL_2_SIZE),
]
LEVEL_2_JUMP_SURF = pygame.transform.scale(pygame.image.load("graphics/player/level_2_jump.png").convert_alpha(), LEVEL_2_SIZE)
# Asteroid used for Level 2 Enemies
ASTEROID_SIZE = (64, 64) # Rescaled as they were too large originally
ASTEROID_FRAMES = [
    pygame.transform.scale(pygame.image.load("graphics/enemy/horizontal_fire_1.png").convert_alpha(), ASTEROID_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/enemy/horizontal_fire_2.png").convert_alpha(), ASTEROID_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/enemy/horizontal_fire_3.png").convert_alpha(), ASTEROID_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/enemy/horizontal_fire_4.png").convert_alpha(), ASTEROID_SIZE),
]

# Level 3 Player Animations 
LEVEL_3_SIZE = (100, 100)
LEVEL_3_WALK = [
    pygame.transform.scale(pygame.image.load("graphics/player/level_3_walk_1.png").convert_alpha(), LEVEL_3_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/player/level_3_walk_2.png").convert_alpha(), LEVEL_3_SIZE),
]
LEVEL_3_JUMP_SURF = LEVEL_3_WALK[0]  # placeholder 

# Recolored Fire used for Level 3 Enemies
RECOLORED_FIRE_SIZE = (64, 64)
RECOLORED_FIRE_FRAMES = [
    pygame.transform.scale(pygame.image.load("graphics/enemy/recolored_fire_1.png").convert_alpha(), RECOLORED_FIRE_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/enemy/recolored_fire_2.png").convert_alpha(), RECOLORED_FIRE_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/enemy/recolored_fire_3.png").convert_alpha(), RECOLORED_FIRE_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/enemy/recolored_fire_4.png").convert_alpha(), RECOLORED_FIRE_SIZE),
]

# Free Asset Gotten off Online
LEVEL_4_SIZE = (78, 78)
LEVEL_4_WALK = [
    pygame.transform.scale(pygame.image.load("graphics/player/level_4_walk_1.png").convert_alpha(), LEVEL_4_SIZE),
    pygame.transform.scale(pygame.image.load("graphics/player/level_4_walk_2.png").convert_alpha(), LEVEL_4_SIZE),
]
LEVEL_4_JUMP_SURF = pygame.transform.scale(pygame.image.load("graphics/player/level_4_jump.png").convert_alpha(), LEVEL_4_SIZE)

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
mascot_surf = pygame.image.load("graphics/level/mascot.png").convert_alpha()
boss_defeated_surf = game_font.render("BOSS DEFEATED", False, "Black")
boss_defeated_rect = boss_defeated_surf.get_rect(center=(400, 250))
fullscreen_hint_surf = small_font.render("Press F for Fullscreen", False, "Black")
fullscreen_hint_rect = fullscreen_hint_surf.get_rect(center=(400, 385))

obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
# Switched from constant to Variable to use the level scaling
pygame.time.set_timer(obstacle_timer, STARTING_SPAWN_INTERVAL) 


# Videos way of displaying score instead of mine
def display_score():
    current_score = (pygame.time.get_ticks() - start_time) // 100
    score_surf = game_font.render(str(current_score), False, "Black")
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_score

# Videos way for Player animations
def player_animation():
    global player_index, player_surf
    if player_rect.bottom < GROUND_Y:
        player_surf = player_jump_surf
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

# Videos way for Obstacles
def obstacle_movement(obstacle_list):
    global egg_index, egg_surf
    if obstacle_list:
        egg_index += 0.1
        if egg_index >= len(egg_frames):
            egg_index = 0
        egg_surf = egg_frames[int(egg_index)]
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= obstacle_speed
            screen.blit(egg_surf, obstacle_rect)
        return [obstacle for obstacle in obstacle_list if obstacle.right > 0]
    else:
        return []

# Checks collisions for a list like in video
def collisions(player, obstacles):
    player_hitbox = player_surf.get_bounding_rect().move(player.x, player.y)
    if obstacles:
        enemy_bb = egg_surf.get_bounding_rect()
        for obstacle_rect in obstacles:
            if player_hitbox.colliderect(enemy_bb.move(obstacle_rect.x, obstacle_rect.y)):
                return False
    return True

def animate_mascot():
    t = pygame.time.get_ticks() / 1000
    for i, base_x in enumerate((140, 660)):
        bob = math.sin(t * 3 + i * math.pi) * 12
        surf = pygame.transform.flip(mascot_surf, i == 1, False)
        rect = surf.get_rect(center=(base_x, 235 + bob))
        screen.blit(surf, rect)

# Boss Bar Animation (Health Bar but its just based off time) and Boss Animation (Up and Down)
def draw_boss(fraction):
    t = pygame.time.get_ticks() / 1000
    bob = math.sin(t * 2) * 10
    boss = pygame.transform.scale(mascot_surf, (150, 150))
    screen.blit(boss, boss.get_rect(center=(670, 150 + bob)))
    pygame.draw.rect(screen, "red", (250, 12, 300, 10))
    pygame.draw.rect(screen, "green", (250, 12, int(300 * fraction), 10))
    pygame.draw.rect(screen, "black", (250, 12, 300, 10), 2)

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except (pygame.error, FileNotFoundError):
        return None

def play_sound(sound):
    if sound:
        sound.play()

jump_sound = load_sound("audio/jump.wav")
death_sound = load_sound("audio/death.wav")
level_up_sound = load_sound("audio/level_up.wav")
boss_defeated_sound = load_sound("audio/boss_defeated.wav")


while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            # When the user presses F, it turns into full screen
            pygame.display.toggle_fullscreen()
        if game_active:
            # Random Enemy Spawn Logic
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
                play_sound(jump_sound)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Resets Everything for Next Run
                players_gravity_speed = 0
                obstacle_rect_list = []
                start_time = pygame.time.get_ticks()
                boss_active = False
                boss_defeated_time = 0
                level_offset = 0
                level = 1
                obstacle_speed = STARTING_OBSTACLE_SPEED
                spawn_interval = STARTING_SPAWN_INTERVAL # Changed these to use level variables
                pygame.time.set_timer(obstacle_timer, spawn_interval)
                level_up_time = 0
                player_walk = LEVEL_1_WALK
                player_jump_surf = LEVEL_1_JUMP_SURF
                egg_frames = DEFAULT_ENEMY_FRAMES
                egg_surf = egg_frames[0]
                player_rect = player_walk[0].get_rect(bottomleft=(25, GROUND_Y))
                game_active = True

    if game_active:
        if boss_active:
            screen.blit(BOSS_BACKGROUND_SURF, (0, 0))
            screen.blit(BOSS_BACKGROUND_BOTTOM_SURF, (0, GROUND_Y))
        elif level >= 3:
            screen.blit(SUNSET_SURF, (0, 0))
            screen.blit(SUNSET_GROUND_SURF, (0, GROUND_Y))
        elif level >= 2:
            screen.blit(FOREST_SURF, (0,0))
            screen.blit(FOREST_GROUND_SURF, (0, GROUND_Y))
        else:
            screen.blit(SKY_SURF, (0, 0))
            screen.blit(GROUND_SURF, (0, GROUND_Y))
        score = display_score()

        players_gravity_speed += 1.2
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
        player_animation() # Players Animation
        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Levels 'UP' the player once it reaches a threshold.
        if not boss_active and (score - level_offset) // LEVEL_INTERVAL + 1 > level:
            level = (score - level_offset) // LEVEL_INTERVAL + 1
            obstacle_speed += SPEED_INCREASE
            spawn_interval = max(MIN_SPAWN_INTERVAL, spawn_interval - SPAWN_DECREASE)
            pygame.time.set_timer(obstacle_timer, spawn_interval)
            level_up_time = pygame.time.get_ticks()
            play_sound(level_up_sound)
            # Beyond level 2: swap player to Cat and egg to Asteroid
            if level >= 2:
                player_walk = LEVEL_2_WALK
                player_jump_surf = LEVEL_2_JUMP_SURF
                player_rect = player_walk[0].get_rect(midbottom=player_rect.midbottom)
                egg_frames = ASTEROID_FRAMES
                egg_surf = egg_frames[0]
            # Level 3: swap to Level 3 player and Recolored Fire enemy
            if level >= 3:
                player_walk = LEVEL_3_WALK
                player_jump_surf = LEVEL_3_JUMP_SURF
                player_rect = player_walk[0].get_rect(midbottom=player_rect.midbottom)
                egg_frames = RECOLORED_FIRE_FRAMES
                egg_surf = egg_frames[0]
            if level >= BOSS_LEVEL:
                boss_active = True
                boss_start_time = pygame.time.get_ticks()
                obstacle_speed = BOSS_OBSTACLE_SPEED
                egg_frames = DEFAULT_ENEMY_FRAMES
                egg_surf = egg_frames[0]
                player_walk = LEVEL_4_WALK
                player_jump_surf = LEVEL_4_JUMP_SURF
                player_rect = player_walk[0].get_rect(midbottom=player_rect.midbottom)
                pygame.time.set_timer(obstacle_timer, BOSS_SPAWN_INTERVAL)
        # Blits the level up screen for longer. Uses the difference in current time and time it reached
        # the interval to hold the level up time for level_up_displays length
        if level_up_time and pygame.time.get_ticks() - level_up_time < LEVEL_UP_DISPLAY:
            screen.blit(level_up_surf, level_up_rect)

        # Boss Fight
        if boss_active:
            boss_fraction = 1 - (pygame.time.get_ticks() - boss_start_time) / BOSS_DURATION
            draw_boss(boss_fraction)
            # Whenever Boss Fight is finished, it resets everything similar to a game restart
            if boss_fraction <= 0:
                boss_active = False
                boss_defeated_time = pygame.time.get_ticks()
                play_sound(boss_defeated_sound)
                level_offset = score
                level = 1
                obstacle_speed = STARTING_OBSTACLE_SPEED
                spawn_interval = STARTING_SPAWN_INTERVAL
                pygame.time.set_timer(obstacle_timer, spawn_interval)
                obstacle_rect_list = []
                player_walk = LEVEL_1_WALK
                player_jump_surf = LEVEL_1_JUMP_SURF
                player_rect = player_walk[0].get_rect(bottomleft=(25, GROUND_Y))
                egg_frames = DEFAULT_ENEMY_FRAMES
                egg_surf = egg_frames[0]

        # When Bossfight is finished, it shows boss defeated aswell
        if boss_defeated_time and pygame.time.get_ticks() - boss_defeated_time < 1500:
            screen.blit(boss_defeated_surf, boss_defeated_rect)

        if not collisions(player_rect, obstacle_rect_list):
            if score > high_score:
                high_score = score
            instance_score = score
            game_active = False
            play_sound(death_sound)

    else:
        # Remade Menu and Game Over Screen into combined one
        screen.fill("lightblue")
        screen.blit(GROUND_SURF, (0, GROUND_Y))

        if instance_score == 0:
            # First-time menu
            screen.blit(title_surf, title_rect)
            screen.blit(sub_title_surf, sub_title_rect)
            screen.blit(press_space_surf, prompt_rect)
            animate_mascot()
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

        screen.blit(fullscreen_hint_surf, fullscreen_hint_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
