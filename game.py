#! python
import pygame # pygame FTW
import numpy # for complex maths

#constants
WIDTH = 1920
HEIGHT = 1080

#setup
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("March")

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
    
    tick += 1

    pygame.display.flip()