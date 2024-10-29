# Enitites and Player File

import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.death_collisions = False
        self.win_collision =  False

        self.action = ''
        self.anim_offset = (-6, -14)
        self.flip = False
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # Horizontal movement and collision
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        rects, _ , _= tilemap.physics_rects_around(self.pos) # tile collision and collision with lava
        
        for rect in rects:
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:  # Check for a collision on the right
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                    
                if frame_movement[0] < 0:  # Check for a collision on the left
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x


        # Vertical movement and collision
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        
        for rect in rects:
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:  # Checks for downward collision
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    
                if frame_movement[1] < 0:  # Checks for upwards collision
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y


        # flip the player animation depending on the direction they are moving
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)


        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()


    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        
        self.is_dead = False     
        self.did_win = False
        
        self.win_timer = 0
        self.death_timer = 0  
        
        self.can_jump = True 
        
        self.death_animation_played = False 
        self.winner_animation_played = False
        

    def update(self, tilemap, movement=(0, 0)):
        # verfiy that the player is neither dead or has not won the game
        if not self.is_dead and not self.did_win:
            
            # Keep updating while the player is alive
            super().update(tilemap, movement=movement)

            if self.collisions['down']:
                self.air_time = 0
                self.can_jump = True 
            else:
                self.air_time += 1
            
            
            # update the players action depending on the condition met
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

            
            #check to see if the player fell of the map and update the action 
            if self.pos[1] > 480:
                self.is_dead = True
                self.death_timer = 30
                self.set_action('death')
            
              
            rects, death, winner = tilemap.physics_rects_around(self.pos)
            if death:
                # checks to see if the death animation is played
                if not self.death_animation_played:
                    self.is_dead = True  
                    self.death_timer = 30  
                    self.set_action('death')
                    
           
            if winner:
                # checks to see if the winner animation is played
                if not self.winner_animation_played:
                    self.did_win = True
                    self.win_timer = 30
                    self.set_action('winner')
                    
                
        else:
            self.animation.update()
            
             # Increment timers for both death and win states
            if self.is_dead:
                self.death_timer += 1

            if self.did_win:
                self.win_timer += 1
            

        # Check if the death animation or winner animation has finished and send to the correlating screen
        if self.death_timer >= 60:  
            self.death_animation_played = True
            self.game.game_over = True 
         
            
        if self.win_timer >= 60:
            self.winner_animation_played = True
            self.game.game_winner = True
                
            
              
                 
    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))
       
    
    # Reset everything to original value after the player dies or wins the game
    def reset(self):
        self.is_dead = False
        self.did_win = False
        
        self.death_animation_played = False
        self.winner_animation_played = False
        
        self.pos = [50, 50]  
        self.velocity = [0, 0]  
        self.set_action('idle')  
