import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH = 400
HEIGHT = 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Define directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Define game variables
player_snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
player_direction = RIGHT
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0
speed = 7
font = pygame.font.Font(None, 24)
obstacles = [(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) for _ in range(20)]
evil_move_delay = 1  # Delay for the evil snake's movement
evil_move_counter = 0

# Function to draw text on the screen
def draw_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x, y))

# Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

# Function to move the player snake
def move_player_snake():
    global player_direction, score, speed
    head = player_snake[0]
    new_head = (head[0] + player_direction[0], head[1] + player_direction[1])
    player_snake.insert(0, new_head)
    if new_head == food:
        generate_food()
        score += 1
        if len(player_snake) % 5 == 0:
            speed += 3
    else:
        player_snake.pop()

# Function to generate food
def generate_food():
    global food
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in player_snake and food not in obstacles:
            break

# Function to move the evil snake
def move_evil_snake():
    global evil_snake, evil_move_counter
    if evil_move_counter == evil_move_delay:
        head = evil_snake[0]
        new_head = (head[0] + evil_direction[0], head[1] + evil_direction[1])
        evil_snake.insert(0, new_head)
        if new_head == food:
            generate_food()
        else:
            evil_snake.pop()
        evil_move_counter = 0
    else:
        evil_move_counter += 1

# Function to update the evil snake's direction
def update_evil_direction():
    global evil_direction
    head = evil_snake[0]
    player_head = player_snake[0]
    dx = player_head[0] - head[0]
    dy = player_head[1] - head[1]
    if abs(dx) > abs(dy):
        evil_direction = (1 if dx > 0 else -1, 0)
    else:
        evil_direction = (0, 1 if dy > 0 else -1)

# Function to handle game over
def game_over():
    screen.fill(BLACK)
    draw_text("Game Over", WIDTH // 2 - 50, HEIGHT // 2 - 10)
    draw_text(f"Final Score: {score}", WIDTH // 2 - 60, HEIGHT // 2 + 20)
    pygame.display.flip()
    pygame.time.wait(5000)  # Pause for 5 seconds before quitting
    pygame.quit()
    sys.exit()

# Main game loop
clock = pygame.time.Clock()
evil_snake = [(GRID_WIDTH // 3, GRID_HEIGHT // 3)]
evil_direction = RIGHT
evil_speed = 3  # Reduced speed for the evil snake
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_direction != DOWN:
                player_direction = UP
            elif event.key == pygame.K_DOWN and player_direction != UP:
                player_direction = DOWN
            elif event.key == pygame.K_LEFT and player_direction != RIGHT:
                player_direction = LEFT
            elif event.key == pygame.K_RIGHT and player_direction != LEFT:
                player_direction = RIGHT

    # Move the player snake
    move_player_snake()

    # Move the evil snake
    move_evil_snake()
    update_evil_direction()

    # Check for collisions with the walls or itself
    head = player_snake[0]
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT or head in player_snake[1:] or head in obstacles:
        game_over()

    # Check for collision with evil snake
    if head in evil_snake:
        game_over()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the grid
    draw_grid()

    # Draw the food
    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, GRAY, (obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the player snake
    for segment in player_snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the evil snake
    for segment in evil_snake:
        pygame.draw.rect(screen, YELLOW, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the score
    draw_text(f"Score: {score}", 5, 5)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(speed)