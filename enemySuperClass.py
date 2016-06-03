import pygame
import random
#import constants
import iCoin

class Enemy(pygame.sprite.Sprite):
    enemy_health = 100
    enemy_attack = 5
    max_speed_x = 5
    max_speed_y = 5
    change_x = max_speed_x
    change_y = max_speed_y
    
    coin_amount = random.randrange(50)
    
    level = None
    
    def __init__(self):
        super().__init__()
        
        self.coin_list = pygame.sprite.Group()
        
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
            
    """def accel(self, value):
        if self.change_x > 0:
            if self.change_x < self.max_speed_x:
                self.change_x += value
            elif self.change_x > self.max_speed_x:
                self.change_x -= value
        elif self.change_x < 0:
            if self.change_x > -self.max_speed_x:
                self.change_x -= value
            elif self.change_x < -self.max_speed_x:
                self.change_x += value"""
                
    def enemy_get_hit(self, damage):
        self.enemy_health -= damage
        if self.enemy_health <= 0:
            self.die()
    
    def die(self):
        pygame.sprite.Sprite.kill(self)
        self.drop_coins(self.coin_amount)
        
    def drop_coins(self, amount):
        for i in range(amount):
            coin = iCoin.Coin()
            coin.rect.x = self.rect.x
            coin.rect.y = self.rect.y
            coin.change_x = random.randrange(-5,6)
            coin.change_y = random.randrange(-10,2)
            coin.player = self.player
            coin.level = self.level
            self.level.interact_list.add(coin)
            