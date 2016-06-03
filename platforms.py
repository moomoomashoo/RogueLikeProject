import pygame
import constants
from spritesheetFunctions import SpriteSheet

DIRT_UDLR_1 = (0,0,48,48)
DIRT_DLR_1 = (48,0,48,48)
DIRT_ULR_1 = (96,0,48,48)
DIRT_UDR_1 = (0,48,48,48)
DIRT_UDL_1 = (48,48,48,48)

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
        
        #self.image = image
 
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.GREEN)
 
        self.rect = self.image.get_rect()