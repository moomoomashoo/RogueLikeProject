import pygame
import constants
import enemySuperClass as esc

class Walker(esc.Enemy):
    width = 40
    height = 60
    enemy_health = 100
    enemy_attack = 20
    change_x = 2
    change_y = 0
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None
    level = None
    
    max_fall_speed = 15
    
    def __init__(self):
        esc.Enemy.__init__(self)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.PURPLE)
        self.rect = self.image.get_rect()

        #if self.change_x > 0:
           # self.moving_right = True

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.left + block.rect.right) / 2
            if self.rect.left < middle:
                self.rect.right = block.rect.left
                self.change_x *= -1
            elif self.rect.left > middle:
                self.rect.left = block.rect.right
                self.change_x *= -1
                
        print(self.change_x)
        
        if self.change_y >= self.max_fall_speed:
            self.change_y = self.max_fall_speed        
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.top + block.rect.bottom) / 2
            if self.rect.bottom < middle:
                self.rect.bottom = block.rect.top
            elif self.rect.top > middle:
                self.rect.top = block.rect.bottom 