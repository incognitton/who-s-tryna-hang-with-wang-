import pygame
import sys
import os

pygame.init()

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Physics
PLAYER_SPEED = 5
JUMP_STRENGTH = 15
GRAVITY = 0.8
MAX_JUMPS = 2

# Colors
WHITE = (255, 255, 255)
MAGENTA = (255, 0, 255)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer — 2 Players")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

# --- Load background ---
try:
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("Loaded background.png")
except Exception as e:
    print("Warning: couldn't load background.png —", e)
    background = None

# --- Load characters ---
def load_char(filename, default_size=(50, 50)):
    try:
        img = pygame.image.load(filename).convert_alpha()
        w, h = img.get_size()
        if w > 300 or h > 300:
            img = pygame.transform.scale(img, (100, 100))
        return img
    except Exception as e:
        print(f"Warning: couldn't load {filename} —", e)
        return None

char1_img = load_char("char1.png")
char2_img = load_char("char2.png")

if char2_img:
    char2_img = pygame.transform.scale(char2_img, (33, 45))

if char1_img:
    char1_img = pygame.transform.scale(char1_img, (33, 45))

# Player data (rect, velocity, jumps, on_ground)
player1 = pygame.Rect(100, SCREEN_HEIGHT - 100, 50, 50)
p1_vel_y = 0
p1_jumps = 0
p1_on_ground = False

player2 = pygame.Rect(700, SCREEN_HEIGHT - 100, 50, 50)
p2_vel_y = 0
p2_jumps = 0
p2_on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),
    pygame.Rect(200, 450, 200, 20),
    pygame.Rect(500, 300, 200, 20),
]

# --- Movement & physics helpers ---
def handle_movement(keys, player, left, right):
    if keys[left]:
        player.x -= PLAYER_SPEED
    if keys[right]:
        player.x += PLAYER_SPEED

def apply_gravity(player, vel_y, jumps):
    vel_y += GRAVITY
    player.y += vel_y
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat) and vel_y >= 0:
            player.bottom = plat.top
            vel_y = 0
            on_ground = True
            jumps = 0
    return vel_y, jumps, on_ground

def jump(vel_y, jumps):
    if jumps < MAX_JUMPS:
        vel_y = -JUMP_STRENGTH
        jumps += 1
    return vel_y, jumps

def wrap_around(player):
    if player.right < 0:
        player.left = SCREEN_WIDTH
    elif player.left > SCREEN_WIDTH:
        player.right = 0
    if player.top > SCREEN_HEIGHT:
        player.bottom = 0

# --- Game loop ---
running = True
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Player 1 jump (arrows + space)
            if event.key in (pygame.K_UP, pygame.K_SPACE):
                p1_vel_y, p1_jumps = jump(p1_vel_y, p1_jumps)
            # Player 2 jump (W)
            if event.key == pygame.K_w:
                p2_vel_y, p2_jumps = jump(p2_vel_y, p2_jumps)

    keys = pygame.key.get_pressed()
    handle_movement(keys, player1, pygame.K_LEFT, pygame.K_RIGHT)
    handle_movement(keys, player2, pygame.K_a, pygame.K_d)

    p1_vel_y, p1_jumps, p1_on_ground = apply_gravity(player1, p1_vel_y, p1_jumps)
    p2_vel_y, p2_jumps, p2_on_ground = apply_gravity(player2, p2_vel_y, p2_jumps)

    wrap_around(player1)
    wrap_around(player2)

    # --- DRAW ---
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(WHITE)

    for plat in platforms:
        pygame.draw.rect(screen, WHITE, plat)

    # Draw players
    if char1_img:
        screen.blit(char1_img, (player1.x, player1.y))
    else:
        pygame.draw.rect(screen, MAGENTA, player1)

    if char2_img:
        screen.blit(char2_img, (player2.x, player2.y))
    else:
        pygame.draw.rect(screen, (0, 200, 200), player2)

    pygame.display.flip()

pygame.quit()
sys.exit()