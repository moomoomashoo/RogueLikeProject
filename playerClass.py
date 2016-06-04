import pygame
import constants
import swordClass
#from platforms import MovingPlatform

class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.RED)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        
        self.speed = 6 #Default is 6
        self.max_fall_speed = 15
        self.player_max_health = 200
        self.player_health = self.player_max_health
        
        self.player_energy = 100
        self.player_max_energy = self.player_energy
        
        self.player_money = 0
        
        self.facing_right = True
        self.face = True
        self.point_down = False
        self.hit_down = False
        self.point_up = False
        self.hit_up = False
        
        self.invincible = False
        self.max_inv_frames = 90
        self.inv_frames = 0
        
        self.dodging = False
        self.max_dodge_frames = 10
        self.dodge_frames= 0
        
        self.sword_out = False
        
        self.on_floor = False
        
        self.hovering = False
        self.crouching = False
 
        # List of sprites we can bump against
        self.level = None
        
        self.sword_list = pygame.sprite.Group()
 
    def update(self):
        """ Move the player. """
        # Gravity
        #if not self.hovering:
            #self.calc_grav()
            
        if self.dodging:
            for swords in self.sword_list:
                pygame.sprite.Sprite.kill(swords)
            self.dodge_frames += 1
            if self.dodge_frames >= self.max_dodge_frames:
                self.change_x = 0
                self.change_y = 0
                self.dodge_frames = 0
                self.dodging = False
        elif self.hovering:
            ()
        else:
            self.calc_grav()
            
        if self.player_health >= self.player_max_health:
            self.player_health = self.player_max_health
            
        if self.on_floor:
            self.player_energy += 1
            
        if self.player_energy >= self.player_max_energy:
            self.player_energy = self.player_max_energy
                
        if self.player_energy <= 0:
            self.player_energy = 0
            
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.left + block.rect.right) / 2
            if self.rect.left < middle:
                self.rect.right = block.rect.left
            elif self.rect.left > middle:
                self.rect.left = block.rect.right
 
        # Move up/down
        if self.change_y >= self.max_fall_speed:
            self.change_y = self.max_fall_speed
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            middle = (block.rect.top + block.rect.bottom) / 2
            if self.rect.bottom < middle:
                self.rect.bottom = block.rect.top
                self.on_floor = True
                #self.rect.x += block.change_x
                self.jumps = 0
            elif self.rect.top > middle:
                self.rect.top = block.rect.bottom            
            self.change_y = 0
            
        if self.invincible:
            if self.inv_frames >= self.max_inv_frames:
                self.invincible = False
                self.inv_frames = 0
            self.inv_frames += 1
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
            self.on_floor = False
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10
            self.on_floor = False
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
    
    def get_hit(self, enemy_attack):
        if enemy_attack > 0 and not self.invincible:
            self.player_health -= enemy_attack
            self.invincible = True
            
    def melee_attack(self):
        sword = swordClass.Sword(self)
        if len(self.sword_list) == 0:
            self.sword_list.add(sword)
    
    def crouch(self):
        self.crouching = True
        #self.speed = 4
        
    def stop_crouch(self):
        self.crouching = False
        self.speed = 6
        
    def hover(self):
        self.change_y = 0
        self.hovering = True
        for swords in self.sword_list:
            pygame.sprite.Sprite.kill(swords)
    
    def stop_hover(self):
        self.hovering = False
        
    def jetpack(self):
        if self.player_energy >= 20:
            self.change_y = -20
            self.on_floor = False
            self.player_energy -= 20
    
    def dodge_left(self):
        self.change_x = -15
        self.change_y = 0
        self.dodging = True
        
    def dodge_right(self):
        self.change_x = 15
        self.change_y = 0
        self.dodging = True