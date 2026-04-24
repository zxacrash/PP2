import pygame
import datetime
import os
import math

pygame.init()
screen = pygame.display.set_mode((1200, 700))

base = os.path.join(os.path.dirname(__file__), 'images')
resized_image = pygame.transform.scale(pygame.image.load(os.path.join(base, 'clock.png')).convert_alpha(), (800, 600))
res_mickey    = pygame.transform.scale(pygame.image.load(os.path.join(base, 'mUmrP.png')).convert_alpha(), (350, 350))
hand_l = pygame.transform.scale(pygame.image.load(os.path.join(base, 'hand_left_centered.png')).convert_alpha(), (160, 160))
hand_r = pygame.transform.scale(pygame.image.load(os.path.join(base, 'hand_right_centered.png')).convert_alpha(), (160, 160))

CENTER = (600, 340)
ARM = 50

def draw_hand(img, angle):
    rad = math.radians(angle)
    tip = (CENTER[0] + ARM * math.sin(rad), CENTER[1] - ARM * math.cos(rad))
    rotated = pygame.transform.rotate(img, -angle)
    screen.blit(rotated, rotated.get_rect(center=tip))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()

    screen.fill((255, 255, 255))
    screen.blit(resized_image, resized_image.get_rect(center=CENTER))
    screen.blit(res_mickey,    res_mickey.get_rect(center=CENTER))
    draw_hand(hand_r, now.minute * 6 + now.second * 0.1)
    draw_hand(hand_l, now.second * 6)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()