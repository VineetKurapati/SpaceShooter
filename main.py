import pygame
import random
import os

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

# Set up the enemy
enemy_width, enemy_height = alien_img.get_size()
enemy_x = random.randint(0, screen_width - enemy_width)
enemy_y = random.randint(50, 200)
enemy_speed = 3

# Set up bullets
bullet_width = 8
bullet_height = 32
bullet_speed = 7
bullets = []

# Set up the clock
clock = pygame.time.Clock()

# Set up game variables
bullet_count = 0
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

# Main game loop
running = True
in_menu = True
while running:
    if in_menu:
        main_menu()
        in_menu = False

        # Reset game variables
        score = 0
        player_x = screen_width // 2 - player_width // 2
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = random.randint(50, 200)

        # Reset bullet count and bullets
        bullet_count = 0
        bullets = []

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

    # End the game if time runs out
    if time_left == 0:
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

    # Move the enemy
    enemy_x += enemy_speed
    if enemy_x <= 0 or enemy_x >= screen_width - enemy_width:
        enemy_speed = -enemy_speed

    # Draw the player's ship and the enemy
    screen.blit(spaceship_img, (player_x, player_y))
    screen.blit(alien_img, (enemy_x, enemy_y))

    # Shoot bullets
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limit bullet count
            bullet_x = player_x + player_width // 2 - bullet_width // 2
            bullet_y = player_y
            bullets.append([bullet_x, bullet_y])
            bullet_count += 1

    # Move and draw bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], bullet_width, bullet_height))

    # Check for collision between bullets and top edge of the screen
    for bullet in bullets.copy():
        if bullet[1] <= 0:
            bullets.remove(bullet)

    # Check for collision between bullets and enemy
    for bullet in bullets:
        if (enemy_x < bullet[0] < enemy_x + enemy_width) and (enemy_y < bullet[1] < enemy_y + enemy_height):
            bullets.remove(bullet)
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = random.randint(50, 200)
            score += 1

    # Update max score if needed
    max_score = max(max_score, score)

    # Display score and time left
    display_text(f"Score: {score}", (255, 255, 255), 100, 20)
    display_text(f"Time Left: {time_left}", (255, 255, 255), screen_width - 100, 20)

    pygame.display.update()
    clock.tick(60)

# Save max score to file
with open(max_score_file, "w") as file:
    file.write(str(max_score))

# Quit Pygame
pygame.quit()
