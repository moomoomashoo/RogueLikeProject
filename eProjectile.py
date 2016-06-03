import pygame
import constants
import enemySuperClass as esc

class Projectile(esc.Enemy):
    width = 10
    height = 10
    enemy_health = 0
    enemy_attack = 40
    
    coin_amount = 0
    
    proj_speed = 15
    
    max_proj_time = 900
    proj_time = 0
    
    change_x = 0
    change_y = 0
    
    hits_walls = False
    
    player = None
    level = None

    def __init__(self):
        esc.Enemy.__init__(self)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.WHITE)
        self.rect = self.image.get_rect()
        
        #self.coin_list = pygame.sprite.Group()
        
    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        if self.proj_time >= self.max_proj_time:
            self.die()
        self.proj_time += 1