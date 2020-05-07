# Import the libraries we need
import pygame
import time
import math

# Initialize variables
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

renderedblocks = []

mapsize = 5
size = 32
speed = 16

blockimg = {}
holdingid = 1
loadblocks = [1, 2, 69, 75, 76, 331, 332]

blockindex = 0

playerxoffset = ((((SCREEN_WIDTH / size) * mapsize) / 2) * size) - ((((SCREEN_WIDTH / size) * mapsize) / 2) * size) * 2
playeryoffset = ((((SCREEN_HEIGHT / size) * mapsize) / 2) * size) - ((((SCREEN_HEIGHT / size) * mapsize) / 2) * size) * 2

hudx = 10
hudy = 10

for id in loadblocks:
    blockimg[id] = pygame.image.load("./assets/redstoneengine/blocks/" + str(id) + ".png")

class Block(pygame.sprite.Sprite):
    #This class represents a block. It derives from the "sprite" class in pygame.
    def __init__(self, id, x, y):
        # Call the parent class (sprite) constructor
        self.id = id

        super().__init__()

        #Give pygame a loaded image
        self.image = blockimg[self.id]

        self.x = x
        self.y = y

        self.parentx = 0
        self.parenty = 0
        self.already_updated = False

        if(self.id == 69):
            self.can_be_powered = True
            self.signal_strength = 15
        else:
            self.can_be_powered = False
            self.signal_strength = 15

        self.powered_state = False

    #Draw the block
    def draw(self, screen):
        image = self.image
        if self.x > (SCREEN_WIDTH) - playerxoffset: return
        if self.x < (size - (size * 2)) - playerxoffset: return
        if self.y > (SCREEN_HEIGHT) - playeryoffset: return
        if self.y < (size - (size * 2)) - playeryoffset: return
        screen.blit(pygame.transform.scale(image, (size, size)), (self.x + playerxoffset, self.y + playeryoffset))

    def isSelected(self, x, y):
        if(x > (self.x + playerxoffset) and x < (self.x + playerxoffset) + size and y > (self.y + playeryoffset) and y < (self.y + size + playeryoffset)): return True
        return False

    def changeID(self, id):
        self.id = id
        self.image = blockimg[self.id]

    def change_can_be_powered(self):
        self.can_be_powered = not self.can_be_powered

    def change_updated(self):
        self.already_updated = False

    def update_powered_state(self):
        if(self.already_updated): return
        self.already_updated = True
        for block in renderedblocks:
            myx = self.x / size
            myy = self.y / size
            if (block.x / size == myx - 1 and block.y / size == myy):
                if(block.id == 69 or block.id == 331 or block.id == 332):
                    self.parentx = block.x / size
                    self.parenty = block.y / size
                    self.parent = block
            if (block.x / size == myx + 1 and block.y / size == myy):
                if(block.id == 69 or block.id == 331 or block.id == 332):
                    self.parentx = block.x / size
                    self.parenty = block.y / size
                    self.parent = block
            if (block.x / size == myx and block.y / size == myy - 1):
                if(block.id == 69 or block.id == 331 or block.id == 332):
                    self.parentx = block.x / size
                    self.parenty = block.y / size
                    self.parent = block
            if (block.x / size == myx and block.y / size == myy + 1):
                if(block.id == 69 or block.id == 331 or block.id == 332):
                    self.parentx = block.x / size
                    self.parenty = block.y / size
                    self.parent = block

            if (block.x / size == myx and block.y / size == myy):
                if(block.id == 69):
                    self.parentx = block.x / size
                    self.parenty = block.y / size
                    self.parent = block

        if(self.parentx == 0): return
        if(self.parenty == 0): return

        if(self.id == 2):
            print("updating block state")
            self.powered_state = not self.powered_state
            self.update_blocks()
            return

        if(self.id == 69):
            self.powered_state = not self.powered_state
            self.update_blocks()
            return

        if(self.id == 76):
            print("Updating torch")
            self.powered_state = False
            self.id = 75
            self.image = blockimg[self.id]
            self.update_blocks()
            return

        if (self.id == 75):
            print("Updating torch")
            self.powered_state = True
            self.id = 76
            self.image = blockimg[self.id]
            self.update_blocks()
            return

        if(self.id == 331):
            print("updating redstone on")
            self.powered_state = True
            self.signal_strength = self.parent.signal_strength - 1
            if(self.signal_strength < 0): return
            print(self.signal_strength)
            self.id = 332
            self.image = blockimg[self.id]
            self.update_blocks()
            return

        if(self.id == 332):
            print("updating redstone off")
            self.powered_state = False
            self.signal_strength = self.parent.signal_strength - 1
            if (self.signal_strength < 0): return
            self.id = 331
            self.image = blockimg[self.id]
            self.update_blocks()
            return

    def update_blocks(self):
        for block in renderedblocks:
            myx = self.x / size
            myy = self.y / size
            if (block.x / size == myx - 1 and block.y / size == myy):
                if (self.parentx == block.x / size and self.parenty == block.y / size): return
                block.update_powered_state()
            if (block.x / size == myx + 1 and block.y / size == myy):
                if (self.parentx == block.x / size and self.parenty == block.y / size): return
                block.update_powered_state()
            if (block.x / size == myx and block.y / size == myy - 1):
                if (self.parentx == block.x / size and self.parenty == block.y / size): return
                block.update_powered_state()
            if (block.x / size == myx and block.y / size == myy + 1):
                if (self.parentx == block.x / size and self.parenty == block.y / size): return
                block.update_powered_state()
        return



