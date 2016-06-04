import pygame
import interactableSuperClass as isc
import constants

class Coin(isc.Interactable):
    """Money dropped by enemies"""
    width = 20
    height = 20
    
    level = None
    player = None
    
    def __init__(self):
        isc.Interactable.__init__(self)
 
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.YELLOW)
 
        self.rect = self.image.get_rect()
        
        self.change_x = 0
        self.change_y = 0
        
        self.bounce = 0.4
        self.max_fall_speed = 15
        
        self.pickupable = False
        self.time_until_pickup = 30
        self.despawn_time = 600
        self.timer = 0
        
        
    def update(self):
        self.calc_grav()
        
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.left + block.rect.right) / 2
            if self.rect.left < middle:
                self.rect.right = block.rect.left
                self.change_x *= -self.bounce
            elif self.rect.left > middle:
                self.rect.left = block.rect.right
                self.change_x *= -self.bounce
 
        # Move up/down
        if self.change_y >= self.max_fall_speed:
            self.change_y = self.max_fall_speed
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.top + block.rect.bottom) / 2
            if self.change_y > 2:
                self.rect.bottom = block.rect.top
                self.change_x *= self.bounce
                self.change_y *= -self.bounce
            elif self.rect.bottom < middle:
                self.rect.bottom = block.rect.top
                self.change_y = 0
                self.change_x *= self.bounce
                #self
            elif self.rect.top > middle:
                self.rect.top = block.rect.bottom 
                self.change_y *= -self.bounce
                
        self.timer += 1
        if self.timer >= self.time_until_pickup:
            self.pickupable = True
        if self.timer >= self.despawn_time:
            pygame.sprite.Sprite.kill(self)
        
    
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
            
    def pickup_money(self):
        if self.pickupable:
            self.player.player_money += 1
            self.player.player_health += 1
            pygame.sprite.Sprite.kill(self)