#! python
import pygame # pygame FTW
import numpy # for complex maths

#constants
WIDTH = 1920
HEIGHT = 1080
SCALE = 4

#classes and functions
class entity:
    def __init__(self):
        self.pos = [500,500]
        self.size = [16, 16]
        self.sprite = pygame.image.load("res\SpriteSheet.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.size[0] * 4 * SCALE, self.size[1] * SCALE))
        self.color = (255,255,255)

    def draw(self):
        screen.blit(self.sprite, (self.pos[0], self.pos[1], self.size[0], self.size[1]), (0,0, self.size[0] * SCALE, self.size[1] * SCALE))

#setup
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("March")

joystick = 0 # eight bit number each bit corresponding to a button, w, a, s, d,

player = entity()

tick = 0

# THE LOOP
while True:
    # Event handling 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_w:
                joystick |= 1
            if event.key == pygame.K_a:
                joystick |= 2
            if event.key == pygame.K_s:
                joystick |= 4
            if event.key == pygame.K_d:
                joystick |= 8
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                joystick &= ~1
            if event.key == pygame.K_a:
                joystick &= ~2
            if event.key == pygame.K_s:
                joystick &= ~4
            if event.key == pygame.K_d:
                joystick &= ~8

    #input
    if joystick & 1:
        player.pos[1] -= 1
    if joystick & 2:
        player.pos[0] -= 1
    if joystick & 4:
        player.pos[1] += 1
    if joystick & 8:
        player.pos[0] += 1
    
    tick += 1

    screen.fill((104, 192, 72))

    player.draw()

    pygame.display.flip()