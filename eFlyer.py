import pygame
import constants
import random
import enemySuperClass as esc


class Flyer(esc.Enemy):
    width = 20
    height = 20
    enemy_health = 10
    enemy_attack = 10
    change_x = 2
    change_y = 2
    
    coin_amount = random.randrange(1,3)

    player = None
    level = None

    def __init__(self):
        esc.Enemy.__init__(self)

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(constants.BLACK)
        self.rect = self.image.get_rect()

        rand_x = random.randrange(2)
        rand_y = random.randrange(2)
        if rand_x == 1:
            self.change_x *= -1
        if rand_y == 1:
            self.change_y *= -1
    
    def update(self):
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
        
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.top + block.rect.bottom) / 2
            if self.rect.bottom < middle:
                self.rect.bottom = block.rect.top
                self.change_y *= -1
            elif self.rect.top > middle:
                self.rect.top = block.rect.bottom 
                self.change_y *= -1