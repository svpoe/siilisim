"""
purpose:
wall repulsion force

"""

import pygame

# margin = distance from where wall repulsion starts
#prevent hedgehog from going through the wall and getting into corners
def get_wall_repulsion(position, world_width, world_height, margin=200, edge_strength=5.0):

        force = pygame.Vector2(0, 0)
        # prevent leaving from left side 
        if position.x < margin:
            closeness = (margin - position.x) / margin
            force.x += edge_strength * closeness
        # right side
        elif position.x > world_width - margin:
            closeness = (position.x - (world_width - margin)) / margin
            force.x -= edge_strength * closeness
        # top ( note: + y is down in pygame)
        if position.y < margin:
            closeness = (margin - position.y) / margin
            force.y += edge_strength * closeness
        # bottom 
        elif position.y > world_height - margin:
            closeness = (position.y - (world_height - margin)) / margin
            force.y -= edge_strength * closeness

        return force


