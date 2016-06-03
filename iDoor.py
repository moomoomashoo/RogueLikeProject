import pygame
import interactableSuperClass as isc
import constants

class Door(isc.Interactable):
    """Door block - Hit this to move to the next room"""
    width = 80
    height = 100
    
    def __init__(self):
        isc.Interactable.__init__(self)
 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.LIGHT_BLUE)
 
        self.rect = self.image.get_rect()