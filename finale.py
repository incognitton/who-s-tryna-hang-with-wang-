import pygame, sys

pygame.init()

# --- Screen ---
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Drag & Play Platformer")
clock = pygame.time.Clock()
FPS = 60

# --- Physics ---
GRAVITY = 0.8
PLAYER_SPEED = 5
JUMP_STRENGTH = 15
MAX_JUMPS = 2
BOUNCE_STRENGTH = 20

# --- Load images ---
char1_img = pygame.image.load("char1.png").convert_alpha()
char1_img = pygame.transform.scale(char1_img, (50,70))
char2_img = pygame.image.load("char2.png").convert_alpha()
char2_img = pygame.transform.scale(char2_img, (50,70))

grass_img = pygame.image.load("grass.png").convert_alpha()
grass_img = pygame.transform.scale(grass_img, (40,40))

platform_img = pygame.image.load("platform.png").convert_alpha()
platform_img = pygame.transform.scale(platform_img, (40,40))

wall_img = pygame.image.load("wall.png").convert_alpha()
wall_img = pygame.transform.scale(wall_img, (100,100))

trampoline_img = pygame.image.load("trampoline.png").convert_alpha()
trampoline_img = pygame.transform.scale(trampoline_img, (40,40))

reset_img = pygame.image.load("reset.png").convert_alpha()
reset_img = pygame.transform.scale(reset_img, (40,40))

# --- Toolbar ---
TOOLBAR_WIDTH = 100
toolbar_rects = {
    "grass": pygame.Rect(SCREEN_WIDTH-TOOLBAR_WIDTH+10, 20, 40,40),
    "platform": pygame.Rect(SCREEN_WIDTH-TOOLBAR_WIDTH+10, 80, 40,40),
    "wall": pygame.Rect(SCREEN_WIDTH-TOOLBAR_WIDTH+10, 140, 40,40),
    "trampoline": pygame.Rect(SCREEN_WIDTH-TOOLBAR_WIDTH+10, 200, 40,40),
    "reset": pygame.Rect(SCREEN_WIDTH-TOOLBAR_WIDTH+10, 260, 40,40),
    "goal": pygame.Rect(SCREEN_WIDTH-TOOLBAR_WIDTH+10, 320, 50,50)
}

# --- Player ---
player = pygame.Rect(50, SCREEN_HEIGHT-70, 50,50)
player_vel_y = 0
jumps = 0

# --- Draggable elements lists ---
grass_list = []
platform_list = []
wall_list = []
trampoline_list = []
goal_rect = pygame.Rect(700, SCREEN_HEIGHT-70, 50,50)

dragging = None
drag_type = None

# --- Ground ---
ground = pygame.Rect(0, SCREEN_HEIGHT-20, SCREEN_WIDTH-TOOLBAR_WIDTH, 20)

# --- Functions ---
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
    if player.bottom >= SCREEN_HEIGHT-20:
        player.bottom = SCREEN_HEIGHT-20
        player_vel_y = 0
        jumps = 0

def jump():
    global player_vel_y, jumps
    if jumps < 2:
        player_vel_y = -JUMP_STRENGTH
        jumps += 1

def wrap_around():
    if player.right < 0:
        player.left = SCREEN_WIDTH-TOOLBAR_WIDTH
    elif player.left > SCREEN_WIDTH-TOOLBAR_WIDTH:
        player.right = 0
    if player.top > SCREEN_HEIGHT:
        player.bottom = 0
    elif player.bottom < 0:
        player.top = SCREEN_HEIGHT

def reset_objects():
    global grass_list, platform_list, wall_list, trampoline_list
    grass_list = []
    platform_list = []
    wall_list = []
    trampoline_list = []

