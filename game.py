#! python
import pygame # pygame FTW
import numpy # for complex maths
from os import path # helps with path finding on multiple OS

#constants
WIDTH = 1920
HEIGHT = 1080
SCALE = 4
FPS = 60

#classes and functions
class entity:
    '''Any entity'''
    def __init__(self, objectImage):
        self.pos = [500,500]
        self.size = [16 * SCALE, 16 * SCALE]
        self.spriteIndex = 0
        self.rot = 0
        self.sprite = pygame.image.load(path.join("res", objectImage))
        self.sprite = pygame.transform.scale(self.sprite, (self.size[0] * 4, self.size[1]))
        self.color = (255,255,255)

    def draw(self):
        '''Draws the entity'''
        self.spriteIndex = self.rot
        screen.blit(
            self.sprite, 
            (
                self.pos[0], 
                self.pos[1], 
                self.size[0], 
                self.size[1]
            ), 
            (
                0 + self.spriteIndex * self.size[0],
                0, 
                self.size[0], 
                self.size[1]
            )
        )

class player(entity):
    def __init__(self, objectImage):
        super().__init__(objectImage)


#setup
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("March")

joystick = 0 # eight bit number each bit corresponding to a button, w, a, s, d,

player = player("SpriteSheet.png")

#Funciton for drawing window
def draw_window():
    screen.fill((104, 192, 72))
    player.draw()

# THE LOOP
def main():
    global joystick
    while True:
        #Set FPS
        clock.tick(FPS)
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
            player.rot = 0
            player.pos[1] -= 5
        if joystick & 2:
            player.rot = 1
            player.pos[0] -= 5
        if joystick & 4:
            player.rot = 2
            player.pos[1] += 5
        if joystick & 8:
            player.rot = 3
            player.pos[0] += 5

        player.spriteIndex = (player.spriteIndex + 1) % 4

        draw_window()

        pygame.display.flip()
        

if __name__ == "__main__":
    main()