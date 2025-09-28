import pygame
import sys

pygame.init()

# --- Screen & Clock ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Char1 Seeks Char2")
clock = pygame.time.Clock()
FPS = 60

# --- Physics ---
PLAYER_SPEED = 5
GRAVITY = 0.8
JUMP_STRENGTH = 15
MAX_JUMPS = 5  # allow more than 2 jumps

# --- Colors ---
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# --- Load images ---
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

char1_img = pygame.image.load("char1.png").convert_alpha()
char1_img = pygame.transform.scale(char1_img, (50, 50))
char2_img = pygame.image.load("char2.png").convert_alpha()
char2_img = pygame.transform.scale(char2_img, (50, 50))
grass_img = pygame.image.load("grass.png").convert_alpha()
grass_img = pygame.transform.scale(grass_img, (100, 100))  # spike size

# --- Player ---
player = pygame.Rect(50, SCREEN_HEIGHT - 70, 50, 50)
player_vel_y = 0
jumps = 0
on_ground = False

# --- Goal ---
goal = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 70, 50, 50)

# --- Grass panel ---
GRASS_PANEL = pygame.Rect(SCREEN_WIDTH - 60, 0, 60, SCREEN_HEIGHT)
GRASS_SIZE = 40
grasses = []
dragging_grass = None


# --- Helper functions ---
def handle_movement(keys):
    global player
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        jump()

def apply_gravity():
    global player_vel_y, jumps
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # Ground collision
    if player.bottom >= SCREEN_HEIGHT - 20:
        player.bottom = SCREEN_HEIGHT - 20
        player_vel_y = 0
        jumps = 0

def jump():
    global player_vel_y, jumps
    if jumps < MAX_JUMPS:
        player_vel_y = -JUMP_STRENGTH
        jumps += 1

def wrap_around():
    if player.right < 0:
        player.left = SCREEN_WIDTH
    elif player.left > SCREEN_WIDTH:
        player.right = 0
    if player.top > SCREEN_HEIGHT:
        player.bottom = 0
    elif player.bottom < 0:
        player.top = SCREEN_HEIGHT

# --- Main loop ---
running = True
while running:
    dt = clock.tick(FPS)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Drag/drop grass from panel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GRASS_PANEL.collidepoint(event.pos):
                dragging_grass = pygame.Rect(mouse_x, mouse_y, GRASS_SIZE, GRASS_SIZE)
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging_grass:
                grasses.append(dragging_grass)
                dragging_grass = None
        if event.type == pygame.MOUSEMOTION:
            if dragging_grass:
                dragging_grass.x = mouse_x - GRASS_SIZE / 2
                dragging_grass.y = mouse_y - GRASS_SIZE / 2
        


    # --- Player movement ---
    keys = pygame.key.get_pressed()
    handle_movement(keys)
    apply_gravity()
    wrap_around()

    # --- Collisions with grass ---
    for grass in grasses:
        if player.colliderect(grass):
            # Reset player if hit
            player.x, player.y = 50, SCREEN_HEIGHT - 70
            player_vel_y = 0
            jumps = 0

        
    # --- Check if reached goal ---
    if player.colliderect(goal):
        print("Char1 found Char2! ❤️")
        running = False

    # --- DRAW ---
    screen.blit(background, (0, 0))

    # Draw grass panel
    pygame.draw.rect(screen, GRAY, GRASS_PANEL)
    screen.blit(grass_img, (SCREEN_WIDTH - GRASS_SIZE - 10, 20))

    # Draw grasses
    for grass in grasses:
        screen.blit(grass_img, (grass.x, grass.y))

    # Draw dragging grass
    if dragging_grass:
        screen.blit(grass_img, (dragging_grass.x, dragging_grass.y))

    # Draw ground
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))

    # Draw goal
    screen.blit(char2_img, (goal.x, goal.y))

    # Draw player
    screen.blit(char1_img, (player.x, player.y))

    pygame.display.flip()

pygame.quit()
sys.exit()