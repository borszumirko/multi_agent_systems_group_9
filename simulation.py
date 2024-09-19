import numpy as np
import pygame
import random
from boid_agent import Boid
from constants import (EXIT_POSITION,
                       EXIT_WIDTH,
                       WIDTH, HEIGHT,
                       BOX_LEFT,
                       BOX_HEIGHT,
                       BOX_TOP,
                       BOX_WIDTH,
                       BOX_COLOR,
                       BOID_RADIUS,
                       EXIT_COLOR,
                       BLACK,
                       BOID_COUNT)

class Simulation:
    # Resolve positions function
    def resolve_positions(self, positions, radius, box_width, box_height, box_left, box_top):
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
    
    def main_loop(self):
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
            resolved_positions = self.resolve_positions(positions, BOID_RADIUS, BOX_WIDTH, BOX_HEIGHT, BOX_LEFT, BOX_TOP)
            
            # Step 3: Update boid positions after resolving
            for i, boid in enumerate(boids):
                boid.position.x, boid.position.y = resolved_positions[i]

            # Step 4: Draw all boids
            for boid in boids:
                boid.draw(screen)
            
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

