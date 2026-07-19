"""
purpose:
- calculates movement forces

"""

import pygame


def get_wall_repulsion(position, world_width,world_height,margin=200,edge_strength=5.0):
    
        force = pygame.Vector2(0, 0)
        if position.x < margin:
            closeness = (
                margin - position.x
            ) / margin

            force.x += edge_strength * closeness

        elif position.x > world_width - margin:
            closeness = (
                position.x -
                (world_width - margin)
            ) / margin

            force.x -= edge_strength * closeness
        if position.y < margin:
            closeness = (
                margin - position.y
            ) / margin

            force.y += edge_strength * closeness

        elif position.y > world_height - margin:
            closeness = (
                position.y -
                (world_height - margin)
            ) / margin

            force.y -= edge_strength * closeness

        return force
