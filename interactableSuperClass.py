import pygame
import constants

class Interactable(pygame.sprite.Sprite):
    """
    A super class for all things you can interact with
    Doors, Keys, Treasure etc
    """
    width = 50
    height = 50
    
    def __init__(self):
        super().__init__()
 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.LIGHT_BLUE)
 
        self.rect = self.image.get_rect()
        
    def update(self):
        ()