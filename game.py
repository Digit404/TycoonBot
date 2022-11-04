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
        self.posAbsolute = [50,50]
        '''The absolute'''
        self.posRelative = [
            (WIDTH // TILESIZE // SCALE // 2 - self.size[0] // TILESIZE // SCALE // 2) * TILESIZE * SCALE, 
            (HEIGHT // TILESIZE // SCALE // 2 - self.size[1] // TILESIZE // SCALE // 2) * TILESIZE * SCALE
        ]
        '''The relatve position of the entity to the camera. Default center of the screen'''
        self.spriteIndex = [0,0]
        '''Direction the entity is facing, Default 2 (South)'''
        self.sprite = pg.image.load(path.join("res", "img", objectImage))
        '''The image of the entity'''
        self.sprite = pg.transform.scale(
            self.sprite, 
            ( # Tring to get the size of the scaled up image. Get the size, which is 64 by default multiply it by the number of sprites in the image
                self.size[0] * (self.sprite.get_rect()[2] // TILESIZE // (self.size[0] // TILESIZE // SCALE)), # which is calculated here
                self.size[1] * (self.sprite.get_rect()[3] // TILESIZE // (self.size[1] // TILESIZE // SCALE)) # There's probably a better way to do this
            )
        )

    def draw(self):
        '''Draws the entity'''
        screen.blit( # Draw
            self.sprite, # Entities sprite
            ( # Sprite position
                self.posRelative[0], # x
                self.posRelative[1], # y
                self.size[0], # width
                self.size[1] # width
            ), 
            ( # crop of sprite image; describe a rectangle within the image that you want to display
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
            self.move(-1.4, -1.4)
        elif joystick & 2 == 2 and joystick & 4 == 4:
            self.spriteIndex = [3,1]
            self.move(-1.4, 1.4)
        elif joystick & 4 == 4 and joystick & 8 == 8:
            self.spriteIndex = [1,0]
            self.move(1.4, 1.4)
        elif joystick & 8 == 8 and joystick & 1 == 1:
            self.spriteIndex = [3,0]
            self.move(1.4, -1.4)
        elif joystick & 1: # moving up
            self.spriteIndex = [0,1]
            self.move(0, -2)
        elif joystick & 2: # moving west
            self.spriteIndex = [2,1]
            self.move(-2, 0)
        elif joystick & 4: # moving south
            self.spriteIndex = [0,0]
            self.move(0, 2)
        elif joystick & 8: # moving east
            self.spriteIndex = [2,0]
            self.move(2, 0)
        
    def move(self, x, y):
        if int(world1.collisionMap[int(self.posAbsolute[1]) // TILESIZE // SCALE][int(self.posAbsolute[0] + x * SCALE) // TILESIZE // SCALE]) == 0:
            self.posAbsolute[0] += x * SCALE
        if int(world1.collisionMap[int(self.posAbsolute[1] + y * SCALE) // TILESIZE // SCALE][int(self.posAbsolute[0]) // TILESIZE // SCALE]) == 0:
            self.posAbsolute[1] += y * SCALE

class world:
    '''A tilemap class'''
    def __init__(self, tileImage):
        '''Size of the tiles that map uses'''
        self.tilesheet = pg.image.load(path.join("res", "img", tileImage))
        '''Tilesheet containing the images'''
        self.tilesheetSize = [self.tilesheet.get_rect()[2] // TILESIZE, self.tilesheet.get_rect()[3] // TILESIZE]
        '''How many tiles across and down the tilesheet is'''
        self.backgroundColor = (104, 192, 72)
        '''Default background color for this world'''
        self.LayerMap1 = []
        '''Layer 1 that goes under the player'''
        self.LayerMap2 = []
        '''Layer 2 that goes over the player'''
        self.collisionMap = []
        '''Map of collision walls'''
        self.textures = {}
        '''A set of all textures from the texture sheet'''
        for y in range(self.tilesheetSize[1]):
            for x in range(self.tilesheetSize[0]):
                self.textures[self.tilesheetSize[0] * y + x] = pg.transform.scale(
                    self.tilesheet.subsurface(
                        (x * TILESIZE),
                        (y * TILESIZE),
                        TILESIZE,
                        TILESIZE
                    ), 
                    (
                        TILESIZE * SCALE, 
                        TILESIZE * SCALE
                    )
                )

    def drawMap(self, tilemap:list):
        '''Draws the tilemap'''
        for y in range(int(cameraPos[1]) // TILESIZE // SCALE, (HEIGHT + TILESIZE * SCALE + int(cameraPos[1])) // TILESIZE // SCALE):
            for x in range(int(cameraPos[0]) // TILESIZE // SCALE, (WIDTH + TILESIZE * SCALE + int(cameraPos[0])) // TILESIZE // SCALE):
                if 0 <= y < len(tilemap) and 0 <= x < len(tilemap[y]) and int(tilemap[y][x]) != 0:
                    # if y is greater than 0 and less the y size, and if 0 < x < size of tilemap in x, and the tile isn't 0: place the tile
                    screen.blit(
                        self.textures[int(tilemap[y][x])], # y before x because its a list of lists. its (x of y of list)
                        (
                            x * TILESIZE * SCALE - cameraPos[0], 
                            y * TILESIZE * SCALE - cameraPos[1]
                        )
                    )

#Funciton for drawing window
def draw_window():
    screen.fill(world1.backgroundColor) # start by filling on 
    world1.drawMap(world1.LayerMap1)
    tycoonBot.draw()
    world1.drawMap(world1.LayerMap2)

def cameraTrack(entity:object):
    cameraPos[0] = entity.posAbsolute[0] - (30 * TILESIZE * SCALE)
    cameraPos[1] = entity.posAbsolute[1] - (16 * TILESIZE * SCALE)

#setup
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
pg.display.set_caption("March")

joystick = 0 # eight bit number each bit corresponding to a button, w, a, s, d,

tycoonBot = player("TycoonBotSheet.png")
cameraPos = [0,0]

world1 = world("TileSheet.png")

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
                match(event.key):
                    case pg.K_ESCAPE:
                        pg.quit()
                        exit()
                    case pg.K_w:
                        joystick |= 1
                    case pg.K_a:
                        joystick |= 2
                    case pg.K_s:
                        joystick |= 4
                    case pg.K_d:
                        joystick |= 8
            elif event.type == pg.KEYUP:
                match(event.key):
                    case pg.K_w:
                        joystick &= ~1
                    case pg.K_a:
                        joystick &= ~2
                    case pg.K_s:
                        joystick &= ~4
                    case pg.K_d:
                        joystick &= ~8

        #input
        tycoonBot.input(world1)

        cameraTrack(tycoonBot) # Camera on TycoonBot

        draw_window()

        pg.display.flip()
        

if __name__ == "__main__":
    main()