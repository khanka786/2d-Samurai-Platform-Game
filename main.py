# Main Game File 

import pygame
import sys
from scripts.utilities import load_image, load_images, Animation
from scripts.entities import Player, PhysicsEntity
from scripts.tilemaps import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Ninja Obstacle Course')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((350, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            # game screens
            'background': load_image('background.png'),
            'game_over': load_image('game_over.png'),
            'game_winner': load_image('game_winner.png'),
            
            # game tiles
            'stone': load_images('tiles/stone'),
            'grass': load_images('tiles/grass'),
            'decor': load_images('tiles/decor'),
            'large_decor': load_images('tiles/large_decor'),
            'platforms': load_images('tiles/platforms'),
            'bridge': load_images('tiles/bridge'),
            'lava': load_images('tiles/lava'),
            'trophy': load_images('tiles/trophy'),
            
            # game entities and animations
            'player': load_image('entities/player/player.png'),
            'player/idle': Animation(load_images("entities/player/idle"), img_dur=6),
            'player/run': Animation(load_images("entities/player/run"), img_dur=4),
            'player/jump': Animation(load_images("entities/player/jump")),
            'player/winner': Animation(load_images("entities/player/winner")),
            'player/death': Animation(load_images("entities/player/death")),
        }

        print(self.assets)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        self.scroll = [0, 0]
        self.game_over = False
        self.game_winner = False

    def reset_game(self):
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap.load('map.json') 
        self.scroll = [0, 0]        
        self.game_over = False    # bool to see if the player died
        self.game_winner = False  # bool to see if the player won

    # show a game over screen after the game has ended
    def show_game_over_screen(self):
        print("Entered show_game_over_screen.")  # Debugging message
        while True:
            # Draw the game over screen
            self.display.blit(self.assets['background'], (0, 0))
            self.display.blit(self.assets['game_over'], (35, 0))
        
            pygame.font.init()
            font = pygame.font.SysFont(None, 25)
            text = font.render('Press Y to Play Again or N to Quit', True, (255, 255, 255))
            self.display.blit(text, (50, 210))

            # Handle events for play again or quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        print("Resetting game...")  # Debugging
                        self.reset_game()  # Reset game state and return to main loop
                        return
                    if event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(110)

     
    # show the player has won on the screen                   
    def show_winner_game_screen(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))
            self.display.blit(self.assets['game_winner'], (35, 0))
            pygame.font.init()
            font = pygame.font.SysFont(None, 25)
            text = font.render('Press Y to Play Again or N to Quit', True, (255, 255, 255))
            self.display.blit(text, (50, 210))

            # Ask the user if they want to play again after they win the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        print("Resetting game...")  # Debugging  
                        self.reset_game()           # reset the game back to the orginial state
                        return  
                    if event.key == pygame.K_n:  
                        pygame.quit()
                        sys.exit()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(110)

    def run(self):
        while True:

            # checks to see if the player has died or won the game
            if self.game_over:
                self.show_game_over_screen()
                continue  
            
            if self.game_winner:
                self.show_winner_game_screen()
                continue
            

            # If the player is not dead or did not win continue displaying the game
            self.display.blit(self.assets['background'], (0, 0))
            

            # Handle camera scrolling
            scroll_inc = 30
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / scroll_inc
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / scroll_inc

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))


            # Render the tilemap and player
            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)


            # Handle movement input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE and self.player.can_jump:
                        self.player.velocity[1] = -3
                        self.player.can_jump = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.movement[1] = False
                        

            # Check if the player has died or won
            if self.player.death_animation_played:
                self.game_over = True
                
            if self.player.winner_animation_played:
                self.game_winner = True


            # Regular screen update
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(110)



Game().run()
