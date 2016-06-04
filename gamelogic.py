import pygame
import constants
from playerClass import Player
import iDoor
import iCoin
import iGold
import iChest
import eProjectile
import levels

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        # Create the player
        self.player = Player()
        
        self.screen = None
        
        self.LB = False
        self.B_Button = False
        
        self.minimap_on = False
        
        self.world_shift_x = 0
        self.world_shift_y = 0

        self.game_over = False
        self.paused = False

        self.joystick_count = pygame.joystick.get_count()
        if self.joystick_count == 0:
            # No joysticks!
            print("Error, I didn't find any joysticks.")
        else:
            # Use joystick #0 and initialize it
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()

        self.active_sprite_list = pygame.sprite.Group()
        
        self.active_sprite_list.add(self.player)
        
        self.current_level_no = 0
        
        self.level_list = []
        self.level_list.append(levels.Level(self.player))
        self.current_level = self.level_list[self.current_level_no]
        
        self.player.level = self.current_level
        
        #self.player.rect.x = self.current_level.pos_x
        #self.player.rect.y = self.current_level.pos_y

        #self.player.rect.x = 100
        #self.player.rect.y = 100

    def next_level(self):
        self.level_list.append(levels.Level(self.player))
        self.current_level_no += 1
        self.current_level = self.level_list[self.current_level_no]
        self.player.level = self.current_level
        self.player.change_x = 0
        self.player.change_y = 0
        self.player.player_health += 50

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """
        if self.paused:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    return True
                    
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.my_joystick.get_button(7): # Start
                        self.paused = False
                        self.minimap_on = False
            
        else:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    return True
    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.go_left()
                    if event.key == pygame.K_RIGHT:
                        self.player.go_right()
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        return True
    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.player.change_x < 0:
                        self.player.stop()
                    if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                        self.player.stop()
    
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.my_joystick.get_button(0): # A
                        self.player.jump()
                    if self.my_joystick.get_button(1): # B
                        ()#self.next_level()
                    if self.my_joystick.get_button(2): # X
                        if self.player.point_down:
                            self.player.hit_down = True
                            self.player.hit_up = False
                            self.player.max_fall_speed = 30
                            self.player.change_y = 20
                        elif self.player.point_up:
                            self.player.hit_up = True
                            self.player.hit_down = False
                        elif self.player.facing_right:
                            self.player.face = True
                            self.player.hit_up = False
                            self.player.hit_down = False
                        else:
                            self.player.face = False
                            self.player.hit_up = False
                            self.player.hit_down = False
                        self.player.melee_attack()
                    if self.my_joystick.get_button(3): # Y
                        () #self.minimap_on = not self.minimap_on
                    if self.my_joystick.get_button(5): # RB
                        self.player.jetpack()
                    if self.my_joystick.get_button(6): # Back
                        self.__init__()
                    if self.my_joystick.get_button(7): # Start
                        self.paused = True
                        self.minimap_on = True
                        
                if self.my_joystick.get_button(4): # LB
                    if event.type == pygame.JOYBUTTONDOWN:
                        self.LB = True
                        self.player.hover()
                        self.player.hit_down = False
                if self.LB and event.type == pygame.JOYBUTTONUP:
                        self.LB = False
                        self.player.stop_hover()
    
            if self.joystick_count != 0:
                horiz_axis_pos = self.my_joystick.get_axis(0)
                if horiz_axis_pos > 0.2 or horiz_axis_pos < -0.2:
                    self.player.rect.x += horiz_axis_pos * self.player.speed
                if horiz_axis_pos > 0.2:
                    self.player.facing_right = True
                elif horiz_axis_pos < -0.2:
                    self.player.facing_right = False
                vert_axis_pos = self.my_joystick.get_axis(1)
                if vert_axis_pos > 0.4:
                    self.player.point_down = True
                    self.player.point_up = False
                elif vert_axis_pos < -0.4:
                    self.player.point_up = True
                    self.player.point_down = False
                else:
                    self.player.point_up = False
                    self.player.point_down = False
                triggers = self.my_joystick.get_axis(2)
                if triggers < -0.5:
                    self.player.dodge_right()
                elif triggers > 0.5:
                    self.player.dodge_left()
            return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        
        if self.paused:
            ()

        elif not self.game_over:
            self.active_sprite_list.update()

            # Update items in the level
            self.current_level.update()

            self.player.level = self.current_level
            
            player_hit_list = pygame.sprite.spritecollide(self.player, self.current_level.enemy_list, False)
            interactable_hit_list = pygame.sprite.spritecollide(self.player, self.current_level.interact_list, False)
            
            for platforms in self.current_level.platform_list:           
                enemy_platform_hit = pygame.sprite.spritecollide(platforms, self.current_level.enemy_list, False)
                for enemy in enemy_platform_hit:
                    if isinstance(enemy, eProjectile.Projectile) and enemy.hits_walls:
                        enemy.die()
            
            if len(player_hit_list) > 0:
                for enemy in player_hit_list:
                    self.player.get_hit(enemy.enemy_attack)
                    if isinstance(enemy, eProjectile.Projectile):
                        enemy.die()
                    
            if len(interactable_hit_list) > 0:
                for interactable in interactable_hit_list:
                    if isinstance(interactable, iDoor.Door) and self.player.point_up:
                        self.next_level()
                    if isinstance(interactable, iCoin.Coin):
                        interactable.pickup_money()
                    if isinstance(interactable, iGold.Gold):
                        interactable.pickup_gold()
                    if isinstance(interactable, iChest.Chest) and self.player.point_up:
                        interactable.open_chest()
                    
            if self.player.player_health <= 0:
                self.game_over = True
            
            for swords in self.player.sword_list:
                enemy_hit_list = pygame.sprite.spritecollide(swords, self.current_level.enemy_list, False)
                for enemy in enemy_hit_list:
                    if isinstance(enemy, eProjectile.Projectile):
                        ()
                    else:
                        enemy.enemy_get_hit(swords.sword_damage)

            left_wall = self.current_level.level_boundary_left + self.current_level.world_shift_x
            right_wall = self.current_level.level_boundary_right + self.current_level.world_shift_x
            floor = self.current_level.level_boundary_bottom + self.current_level.world_shift_y
            ceiling = self.current_level.level_boundary_top + self.current_level.world_shift_y

            self.cur_pos_x = self.current_level.level_boundary_left + self.player.rect.x - self.current_level.world_shift_x
            self.cur_pos_y = self.current_level.level_boundary_top + self.player.rect.y - self.current_level.world_shift_y
            
            move_bound = constants.SCREEN_WIDTH - 300

            # If the player gets near the right side, shift the world left (-x)
            if right_wall >= constants.SCREEN_WIDTH and self.player.rect.right >= move_bound:
                diff = self.player.rect.right - move_bound
                self.player.rect.right = move_bound
                self.current_level.shift_world_x(-diff)
                
            move_bound = 300

            # If the player gets near the left side, shift the world right (+x)
            if left_wall <= 0 and self.player.rect.left <= move_bound:
                diff = move_bound - self.player.rect.left
                self.player.rect.left = move_bound
                self.current_level.shift_world_x(diff)
                
            move_bound = 200

            if ceiling <= 0 and self.player.rect.top <= move_bound:
                diff = self.player.rect.top - move_bound
                self.player.rect.top = move_bound
                self.current_level.shift_world_y(-diff)
                
            move_bound = constants.SCREEN_HEIGHT - 400

            if floor >= constants.SCREEN_HEIGHT and self.player.rect.bottom >= move_bound:
                diff = move_bound - self.player.rect.bottom
                self.player.rect.bottom = move_bound
                self.current_level.shift_world_y(diff)


    def draw_HUD(self, screen):
        font = pygame.font.SysFont("serif", 25, True)
        text = font.render("Health: ", True, constants.BLACK)
        screen.blit(text, [20,20])
        pygame.draw.rect(screen, constants.RED, (110, 20, self.player.player_max_health, 25), 0)
        if self.player.player_health >= 0:
            pygame.draw.rect(screen, constants.DARK_GREEN, (110, 20, self.player.player_health, 25), 0)
        pygame.draw.rect(screen, constants.BLACK, (110, 20, self.player.player_max_health, 25), 3)
        
        text = font.render("Energy: ", True, constants.BLACK)
        screen.blit(text, [constants.SCREEN_WIDTH - text.get_width() - 150,20])
        pygame.draw.rect(screen, constants.RED, (constants.SCREEN_WIDTH- 150, 20, self.player.player_max_energy, 25), 0)
        if self.player.player_energy >= 0:
            pygame.draw.rect(screen, constants.ORANGE, (constants.SCREEN_WIDTH - 150, 20, self.player.player_energy, 25), 0)
        pygame.draw.rect(screen, constants.BLACK, (constants.SCREEN_WIDTH - 150, 20, self.player.player_max_energy, 25), 3)
        
        text = font.render("Money: " + str(self.player.player_money), True, constants.BLACK)
        screen.blit(text, [20, 50])
        text = font.render("Level no: " + str(self.current_level_no), True, constants.BLACK)
        screen.blit(text, [20, 80])
        
    def minimap(self, screen):
        p = 10
        buffer = 100
        center_x = (constants.SCREEN_WIDTH // 2)
        pygame.draw.rect(screen, constants.BLACK, (center_x - (constants.screen_tiles_width*p//2)-10, buffer-10, constants.screen_tiles_width*p+20, constants.screen_tiles_height*p+20), 0)
        pygame.draw.rect(screen, constants.WHITE, (center_x - (constants.screen_tiles_width*p//2), buffer, constants.screen_tiles_width*p, constants.screen_tiles_height*p), 0)
        for r in range(0, constants.screen_tiles_height):
            for c in range(0, constants.screen_tiles_width):
                if self.current_level.level[r][c] in (constants.PERM_WALL, constants.WALL, constants.FLOOR):
                    pygame.draw.rect(screen, constants.GREY, (center_x - (constants.screen_tiles_width*p//2) + c*p, r*p + buffer, p, p), 0)
        pygame.draw.rect(screen, constants.RED, ((center_x - (constants.screen_tiles_width*p//2)) + (self.cur_pos_x//constants.tile_size)*p, (self.cur_pos_y//constants.tile_size)*p + buffer, p, p*2), 0)
        
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(constants.WHITE)
        
        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            self.current_level.draw(screen)
            self.draw_HUD(screen)
            font2 = pygame.font.SysFont('Arial Black', 40)
            text = font2.render("Game Over", True, constants.BLACK)
            font_small = pygame.font.SysFont('Arial Black', 20)
            text2 = font_small.render("Press Back to restart", True, constants.BLACK)
            center_x = (constants.SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (constants.SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y - 10])
            screen.blit(text2, [center_x, center_y + text2.get_height() + 10])
            
        elif self.paused:
            self.current_level.draw(screen)
            self.draw_HUD(screen)
            self.active_sprite_list.draw(screen)
            font2 = pygame.font.SysFont('Arial Black', 40)
            text = font2.render("Paused", True, constants.BLACK)
            center_x = (constants.SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (constants.SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            if self.minimap_on:
                self.minimap(screen)
            screen.blit(text, [center_x, 30])
            
        else:
            self.current_level.draw(screen)
            self.active_sprite_list.draw(screen)
            self.draw_HUD(screen)
            if self.minimap_on:
                self.minimap(screen)
                
        pygame.display.flip()