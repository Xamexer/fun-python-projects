from __future__ import annotations
import math
class CollisionBall:
    def __init__(self,
                 center: tuple,
                 velocity: tuple,
                 radius: float = 20.0,
                 mass: float = 1.0,
                 color: str = "white"
                 ) -> None:
        self.center = center
        self.velocity = velocity
        self.radius = radius
        self.mass = mass
        self.color = color
    
    def vector_between_ball(self, other_ball: CollisionBall) -> bool:
        return (other_ball.center[0] - self.center[0], other_ball.center[1] - self.center[1])