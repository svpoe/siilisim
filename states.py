"""
Purpose: 
defines avaiable states (finite state machine logic / behavior itself is in hedgehog.py) 
"""
from enum import Enum, auto

class HedgehogState(Enum):
    WANDERING = auto()
    SEEKING_STRAWBERRY = auto()
    EATING = auto()


    