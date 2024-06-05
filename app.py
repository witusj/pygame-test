import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 20
PIZZA_WIDTH = 50
PIZZA_HEIGHT = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Pizzas")

# Load images
player_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
player_image.fill(RED)
pizza_image = pygame.Surface((PIZZA_WIDTH, PIZZA_HEIGHT))
pizza_image.fill(WHITE)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        # Keep player within screen bounds
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

# Pizza class
class Pizza(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pizza_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - PIZZA_WIDTH)
        self.rect.y = 0

    def update(self):
        self.rect.y += 5
        # Remove pizza if it goes off the bottom of the screen
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
pizzas = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create a new pizza occasionally
    if random.randint(1, 20) == 1:
        pizza = Pizza()
        all_sprites.add(pizza)
        pizzas.add(pizza)

    # Update sprites
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollideany(player, pizzas):
        print("Caught a pizza! Yum!")
        pygame.sprite.spritecollide(player, pizzas, True)

    # Check if any pizzas hit the bottom
    for pizza in pizzas:
        if pizza.rect.y > SCREEN_HEIGHT:
            print("Missed a pizza! Game Over!")
            running = False

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
