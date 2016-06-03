import pygame
import constants
import random
import enemySuperClass as esc

class Bouncer(esc.Enemy):
    width = 40
    height = 40
    enemy_health = 100
    enemy_attack = 60
    
    change_x = 2
    change_y = 0
    
    coin_amount = random.randrange(3,7)

    player = None
    level = None
    
    max_fall_speed = 15
    
    bounce = 1
    
    def __init__(self):
        esc.Enemy.__init__(self)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.PURPLE)
        self.rect = self.image.get_rect()

    def update(self):
        self.calc_grav()
        if self.change_x >= self.max_fall_speed//2:
            self.change_x = self.max_fall_speed//2
        self.rect.x += self.change_x
        
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.left + block.rect.right) / 2
            if self.rect.left < middle:
                self.rect.right = block.rect.left
                self.change_x *= -self.bounce
            elif self.rect.left > middle:
                self.rect.left = block.rect.right
                self.change_x *= -self.bounce
        
        if self.change_y >= self.max_fall_speed:
            self.change_y = self.max_fall_speed   
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.top + block.rect.bottom) / 2
            if self.rect.bottom < middle:
                self.rect.bottom = block.rect.top
                self.change_y *= -self.bounce
            elif self.rect.top > middle:
                self.rect.top = block.rect.bottom 
                self.change_y *= -self.bounce