# --- Main loop ---
running = True
while running:
    dt = clock.tick(FPS)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Mouse down ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            for t_name, t_rect in toolbar_rects.items():
                if t_rect.collidepoint(event.pos):
                    if t_name=="reset":
                        reset_objects()
                    else:
                        dragging = pygame.Rect(mouse_x, mouse_y, t_rect.width, t_rect.height)
                        drag_type = t_name
            # Drag goal
            if goal_rect.collidepoint(event.pos):
                dragging = goal_rect
                drag_type = "goal"

        # --- Mouse up ---
        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                if drag_type=="grass":
                    grass_list.append(dragging)
                elif drag_type=="platform":
                    platform_list.append(dragging)
                elif drag_type=="wall":
                    wall_list.append(dragging)
                elif drag_type=="trampoline":
                    trampoline_list.append(dragging)
                dragging = None
                drag_type = None

        # --- Mouse motion ---
        if event.type == pygame.MOUSEMOTION:
            if dragging and drag_type != "goal":
                dragging.x = mouse_x - dragging.width//2
                dragging.y = mouse_y - dragging.height//2
            elif dragging and drag_type=="goal":
                dragging.x = mouse_x - dragging.width//2
                dragging.y = mouse_y - dragging.height//2

    # --- Player movement ---
    keys = pygame.key.get_pressed()
    handle_movement(keys)
    apply_gravity()
    wrap_around()

    # --- Collisions ---
    # Grass kills
    for g in grass_list:
        if player.colliderect(g):
            player.x, player.y = 50, SCREEN_HEIGHT-70
            player_vel_y = 0
            jumps = 0

    # Platforms
    for p in platform_list:
        if player.colliderect(p) and player_vel_y>=0:
            player.bottom = p.top
            player_vel_y = 0
            jumps = 0

    # Wall climb
    for w in wall_list:
        if player.colliderect(w):
            if keys[pygame.K_UP]:
                player.y -= PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                player.y += PLAYER_SPEED

    # Trampoline
    for t in trampoline_list:
        if player.colliderect(t) and player_vel_y>=0:
            player.bottom = t.top
            player_vel_y = -BOUNCE_STRENGTH
            jumps = 0

    # --- Check win ---
    if player.colliderect(goal_rect):
        print("Char1 reached Char2! ❤️")
        running = False

    # --- Draw ---
    screen.fill((150,200,250))
    # Toolbar background
    pygame.draw.rect(screen, (100,100,100), (SCREEN_WIDTH-TOOLBAR_WIDTH,0,TOOLBAR_WIDTH,SCREEN_HEIGHT))

    # Draw toolbar elements
    screen.blit(grass_img, toolbar_rects["grass"].topleft)
    screen.blit(platform_img, toolbar_rects["platform"].topleft)
    screen.blit(wall_img, toolbar_rects["wall"].topleft)
    screen.blit(trampoline_img, toolbar_rects["trampoline"].topleft)
    screen.blit(reset_img, toolbar_rects["reset"].topleft)
    screen.blit(char2_img, toolbar_rects["goal"].topleft)

    # Draw all placed objects
    for g in grass_list:
        screen.blit(grass_img, (g.x, g.y))
    for p in platform_list:
        screen.blit(platform_img, (p.x, p.y))
    for w in wall_list:
        screen.blit(wall_img, (w.x, w.y))
    for t in trampoline_list:
        screen.blit(trampoline_img, (t.x, t.y))

    # Draw dragging
    if dragging and drag_type!="goal":
        if drag_type=="grass":
            screen.blit(grass_img, (dragging.x, dragging.y))
        elif drag_type=="platform":
            screen.blit(platform_img, (dragging.x, dragging.y))
        elif drag_type=="wall":
            screen.blit(wall_img, (dragging.x, dragging.y))
        elif drag_type=="trampoline":
            screen.blit(trampoline_img, (dragging.x, dragging.y))
    # Draw goal last
    screen.blit(char2_img, (goal_rect.x, goal_rect.y))

    # Draw player
    screen.blit(char1_img, (player.x, player.y))

    # Draw ground
    pygame.draw.rect(screen, (100,250,100), ground)

    pygame.display.flip()

pygame.quit()
sys.exit()