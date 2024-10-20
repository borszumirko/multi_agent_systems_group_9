import pygame
import random
import numpy as np
from constants import (
    AGENT_MAX_FORCE,
    AGENT_MAX_SPEED,
    AGENT_RADIUS,
    EXITS,
    EXIT_WIDTH,
    AGENT_COLOR,
    AGENT_COUNT,
    ENV_LENGTH,
    BOX_LEFT,
    BOX_HEIGHT,
    BOX_TOP,
    BOX_WIDTH
)
class Agent:
    def __init__(self, x, y, id):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = random.uniform(AGENT_MAX_SPEED * 0.85, AGENT_MAX_SPEED)
        self.max_force = AGENT_MAX_FORCE
        self.avoid_distance = 2 * AGENT_RADIUS + 2
        self.cohesion_distance = 8 * AGENT_RADIUS
        self.alignment_distance = 4 * AGENT_RADIUS
        self.perception = max(self.avoid_distance, self.alignment_distance, self.cohesion_distance) # perception required for the record distances function
        self.id = id
        self.distances = np.full(AGENT_COUNT, fill_value=-1) # distance of agents around
        self.color = AGENT_COLOR
        self.previous_update = pygame.Vector2(0, 0)
        self.panic = 0
        self.ease_distance = AGENT_RADIUS * 10
        self.physical_discomfort = 0
        self.avg_panic_around = 0

    
    def apply_force(self, force):
        """
        Add force to acceleration.
        """
        self.acceleration += force

    def update(self):
        """
        Update boid's velocity and position.
        """

        if self.acceleration.length() > self.max_force:
                self.acceleration.scale_to_length(self.max_force)
        # panic influences change in velocity
        self.velocity = self.velocity * self.panic + self.acceleration * (1 - self.panic)
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
            
        self.position += self.velocity
        self.acceleration *= 0

    def flock(self, agents, obstacles):
        """
        Apply flocking behaviors with a bias towards the exit.
        """
        alignment, align_panic = self.align(agents)
        cohesion, physical_panic = self.cohere(agents)
        separation = self.separate(agents)
        exit_steering, exit_panic = self.steer_to_exit()
        avoid_obstacles = self.avoid_obstacles(obstacles)
        
        new_panic = (align_panic + exit_panic + physical_panic) / 3
        panic_update = min(1, (self.panic + new_panic) / 2)
        if panic_update >= 0:
            self.panic = panic_update
        else:
            self.panic = 0
        # Agents change color based on their panic level
        (_, g, b) = self.color
        g = 255 * (1 - self.panic)
        b = 255 * (1 - self.panic)
        self.color = (255, g, b)
        # High panic ==> only cohesion (herding) behaviour
        if self.panic >= 0.5:
            self.apply_force(cohesion)
            self.panic = self.avg_panic_around
            return
        self.apply_force(alignment)
        self.apply_force(separation)
        self.apply_force(exit_steering)
        self.apply_force(avoid_obstacles)
        

    def align(self, agents):
        '''
        An agent tries to align its velocity vector with the ones
        around it within self.alignment_distance
        '''
        total = 0
        steering = pygame.Vector2(0, 0)
        panic_component = 0
        for other in agents:
            distance = self.distances[other.id]
            if other != self and distance < self.alignment_distance and distance != -1:
                steering += other.velocity
                total += 1
        if total > 0:
            steering /= total
            panic_component = 1 / self.max_speed * (steering.length() - self.velocity.length())
            steering -= self.velocity
            steering = steering.normalize()
            steering *= 1.5
            
        return steering, panic_component

    def cohere(self, agents):
        '''
        Agents try to move tovards the average position of agents within
        self.cohesion_distance
        '''
        total = 0
        close_neighbors = 0
        steering = pygame.Vector2(0, 0)
        others_panic = 0
        panic_component = 0
        for other in agents:
            distance = self.distances[other.id]
            # if other != self and distance < AGENT_RADIUS * 2.1 and distance != -1:
            #     close_neighbors += 1
            if other != self and distance < self.cohesion_distance and distance != -1:
                steering += other.position
                others_panic += other.panic
                total += 1
        if total > 0:
            others_panic /= total
            self.avg_panic_around = others_panic
            steering /= total
            steering -= self.position
            steering -= self.velocity
            steering = steering.normalize()
            steering *= 1.5

            # /45 instead of /len(agents), since we have more agents than in the paper.
            # 45 is the maximum number of other agents close by, given the cohesion_distance
            panic_component = total / (45)
            # panic_component = close_neighbors / 6
        
        return steering, panic_component

    def separate(self, agents):
        '''
        Agent try to separate themself from nearby agents within
        self.avoid_distance
        '''
        total = 0
        steering = pygame.Vector2(0, 0)
        for other in agents:
            distance = self.distances[other.id]
            if other != self and distance < self.avoid_distance and distance != -1:
                diff = self.position - other.position
                diff /= distance + 0.00000000001
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            steering -= self.velocity
            steering = steering.normalize()
            steering *= 2.5
            
        return steering

    def steer_to_exit(self):
        '''
        Agents choose a subgoal based on their position and try to steer towards it
        '''
        # If on the side out from the rows, go down
        if  (BOX_LEFT <= self.position.x <= BOX_LEFT + 100 - AGENT_RADIUS and self.position.y < BOX_TOP + BOX_HEIGHT - 200) or (BOX_LEFT + BOX_WIDTH - 100 + AGENT_RADIUS <= self.position.x <= BOX_LEFT + BOX_WIDTH and self.position.y < BOX_TOP + BOX_HEIGHT - 200):
            target = pygame.Vector2(self.position.x, BOX_TOP + BOX_HEIGHT)
        elif self.position.y >= BOX_TOP + BOX_HEIGHT - 200:  # go towards exit
            # Find the nearest exit
            min_distance = float('inf')
            target = None

            for exit in EXITS:
                exit_position = pygame.Vector2(exit["position"][0], exit["position"][1] + exit["width"] / 2)
                distance_to_exit = self.position.distance_to(exit_position)
                if distance_to_exit < min_distance:
                    min_distance = distance_to_exit
                    target = exit_position
        else: # go left or right from the desks
            if self.position.x - BOX_LEFT < BOX_LEFT + BOX_WIDTH - self.position.x:
                x = BOX_LEFT
            else:
                x = BOX_LEFT + BOX_WIDTH                                              
            target = pygame.Vector2(x, self.position.y)
        steering = target - self.position
        panic_component = 1 / ENV_LENGTH * (steering.length() - self.ease_distance)
        
        steering -= self.velocity
        steering = steering.normalize()
        steering *= 6.5
        
        return steering, panic_component
    
    def avoid_obstacles(self, obstacles):
        '''
        Agents try to steer away from nearby obstacles
        '''
        total = 0
        steering = pygame.Vector2(0, 0)
        for obstacle in obstacles:
            vector, vector_length = obstacle.away_from_obst(self.position.x, self.position.y)
            if vector_length <= self.avoid_distance:
                steering += vector
                total += 1
        if total > 0:
            steering /= total
            steering -= self.velocity
            steering = steering.normalize()
            steering *= 3.5
            
        return steering

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), AGENT_RADIUS)
        