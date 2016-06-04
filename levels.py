import pygame
import random
from spritesheetFunctions import SpriteSheet

import constants as con
import eGhost
import eShooter
import eCannon
import eFlyer
import eBouncer

import iDoor
import iChest
import iGold

import platforms
from CA_CaveFactory import CA_CaveFactory

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.interact_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        
        self.player.rect.x = (con.screen_tiles_width*con.tile_size) // 2
        self.player.rect.y = (con.screen_tiles_height*con.tile_size) // 2

        # Background image
        self.background = None

        # How far this world has been scrolled left/right
        self.world_shift_x = 0
        self.world_shift_y = 0
        
        keep_level = False
        
        while not keep_level:
            
            big_enough = False
            spawn_ok = False
            
            cave = CA_CaveFactory(con.screen_tiles_height, con.screen_tiles_width, con.percent_fill)

            """ Loop through 5 times """
            for i in range(5):
                self.level = cave.gen_map()
                #cave.print_grid()
                    
            cave.set_spawn()
            s_p = cave.get_spawn()
            if self.level[s_p[0]][s_p[1]] is con.SPAWN_POINT:
                spawn_ok = True
            
            cave.flood_fill(self.level, s_p[0], s_p[1]-1, con.FLOOR, con.PERM_FLOOR)
            cave.set_exit()
            big_enough = cave.check_percent_fill(self.level)
            
            if big_enough and spawn_ok:
                keep_level = True
            
            if keep_level:
                break
        
        rand_num = random.randrange(con.min_ghosts, con.max_ghosts+1)
        cave.set_object_spawn(con.GHOST, rand_num, False)
        
        rand_num = random.randrange(con.min_shooters, con.max_shooters+1)
        cave.set_object_spawn(con.SHOOTER, rand_num, False)
        
        rand_num = random.randrange(con.min_cannons, con.max_cannons+1)
        cave.set_object_spawn(con.CANNON, rand_num, False)
        
        rand_num = random.randrange(con.min_flyers, con.max_flyers+1)
        cave.set_object_spawn(con.FLYER, rand_num, False)
        
        rand_num = random.randrange(con.min_bouncers, con.max_bouncers+1)
        cave.set_object_spawn(con.BOUNCER, rand_num, False)
        
        rand_num = random.randrange(con.min_chests, con.max_chests+1)        
        cave.set_object_spawn(con.CHEST, rand_num, True)
        
        rand_num = random.randrange(con.min_treasure, con.max_treasure+1)
        cave.set_object_spawn(con.TREASURE, rand_num, True)
        
        #cave.print_grid()

        """ Define level Boundaries """
        self.level_boundary_left = 0
        self.level_boundary_right = con.screen_tiles_width * con.tile_size
        self.level_boundary_top = 0
        self.level_boundary_bottom = con.screen_tiles_height * con.tile_size
        
        
        """Import the sprites"""
        """sprite_sheet = SpriteSheet("SpriteSheets/TestDirt.png")
        
        dirt_blocks = []
        dirt_blocks.append(sprite_sheet.get_image2(platforms.DIRT_UDLR_1))
        dirt_blocks.append(sprite_sheet.get_image2(platforms.DIRT_DLR_1))
        dirt_blocks.append(sprite_sheet.get_image2(platforms.DIRT_ULR_1))
        dirt_blocks.append(sprite_sheet.get_image2(platforms.DIRT_UDR_1))
        dirt_blocks.append(sprite_sheet.get_image2(platforms.DIRT_ULR_1))"""
        

        """Add extra borders to make it look nicer """
        for j in range(-1, con.screen_tiles_height + 1):
            block = platforms.Platform(con.tile_size, con.tile_size)
            #block = platforms.Platform(dirt_blocks[0])
            block.rect.x = self.level_boundary_left - con.tile_size
            block.rect.y = j * con.tile_size
            block.player = self.player
            self.platform_list.add(block)
            
            block = platforms.Platform(con.tile_size, con.tile_size)
            #block = platforms.Platform(dirt_blocks[0])
            block.rect.x = self.level_boundary_right
            block.rect.y = j * con.tile_size
            block.player = self.player
            self.platform_list.add(block)

        for j in range(-1, con.screen_tiles_width + 1):
            block = platforms.Platform(con.tile_size, con.tile_size)            
            #block = platforms.Platform(dirt_blocks[0])
            block.rect.x = j * con.tile_size
            block.rect.y = self.level_boundary_top - con.tile_size
            block.player = self.player
            self.platform_list.add(block)

            block = platforms.Platform(con.tile_size, con.tile_size)
            #block = platforms.Platform(dirt_blocks[0])
            block.rect.x = j * con.tile_size
            block.rect.y = self.level_boundary_bottom
            block.player = self.player
            self.platform_list.add(block)
        
        #ghost_count = 5
        # Add stuff to level
        for r in range(0, con.screen_tiles_height):
            for c in range(0, con.screen_tiles_width):
                if self.level[r][c] in (con.PERM_WALL, con.WALL, con.FLOOR):
                    block = platforms.Platform(con.tile_size, con.tile_size)
                    #block = platforms.Platform(platforms.DIRT_DLR_1)
                    #block = platforms.Platform(dirt_blocks[0])
                    block.rect.x = c * con.tile_size
                    block.rect.y = r * con.tile_size
                    block.player = self.player
                    self.platform_list.add(block)
                elif self.level[r][c] == con.SPAWN_POINT:
                    self.player.rect.x = c * con.tile_size + 5
                    self.player.rect.bottom = r * con.tile_size + con.tile_size -2
                elif self.level[r][c] == con.EXIT_POINT:
                    e_door = iDoor.Door()
                    e_door.rect.x = c * con.tile_size
                    e_door.rect.bottom = r * con.tile_size + con.tile_size
                    e_door.player = self.player
                    self.interact_list.add(e_door)
                elif self.level[r][c] == con.GHOST:
                    ghost = eGhost.Ghost()
                    ghost.rect.x = c * con.tile_size
                    ghost.rect.y = r * con.tile_size
                    ghost.player = self.player
                    ghost.level = self
                    self.enemy_list.add(ghost)
                elif self.level[r][c] == con.SHOOTER:
                    shooter = eShooter.Shooter()
                    shooter.rect.x = c * con.tile_size
                    shooter.rect.y = r * con.tile_size
                    shooter.player = self.player
                    shooter.level = self
                    self.enemy_list.add(shooter)
                elif self.level[r][c] == con.CANNON:
                    cannon = eCannon.Cannon()
                    cannon.rect.x = (((c * con.tile_size)+(c*con.tile_size + con.tile_size))//2) - (cannon.rect.width//2)
                    cannon.rect.bottom = r * con.tile_size + con.tile_size
                    cannon.player = self.player
                    cannon.level = self
                    self.enemy_list.add(cannon)
                elif self.level[r][c] == con.FLYER:
                    flyer = eFlyer.Flyer()
                    flyer.rect.x = c * con.tile_size
                    flyer.rect.y = r * con.tile_size
                    flyer.player = self.player
                    flyer.level = self
                    self.enemy_list.add(flyer)
                elif self.level[r][c] == con.BOUNCER:
                    bouncer = eBouncer.Bouncer()
                    bouncer.rect.x = c * con.tile_size
                    bouncer.rect.y = r * con.tile_size
                    bouncer.player = self.player
                    bouncer.level = self
                    self.enemy_list.add(bouncer)
                elif self.level[r][c] == con.CHEST:
                    chest = iChest.Chest()
                    chest.rect.x = (((c * con.tile_size)+(c*con.tile_size + con.tile_size))//2) - (chest.rect.width//2)
                    chest.rect.bottom = r * con.tile_size + con.tile_size
                    chest.player = self.player
                    chest.level = self
                    self.interact_list.add(chest)
                elif self.level[r][c] == con.TREASURE:
                    gold = iGold.Gold()
                    gold.rect.x = (((c * con.tile_size)+(c*con.tile_size + con.tile_size))//2) - (gold.rect.width//2)
                    gold.rect.bottom = r * con.tile_size + con.tile_size
                    gold.player = self.player
                    gold.level = self
                    self.interact_list.add(gold)
                else:
                    ()
            
    def update(self):
        """ Update everything in this level."""
        
        self.platform_list.update()
        self.interact_list.update()
        self.enemy_list.update()
        self.player.sword_list.update()
        for enemy in self.enemy_list:
            enemy.coin_list.update()
    
    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(con.BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.interact_list.draw(screen)
        self.enemy_list.draw(screen)
        self.player.sword_list.draw(screen)
        

    def shift_world_x(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:"""
        # Keep track of the shift amount
        self.world_shift_x += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
            
        for interact in self.interact_list:
            interact.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        
        for sword in self.player.sword_list:
            sword.rect.x += shift_x

    def shift_world_y(self, shift_y):
        self.world_shift_y += shift_y

        for platform in self.platform_list:
            platform.rect.y += shift_y
        
        for interact in self.interact_list:
            interact.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.y += shift_y
        
        for sword in self.player.sword_list:
            sword.rect.y += shift_y