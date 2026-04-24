import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()

x, y = 600, 350
SPEED = 20

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:    y = max(25, y - SPEED)
    if keys[pygame.K_DOWN]:  y = min(675, y + SPEED)
    if keys[pygame.K_LEFT]:  x = max(25, x - SPEED)
    if keys[pygame.K_RIGHT]: x = min(1175, x + SPEED)
    white = (255 , 255 , 255 )
    red = ( 255 , 0 , 0)
    radius = 25
    screen.fill(white)
    pygame.draw.circle(screen, red , (x, y), radius)
    pygame.display.flip()
    clock.tick(60)