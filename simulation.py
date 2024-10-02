import numpy as np
import pygame
import random
import math
import time

from agent import Agent
from obstacle import Obstacle
from constants import (EXITS,
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
                       AGENT_COUNT,
                       CLOCK_BOX_WIDTH,
                       CLOCK_BOX_HEIGHT,
                       CLOCK_BOX_LEFT,
                       CLOCK_BOX_TOP
                       )

class Simulation:
    def __init__(self):
        self.total_agents = AGENT_COUNT

    def resolve_positions(self, positions, radius, box_width, box_height, box_left, box_top, obstacles):
        '''
        Ensures that agents don't overlap and stay within the box
        '''
        positions = np.array(positions)
        n_agents = len(positions)

        # Resolve boundary constraints and overlaps for each agent
        for i in range(n_agents):
            x, y = positions[i]
            
            # Determine if the agent is near any exit
            in_exit_area = False
            for exit in EXITS:
                exit_x, exit_y = exit["position"]
                exit_width = exit["width"]

                # If the exit is on the right or left, check if the agent is near it
                if ((x > box_left + box_width - radius and exit_x >= box_left + box_width - radius) or
                    (x < box_left + radius and exit_x <= box_left + radius)) and (exit_y <= y <= exit_y + exit_width):
                    in_exit_area = True
                    break

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
                    for agent_position in [positions[i], positions[j]]:
                        in_exit_area = False
                        for exit in EXITS:
                            exit_x, exit_y = exit["position"]
                            exit_width = exit["width"]

                            # Allow movement through the exit areas on either side
                            if ((agent_position[0] > box_left + box_width - radius and exit_x >= box_left + box_width - radius) or
                                (agent_position[0] < box_left + radius and exit_x <= box_left + radius)) and (exit_y <= agent_position[1] <= exit_y + exit_width):
                                in_exit_area = True
                                break

                        if not in_exit_area:
                            agent_position[0] = max(box_left + radius, min(agent_position[0], box_left + box_width - radius))
                            agent_position[1] = max(box_top + radius, min(agent_position[1], box_top + box_height - radius))

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
        start_ticks = pygame.time.get_ticks()

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
            
            # Draw all exits
            for exit in EXITS:
                pygame.draw.rect(screen, EXIT_COLOR, (*exit["position"], 15, exit["width"]))

            # Clock
            pygame.draw.rect(screen, BOX_COLOR, (CLOCK_BOX_LEFT, CLOCK_BOX_TOP, CLOCK_BOX_WIDTH, CLOCK_BOX_HEIGHT), 1)

            
            # Obstacles
            obstacles = []
            for i in range(10):
                obstacles.append(Obstacle(BOX_LEFT + 100, BOX_TOP + (i+1) * 60 + 50, 1000, 20))

            for obstacle in obstacles:
                obstacle.draw(screen)

            # Update and draw agents, only keep agents that have not exited yet
            agents = [
                agent for agent in agents 
                if not any(
                    (agent.position.x > BOX_LEFT + BOX_WIDTH and
                    exit["position"][1] <= agent.position.y <= exit["position"][1] + exit["width"])
                    or 
                    (agent.position.x < BOX_LEFT and
                    exit["position"][1] <= agent.position.y <= exit["position"][1] + exit["width"])
                    for exit in EXITS
                )
            ]


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

            # Clock update
            elapsed_time_sec = (pygame.time.get_ticks()-start_ticks)/1000
            time_text = pygame.font.Font(None, 36).render(f"{elapsed_time_sec:.2f}", True, (255, 255, 255))
            screen.blit(time_text, (CLOCK_BOX_LEFT+5, CLOCK_BOX_TOP+8))

            pygame.display.flip()

            # Framerate set to maximum of 60 FPS
            clock.tick(60)

        pygame.quit()

