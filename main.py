"""
Purpose: simulation loop - run and coordinate the world
- initialize Pygame
- create the mother, baby, and strawberries
- process events
- call each object’s update()
- call each object’s draw()
- remove eaten strawberries
- draw the world
"""

import pygame
import random
import math
from hedgehog import Hedgehog
from strawberry import Strawberry

WIDTH = 1000
HEIGHT = 700
FPS = 60

GRASS_COLOR = (104,159,80)
# HEDGEHOG_COLOR = (95, 65, 45)#

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hedgehog Simulator")
    clock = pygame.time.Clock()


    # random_nudge_timer = 0.0
    mother = Hedgehog( position=(WIDTH / 2, HEIGHT / 2))
    strawberry = Strawberry(position=(WIDTH / 2 + 50, HEIGHT / 2 + 50))
    strawberry2 = Strawberry(position=(WIDTH / 2 + 200, HEIGHT / 2 + 30))
    #baby= Hedgehog(image_path="assets/hedgehog_body.png", position=(WIDTH / 2 + 50, HEIGHT / 2 + 50))
    running = True
    while running:
         # Time since the previous frame, in seconds
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mother.update(dt, WIDTH, HEIGHT, strawberries = [])
        
    
        #baby.update(dt, WIDTH, HEIGHT, strawberries = [])
        
        
       
        screen.fill(GRASS_COLOR)
       
        screen.blit(pygame.image.load("assets/grass.png"), (0, 0))
        mother.draw(screen)
        strawberry.draw(screen)
        strawberry2.draw(screen)
        #baby.draw(screen)
        pygame.display.flip()

    pygame.quit()   

if __name__ == "__main__":
    main()  

