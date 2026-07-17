import pygame

WIDTH = 1000
HEIGHT = 700
FPS = 60

GRASS_COLOR = (104,159,80)
HEDGEHOG_COLOR = (95, 65, 45)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hedgehog Simulator")
    clock = pygame.time.Clock()

    position =pygame.Vector2(WIDTH / 2, HEIGHT / 2)
    velocity = pygame.Vector2(100, 60)
    radius = 25
    running = True

    while running:
         # Time since the previous frame, in seconds
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the position of the hedgehog
        position += velocity * dt
        
        #limit the hedgehog to the screen boundaries
        if position.x - radius < 0 or position.x + radius > WIDTH:
            velocity.x *= -1    
        if position.y - radius < 0 or position.y + radius > HEIGHT:
            velocity.y *= -1
        


        screen.fill(GRASS_COLOR)
        # Draw the hedgehog (placeholder)
        pygame.draw.circle(screen, HEDGEHOG_COLOR, position, radius)




        pygame.display.flip()

    pygame.quit()   

if __name__ == "__main__":
    main()  

