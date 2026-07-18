import pygame
import random
import math


class Hedgehog:
    def __init__(self, image_path, position):
        # These are copied from your main.py
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(100, 60)

        self.wander_angle = 0.0
        self.speed = 80
        self.random_nudge_timer = 0.0

        #adding variables for flipping image
        self.facing_right = False
        self.flip_timer = 0.0
        self.flip_delay = 0.5  # seconds to wait before flipping
        self.dt = 0.0

        # New: load your PNG
        self.image = pygame.image.load(image_path).convert_alpha()

        # Resize it if needed
        # self.image = pygame.transform.smoothscale(self.image,(100, 65))
        self.image = pygame.transform.smoothscale(self.image,(200, 130))

        # #adding brown shading

        # # Darken the image slightly
        # self.image.fill( (220, 210, 195, 255),special_flags=pygame.BLEND_RGBA_MULT )

        # # Add a subtle brown tone
        # brown_overlay = pygame.Surface(
        #     self.image.get_size(),
        #     pygame.SRCALPHA
        # )

        # brown_overlay.fill((70, 35, 15, 25))
        # self.image.blit(brown_overlay, (0, 0))

    def update(self, dt, world_width, world_height):
        # Everything below is your existing movement logic,
        # with variables changed to self.variable.
        self.dt = dt
        self.wander_angle += random.uniform(-1.0, 1.0) * dt

        self.random_nudge_timer += dt

        if self.random_nudge_timer >= 3.0:
            self.wander_angle += random.uniform(
                -math.pi / 2,
                math.pi / 2
            )

            self.random_nudge_timer = 0.0

        wander_direction = pygame.Vector2(
            math.cos(self.wander_angle),
            math.sin(self.wander_angle)
        )

        steering = wander_direction.copy()

        margin = 200
        edge_strength = 5.0

        if self.position.x < margin:
            closeness = (
                margin - self.position.x
            ) / margin

            steering.x += edge_strength * abs(closeness)

        elif self.position.x > world_width - margin:
            closeness = (
                self.position.x -
                (world_width - margin)
            ) / margin

            steering.x -= edge_strength * abs(closeness)

        if self.position.y < margin:
            closeness = (
                margin - self.position.y
            ) / margin

            steering.y += edge_strength * abs(closeness)

        elif self.position.y > world_height - margin:
            closeness = (
                self.position.y -
                (world_height - margin)
            ) / margin

            steering.y -= edge_strength * abs(closeness)

        # Top-left corner
        if (
            self.position.x < margin
            and self.position.y < margin
        ):
            closeness_x = (
                margin - self.position.x
            ) / margin

            closeness_y = (
                margin - self.position.y
            ) / margin

            steering.x += (
                3 * edge_strength * abs(closeness_x)
            )

            steering.y += (
                3 * edge_strength * abs(closeness_y)
            )

        # Bottom-left corner
        elif (
            self.position.x < margin
            and self.position.y > world_height - margin
        ):
            closeness_x = (
                margin - self.position.x
            ) / margin

            closeness_y = (
                self.position.y -
                (world_height - margin)
            ) / margin

            steering.x += (
                3 * edge_strength * abs(closeness_x)
            )

            steering.y -= (
                3 * edge_strength * abs(closeness_y)
            )

        # Top-right corner
        elif (
            self.position.x > world_width - margin
            and self.position.y < margin
        ):
            closeness_x = (
                self.position.x -
                (world_width - margin)
            ) / margin

            closeness_y = (
                margin - self.position.y
            ) / margin

            steering.x -= (
                3 * edge_strength * abs(closeness_x)
            )

            steering.y += (
                3 * edge_strength * abs(closeness_y)
            )

        # Bottom-right corner
        elif (
            self.position.x > world_width - margin
            and self.position.y > world_height - margin
        ):
            closeness_x = (
                self.position.x -
                (world_width - margin)
            ) / margin

            closeness_y = (
                self.position.y -
                (world_height - margin)
            ) / margin

            steering.x -= (
                3 * edge_strength * abs(closeness_x)
            )

            steering.y -= (
                3 * edge_strength * abs(closeness_y)
            )

        if steering.length_squared() > 0:
            desired_velocity = (
                steering.normalize() * self.speed
            )
        else:
            desired_velocity = pygame.Vector2()

        turning_speed = 2.0

        self.velocity += (
            desired_velocity - self.velocity
        ) * turning_speed * dt


        #turnign behavior 
        desired_right = self.velocity.x > 2

        if desired_right != self.facing_right:
            self.flip_timer += dt

            if self.flip_timer >= self.flip_delay:
                self.facing_right = desired_right
                self.flip_timer = 0.0
        else:
            self.flip_timer = 0.0


    #update
        self.position += self.velocity * dt

  

    def draw(self, screen):
        if self.facing_right:
            image_to_draw = pygame.transform.flip(
                self.image,
                True,
                False
            )
        else:
            image_to_draw = self.image

        image_rect = image_to_draw.get_rect(
            center=self.position
        )

        screen.blit(
            image_to_draw,
            image_rect
        )