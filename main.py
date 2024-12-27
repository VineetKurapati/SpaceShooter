import pygame
import random
import os
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Load and scale the background image
background_img = pygame.transform.scale(pygame.image.load("assets/space.png"), (screen_width, screen_height))

# Load images and scale them
spaceship_img = pygame.transform.scale(pygame.image.load("assets/spaceship.png"), (64, 64))
alien_img = pygame.transform.scale(pygame.image.load("assets/alien.png"), (64, 64))

# Set up the player's ship
player_width, player_height = spaceship_img.get_size()
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
player_life = 3  # Initial life count

# Set up the enemies
enemy_width, enemy_height = alien_img.get_size()
enemies = []  # List to store multiple aliens
enemy_speed = 3
enemy_vertical_speed = 30  # Speed of vertical movement when they reach the screen edge

# Set up bullets
bullet_width = 8
bullet_height = 32
bullet_speed = 7
bullets = []

# Set up alien bullets
alien_bullet_width = 8
alien_bullet_height = 32
alien_bullet_speed = 5
alien_bullets = []

# Alien shooting variables
alien_shoot_delay = 60
alien_shoot_timer = alien_shoot_delay  # Initial timer value

# Set up the clock
clock = pygame.time.Clock()

# Set up game variables
score = 0
max_score_file = "max_score.txt"
max_score = 0

# Load font
font = pygame.font.Font(None, 36)

# Function to display text on the screen
def display_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Function to display player's life as a bar
def display_life_bar(life, max_life, x, y, width, height):
    bar_length = (life / max_life) * width
    pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_length, height))
    pygame.draw.rect(screen, (255, 0, 0), (x + bar_length, y, width - bar_length, height), 2)

# Main menu
def main_menu():
    screen.fill((0, 0, 0))  # Clear the screen
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    display_text("Space Shooter", (255, 255, 255), screen_width // 2, screen_height // 3)
    display_text("Press any key to start", (255, 255, 255), screen_width // 2, screen_height // 2)
    display_text(f"High Score: {max_score}", (255, 255, 255), screen_width // 2, screen_height // 2 + 50)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return

# Load max score from file
if os.path.exists(max_score_file):
    with open(max_score_file, "r") as file:
        max_score = int(file.read())

# Function for the alien to shoot bullets
def alien_shoot(enemy_x, enemy_y):
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    angle = math.atan2(dy, dx)
    # Calculate velocity components based on angle
    velocity_x = alien_bullet_speed * math.cos(angle)
    velocity_y = alien_bullet_speed * math.sin(angle)
    # Add bullet with calculated velocity
    bullet_x = enemy_x + enemy_width // 2 - alien_bullet_width // 2
    bullet_y = enemy_y + enemy_height // 2 - alien_bullet_height // 2
    alien_bullets.append([bullet_x, bullet_y, velocity_x, velocity_y])

# Function to spawn a new alien
def spawn_alien():
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = random.randint(50, 200)
    enemies.append([enemy_x, enemy_y])

# Main game loop
running = True
in_menu = True
while running:
    if in_menu:
        main_menu()
        in_menu = False

        # Reset game variables
        score = 0
        player_life = 3
        player_x = screen_width // 2 - player_width // 2

        # Reset bullets
        bullets = []

        # Reset alien bullets
        alien_bullets = []

        # Reset enemies
        enemies = []
        for _ in range(3):  # Start with 3 aliens
            spawn_alien()

        # Reset game time
        start_time = pygame.time.get_ticks()

    # Set background image
    screen.blit(background_img, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate game time
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_left = max(0, 60 - elapsed_time)

    # End the game if time runs out or player life reaches zero
    if time_left == 0 or player_life <= 0:
        screen.fill((0, 0, 0))  # Clear the screen
        display_text("Game Over", (255, 255, 255), screen_width // 2, screen_height // 3)
        display_text(f"Final Score: {score}", (255, 255, 255), screen_width // 2, screen_height // 2)
        display_text("Press any key to play again", (255, 255, 255), screen_width // 2, screen_height // 2 + 50)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_menu = True
                    waiting = False
                    break

    # Move the player's ship
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Move the enemies
    for enemy in enemies:
        enemy[0] += enemy_speed  # Move horizontally
        
        # If alien hits screen boundary, reverse direction and move down
        if enemy[0] <= 0 or enemy[0] >= screen_width - enemy_width:
            enemy_speed = -enemy_speed  # Reverse horizontal movement
            enemy[1] += enemy_vertical_speed  # Move down

        # Alien shoots at regular intervals
        if alien_shoot_timer <= 0:
            alien_shoot(enemy[0], enemy[1])
            alien_shoot_timer = alien_shoot_delay
        else:
            alien_shoot_timer -= 1

    # Draw the player's ship
    screen.blit(spaceship_img, (player_x, player_y))

    # Draw the aliens
    for enemy in enemies:
        screen.blit(alien_img, (enemy[0], enemy[1]))

    # Shoot bullets
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limit bullet count
            bullet_x = player_x + player_width // 2 - bullet_width // 2
            bullet_y = player_y
            bullets.append([bullet_x, bullet_y])

    # Move and draw bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], bullet_width, bullet_height))

    # Check for collision between bullets and top edge of the screen
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Check for collision between bullets and enemies
    for bullet in bullets:
        for enemy in enemies:
            if (enemy[0] < bullet[0] < enemy[0] + enemy_width) and (enemy[1] < bullet[1] < enemy[1] + enemy_height):
                bullets.remove(bullet)
                enemies.remove(enemy)
                player_life = (player_life + 1) if player_life < 3 else player_life  # Increase player's life
                score += 1
                spawn_alien()  # Spawn a new alien when one is destroyed
                break

    # Move and draw alien bullets
    for bullet in alien_bullets:
        bullet[0] += bullet[2]  # Update bullet x position
        bullet[1] += bullet[3]  # Update bullet y position
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], alien_bullet_width, alien_bullet_height))

    # Handle collision with player ship
    for bullet in alien_bullets:
        if (player_x < bullet[0] < player_x + player_width) and (player_y < bullet[1] < player_y + player_height):
            alien_bullets.remove(bullet)
            player_life -= 1  # Decrease player's life

    # Display the score and player's life
    display_text(f"Score: {score}", (255, 255, 255), 100, 30)
    display_life_bar(player_life, 3, 100, 50, 200, 10)

    pygame.display.update()

    # Control the frame rate
    clock.tick(60)

pygame.quit()
