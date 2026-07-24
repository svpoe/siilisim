# SiiliSim - Autonomous Hedgehog Simulator

A simple autonomous hedgehog built in **Python** using **Pygame**. The hedgehog explores its environment independently, searches for the nearest strawberry, avoids walls using steering behaviors, and removes strawberries upon collision.

## Features

* Autonomous hedgehog behavior (no player input)
* Finite State Machine (FSM)

  * **WANDERING**
  * **SEEKING_STRAWBERRY**
* Nearest-target selection
* Steering behaviors
* Potential-field-inspired wall avoidance
* Collision detection using Pygame `Rect.colliderect()`
* Sprite animation and random recovery nudges

## How It Works

### 1. State Machine

The hedgehog's decision-making is handled by `update_state()`.

* While in the **WANDERING** state, it calls `find_nearest_strawberry()`.
* The closest strawberry is selected as the current target.
* If a target exists, the hedgehog transitions to the **SEEKING_STRAWBERRY** state.

### 2. Steering Behaviors

Movement is computed in `get_behavior_force()` by combining multiple steering forces.

* `seek_strawberry_behavior()` returns a normalized direction toward the current target.
* `get_wall_repulsion()` produces a repulsive force that increases as the hedgehog approaches the boundaries of the environment.

These steering forces are combined to generate the final movement direction each frame.

### 3. Collision Detection

Both the hedgehog and strawberries have bounding rectangles created using `Surface.get_rect()`.

Pygame's `Rect.colliderect()` method checks whether these rectangles overlap. When a collision is detected, the strawberry is removed from the environment, simulating the hedgehog eating it.

## AI Techniques Used

* Finite State Machine (FSM)
* Target selection (nearest strawberry)
* Steering behaviors
* Potential-field-inspired wall avoidance
* Autonomous agent architecture

## Technologies

* Python
* Pygame


    