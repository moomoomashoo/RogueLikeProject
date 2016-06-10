import pygame
import constants as con
import gamelogic
import sys

def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()
    
    sys.setrecursionlimit(4000)

    size = [con.SCREEN_WIDTH, con.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    pygame.display.set_caption("Something about Chainsaws")
    pygame.mouse.set_visible(False)

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = gamelogic.Game()

    # Main game loop
    while not done:

        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(con.frame_rate)

    # Close window and exit
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
