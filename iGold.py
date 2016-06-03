import pygame
import interactableSuperClass as isc
import constants

class Gold(isc.Interactable):
    """Money distributed throughout the world"""
    width = 30
    height = 30
    
    level = None
    player = None
    
    def __init__(self):
        isc.Interactable.__init__(self)
 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.ORANGE)
 
        self.rect = self.image.get_rect()
        
    def pickup_gold(self):
        self.player.player_money += 5
        self.player.player_health += 5
        pygame.sprite.Sprite.kill(self)