import pygame
import random

CELL        = 20
COLS        = 40      
ROWS        = 27  
HUD_H       = 60
SCREEN_W    = COLS * CELL
SCREEN_H    = ROWS * CELL + HUD_H
BASE_FPS    = 10

UP    = ( 0, -1); DOWN  = ( 0,  1)
LEFT  = (-1,  0); RIGHT = ( 1,  0)

BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
BG          = (30,  30,  30)
GRID_LINE   = (45,  45,  45)
SNAKE_HEAD  = (0,   210, 80)
SNAKE_BODY  = (0,   160, 60)
SNAKE_EYE   = (255, 255, 255)
RED         = (220, 50,  50)
YELLOW      = (255, 220, 0)
ORANGE      = (255, 140, 0)
PURPLE      = (180, 60,  200)
SILVER      = (192, 192, 192)
CYAN        = (0,   255, 255)
BLUE        = (0,   0,   255)
MAGENTA     = (255, 0,   255)
DARK_RED    = (139, 0,   0)
GRAY        = (100, 100, 100)

FOOD_TYPES = [
    {"label": "Apple",  "value": 10, "colour": RED,    "weight": 50, "lifetime": None},
    {"label": "Orange", "value": 20, "colour": ORANGE, "weight": 30, "lifetime": 50},
    {"label": "Grape",  "value": 30, "colour": PURPLE, "weight": 15, "lifetime": 30},
    {"label": "Star",   "value": 50, "colour": YELLOW, "weight": 5,  "lifetime": 20},
]
MAX_FOOD = 4


def weighted_choice(items):
    total, roll, running = sum(i["weight"] for i in items), random.randint(1, sum(i["weight"] for i in items)), 0
    for item in items:
        running += item["weight"]
        if roll <= running:
            return item
    return items[-1]

