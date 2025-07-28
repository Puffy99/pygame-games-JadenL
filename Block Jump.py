import pygame
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)

# Game variables
FPS = 60
GRAVITY = 0.3  # Slower falling
JUMP_STRENGTH = -12  # Higher jump
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLATFORM_WIDTH, PLATFORM_HEIGHT = 60, 10


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 100)
        self.vel_y = 0

    def update(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Screen wrap
        if self.rect.right < 0:
            self.rect.left = WIDTH
        if self.rect.left > WIDTH:
            self.rect.right = 0


# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, is_moving=False):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(RED if is_moving else BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_moving = is_moving
        self.vel_x = random.choice([-2, 2]) if is_moving else 0

    def update(self):
        if self.is_moving:
            self.rect.x += self.vel_x
            if self.rect.left <= 0 or self.rect.right >= WIDTH:
                self.vel_x *= -1  # Bounce off edges


def main():
    clock = pygame.time.Clock()

    # Create starting platform
    start_platform = Platform(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 150)
    platforms = pygame.sprite.Group(start_platform)

    # Add random platforms
    for i in range(5):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = i * 100
        is_moving = random.random() < 0.4
        plat = Platform(x, y, is_moving)
        platforms.add(plat)

    # Create player on top of starting platform
    player = Player()
    player.rect.midbottom = start_platform.rect.midtop
    all_sprites = pygame.sprite.Group(player, *platforms)

    score = 0
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.update()
        for plat in platforms:
            plat.update()

        # Collision (falling only)
        if player.vel_y > 0:
            hits = pygame.sprite.spritecollide(player, platforms, False)
            if hits:
                player.rect.bottom = hits[0].rect.top
                player.vel_y = JUMP_STRENGTH

        # Scroll logic
        if player.rect.top <= HEIGHT // 4:
            player.rect.y += abs(player.vel_y)
            for plat in platforms:
                plat.rect.y += abs(player.vel_y)
                if plat.rect.top > HEIGHT:
                    plat.kill()
                    x = random.randint(0, WIDTH - PLATFORM_WIDTH)
                    is_moving = random.random() < 0.4
                    new_plat = Platform(x, -10, is_moving)
                    platforms.add(new_plat)
                    all_sprites.add(new_plat)
                    score += 1

        # Game over
        if player.rect.top > HEIGHT:
            print("Game Over! Score:", score)
            run = False

        win.fill(WHITE)
        all_sprites.draw(win)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
