import matplotlib.pyplot as plt
import statistics
import csv
import numpy as np

class Metrics:
    def __init__(self, number_of_agents, initial_tick=0) -> None:
        self.number_of_agents = number_of_agents
        self.agent_ticks = [initial_tick for _ in range(number_of_agents)]
        self.agent_panic = [[] for _ in range(number_of_agents)]
        self.agent_escaped = [False for _ in range(number_of_agents)]
    
    def increment_tick(self):
        for id in range(self.number_of_agents):
            if not self.agent_escaped[id]:
                self.agent_ticks[id] += 1
    
    def record_agent_escape(self, agents):
        for agent in agents:
            self.agent_escaped[agent.id] = True

    def update_panic_levels(self, agents):
        for agent in agents:
            if not self.agent_escaped[agent.id]:
                self.agent_panic[agent.id].append(agent.panic)

        
    def get_last_tick_of_agent(self, agent_id):
        if 0 <= agent_id < self.number_of_agents:
            return self.agent_ticks[agent_id]
        else:
            raise ValueError(f"Invalid agent_id: {agent_id}. Must be between 0 and {self.number_of_agents - 1}.")

    @property
    def last_tick(self):
        return max(self.agent_ticks)
    
    def calculate_average_panic(self):
        return [sum(panic) / len(panic) if panic else 0 for panic in self.agent_panic]

    def calculate_escape_statistics(self):
        valid_times = [self.get_last_tick_of_agent(agent_id) for agent_id in range(self.number_of_agents) if self.agent_escaped[agent_id]]
        if valid_times:
            return {
                'min_time': min(valid_times),
                'max_time': max(valid_times),
                'average_time': sum(valid_times) / len(valid_times),
                'median_time': statistics.median(valid_times)
            }
        return None

    def show_tick_distribution(self):
        # Plot the histogram of agent ticks
        plt.hist(self.agent_ticks, bins=20, color='skyblue', edgecolor='black')

        # Calculate the mean tick value
        mean_tick = np.mean(self.agent_ticks)
        
        # Add a vertical red line at the mean tick value
        plt.axvline(mean_tick, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_tick:.2f}')
        
        # Add labels, title, and legend
        plt.xlabel('Ticks to Exit')
        plt.ylabel('Number of Agents')
        plt.title('Distribution of Escape Times')
        plt.legend()  # Add legend to show the mean value line
        plt.show()

    def plot_average_panic_over_time(self):
        avg_panic_over_time = []

        for i in range(self.last_tick):
            panic_values = [panic[i] for panic in self.agent_panic  if len(panic) > i]
            if not panic_values:
                break
            else:
                avg_panic_over_time.append(sum(panic_values) / len(panic_values))

        plt.plot(avg_panic_over_time, color='red')
        plt.xlabel('Tick')
        plt.ylabel('Average Panic Level')
        plt.title('Average Panic Level Over Time')
        plt.show()

    def show_panic_distribution(self):
        flat_panic = [panic for agent_panic in self.agent_panic for panic in agent_panic]
        plt.hist(flat_panic, bins=20, color='green', edgecolor='black')
        plt.xlabel('Panic Level')
        plt.ylabel('Frequency')
        plt.title('Distribution of Panic Levels')
        plt.show()

    def save_metrics(self, filename='metrics.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Agent ID', 'Ticks to Exit', 'Average Panic Level'])
            for agent_id in range(self.number_of_agents):
                avg_panic = (
                    sum(self.agent_panic[agent_id]) / len(self.agent_panic[agent_id])
                    if self.agent_panic[agent_id] else 0
                )
                writer.writerow([agent_id, self.agent_ticks[agent_id], avg_panic])