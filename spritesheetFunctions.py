import constants as con
import pygame as py

class SpriteSheet(object):
    def __init__(self, file_name):
        self.sprite_sheet = py.image.load(file_name).convert()
        
    def get_image(self, x, y, width, height):
        image = py.Surface([width, height]).convert()
        
        image.blit(self.sprite_sheet, (0,0), (x,y,width,height))
        
        image.set_colorkey(con.WHITE)
        
        return image
    
    def get_image2(self, tup):
        image = py.Surface([tup[2], tup[3]]).convert()
        
        image.blit(self.sprite_sheet, (0,0), (tup[0],tup[1],tup[2],tup[3]))
        
        image.set_colorkey(con.WHITE)
        
        return image