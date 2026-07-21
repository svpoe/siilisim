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
# import math
from hedgehog import Hedgehog, Baby
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
    strawberries = [
        Strawberry(position=(WIDTH / 2 + 50, HEIGHT / 2 + 50)),
        Strawberry(position=(WIDTH / 2 + 200, HEIGHT / 2 + 30)),
    
    ]
   # baby = Baby(position=(WIDTH / 2 + 200, HEIGHT / 2 + 40))
    spawn_timer = 0.0
    SPAWN_INTERVAL = 3.0
    # Match wall-repulsion margin so strawberries spawn in reachable space.
    MARGIN = 200
    running = True
    while running:
         # Time since the previous frame, in seconds
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        spawn_timer += dt
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_timer = 0.0
            x = random.randint(MARGIN, WIDTH - MARGIN)
            y = random.randint(MARGIN, HEIGHT - MARGIN)
            strawberries.append(Strawberry(position=(x, y)))

        mother.update(dt, WIDTH, HEIGHT, strawberries)
        
    
       # baby.update(dt, WIDTH, HEIGHT, strawberries)
        
        
       
        screen.fill(GRASS_COLOR)
       
        screen.blit(pygame.image.load("assets/grass.png"), (0, 0))
        mother.draw(screen)
        for s in strawberries:
            s.draw(screen)
        #baby.draw(screen)
        pygame.display.flip()

    pygame.quit()   

if __name__ == "__main__":
    main()  

