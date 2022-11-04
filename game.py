#! python
import pygame as pg # pygame FTW
import numpy # for complex maths
from os import path # helps with path finding on multiple OS
import csv # for reading csv files

#constants
WIDTH = 1920 
'''Screen width'''
HEIGHT = 1080
'''Screen height'''
TILESIZE = 8
'''Size of a tile in pixels'''
SCALE = 4
'''Scale of the game'''
FPS = 60
'''FPS of the game'''

#classes and functions
class entity:
    '''Any entity'''
    def __init__(self, objectImage:str):
        self.size = [2 * TILESIZE * SCALE, 2 * TILESIZE * SCALE]
        '''The size of the entity. Default 2 tiles wide and tall'''
        self.pos = [WIDTH // 2 - self.size[0] // 2, HEIGHT // 2 - self.size[1] // 2]
        '''The position of the entity. Default center of the screen'''
        self.spriteIndex = [0,0]
        '''Direction the entity is facing, Default 2 (South)'''
        self.sprite = pg.image.load(
            path.join(
                "res", 
                objectImage
            )
        )
        '''The image of the entity'''
        self.sprite = pg.transform.scale(
            self.sprite, 
            ( # Tring to get the size of the scaled up image. Get the size, which is 64 by default multiply it by the number of sprites in the image
                self.size[0] * (self.sprite.get_rect()[2] // TILESIZE // (self.size[0] // TILESIZE // SCALE)), # which is calculated here
                self.size[1] * (self.sprite.get_rect()[3] // TILESIZE // (self.size[1] // TILESIZE // SCALE))
            )
        )

    def draw(self):
        '''Draws the entity'''
        screen.blit( # Draw
            self.sprite, # Entities sprite
            ( # Sprite position
                self.pos[0], # x
                self.pos[1], # y
                self.size[0], # width
                self.size[1] # width
            ), 
            ( # crop of sprite image
                self.spriteIndex[0] * self.size[0], # Crop x is the sprite index in the x multiplied by it's size
                self.spriteIndex[1] * self.size[1], # Crop y is the same but in y
                self.size[0], # Crop width is size x
                self.size[1] # Crop height is size y
            )
        )

class player(entity):
    '''The player'''
    def __init__(self, objectImage):
        super().__init__(objectImage)
    def input(self, world:object):
        '''Doesn't actually move the player, it moves the camera'''
        if joystick & 1 and joystick & 2 == 2:
            self.spriteIndex = [1,1]
            cameraPos[1] -= SCALE * 1.4
            cameraPos[0] -= SCALE * 1.4
        elif joystick & 2 == 2 and joystick & 4 == 4:
            self.spriteIndex = [3,1]
            cameraPos[1] += SCALE * 1.4
            cameraPos[0] -= SCALE * 1.4
        elif joystick & 4 == 4 and joystick & 8 == 8:
            self.spriteIndex = [1,0]
            cameraPos[1] += SCALE * 1.4 
            cameraPos[0] += SCALE * 1.4 
        elif joystick & 8 == 8 and joystick & 1 == 1:
            self.spriteIndex = [3,0]
            cameraPos[1] -= SCALE * 1.4 
            cameraPos[0] += SCALE * 1.4 
        elif joystick & 1: # moving up
            self.spriteIndex = [0,1]
            cameraPos[1] -= SCALE * 2
        elif joystick & 2: # moving west
            self.spriteIndex = [2,1]
            cameraPos[0] -= SCALE * 2
        elif joystick & 4: # moving south
            self.spriteIndex = [0,0]
            cameraPos[1] += SCALE * 2
        elif joystick & 8: # moving east
            self.spriteIndex = [2,0]
            cameraPos[0] += SCALE * 2

class world:
    '''A tilemap class'''
    def __init__(self, tileImage):
        '''Size of the tiles that map uses'''
        self.tilesheet = pg.image.load(path.join("res", tileImage))
        '''Tilesheet containing the images'''
        self.size = [self.tilesheet.get_rect()[2] // TILESIZE, self.tilesheet.get_rect()[3] // TILESIZE]
        self.LayerMap1 = []
        self.LayerMap2 = []
        self.collisionMap = []
        self.textures = {}
        for row in range(self.size[1]):
            for column in range(self.size[0]):
                self.textures[self.size[0] * row + column] = pg.transform.scale(
                    self.tilesheet.subsurface(
                        (column * TILESIZE),
                        (row * TILESIZE),
                        TILESIZE,
                        TILESIZE
                    ), 
                    (
                        TILESIZE * SCALE, 
                        TILESIZE * SCALE
                    )
                )

    def drawMap(self, map:list):
        '''Draws the tilemap'''
        for row in range(int(cameraPos[1]) // TILESIZE // SCALE, (HEIGHT + TILESIZE * SCALE + int(cameraPos[1])) // TILESIZE // SCALE):
            for column in range(int(cameraPos[0]) // TILESIZE // SCALE, (WIDTH + TILESIZE * SCALE + int(cameraPos[0])) // TILESIZE // SCALE):
                try:
                    if int(map[row][column]) != 0:
                        screen.blit(
                            self.textures[
                                int(map[row][column])
                            ], 
                            (
                                column * TILESIZE * SCALE - cameraPos[0], 
                                row * TILESIZE * SCALE - cameraPos[1]
                            )
                        )
                except:
                    pass

#Funciton for drawing window
def draw_window():
    screen.fill((104, 192, 72))
    world1.drawMap(world1.LayerMap1)
    player.draw()
    world1.drawMap(world1.LayerMap2)

#setup
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
pg.display.set_caption("March")

joystick = 0 # eight bit number each bit corresponding to a button, w, a, s, d,

player = player("SpriteSheet.png")
cameraPos = [0,0]

world1 = world("tiles.png")

with open(path.join("res", "maps", "tycoon-map_layer1.csv")) as layer1file:
    world1.LayerMap1 = list(csv.reader(layer1file))

with open(path.join("res", "maps", "tycoon-map_layer2.csv")) as layer2file:
    world1.LayerMap2 = list(csv.reader(layer2file))

with open(path.join("res", "maps", "tycoon-map_collision.csv")) as collisionFile:
    world1.collisionMap = list(csv.reader(collisionFile))

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
        player.input(world1)

        draw_window()

        pg.display.flip()
        

if __name__ == "__main__":
    main()