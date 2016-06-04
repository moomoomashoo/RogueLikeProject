import pygame
import random
import constants
import math
import enemySuperClass as esc

class Ghost(esc.Enemy):
    width = 40
    height = 40
    enemy_health = 200
    enemy_attack = 60
    
    coin_amount = random.randrange(2,5)
    
    max_speed_x = 0
    max_speed_y = 0
    change_x = 0
    change_y = 0

    awake = False

    player = None
    level = None

    def __init__(self):
        esc.Enemy.__init__(self)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.WHITE)
        self.rect = self.image.get_rect()
        
        #self.coin_list = pygame.sprite.Group()

    def update(self):
        value = .2

        centre_x = (self.rect.left+self.rect.right)//2
        centre_y = (self.rect.top+self.rect.bottom)//2

        dist_x = centre_x - (self.player.rect.left+self.player.rect.right)/2
        dist_y = centre_y - (self.player.rect.top+self.player.rect.bottom)/2
        hyp = math.sqrt((dist_x*dist_x)+(dist_y*dist_y))
        if hyp < 400:
            self.awake = True
        if hyp > 800:
            self.awake = False

        if centre_x > self.player.rect.left and centre_x < self.player.rect.right:
            self.max_speed_x = 0
        else:
            self.max_speed_x = 3
        
        if centre_y > self.player.rect.top and centre_y < self.player.rect.bottom:
            self.max_speed_y = 0
        else:
            self.max_speed_y = 3
        
        if self.awake:
            #self.fire_proj()
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