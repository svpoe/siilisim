import pygame
import random
import math

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

    wander_angle = 0.0
    speed = 80

    random_nudge_timer = 0.0
    while running:
         # Time since the previous frame, in seconds
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        #  # Gradually vary the wandering direction
        # wander_angle += random.uniform(-1.0, 1.0) * dt

        # wander_direction = pygame.Vector2(
        #     math.cos(wander_angle),
        #     math.sin(wander_angle)
        # )
        wander_angle += random.uniform(-1.0, 1.0) * dt

        random_nudge_timer += dt

        if random_nudge_timer >= 3.0:
            wander_angle += random.uniform(
                -math.pi / 2,
                math.pi / 2
            )
            random_nudge_timer = 0.0

        wander_direction = pygame.Vector2(
            math.cos(wander_angle),
            math.sin(wander_angle)
        )



        # Start with the wandering influence
        steering = wander_direction.copy()

        

        # Gradual edge avoidance
        margin = 200
        edge_strength = 5.0

        if position.x < margin:
            closeness = (margin - position.x) / margin
            steering.x += edge_strength * abs(closeness)

        elif position.x > WIDTH - margin:
            closeness = (position.x - (WIDTH - margin)) / margin
            steering.x -= edge_strength * abs(closeness)
            

        if position.y < margin:
            closeness = (margin - position.y) / margin
            steering.y += edge_strength * abs(closeness)

        elif position.y > HEIGHT - margin:
            closeness = (position.y - (HEIGHT - margin)) / margin
            steering.y -= edge_strength * abs(closeness)


        margin = 200
        # extra strong avoidance for corners
        # Top-left corner
        if position.x < margin and position.y < margin:

            closeness_x = (margin - position.x) / margin
            closeness_y = (margin - position.y) / margin

            steering.x += 3 * edge_strength * abs(closeness_x)
            steering.y += 3 * edge_strength * abs(closeness_y)


        # Bottom-left corner
        elif position.x < margin and position.y > HEIGHT - margin:

            closeness_x = (margin - position.x) / margin
            closeness_y = (position.y - (HEIGHT - margin)) / margin

            steering.x += 3 * edge_strength * abs(closeness_x)
            steering.y -= 3 * edge_strength * abs(closeness_y)


        # Top-right corner
        elif position.x > WIDTH - margin and position.y < margin:

            closeness_x = (position.x - (WIDTH - margin)) / margin
            closeness_y = (margin - position.y) / margin

            steering.x -= 3 * edge_strength * abs(closeness_x)
            steering.y += 3 * edge_strength * abs(closeness_y)


        # Bottom-right corner
        elif position.x > WIDTH - margin and position.y > HEIGHT - margin:

            closeness_x = (position.x - (WIDTH - margin)) / margin
            closeness_y = (position.y - (HEIGHT - margin)) / margin

            steering.x -= 3 * edge_strength * abs(closeness_x)
            steering.y -= 3 * edge_strength * abs(closeness_y)
            

                

        # Convert the combined influences into a desired velocity
        if steering.length_squared() > 0:
            desired_velocity = steering.normalize() * speed
        else:
            desired_velocity = pygame.Vector2()

        # Smoothly change the current velocity
        turning_speed = 2.0
        velocity += (desired_velocity - velocity) * turning_speed * dt

        # Move the hedgehog
        position += velocity * dt
            


        screen.fill(GRASS_COLOR)
        # Draw the hedgehog (placeholder)
        pygame.draw.circle(screen, HEDGEHOG_COLOR, position, radius)




        pygame.display.flip()

    pygame.quit()   

if __name__ == "__main__":
    main()  

