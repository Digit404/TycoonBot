#! python
import pygame as pg # pygame FTW
import numpy # for complex maths
from os import path # helps with path finding on multiple OS
import csv # for reading csv files

#constants
WIDTH = 1920
HEIGHT = 1080
TILESIZE = 8
SCALE = 4
FPS = 60

#classes and functions
class entity:
    '''Any entity'''
    def __init__(self, objectImage):
        self.pos = [500,500]
        self.size = [2 * TILESIZE * SCALE, 2 * TILESIZE * SCALE]
        self.spriteIndex = 0 # index of the sprite you want to display
        self.rot = 2 # players facing
        self.sprite = pg.image.load(path.join("res", objectImage))
        self.sprite = pg.transform.scale(self.sprite, (self.size[0] * 4, self.size[1]))
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
    '''The player'''
    def __init__(self, objectImage):
        super().__init__(objectImage)

class map:
    '''A tilemap class'''
    def __init__(self, tileImage):
        self.tilesize = 8 * SCALE
        self.tilesheet = pg.image.load(path.join("res", tileImage))
        self.numtex = self.tilesheet.get_rect()[2] // (self.tilesize // SCALE)
        self.textures = {}
        for i in range(self.numtex):
            self.textures[i] = pg.transform.scale(
                self.tilesheet.subsurface(
                    0 + (i * self.tilesize // SCALE),
                    0,
                    self.tilesize // SCALE,
                    self.tilesize // SCALE
                ), 
                (
                    self.tilesize, 
                    self.tilesize
                )
            )
        self.tilemap = []

    def draw(self):
        '''Draws the tilemap'''
        for row in range(len(self.tilemap)):
            for column in range(len(self.tilemap[row])):
                screen.blit(self.textures[int(self.tilemap[row][column])], (column*self.tilesize, row*self.tilesize))

#Funciton for drawing window
def draw_window():
    screen.fill((104, 192, 72))
    map1.draw()
    player.draw()

#setup
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
pg.display.set_caption("March")

joystick = 0 # eight bit number each bit corresponding to a button, w, a, s, d,

player = player("SpriteSheet.png")
cameraPos = [0,0]

map1 = map("tiles.png")
with open(path.join("res", "Map.csv")) as mapfile:
    map1.tilemap = list(csv.reader(mapfile))
        
print(map1.tilemap)

# THE LOOP
def main():
    global joystick
    while True:
        #Set FPS
        clock.tick(FPS)
        # Event handling 
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                if event.key == pg.K_w:
                    joystick |= 1
                if event.key == pg.K_a:
                    joystick |= 2
                if event.key == pg.K_s:
                    joystick |= 4
                if event.key == pg.K_d:
                    joystick |= 8
            elif event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    joystick &= ~1
                if event.key == pg.K_a:
                    joystick &= ~2
                if event.key == pg.K_s:
                    joystick &= ~4
                if event.key == pg.K_d:
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

        pg.display.flip()
        

if __name__ == "__main__":
    main()