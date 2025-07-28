import pygame
import random

# Define screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define bird properties
bird_size = 15
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_drop_speed = 0
gravity = 0.25
jump_strength = -6

# Define pipe properties
pipe_width = 50
pipe_gap = 150
pipe_speed = 6
pipes = []

# Define game properties
score = 0

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Function to draw the bird
def draw_bird():
    pygame.draw.circle(screen, WHITE, (bird_x, bird_y), bird_size)


# Function to draw pipes
def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, WHITE, pipe)


# Function to generate pipes
def generate_pipe():
    top_pipe_height = random.randint(100, SCREEN_HEIGHT - pipe_gap - 100)
    bottom_pipe_height = SCREEN_HEIGHT - top_pipe_height - pipe_gap
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, top_pipe_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, SCREEN_HEIGHT - bottom_pipe_height, pipe_width, bottom_pipe_height)
    pipes.append(top_pipe)
    pipes.append(bottom_pipe)


# Function to move pipes
def move_pipes():
    for pipe in pipes:
        pipe.x -= pipe_speed


# Function to check collisions
def check_collisions():
    global bird_drop_speed
    for pipe in pipes:
        if pipe.colliderect((bird_x - bird_size, bird_y - bird_size, bird_size * 2, bird_size * 2)):
            return True
    if bird_y >= SCREEN_HEIGHT - bird_size or bird_y <= 0:
        return True
    return False


# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_drop_speed = jump_strength

    # Move bird
    bird_drop_speed += gravity
    bird_y += bird_drop_speed

    # Generate pipes
    if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - pipe_gap * 2:
        generate_pipe()

    # Move pipes
    move_pipes()

    # Check collisions
    if check_collisions():
        print("Game Over!")
        break

    # Clear screen
    screen.fill(BLACK)

    # Draw bird
    draw_bird()

    # Draw pipes
    draw_pipes()

    # Update display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60 )

# Quit Pygame
pygame.quit()
