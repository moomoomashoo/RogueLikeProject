import math
import pygame as py
import constants as con

class Sword(py.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        
        self.player = player
        self.player_damage = 0
        self.sword_damage = 50
        self.arc = -90
        self.arcul = -150
        self.arcur = -30
        
        self.slash_dist = 60
        
        self.image = py.Surface([10,10])
        self.image.fill(con.WHITE)
        
        self.rect = self.image.get_rect()
        
    def update(self):
        self.sword_damage = 50
        self.player.max_fall_speed = 15
        
        if self.player.hit_down:
            self.sword_damage = 100
            self.down_stab()
        elif self.player.hit_up and self.player.facing_right:
            self.slash_up_right()
        elif self.player.hit_up:
            self.slash_up_left()
        elif self.player.face:
            self.slash_right()
        elif not self.player.face:
            self.slash_left()
        else:
            ()
    
    def slash_right(self):
        rad = math.radians(self.arc)
        cen_x = (self.player.rect.left + self.player.rect.right) // 2
        cen_y = (self.player.rect.top + self.player.rect.bottom) // 2
        self.rect.x = cen_x + (self.slash_dist * math.cos(rad)) - (self.rect.width//2)
        self.rect.y = cen_y + (self.slash_dist * math.sin(rad)) - (self.rect.height//2)
        if self.arc >= 30:
            py.sprite.Sprite.kill(self)
            self.arc = -90
        self.arc += 15

    def slash_left(self):
        rad = math.radians(self.arc)
        cen_x = (self.player.rect.left + self.player.rect.right) // 2
        cen_y = (self.player.rect.top + self.player.rect.bottom) // 2
        self.rect.x = cen_x + (self.slash_dist * math.cos(rad)) - (self.rect.width//2)
        self.rect.y = cen_y + (self.slash_dist * math.sin(rad)) - (self.rect.height//2)
        if self.arc <= -210:
            py.sprite.Sprite.kill(self)
            self.arc = -90
        self.arc -= 15
        
    def slash_up_right(self):
        rad = math.radians(self.arcul)
        cen_x = (self.player.rect.left + self.player.rect.right) // 2
        cen_y = (self.player.rect.top + self.player.rect.bottom) // 2
        self.rect.x = cen_x + (self.slash_dist * math.cos(rad)) - (self.rect.width//2)
        self.rect.y = cen_y + (self.slash_dist * math.sin(rad)) - (self.rect.height//2)
        if self.arcul >= -30:
            py.sprite.Sprite.kill(self)
            self.arcul = -150
        self.arcul += 15
        
    def slash_up_left(self):
        rad = math.radians(self.arcur)
        cen_x = (self.player.rect.left + self.player.rect.right) // 2
        cen_y = (self.player.rect.top + self.player.rect.bottom) // 2
        self.rect.x = cen_x + (self.slash_dist * math.cos(rad)) - (self.rect.width//2)
        self.rect.y = cen_y + (self.slash_dist * math.sin(rad)) - (self.rect.height//2)
        if self.arcur <= -150:
            py.sprite.Sprite.kill(self)
            self.arcur = -30
        self.arcur -= 15
        
    def down_stab(self):
        cen_x = (self.player.rect.left + self.player.rect.right) // 2
        self.rect.x = cen_x - (self.rect.width//2)
        self.rect.bottom = (self.player.rect.top + self.player.rect.bottom)//2 + self.slash_dist
        if self.arc >= -30 or self.player.on_floor:
            py.sprite.Sprite.kill(self)
            self.arc = -90
        self.arc += 1
        