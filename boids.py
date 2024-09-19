import pygame
import random
import numpy as np

# Constants
WIDTH, HEIGHT = 1600, 800
BOX_WIDTH, BOX_HEIGHT = 1200, 600
BOX_LEFT = (WIDTH - BOX_WIDTH) // 2
BOX_TOP = (HEIGHT - BOX_HEIGHT) // 2
EXIT_WIDTH = 60
EXIT_POSITION = (BOX_LEFT + BOX_WIDTH, BOX_TOP + (BOX_HEIGHT // 2) - EXIT_WIDTH // 2)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOID_COLOR = (0, 255, 0)
BOX_COLOR = (255, 0, 0)
EXIT_COLOR = (0, 0, 255)
BOID_COUNT = 50
BOID_RADIUS = 15  # Increased the size of the boids for better visibility

# Resolve positions function
def resolve_positions(positions, radius, box_width, box_height, box_left, box_top):
    positions = np.array(positions)
    n_agents = len(positions)
    
    # Step 1: Ensure all agents are within the bounding box, except those near the exit
    for i in range(n_agents):
        x, y = positions[i]
        
        # Check if the boid is near the exit
        in_exit_area = (x > box_left + box_width - radius) and (EXIT_POSITION[1] <= y <= EXIT_POSITION[1] + EXIT_WIDTH)
        
        if not in_exit_area:
            # Regular boundary checks if not in the exit area
            x = max(box_left + radius, min(x, box_left + box_width - radius))
            y = max(box_top + radius, min(y, box_top + box_height - radius))
        
        positions[i] = np.array([x, y])

    # Step 2: Resolve overlaps between agents
    for i in range(n_agents):
        for j in range(i + 1, n_agents):
            pos_i = positions[i]
            pos_j = positions[j]
            distance = np.linalg.norm(pos_i - pos_j)
            
            # If overlapping, move them apart
            if distance < 2 * radius:
                overlap = 2 * radius - distance
                direction = (pos_i - pos_j) / distance
                positions[i] += direction * overlap / 2
                positions[j] -= direction * overlap / 2

                # Ensure the adjusted positions are within the boundaries again
                in_exit_area_i = (positions[i][0] > box_left + box_width - radius) and (EXIT_POSITION[1] <= positions[i][1] <= EXIT_POSITION[1] + EXIT_WIDTH)
                in_exit_area_j = (positions[j][0] > box_left + box_width - radius) and (EXIT_POSITION[1] <= positions[j][1] <= EXIT_POSITION[1] + EXIT_WIDTH)
                
                if not in_exit_area_i:
                    positions[i][0] = max(box_left + radius, min(positions[i][0], box_left + box_width - radius))
                    positions[i][1] = max(box_top + radius, min(positions[i][1], box_top + box_height - radius))
                
                if not in_exit_area_j:
                    positions[j][0] = max(box_left + radius, min(positions[j][0], box_left + box_width - radius))
                    positions[j][1] = max(box_top + radius, min(positions[j][1], box_top + box_height - radius))

    return positions.tolist()


# Boid class definition
class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 3
        self.max_force = 0.3
        self.perception = BOID_RADIUS * 4

    def edges(self):
        """Handle boid bounding within the box with an exit."""
        if self.position.x < BOX_LEFT + BOID_RADIUS:
            self.position.x = BOX_LEFT + BOID_RADIUS
            self.velocity.x *= -1
        elif self.position.x > BOX_LEFT + BOX_WIDTH - BOID_RADIUS and not (EXIT_POSITION[1] <= self.position.y <= EXIT_POSITION[1] + EXIT_WIDTH):
            self.position.x = BOX_LEFT + BOX_WIDTH - BOID_RADIUS
            self.velocity.x *= -1
        
        if self.position.y < BOX_TOP + BOID_RADIUS:
            self.position.y = BOX_TOP + BOID_RADIUS
            self.velocity.y *= -1
        elif self.position.y > BOX_TOP + BOX_HEIGHT - BOID_RADIUS:
            self.position.y = BOX_TOP + BOX_HEIGHT - BOID_RADIUS
            self.velocity.y *= -1
    
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
            if other != self and distance < BOID_RADIUS * 2:
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
        pygame.draw.circle(screen, BOID_COLOR, (int(self.position.x), int(self.position.y)), BOID_RADIUS)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create a list of boids
boids = [Boid(random.randint(BOX_LEFT + BOID_RADIUS, BOX_LEFT + BOX_WIDTH - BOID_RADIUS), 
              random.randint(BOX_TOP + BOID_RADIUS, BOX_TOP + BOX_HEIGHT - BOID_RADIUS)) for _ in range(BOID_COUNT)]

# Main loop
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the box
    pygame.draw.rect(screen, BOX_COLOR, (BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT), 2)
    
    # Draw the exit
    pygame.draw.rect(screen, EXIT_COLOR, (*EXIT_POSITION, 5, EXIT_WIDTH))
    
    # Update and draw all boids
    boids = [boid for boid in boids if boid.position.x <= BOX_LEFT + BOX_WIDTH or not (EXIT_POSITION[1] <= boid.position.y <= EXIT_POSITION[1] + EXIT_WIDTH)]
    
    # Step 1: Update positions of the boids
    for boid in boids:
        boid.edges()
        boid.flock(boids)
        boid.update()
    
    # Step 2: Resolve any overlaps or boundary issues
    positions = [(boid.position.x, boid.position.y) for boid in boids]
    resolved_positions = resolve_positions(positions, BOID_RADIUS, BOX_WIDTH, BOX_HEIGHT, BOX_LEFT, BOX_TOP)
    
    # Step 3: Update boid positions after resolving
    for i, boid in enumerate(boids):
        boid.position.x, boid.position.y = resolved_positions[i]

    # Step 4: Draw all boids
    for boid in boids:
        boid.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