class Food:
    def __init__(self, occupied):
        ft = weighted_choice(FOOD_TYPES)
        self.label, self.value, self.colour, self.lifetime = ft["label"], ft["value"], ft["colour"], ft["lifetime"]
        self.age = 0
        free = [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) not in occupied]
        self.pos = random.choice(free) if free else (COLS // 2, ROWS // 2)

    def update(self):
        if self.lifetime:
            self.age += 1
            return self.age >= self.lifetime
        return False

    def fraction(self):
        return max(0.0, 1.0 - self.age / self.lifetime) if self.lifetime else None

    def draw(self, surface):
        col, row = self.pos
        px, py = col * CELL + CELL // 2, row * CELL + CELL // 2 + HUD_H
        frac = self.fraction()
        if frac is not None:
            surf = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
            alpha = int(80 + 175 * frac)
            r, g, b = self.colour
            pygame.draw.circle(surf, (r, g, b, alpha), (CELL // 2, CELL // 2), CELL // 2 - 2)
            surface.blit(surf, (col * CELL, row * CELL + HUD_H))
            pygame.draw.circle(surface, WHITE, (px, py), CELL // 2 - 1, 2)
        else:
            pygame.draw.circle(surface, self.colour, (px, py), CELL // 2 - 2)
        font_s = pygame.font.SysFont("arial", 11, bold=True)
        txt = font_s.render(str(self.value), True, WHITE if self.colour != YELLOW else BLACK)
        surface.blit(txt, txt.get_rect(center=(px, py)))

class Poison:
    def __init__(self, occupied):
        free = [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) not in occupied]
        self.pos = random.choice(free) if free else (0, 0)

    def draw(self, surface):
        col, row = self.pos
        px, py = col * CELL + CELL // 2, row * CELL + CELL // 2 + HUD_H
        pygame.draw.circle(surface, DARK_RED, (px, py), CELL // 2 - 2)
        font_s = pygame.font.SysFont("arial", 11, bold=True)
        txt = font_s.render("✕", True, WHITE)
        surface.blit(txt, txt.get_rect(center=(px, py)))

class PowerUp:
    COLOURS = {"speed": CYAN, "slow": BLUE, "shield": MAGENTA}

    def __init__(self, occupied):
        self.type = random.choice(["speed", "slow", "shield"])
        self.colour = self.COLOURS[self.type]
        free = [(c, r) for c in range(COLS) for r in range(ROWS) if (c, r) not in occupied]
        self.pos = random.choice(free) if free else (1, 1)
        self.born = pygame.time.get_ticks()

    def expired(self):
        return pygame.time.get_ticks() - self.born > 8000

    def draw(self, surface):
        col, row = self.pos
        px, py = col * CELL + CELL // 2, row * CELL + CELL // 2 + HUD_H
        pygame.draw.rect(surface, self.colour,
                         (col * CELL + 2, row * CELL + HUD_H + 2, CELL - 4, CELL - 4), border_radius=4)
        font_s = pygame.font.SysFont("arial", 9, bold=True)
        txt = font_s.render(self.type[0].upper(), True, BLACK)
        surface.blit(txt, txt.get_rect(center=(px, py)))

class Obstacle:
    def __init__(self, level):
        self.cells = []
        if level >= 3:
            for _ in range(level * 2):
                for _ in range(100):
                    c = random.randrange(0, COLS)
                    r = random.randrange(0, ROWS)
                    mid_c, mid_r = COLS // 2, ROWS // 2
                    if not (mid_c - 5 <= c <= mid_c + 5 and mid_r - 5 <= r <= mid_r + 5):
                        self.cells.append((c, r))
                        break

    def draw(self, surface):
        for col, row in self.cells:
            pygame.draw.rect(surface, GRAY,
                             (col * CELL, row * CELL + HUD_H, CELL, CELL), border_radius=3)

class Snake:
    def __init__(self):
        mid = (COLS // 2, ROWS // 2)
        self.body = [(mid[0] - i, mid[1]) for i in range(3)]
        self.direction = RIGHT
        self.grew = False

    def change_dir(self, new_dir):
        if new_dir != (-self.direction[0], -self.direction[1]):
            self.direction = new_dir

    def move(self):
        hx, hy = self.body[0]
        new_head = (hx + self.direction[0], hy + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grew:
            self.body.pop()
        else:
            self.grew = False

    def head(self): return self.body[0]

    def is_dead(self, obstacle_cells):
        hx, hy = self.head()
        if not (0 <= hx < COLS and 0 <= hy < ROWS): return True
        if self.head() in self.body[1:]: return True
        if self.head() in obstacle_cells: return True
        return False

    def occupied(self): return set(self.body)

    def draw(self, surface, snake_color, shield_active):
        for i, (col, row) in enumerate(self.body):
            if i == 0 and shield_active:
                colour = MAGENTA
            elif i == 0:
                colour = SNAKE_HEAD
            else:
                colour = tuple(snake_color)
            pygame.draw.rect(surface, colour,
                             (col * CELL + 1, row * CELL + HUD_H + 1, CELL - 2, CELL - 2), border_radius=4)
            
        hx, hy = self.body[0]
        cx, cy = hx * CELL + CELL // 2, hy * CELL + CELL // 2 + HUD_H
        dx, dy = self.direction
        perp = (-dy, dx)
        for side in (+1, -1):
            ex = cx + dx * 4 + perp[0] * side * 4
            ey = cy + dy * 4 + perp[1] * side * 4
            pygame.draw.circle(surface, SNAKE_EYE, (ex, ey), 3)
            pygame.draw.circle(surface, BLACK, (ex + dx, ey + dy), 1)


def run_game(screen, settings, personal_best):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    small_font = pygame.font.SysFont("arial", 13)

    snake_color = settings["snake_color"]
    score, level, food_eaten = 0, 1, 0
    shield_active = False
    active_effect = None
    effect_end = 0

    snake = Snake()
    obstacle = Obstacle(level)

    foods, poison, powerup = [], None, None

    def occupied_all():
        occ = snake.occupied() | set(obstacle.cells)
        occ |= {f.pos for f in foods}
        if poison: occ.add(poison.pos)
        if powerup: occ.add(powerup.pos)
        return occ

    def spawn_food():
        if len(foods) < MAX_FOOD:
            foods.append(Food(occupied_all()))

    spawn_food()

    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP,    pygame.K_w): snake.change_dir(UP)
                elif event.key in (pygame.K_DOWN,  pygame.K_s): snake.change_dir(DOWN)
                elif event.key in (pygame.K_LEFT,  pygame.K_a): snake.change_dir(LEFT)
                elif event.key in (pygame.K_RIGHT, pygame.K_d): snake.change_dir(RIGHT)

        snake.move()

        # collision check (with shield)
        if snake.is_dead(set(obstacle.cells)):
            if shield_active:
                shield_active = False
                active_effect = None
                hx, hy = snake.head()
                fixed = ((hx % COLS + COLS) % COLS, (hy % ROWS + ROWS) % ROWS)
                snake.body[0] = fixed
            else:
                running = False
                continue

        head = snake.head()

        # eat food
        for food in foods[:]:
            if food.pos == head:
                score += food.value
                food_eaten += 1
                snake.grew = True
                foods.remove(food)
                spawn_food()
                if food_eaten % 5 == 0:
                    level += 1
                    obstacle = Obstacle(level)
                if random.random() < 0.3:
                    poison = Poison(occupied_all())
                break

        # update food timers
        for food in foods[:]:
            if food.update():
                foods.remove(food)
                spawn_food()

        # eat poison
        if poison and poison.pos == head:
            snake.body = snake.body[:-2] if len(snake.body) > 3 else snake.body[:1]
            poison = None
            if len(snake.body) <= 1:
                running = False
                continue

        # powerup logic
        if powerup is None and random.random() < 0.005:
            powerup = PowerUp(occupied_all())
        if powerup and powerup.expired():
            powerup = None
        if powerup and powerup.pos == head:
            active_effect = powerup.type
            effect_end = now + 5000
            shield_active = (powerup.type == "shield")
            powerup = None
        if active_effect and active_effect != "shield" and now > effect_end:
            active_effect = None

        # ── Draw ─────────────────────────────────────
        screen.fill(BG)

        if settings.get("grid_overlay"):
            for c in range(COLS):
                for r in range(ROWS):
                    pygame.draw.rect(screen, GRID_LINE, (c * CELL, r * CELL + HUD_H, CELL, CELL), 1)

        obstacle.draw(screen)
        for food in foods: food.draw(screen)
        if poison: poison.draw(screen)
        if powerup: powerup.draw(screen)
        snake.draw(screen, snake_color, shield_active)

        # HUD
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, SCREEN_W, HUD_H))
        pygame.draw.line(screen, YELLOW, (0, HUD_H), (SCREEN_W, HUD_H), 2)
        screen.blit(font.render(f"Score: {score}", True, YELLOW), (10, 8))
        screen.blit(font.render(f"Best: {personal_best}", True, SILVER), (200, 8))
        screen.blit(font.render(f"Lvl: {level}", True, WHITE), (420, 8))
        screen.blit(font.render(f"Len: {len(snake.body)}", True, WHITE), (560, 8))
        if active_effect:
            screen.blit(font.render(f"[{active_effect.upper()}]", True, CYAN), (680, 8))

        # food legend
        lx = 10
        for ft in FOOD_TYPES:
            pygame.draw.circle(screen, ft["colour"], (lx + 7, HUD_H - 14), 7)
            txt = small_font.render(f"+{ft['value']}", True, ft["colour"])
            screen.blit(txt, (lx + 17, HUD_H - 21))
            lx += 60

        fps = BASE_FPS + level * 2
        if active_effect == "speed": fps += 8
        elif active_effect == "slow": fps = max(4, fps - 5)

        pygame.display.flip()
        clock.tick(fps)

    return score, level