# main.py: Main game loop, Pygame setup, event handling
import pygame
from settings import *
from snake import Snake
from food import Food
from game_manager import GameManager
from logger_setup import setup_logger # Import the logger setup

# Initialize logger globally or pass it around
game_logger = setup_logger()

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Battle Royale")
    clock = pygame.time.Clock()

    game_manager = GameManager(game_logger) # Pass logger to GameManager

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic updates
        game_manager.update()

        # Drawing
        screen.fill(BG_COLOR)
        game_manager.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()

