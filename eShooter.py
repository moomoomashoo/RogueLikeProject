import pygame
import random
import constants
import math
import enemySuperClass as esc
import eProjectile

class Shooter(esc.Enemy):
    width = 40
    height = 40
    enemy_health = 50
    enemy_attack = 40
    
    coin_amount = random.randrange(2,5)
    
    max_speed_x = 0
    max_speed_y = 0
    change_x = 0
    change_y = 0

    awake = False
    aim_mode = False
    fire_mode = False
    
    fire_speed = 36
    fire_timer = 0
    
    fire_spot_x = 0
    fire_spot_y = 0
    
    theta = 0
    
    player = None
    level = None

    def __init__(self):
        esc.Enemy.__init__(self)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.GREY)
        self.rect = self.image.get_rect()
        
        #self.coin_list = pygame.sprite.Group()

    def update(self):
        value = .2
        

        centre_x = (self.rect.left+self.rect.right)//2
        centre_y = (self.rect.top+self.rect.bottom)//2

        dist_x = (self.player.rect.left+self.player.rect.right)/2 - centre_x
        dist_y = (self.player.rect.top+self.player.rect.bottom)/2 - centre_y
        hyp = math.sqrt((dist_x*dist_x)+(dist_y*dist_y))
        
        if hyp < 200:
            self.aim_mode = True
            
        if self.fire_timer >= self.fire_speed and self.aim_mode:
            self.fire_mode = True
            self.aim_mode = False
            
            
        if hyp < 400:
            self.awake = True
        if hyp > 800:
            self.awake = False
            self.fire_timer = 0

        if centre_x > self.player.rect.left and centre_x < self.player.rect.right:
            self.max_speed_x = 0
        else:
            self.max_speed_x = 3
        
        if centre_y > self.player.rect.top and centre_y < self.player.rect.bottom:
            self.max_speed_y = 0
        else:
            self.max_speed_y = 3
            
        if self.fire_mode:
            self.fire_timer += 1
            if self.fire_timer >= self.fire_speed + 10:
                self.fire_proj(dist_x, dist_y)
                self.fire_timer = 0
                self.fire_mode = False
                
            self.theta = math.atan2(dist_y,dist_x)
            
        elif self.aim_mode:
            self.fire_timer += 1
            self.rect.x = (self.player.rect.left+self.player.rect.right)//2 + (-hyp * math.cos(self.theta)) - (self.rect.width//2)
            self.rect.y = (self.player.rect.top+self.player.rect.bottom)//2 + (-hyp * math.sin(self.theta)) - (self.rect.height//2)
            
            self.theta += 0.01
        
        elif self.awake:
            self.rect.x += round(self.change_x)
        
            if self.rect.left < self.player.rect.right and self.change_x < self.max_speed_x:
                self.change_x += value
            elif self.rect.right > self.player.rect.left and self.change_x > -self.max_speed_x:
                self.change_x -= value

            self.rect.y += round(self.change_y)
        
            if self.rect.y < self.player.rect.y and self.change_y < self.max_speed_y:
                self.change_y += value
            if self.rect.y > self.player.rect.y and self.change_y > -self.max_speed_y:
                self.change_y -= value
                
            self.theta = math.atan2(dist_y,dist_x)
                
    def fire_proj(self, x, y):
        proj = eProjectile.Projectile()
        theta = math.atan2(y,x)
        proj.rect.x = (self.rect.left+self.rect.right)//2 - proj.rect.width//2
        proj.rect.y = (self.rect.top+self.rect.bottom)//2 - proj.rect.height//2
        proj.change_x = round(proj.proj_speed * math.cos(theta))
        proj.change_y = round(proj.proj_speed * math.sin(theta))
        proj.player = self.player
        proj.level = self.level
        self.level.enemy_list.add(proj)
        
        