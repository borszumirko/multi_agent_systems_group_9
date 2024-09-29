import numpy as np
import pygame
import random
import math
import time

from agent import Agent
from obstacle import Obstacle
from constants import (EXIT_POSITION,
                       EXIT_WIDTH,
                       WIDTH, HEIGHT,
                       BOX_LEFT,
                       BOX_HEIGHT,
                       BOX_TOP,
                       BOX_WIDTH,
                       BOX_COLOR,
                       AGENT_RADIUS,
                       EXIT_COLOR,
                       BLACK,
                       AGENT_COUNT)

class Simulation:
    def __init__(self):
        self.total_agents = AGENT_COUNT

    def resolve_positions(self, positions, radius, box_width, box_height, box_left, box_top, obstacles):
        ''' Ensures that agents don't overlap and stay within the box '''

        positions = np.array(positions)
        n_agents = len(positions)
        
        # All agents are within the bounding box, except those near the exit
        for i in range(n_agents):
            x, y = positions[i]
            
            # Check if the boid is near the exit
            in_exit_area = (x > box_left + box_width - radius) and (EXIT_POSITION[1] <= y <= EXIT_POSITION[1] + EXIT_WIDTH)
            
            if not in_exit_area:
                # Boundary checks if not in the exit area
                x = max(box_left + radius, min(x, box_left + box_width - radius))
                y = max(box_top + radius, min(y, box_top + box_height - radius))
            
            positions[i] = np.array([x, y])
        

        # Resolve overlaps between agents
        for i in range(n_agents):
            for j in range(i + 1, n_agents):
                pos_i = positions[i]
                pos_j = positions[j]

                # If too far, don't calculate norm
                if abs(pos_i[0] - pos_j[0]) > AGENT_RADIUS * 2 or abs(pos_i[1] - pos_j[1]) > AGENT_RADIUS * 2:
                    continue

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

    def record_distances(self, boids):
        '''
        Records distances of other agents within every agent's perception so they don't
        have to be recaluculated when trying to execute the bois behavours
        '''

        count = len(boids)
        for i in range(count):
            boids[i].distances = np.full(AGENT_COUNT, fill_value=-1)
            for j in range(i+1, count):
                boid_x = boids[i].position.x
                boid_y = boids[i].position.y
                other_x = boids[j].position.x
                other_y = boids[j].position.y
                # If too far, don't calculate norm
                if abs(boid_x - other_x) > boids[i].perception or abs(boid_y - other_y) > boids[i].perception:
                    continue
                distance = math.dist((boid_x, boid_y),  (other_x, other_y))
                
                boids[i].distances[boids[j].id] = distance
                boids[j].distances[boids[i].id] = distance


    def main_loop(self):
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        # Agents start behind the desks
        starting_positions = []
        for i in range(AGENT_COUNT // 15):
            row = i % 10
            for j in range(15):
                col = j
                starting_positions.append((BOX_LEFT + 145 + col * (AGENT_RADIUS + 50), BOX_TOP + 30 + (row+1)* 60))

        agents = [Agent(x, y, id) for (id, (x, y)) in enumerate(starting_positions)]
        
        # Main loop
        running = True
        while running:
            screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Box
            pygame.draw.rect(screen, BOX_COLOR, (BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT), 1)
            
            # Exit
            pygame.draw.rect(screen, EXIT_COLOR, (*EXIT_POSITION, 15, EXIT_WIDTH))
            
            # Obstacles
            obstacles = []
            for i in range(10):
                obstacles.append(Obstacle(BOX_LEFT + 100, BOX_TOP + (i+1) * 60 + 50, 1000, 20))

            for obstacle in obstacles:
                obstacle.draw(screen)

            # Update and draw agents
            agents = [agent for agent in agents if agent.position.x <= BOX_LEFT + BOX_WIDTH or not (EXIT_POSITION[1] <= agent.position.y <= EXIT_POSITION[1] + EXIT_WIDTH)]
            
            # Exit if no more agents
            if agents == []:
                running = False
            
            np_agents = np.array(agents, dtype=object)
            self.record_distances(np_agents)

            # Update positions of the agents
            for agent in agents:
                agent.flock(np_agents, obstacles)
                agent.update()
            
            # Resolve any overlaps or boundary issues
            positions = [(agent.position.x, agent.position.y) for agent in agents]
            resolved_positions = self.resolve_positions(positions, AGENT_RADIUS, BOX_WIDTH, BOX_HEIGHT, BOX_LEFT, BOX_TOP, obstacles)
            
            # Update boid positions after resolving
            for i, agent in enumerate(agents):
                agent.position.x, agent.position.y = resolved_positions[i]

            # Draw all agents
            for agent in agents:
                agent.draw(screen)

            pygame.display.flip()
        
            clock.tick(60)

        pygame.quit()

