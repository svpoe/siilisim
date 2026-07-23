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
        self.target = None
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(100, 60) # random starting direction

        # INTERNAL INFO
        self.wander_angle = 0.0
        self.speed = 80
        self.random_nudge_timer = 2.0
        self.foot_phase = 0.0
        self.foot_cycle_speed = 10.0
        self.min_walk_speed = 12.0
        #adding variables for flipping image
        self.facing_right = False
        self.turning = False
        self.turn_timer = 0.0
        self.turn_duration = 0.5

        # LOADING IMAGE
        self.image = pygame.image.load("assets/hedgehog_body.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,(100*2, 65*2))
        self.rolled_image = pygame.image.load("assets/hedgehog_rolled.png").convert_alpha()
        self.rolled_image = pygame.transform.smoothscale(self.rolled_image,(70*2,70*2   ))

        self.rectangle = self.image.get_rect(center=self.position)


  # determine new position based on current state, apply steering (update animation) 
    def update(self, dt, world_width, world_height,strawberries):

        self.update_state(strawberries)

        # CALCULATE steering force
        behavior_force = self.get_behavior_force(dt) # gets steering direction based on current state
        wall_force = get_wall_repulsion(self.position, world_width, world_height)
        steering = behavior_force + wall_force
        self.apply_steering(steering, dt)

        self.update_turning(dt)
        self.update_feet_animation(dt)

        self.position += self.velocity * dt
        self.rectangle.center = self.position

        
    # returns main wandering steering direction
    def wandering_behavior(self, dt):
        #adding dt ensures same behavior regardless of framerate
        self.wander_angle += random.uniform(-1.0, 1.0) * dt 

        self.random_nudge_timer += dt

        # ADDS randomness to wandering behavior every 3 sec 
        if self.random_nudge_timer >= 3.0: 
            # keep movement at -90 to +90 from current dir
        
            self.wander_angle += random.uniform(
                -math.pi / 2,
                math.pi / 2
            )

            self.random_nudge_timer = 0.0

        return pygame.Vector2(math.cos(self.wander_angle),math.sin(self.wander_angle))
    
    
    
    # GETTING direction based on current state
    def get_behavior_force(self, dt):
        if self.state == HedgehogState.WANDERING:
            return self.wandering_behavior(dt)

        elif self.state == HedgehogState.SEEKING_STRAWBERRY:
            return self.seek_strawberry_behavior()

        return pygame.Vector2()
    

   # checks if in range of strawberry -> transition to seeking
    def update_state(self, strawberries):
        if self.state == HedgehogState.WANDERING:
            nearest = self.find_nearest_strawberry(strawberries)
            if nearest is not None:
                self.target = nearest
                self.state = HedgehogState.SEEKING_STRAWBERRY

        elif self.state == HedgehogState.SEEKING_STRAWBERRY:
            if self.target not in strawberries:
                self.target = None
                self.state = HedgehogState.WANDERING
                return

            # bounding boxes overlap → eat strawberry → return to WANDERING
            if self.rectangle.colliderect(self.target.rect):
                strawberries.remove(self.target)
                self.target = None
                self.state = HedgehogState.WANDERING



    def apply_steering(self, steering, dt):
        #check if steering vector is not zero to avoid division by zero error
        if steering.length_squared() > 0:
            desired_velocity = steering.normalize() * self.speed
        else:
            desired_velocity = pygame.Vector2()

        turning_speed = 2.0
        self.velocity += (desired_velocity - self.velocity) * turning_speed * dt


    def update_turning(self, dt):
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


    #FEET
    def update_feet_animation(self, dt):
        speed = self.velocity.length()
        if speed <= self.min_walk_speed or self.turning:
            return

        cycle_scale = min(speed / self.speed, 1.5)
        self.foot_phase += dt * self.foot_cycle_speed * cycle_scale


   
    def draw_feet(self, screen):
        if self.turning:
            return

        speed = self.velocity.length()
        swing = math.sin(self.foot_phase) if speed > self.min_walk_speed else 0.0

        base_y = self.position.y + 50

        front_offset_x = 28 if self.facing_right else -28
        rear_offset_x = -35 if self.facing_right else 35

        front_x = self.position.x + front_offset_x + swing * 3
        rear_x  = self.position.x + rear_offset_x  - swing * 3

        front_y = base_y - max(0.0, swing) * 3
        rear_y  = base_y - max(0.0, -swing) * 3

        foot_color = (80, 65, 55)

        foot_width = 6
        foot_height = 8
        foot_gap = 4      # distance between the two feet

        # Front feet
        pygame.draw.ellipse(
            screen, foot_color,
            pygame.Rect(front_x - foot_gap, front_y - 3, foot_width, foot_height)
        )
        pygame.draw.ellipse(
            screen, foot_color,
            pygame.Rect(front_x + foot_gap, front_y - 3, foot_width, foot_height)
        )

        # Rear feet
        pygame.draw.ellipse(
            screen, foot_color,
            pygame.Rect(rear_x - foot_gap, rear_y - 5, foot_width, foot_height)
        )
        pygame.draw.ellipse(
            screen, foot_color,
            pygame.Rect(rear_x + foot_gap, rear_y - 5, foot_width, foot_height)
        )
        

    # DRAW HEDGEHOG
    def draw(self, screen):
        self.draw_feet(screen)

        if self.turning:
            image_to_draw = self.rolled_image
        elif self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        else:
            image_to_draw = self.image

        image_rect = image_to_draw.get_rect(center=self.position)
        screen.blit(image_to_draw, image_rect)


    ## STRAWBERRY SEEKING
    # CALCULATE the distance to every strawberry, target the one with the smallest distance
    def find_nearest_strawberry(self, strawberries):
        nearest = None 
        nearest_dist_sq = float('inf')

        #loop though all strawberries to find the nearest one
        for s in strawberries:

            d_sq = (s.position - self.position).length_squared()
            if d_sq < nearest_dist_sq:
                nearest_dist_sq = d_sq
                nearest = s

        return nearest

    
#move based on the target
    def seek_strawberry_behavior(self):
        if self.target is None:
            return pygame.Vector2() #zero vector aka nowhere to go
        
        direction = self.target.position - self.position

        #checking if hedgehog already at target
        if direction.length_squared() == 0: 
            return pygame.Vector2()
        
        return direction.normalize()



class Baby(Hedgehog):
    def __init__(self, position, scale=0.6):
        super().__init__(position)
        self.speed = 50
        body_size = (
            int(self.image.get_width() * scale),
            int(self.image.get_height() * scale),
        )
        rolled_size = (
            int(self.rolled_image.get_width() * scale),
            int(self.rolled_image.get_height() * scale),
        )

        self.image = pygame.transform.smoothscale(self.image, body_size)
        self.rolled_image = pygame.transform.smoothscale(self.rolled_image, rolled_size)
        self.rectangle = self.image.get_rect(center=self.position)

    #removed bc mini feet
    def draw_feet(self, screen):
        return
    



