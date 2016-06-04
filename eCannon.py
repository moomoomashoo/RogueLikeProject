import pygame
import random
import constants
import enemySuperClass as esc
import eProjectile

class Cannon(esc.Enemy):
    width = 40
    height = 40
    enemy_health = 50
    enemy_attack = 40
    
    coin_amount = random.randrange(2,5)
    
    direction = 0
    
    fire_speed = 36
    fire_timer = 0
    
    player = None
    level = None

    def __init__(self):
        esc.Enemy.__init__(self)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.BLACK)
        self.rect = self.image.get_rect()
        
        self.direction = random.randrange(0,4)
        

    def update(self):
        if self.fire_timer >= self.fire_speed:
            self.fire_proj(self.direction)
            self.fire_timer = 0
            self.direction += 1
            if self.direction >= 4:
                self.direction = 0
        self.fire_timer += 1
                
    def fire_proj(self, direction):
        proj = eProjectile.Projectile()
        proj.hits_walls = True
        if direction == 0:
            proj.change_x = -proj.proj_speed
            proj.change_y = 0
        elif direction == 1:
            proj.change_x = 0
            proj.change_y = -proj.proj_speed
        elif direction == 2:
            proj.change_x = proj.proj_speed
            proj.change_y = 0
        elif direction == 3:
            proj.change_x = 0
            proj.change_y = proj.proj_speed
        proj.rect.x = (self.rect.left+self.rect.right)//2 - proj.rect.width//2
        proj.rect.y = (self.rect.top+self.rect.bottom)//2 - proj.rect.height//2
        proj.player = self.player
        proj.level = self.level
        self.level.enemy_list.add(proj)
        
        