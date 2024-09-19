import pygame
import random
from constants import (
    AGENT_MAX_FORCE,
    AGENT_MAX_SPEED,
    AGENT_PERCEPTION,
    AGENT_RADIUS,
    EXIT_POSITION,
    EXIT_WIDTH,
    AGENT_COLOR
)
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = AGENT_MAX_SPEED
        self.max_force = AGENT_MAX_FORCE
        self.perception = AGENT_RADIUS * AGENT_PERCEPTION
    
    def apply_force(self, force):
        """Add force to acceleration."""
        self.acceleration += force

    def update(self):
        """Update boid's velocity and position."""
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0
    
    def flock(self, boids):
        """Apply flocking behaviors with a bias towards the exit."""
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        exit_steering = self.steer_to_exit()
        
        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)
        self.apply_force(exit_steering)
    
    # TODO: Store distance to other agents so we don't have to calculate it for every boid method

    def align(self, boids):
        total = 0
        steering = pygame.Vector2(0, 0)
        for other in boids:
            if other != self and self.position.distance_to(other.position) < self.perception:
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohere(self, boids):
        total = 0
        steering = pygame.Vector2(0, 0)
        for other in boids:
            if other != self and self.position.distance_to(other.position) < self.perception:
                steering += other.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separate(self, boids):
        total = 0
        steering = pygame.Vector2(0, 0)
        for other in boids:
            distance = self.position.distance_to(other.position)
            if other != self and distance < AGENT_RADIUS * 2:
                diff = self.position - other.position
                diff /= distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def steer_to_exit(self):
        target = pygame.Vector2(EXIT_POSITION[0], EXIT_POSITION[1] + EXIT_WIDTH / 2)
        steering = target - self.position
        if steering.length() > 0:
            steering = steering.normalize() * self.max_speed
        steering -= self.velocity
        if steering.length() > self.max_force:
            steering.scale_to_length(self.max_force)
        return steering
    
    def draw(self, screen):
        pygame.draw.circle(screen, AGENT_COLOR, (int(self.position.x), int(self.position.y)), AGENT_RADIUS)
