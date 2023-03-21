import pygame
import random
import os
import sys

# Constants
START_WIDTH = 800
START_HEIGHT = 600
WIDTH_INCREASE = 200
HEIGHT_INCREASE = 100
PLAYER_SPEED = 5
FIREBALL_SPEED = 4
NUM_FIREBALLS = 10
BOSS_SPEED = 2
BLUE_LASER_SPEED = 10
FPS = 60
FIREBALL_SPAWN_RATE= 10

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

level = 1
WIDTH, HEIGHT = START_WIDTH, START_HEIGHT

def update_dimensions(level):
    global WIDTH, HEIGHT
    WIDTH = START_WIDTH + WIDTH_INCREASE * (level - 1)
    HEIGHT = START_HEIGHT + HEIGHT_INCREASE * (level - 1)
    return WIDTH, HEIGHT



def check_level_completion(player, level_width):
    return player.rect.x >= level_width - player.rect.width

def update_num_fireballs(level):
    return NUM_FIREBALLS + level * 2

# Player class
class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__()
        self.image = pygame.image.load('dinosaur.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = 50
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.y < self.HEIGHT - self.rect.height:
            self.rect.y += PLAYER_SPEED
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.x < self.WIDTH - self.rect.width:
            self.rect.x += PLAYER_SPEED

    def load_image(self):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(script_dir, "dinosaur.png")
        print("Loading dinosaur image from:", image_path)
        try:
            image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print("Error loading dinosaur image:", e)
            sys.exit()

        SCALE_FACTOR = 0.15
        image = pygame.transform.scale(image, (int(image.get_width() * SCALE_FACTOR), int(image.get_height() * SCALE_FACTOR)))

        return image

# Fireball class
class fireball(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        self.image = pygame.image.load("fireball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-500, -100)

    def update(self):
        self.rect.x -= FIREBALL_SPEED
        if self.rect.right < 0:
            self.rect.x = random.randrange(self.WIDTH, self.WIDTH + 100)
            self.rect.y = random.randrange(0, self.HEIGHT - self.rect.height)


    def update_num_fireballs(level):
        if level == 1:
            return 2
        elif level == 2:
            return 4
        elif level == 3:
            return 6
        else:
            return 0


# Blue Laser class
class bluelaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 5))


# Boss class
class boss(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        self.image = pygame.image.load("boss.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.rect.y = 0


    def update(self):
        self.rect.y += random.choice([-1, 1]) * BOSS_SPEED
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > self.HEIGHT - self.rect.height:
            self.rect.y = self.HEIGHT - self.rect.height

    def hit(self):
        self.hit_count += 1
        



def game_loop(level):
    WIDTH, HEIGHT = update_dimensions(level)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fireball Game - Level {}".format(level))
    all_sprites = pygame.sprite.Group()
    fireballs = pygame.sprite.Group()


    if level <= 4:
        
        for _ in range(update_num_fireballs(level)):
            fireball = fireball(WIDTH, HEIGHT)
            all_sprites.add(fireball)
            fireballs.add(fireball)
            
    if level == 4:
        boss = boss(WIDTH, HEIGHT)
        all_sprites.add(boss)
    else:
        for _ in range(update_num_fireballs(level)):
            fireball = fireball(WIDTH, HEIGHT)
            all_sprites.add(fireball)
            fireballs.add(fireball)



    running = True    
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        all_sprites.update()

        if pygame.sprite.spritecollide(player, fireballs, False):
            running = False

        if check_level_completion(player, WIDTH):
            level += 1
            running = False

        screen.fill(GREEN)
        all_sprites.draw(screen)
        pygame.display.flip()





        if level <= 4:
            game_loop(level)
            
            hits = pygame.sprite.spritecollide(player, fireballs, False)

            
        if hits:
                game_over = True
                
    else:
            if pygame.sprite.collide_rect(player, boss):
                game_over = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    blue_laser = bluelaser(player.rect.right, player.rect.centery)
                    all_sprites.add(blue_laser)
                    blue_lasers.add(blue_laser)

            hits = pygame.sprite.spritecollide(boss, bluelaser, True)
            for hit in hits:
                boss.hit()
                if boss.hit_count >= 3:
                    game_over = True
                    break


def main():
    if __name__ == "__main__":
        player = player(WIDTH, HEIGHT)
        level = 1
    while True:
        game_loop(level, player)
        level += 1

    while level <= 4:  # Change the upper limit to 4 to include the boss level
        game_loop(level)
        level += 1
        

game_loop(level)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireball Dodger")
clock = pygame.time.Clock()

# Sprite groups
all_sprites = pygame.sprite.Group()
fireballs = pygame.sprite.Group(fireball)
player = player(WIDTH, HEIGHT)
all_sprites.add(player)

# Game loop
running = True
spawn_timer = 0
while running:
    clock.tick(FPS)

    # Fireball spawning
    spawn_timer += 1
    if spawn_timer >= FIREBALL_SPAWN_RATE:
        fireball = fireball(WIDTH,HEIGHT)
        all_sprites.add(fireball)
        fireballs.add(fireball)
        spawn_timer = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollide(player, fireballs, True):
        running = False

    # Check if player reached the other end
    if player.rect.x + player.rect.width >= WIDTH:
        print("You won!")
        running = False

    # Draw
    screen.fill(0)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
