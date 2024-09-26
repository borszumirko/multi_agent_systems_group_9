import pygame
import random
import numpy as np
from constants import (
    AGENT_MAX_FORCE,
    AGENT_MAX_SPEED,
    AGENT_PERCEPTION,
    AGENT_RADIUS,
    EXIT_POSITION,
    EXIT_WIDTH,
    AGENT_COLOR,
    AGENT_COUNT,
    ENV_LENGTH
)
class Agent:
    def __init__(self, x, y, id):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = random.uniform(1.5, AGENT_MAX_SPEED)
        self.max_force = AGENT_MAX_FORCE
        self.avoid_distance = 2 * AGENT_RADIUS + 2
        self.cohesion_distance = 8 * AGENT_RADIUS
        self.alignment_distance = 4 * AGENT_RADIUS
        self.perception = max(self.avoid_distance, self.alignment_distance, self.cohesion_distance)
        self.id = id
        self.distances = np.full(AGENT_COUNT, fill_value=-1)
        self.color = AGENT_COLOR
        self.previous_update = pygame.Vector2(0, 0)
        self.panic = 0
        self.ease_distance = AGENT_RADIUS * 10
        self.physical_discomfort = 0
        self.avg_panic_around = 0

    
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
        alignment, align_panic = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        exit_steering, exit_panic = self.steer_to_exit()
        
        new_panic = (align_panic + exit_panic) / 2
        panic_update = (self.panic + new_panic) / 2
        if panic_update >= 0:
            self.panic = panic_update
        else:
            self.panic = 0
        (_, g, b) = self.color
        g = 255 * (1 - self.panic)
        b = 255 * (1 - self.panic)
        self.color = (255, g, b)
        
        if self.panic >= 0.5:
            self.apply_force(cohesion)
            self.panic = self.avg_panic_around
            return
        self.apply_force(alignment)
        self.apply_force(separation)
        self.apply_force(exit_steering)
    

    def align(self, boids):
        total = 0
        steering = pygame.Vector2(0, 0)
        panic_component = 0
        for other in boids:
            distance = self.distances[other.id]
            if other != self and distance < self.alignment_distance and distance != -1:
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            panic_component = 1 / self.max_speed * (steering.length() - self.velocity.length())
            steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            steering *= 1.5
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering, panic_component

    def cohere(self, boids):
        total = 0
        steering = pygame.Vector2(0, 0)
        others_panic = 0
        for other in boids:
            distance = self.distances[other.id]
            if other != self and distance < self.cohesion_distance and distance != -1:
                steering += other.position
                others_panic += other.panic
                total += 1
        if total > 0:
            others_panic /= total
            self.avg_panic_around = others_panic
            steering /= total
            steering -= self.position
            steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            steering *= 1.5
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separate(self, boids):
        total = 0
        steering = pygame.Vector2(0, 0)
        for other in boids:
            distance = self.distances[other.id]
            if other != self and distance < self.avoid_distance and distance != -1:
                diff = self.position - other.position
                diff /= distance + 0.00000000001
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            steering *= 2.5
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def steer_to_exit(self):
        target = pygame.Vector2(EXIT_POSITION[0], EXIT_POSITION[1] + EXIT_WIDTH / 2)
        steering = target - self.position
        panic_component = 1 / ENV_LENGTH * (steering.length() - self.ease_distance)
        if steering.length() > 0:
            steering = steering.normalize() * self.max_speed
        steering -= self.velocity
        steering *= 6.5
        if steering.length() > self.max_force:
            steering.scale_to_length(self.max_force)
        return steering, panic_component
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), AGENT_RADIUS)
        