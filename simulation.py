import numpy as np
import pygame
import math
from metrics import Metrics
import csv
from agent import Agent
from obstacle import Obstacle
from constants import (EXITS,
                       WIDTH, HEIGHT,
                       BOX_LEFT,
                       BOX_HEIGHT,
                       BOX_TOP,
                       BOX_WIDTH,
                       BOX_COLOR,
                       AGENT_RADIUS,
                       AGENT_AVG_SPEED,
                       EXIT_COLOR,
                       BLACK,
                       AGENT_COUNT,
                       CLOCK_BOX_WIDTH,
                       CLOCK_BOX_HEIGHT,
                       CLOCK_BOX_LEFT,
                       CLOCK_BOX_TOP,
                       OBSTACLE_WIDTH,
                       OBSTACLE_HEIGHT,
                       CORR_WIDTH,
                       BIG_OBSTACLE_H,
                       BIG_OBSTACLE_W,
                       CSV_FILE_NAME,
                       COLUMN_NAMES,
                       SCALING, 
                       SUBGOAL_ZONES,
                       VISUALIZE_SUBGOALS,
                       BASE_ZONE, 
                       AGENT_SPEED_SIGMA,
                       RENDER,
                       SEPARATION_THRESHOLD
                       )


class Simulation:
    def __init__(self):
        self.total_agents = AGENT_COUNT
        self.frame_counter = 0
        self.metrics = Metrics(AGENT_COUNT, run_name=run_name)
        self.run_name = run_name
        self.show_plots = show_plots

    def resolve_positions(self, positions, radius, box_width, box_height, box_left, box_top, obstacles, agents):
        '''
        Ensures that agents don't overlap with the teacher desk and stay within the box
        '''

        positions = np.array(positions)
        n_agents = len(positions)

        # Resolve boundary constraints and overlaps for each agent and obstacles
        for i in range(n_agents):
            x, y = positions[i]

            # Determine if the agent is near any exit
            in_exit_area = False
            for exit in EXITS:
                exit_x, exit_y = exit["position"]
                exit_width = exit["width"]

                # If the exit is on the top or bottom, check if the agent is near it
                if ((y < box_top + radius and exit_y <= box_top + radius) or
                    (y > box_top + box_height - radius and exit_y >= box_top + box_height - radius)) and (
                        exit_x <= x <= exit_x + exit_width):
                    in_exit_area = True
                    break

            if not in_exit_area:
                # Boundary checks if not in the exit area
                x = max(box_left + radius, min(x, box_left + box_width - radius))
                y = max(box_top + radius, min(y, box_top + box_height - radius))

                # Obstacle collision detection for the big obstacle
                for obstacle in obstacles:
                    if obstacle.width == BIG_OBSTACLE_W and obstacle.height == BIG_OBSTACLE_H:
                        if (obstacle.left - radius <= x <= obstacle.left + obstacle.width + radius) and (
                                obstacle.top - radius <= y <= obstacle.top + obstacle.height + radius):
                            # Adjust x position if in an Obstacle
                            if x < obstacle.left:
                                x = obstacle.left - radius
                            elif x > obstacle.left + obstacle.width:
                                x = obstacle.left + obstacle.width + radius

                            # Adjust y position if in an Obstacle
                            if y < obstacle.top:
                                y = obstacle.top - radius
                            elif y > obstacle.top + obstacle.height:
                                y = obstacle.top + obstacle.height + radius

            # resolve_positions is not allowed to make an arbitrary size displacement to the agents
            old_pos = positions[i]
            new_pos = np.array([x, y])
            diff = new_pos - old_pos
            length = np.linalg.norm(diff)
            max_displacement = AGENT_AVG_SPEED
            if length > (max_displacement):
                new_pos = (diff / length * max_displacement) + old_pos
            positions[i] = new_pos
        
        return positions.tolist()

    def record_distances(self, agents):
        '''
        Records distances of other agents within every agent's perception so they don't
        have to be recaluculated when trying to execute the boids behaviours
        '''

        count = len(agents)
        for i in range(count):
            # Empty distances, in the case one agent is out via the exit.
            agents[i].distances = np.full(AGENT_COUNT, fill_value=-1)

        for i in range(count):
            for j in range(i + 1, count):
                agent_x = agents[i].position.x
                agent_y = agents[i].position.y
                other_x = agents[j].position.x
                other_y = agents[j].position.y
                # If too far, don't calculate norm
                if abs(agent_x - other_x) > agents[i].perception or abs(agent_y - other_y) > agents[i].perception:
                    continue
                distance = math.dist((agent_x, agent_y), (other_x, other_y))

                agents[i].distances[agents[j].id] = distance
                agents[j].distances[agents[i].id] = distance


    def main_loop(self, avg_speed=AGENT_AVG_SPEED, sigma=AGENT_SPEED_SIGMA, sep_threshold=SEPARATION_THRESHOLD):
        
        # Initialize Pygame
        if RENDER:
            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            clock = pygame.time.Clock()
            start_ticks = pygame.time.get_ticks()

        # Agents start behind the desks
        starting_positions = []
        space_between_starting_agents = ((OBSTACLE_HEIGHT / 16) - AGENT_RADIUS * 2)
        for i in range(AGENT_COUNT // 15):
            row = i % 16
            for j in range(15):
                col = j
                starting_positions.append((BOX_LEFT + 75 - AGENT_RADIUS + col * (AGENT_RADIUS + OBSTACLE_WIDTH*2 - AGENT_RADIUS), BOX_TOP + CORR_WIDTH + AGENT_RADIUS + 5 + (row)* AGENT_RADIUS*3))

        agents = [Agent(x, y, id, avg_speed, sigma) for (id, (x, y)) in enumerate(starting_positions)]
        
        # Main loop
        running = True
        paused = False
        while running:
            # Pause block
            if RENDER:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            paused = not paused
                if paused:
                    continue

                screen.fill(BLACK)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            
                # Box
                pygame.draw.rect(screen, BOX_COLOR, (BOX_LEFT, BOX_TOP, BOX_WIDTH, BOX_HEIGHT), 1)
                
                # Draw all exits
                for exit in EXITS:
                    pygame.draw.rect(screen, EXIT_COLOR, (*exit["position"], exit["width"], exit['height']))

                # Clock
                pygame.draw.rect(screen, BOX_COLOR, (CLOCK_BOX_LEFT, CLOCK_BOX_TOP, CLOCK_BOX_WIDTH, CLOCK_BOX_HEIGHT), 1)

                # zones for subgoal finding
                if VISUALIZE_SUBGOALS:
                    for subgoals_dicts in SUBGOAL_ZONES.values():
                        subgoals = [Obstacle(**p) for p in subgoals_dicts]
                        for subgoal in subgoals:
                            subgoal.draw(screen)
                    base_zone = Obstacle(**BASE_ZONE)
                    base_zone.draw(screen)
            
            # Obstacles
            obstacles = []
            for i in range(15):
                obstacles.append(Obstacle(BOX_LEFT + 75 + (i) * OBSTACLE_WIDTH * 2, BOX_TOP + CORR_WIDTH, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            obstacles.append(Obstacle(BOX_LEFT + ((1250+450+90) // SCALING), BOX_TOP + CORR_WIDTH + (55//SCALING), BIG_OBSTACLE_W, BIG_OBSTACLE_H))
            
            if RENDER:
                for obstacle in obstacles:
                    obstacle.draw(screen)

            # Epsilon for escape-easing
            epsilon = 2

            dropped_out_agents = [
                agent for agent in agents
                if any(
                    (agent.position.y >= BOX_TOP + BOX_HEIGHT - epsilon and
                     exit["position"][0] <= agent.position.x <= exit["position"][0] + exit["width"])
                    or
                    (agent.position.y <= BOX_TOP + epsilon and
                     exit["position"][0] <= agent.position.x <= exit["position"][0] + exit["width"])
                    for exit in EXITS
                )
            ]

            self.metrics.record_agent_escape(dropped_out_agents)

            # Update and draw agents, only keep agents that have not exited yet
            agents = [
                agent for agent in agents
                if not any(
                    (agent.position.y >= BOX_TOP + BOX_HEIGHT - epsilon and
                     exit["position"][0] <= agent.position.x <= exit["position"][0] + exit["width"])
                    or
                    (agent.position.y <= BOX_TOP + epsilon and
                     exit["position"][0] <= agent.position.x <= exit["position"][0] + exit["width"])
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
                agent.flock(np_agents, obstacles, sep_threshold)
                agent.update()

            # Update all active Agents time-steps
            self.metrics.increment_tick()
            # Update panic levels in the Metrics class (for all active Agents)
            self.metrics.update_panic_levels(agents)
            # Resolve any overlaps or boundary issues
            positions = [(agent.position.x, agent.position.y) for agent in agents]
            resolved_positions = self.resolve_positions(positions, AGENT_RADIUS, BOX_WIDTH, BOX_HEIGHT, BOX_LEFT, BOX_TOP, obstacles, agents)
            # Update boid positions after resolving
            for i, agent in enumerate(agents):
                agent.position.x, agent.position.y = resolved_positions[i]

            # Draw all agents
            if RENDER:
                for agent in agents:
                    agent.draw(screen)

                # Clock update
                elapsed_time_sec = (pygame.time.get_ticks()-start_ticks)/1000
                time_text = pygame.font.Font(None, 26).render(f"Time: {elapsed_time_sec:.2f}", True, (255, 255, 255))
                screen.blit(time_text, (CLOCK_BOX_LEFT+5, CLOCK_BOX_TOP+8))
                self.frame_counter += 1
                time_text = pygame.font.Font(None, 26).render(f"Frames: {self.frame_counter}", True, (255, 255, 255))
                screen.blit(time_text, (CLOCK_BOX_LEFT+5, CLOCK_BOX_TOP+32))

                pygame.display.flip()


                clock.tick(60)
        if RENDER:
            pygame.quit()
        avg_panics = []
        for panic in self.metrics.agent_panic:
            avg_panics.append(np.mean(panic))
        mean_panic = np.mean(avg_panics)
        mean_ticks = np.mean(self.metrics.agent_ticks)
        print(f"Separation threshold: {sep_threshold}, Avg speed: {avg_speed}, Sigma: {sigma}, avg evac time: {mean_ticks}, avg panic: {mean_panic}")
        self.metrics.show_tick_distribution()
        self.metrics.show_mean_panic_distribution()
        self.metrics.plot_average_panic_over_time()
        self.metrics.save_metrics()


        data = [[sep_threshold, avg_speed, sigma, mean_ticks, mean_panic]]
        # Writing to CSV
        with open("data/" + CSV_FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(COLUMN_NAMES)
            for row in data:                
                writer.writerow(row)

        print(f"Data written to {CSV_FILE_NAME}")