level = []

#world generation

rownumber = (SCREEN_WIDTH / size) * mapsize
coloumnumber = (SCREEN_HEIGHT / size) * mapsize

for x in range(int(rownumber)):
    temp = []
    for y in range(int(coloumnumber)):
        temp.append(1)

    level.append(temp)






running = True

def render(level):
    xoffset = 0
    while xoffset < len(level):
        coloumn = level[xoffset]
        xoffset += 1

        yoffset = 0
        while yoffset < len(coloumn):
            blocks = coloumn[yoffset]
            yoffset += 1

            renderedblocks.append(Block(blocks, ((xoffset - 1) * size), (yoffset - 1) * size))

down = []
render(level)

# Main game loop
while running:
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if (event.type == pygame.KEYUP):
            down = []

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_w or event.unicode == 'w'): down.append("w")
            if (event.key == pygame.K_a or event.unicode == 'a'): down.append("a")
            if (event.key == pygame.K_s or event.unicode == 's'): down.append("s")
            if (event.key == pygame.K_d or event.unicode == 'd'): down.append("d")
            if (event.key == pygame.K_1 or event.unicode == '1'): down.append("1")
            if (event.key == pygame.K_2 or event.unicode == '2'): down.append("2")
            if (event.key == pygame.K_e or event.unicode == 'e'): down.append("e")

            if (event.key == pygame.K_z or event.unicode == 'z'):
                increase = math.floor(SCREEN_WIDTH / size) + 1
                size = math.floor(SCREEN_WIDTH / increase)
                renderedblocks = []
                render(level)
            if (event.key == pygame.K_x or event.unicode == 'x'):
                increase = math.floor(SCREEN_WIDTH / size) - 1
                size = math.floor(SCREEN_WIDTH / increase)
                renderedblocks = []
                render(level)
    # erase the screen
    screen.fill((0, 0, 0))

    Mouse_x, Mouse_y = pygame.mouse.get_pos()

    if "w" in down: playeryoffset += speed
    if "s" in down: playeryoffset -= speed
    if "a" in down: playerxoffset += speed
    if "d" in down: playerxoffset -= speed

    if "1" in down:
        time.sleep(0.2)
        blockindex += 1
        blockindex = blockindex + len(loadblocks)
        blockindex %= len(loadblocks)
        holdingid = loadblocks[blockindex]

    if "2" in down:
        time.sleep(0.2)
        blockindex -= 1
        blockindex = blockindex + len(loadblocks)
        blockindex %= len(loadblocks)
        holdingid = loadblocks[blockindex]

    # draw stuff on the screen here!

    for block in renderedblocks:
        block.draw(screen)

        block.change_updated()

        if(block.isSelected(Mouse_x, Mouse_y)):
            if "e" in down:
                block.update_blocks()
                time.sleep(0.2)
                if (block.id == 69):
                    print("Updating State On Lever")
                    block.update_powered_state()


            if(pygame.mouse.get_pressed()[0]):
                block.changeID(holdingid)
            if(pygame.mouse.get_pressed()[2]):
                block.changeID(1)

    pygame.draw.rect(screen, (255, 255, 255), (hudx, hudy, size + 5, size + 5))
    screen.blit(pygame.transform.scale(blockimg[holdingid], (size, size)), (hudx + 2.5, hudy + 2.5))

    # show the screen
    pygame.display.update()

    # run at 15fps
    clock.tick(15)

pygame.quit()