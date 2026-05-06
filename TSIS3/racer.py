import pygame
import random
import os

LANES = [200, 300, 400]
SPEED_BASE = 5

COIN_TYPES = [
    {"label": "BRONZE", "value": 1, "colour": (180, 100, 30), "weight": 60},
    {"label": "SILVER", "value": 2, "colour": (192, 192, 192), "weight": 30},
    {"label": "GOLD",   "value": 3, "colour": (255, 220, 0),   "weight": 10},
]

def weighted_choice(items):
    total, roll, running = sum(i["weight"] for i in items), random.randint(1, sum(i["weight"] for i in items)), 0
    for item in items:
        running += item["weight"]
        if roll <= running:
            return item
    return items[-1]

def load_image(name, width, height):
    path = os.path.join('assets', 'images', name)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except FileNotFoundError:
        surf = pygame.Surface((width, height))
        surf.fill((255, 0, 255))
        return surf


class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image = load_image(f"player_{color_name}.png", 40, 70)
        self.rect = self.image.get_rect(center=(300, 500))
        self.speed = 6
        self.shield_active = False
        self.nitro_active = False
        self.powerup_timer = 0
        self.crashes_allowed = 0

    def update(self):
        keys = pygame.key.get_pressed()
        spd = int(self.speed * 1.5) if self.nitro_active else self.speed
        if keys[pygame.K_LEFT]  and self.rect.left > 150:   self.rect.x -= spd
        if keys[pygame.K_RIGHT] and self.rect.right < 450:  self.rect.x += spd
        if keys[pygame.K_UP]    and self.rect.top > 0:      self.rect.y -= spd
        if keys[pygame.K_DOWN]  and self.rect.bottom < 600: self.rect.y += spd

        if (self.nitro_active or self.shield_active) and pygame.time.get_ticks() > self.powerup_timer:
            self.nitro_active = False
            self.shield_active = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        super().__init__()
        self.image = load_image("enemy.png", 40, 70)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))
        self.speed = SPEED_BASE + (2 if difficulty == "hard" else 0)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("obstacle.png", 40, 40)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["Nitro", "Shield", "Repair"])
        self.image = load_image(self.type.lower() + ".png", 30, 30)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -50))

    def update(self):
        self.rect.y += SPEED_BASE
        if self.rect.top > 600:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ctype = weighted_choice(COIN_TYPES)
        self.value = ctype["value"]
        self.label = ctype["label"]
        self.colour = ctype["colour"]
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.colour, (12, 12), 12)
        pygame.draw.circle(self.image, (0, 0, 0), (12, 12), 12, 2)
        font = pygame.font.SysFont("arial", 11, bold=True)
        txt = font.render(str(self.value), True, (0, 0, 0))
        self.image.blit(txt, txt.get_rect(center=(12, 12)))
        self.rect = self.image.get_rect(center=(random.choice(LANES), -20))
        self.speed = SPEED_BASE

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()