import pygame
import random
import interactableSuperClass as isc
import iCoin
import constants

class Chest(isc.Interactable):
    """Treasure Chest full of money!"""
    width = 40
    height = 40
    
    amount = 10
    
    def __init__(self):
        isc.Interactable.__init__(self)
 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.BROWN)
 
        self.rect = self.image.get_rect()
        
        self.chest_closed = True
        
    def open_chest(self):
        if self.chest_closed:
            self.chest_closed = False
            self.image.fill(constants.WHITE)
            for i in range(self.amount):
                coin = iCoin.Coin()
                coin.rect.x = random.randrange(self.rect.x, self.rect.x + self.rect.width)
                coin.rect.y = self.rect.y
                coin.change_x = random.randrange(-5,6)
                coin.change_y = random.randrange(-10,2)
                coin.player = self.player
                coin.level = self.level
                self.level.interact_list.add(coin)