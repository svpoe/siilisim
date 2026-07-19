"""
Autonomous agent 
- internal information - in init 
- perception  - from update()
- finite state machine logic:
   - states - defines what each states does & when to transition to another state (state names defined in states.py )

"""

import pygame
import random
import math
from steering import get_wall_repulsion
from states import HedgehogState


class Hedgehog:
    def __init__(self, position):
        # These are copied from your main.py
        
        self.state = HedgehogState.WANDERING
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(100, 60)


        # INTERNAL INFO
        self.wander_angle = 0.0
        self.speed = 80
        self.random_nudge_timer = 2.0
        #adding variables for flipping image
        self.facing_right = False
        self.turning = False
        self.turn_timer = 0.0
        self.turn_duration = 0.5


        # LOADING IMAGE
        self.image = pygame.image.load("assets/hedgehog_body.png").convert_alpha()
        # Resize it if needed
        # self.image = pygame.transform.smoothscale(self.image,(100, 65))
        self.image = pygame.transform.smoothscale(self.image,(100*2, 65*2))
        #load rolled hedgehog
        self.rolled_image = pygame.image.load("assets/hedgehog_rolled.png").convert_alpha()
        self.rolled_image = pygame.transform.smoothscale(self.rolled_image,(70*2,70*2   ))



  # Getting info from enviornment
    def update(self, dt, world_width, world_height,strawberries):

        self.update_state(strawberries)

        behavior_force = self.get_behavior_steering(dt)

        wall_force = get_wall_repulsion(self.position, world_width, world_height)

        steering = behavior_force + wall_force

        self.apply_steering(steering, dt)
        self.uppdate_turning(dt)

        self.position += self.velocity * dt

        
    # returns main wandering steering direction
    def wandering_behavior(self, dt):
        self.wander_angle += random.uniform(-1.0, 1.0) * dt

        self.random_nudge_timer += dt

        if self.random_nudge_timer >= 3.0:
            # keep movement at -90 to +90 from current dir
        
            self.wander_angle += random.uniform(
                -math.pi / 2,
                math.pi / 2
            )

            self.random_nudge_timer = 0.0

        return pygame.Vector2(math.cos(self.wander_angle),math.sin(self.wander_angle))
    

    def seek_strawberry_behavior(self):
        if self.target is None:
            return pygame.Vector2()
        
        direction = self.target.position - self.position

        #hedgehot already at target
        if direction.length_squared() == 0:
            return pygame.Vector2()
        return direction.normalize()
    
    
    def get_behavior_steering(self, dt):
        if self.state == HedgehogState.WANDERING:
            return self.wandering_behavior(dt)

        elif self.state == HedgehogState.SEEKING_STRAWBERRY:
            return self.seek_strawberry_behavior()

        elif self.state == HedgehogState.EATING:
            return self.eating_behavior(dt)

        return pygame.Vector2()
    
    def update_state(self, strawberries):
        if self.state == HedgehogState.WANDERING:
            target = self.find_nearest_ripe_strawberry(
                strawberries
            )

            if target is not None:
                self.target = target
                self.state = HedgehogState.SEEKING_STRAWBERRY

        elif self.state == HedgehogState.SEEKING_STRAWBERRY:
            if self.target is None or not self.target.ripe:
                self.target = None
                self.state = HedgehogState.WANDERING
                return

            distance = self.position.distance_to(
                self.target.position
            )

            if distance < self.eating_distance:
                self.state = HedgehogState.EATING
                self.eating_timer = 0.0

        elif self.state == HedgehogState.EATING:
            if self.eating_timer >= self.eating_duration:
                self.target = None
                self.state = HedgehogState.WANDERING


    def find_nearest_ripe_strawberry(self, strawberries):
        nearest = None
        nearest_dist_sq = float('inf')
        for s in strawberries:
            if not s.ripe:
                continue

            d_sq = (s.position - self.position).length_squared()
            if d_sq < nearest_dist_sq:
                nearest_dist_sq = d_sq
                nearest = s

        return nearest

    def apply_steering(self, steering, dt):
        if steering.length_squared() > 0:
            desired_velocity = steering.normalize() * self.speed
        else:
            desired_velocity = pygame.Vector2()

        turning_speed = 2.0
        self.velocity += (desired_velocity - self.velocity) * turning_speed * dt

    def uppdate_turning(self, dt):
        if self.velocity.x > 0 and not self.facing_right:
            self.turning = True
            self.turn_timer = 0.0
            self.facing_right = True

        elif self.velocity.x < 0 and self.facing_right:
            self.turning = True
            self.turn_timer = 0.0
            self.facing_right = False

        if self.turning:
            self.turn_timer += dt
            if self.turn_timer >= self.turn_duration:
                self.turning = False
    def eating_behavior(self, dt):
        self.eating_timer += dt
        return pygame.Vector2()
    

    def draw(self, screen):
        if self.turning:
            image_to_draw = self.rolled_image
        elif self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        else:
            image_to_draw = self.image

        image_rect = image_to_draw.get_rect(center=self.position)
        screen.blit(image_to_draw, image_rect)