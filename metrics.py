import matplotlib.pyplot as plt
import statistics
import csv
import numpy as np
import glob
import pandas as pd
from constants import CSV_FILE_NAME

class Metrics:
    """
    Tracks and visualizes simulation metrics, such as escape times and panic levels, for agents in a simulation.
    """
    def __init__(self, number_of_agents:int, run_name:str=CSV_FILE_NAME, initial_tick:int=0) -> None:
        """
        Initializes the metrics tracker with initial values for each agent.

        Parameters:
            number_of_agents (int): Number of agents to track.
            run_name (str): Filename for saving metrics data.
            initial_tick (int): Initial tick value, default is 0.
        """
        self.number_of_agents = number_of_agents
        self.agent_ticks = [initial_tick for _ in range(number_of_agents)]
        self.agent_panic = [[] for _ in range(number_of_agents)]
        self.agent_escaped = [False for _ in range(number_of_agents)]
        self.run_name = run_name
    
    def increment_tick(self) -> None:
        """Increments the tick count for each agent that has not escaped."""
        for id in range(self.number_of_agents):
            if not self.agent_escaped[id]:
                self.agent_ticks[id] += 1
    
    def record_agent_escape(self, agents:list) -> None:
        """
        Marks agents as escaped based on their IDs.

        Parameters:
            agents (list): List of agent objects with attribute 'id' to mark as escaped.
        """
        for agent in agents:
            self.agent_escaped[agent.id] = True

    def update_panic_levels(self, agents:list) -> None:
        """
        Updates panic levels for agents that have not yet escaped.

        Parameters:
            agents (list): List of agent objects with attributes 'id' and 'panic'.
        """
        for agent in agents:
            if not self.agent_escaped[agent.id]:
                self.agent_panic[agent.id].append(agent.panic)

        
    def get_last_tick_of_agent(self, agent_id:int) -> int:
        """
        Returns the last tick count for a specified agent.

        Parameters:
            agent_id (int): ID of the agent.

        Returns:
            int: Last tick count for the specified agent.
        """
        if 0 <= agent_id < self.number_of_agents:
            return self.agent_ticks[agent_id]
        else:
            raise ValueError(f"Invalid agent_id: {agent_id}. Must be between 0 and {self.number_of_agents - 1}.")

    @property
    def last_tick(self) -> int:
        """Returns the highest tick count among all agents."""
        return max(self.agent_ticks)
    
    def calculate_average_panic(self) -> list:
        """
        Calculates the average panic level for each agent.

        Returns:
            list: Average panic level for each agent.
        """
        return [sum(panic) / len(panic) if panic else 0 for panic in self.agent_panic]

    def calculate_escape_statistics(self) -> dict:
        """
        Calculates statistics for escape times among agents who have escaped.

        Returns:
            dict: Dictionary with min, max, average, and median escape times.
        """
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
        """Displays a histogram showing the distribution of ticks (escape times) for agents."""
        plt.hist(self.agent_ticks, bins=20, color='skyblue', edgecolor='black')
        mean_tick = np.mean(self.agent_ticks)
        plt.axvline(mean_tick, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_tick:.2f}')
        plt.xlabel('Ticks to Exit')
        plt.ylabel('Number of Agents')
        plt.title('Distribution of Escape Times')
        plt.legend()
        plt.show()

    def plot_average_panic_over_time(self, save_directory:str='plots') -> None:
        """
        Plots the average panic level over time and saves the plot.

        Parameters:
            save_directory (str): Directory to save the plot image.
        """
        import os 
        os.makedirs(save_directory, exist_ok=True)
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
        #plt.title('Average Panic Level Over Time')
        panic_over_time_path = os.path.join(save_directory, f'panic_over_time{self.run_name[:-4]}.png')
        plt.savefig(panic_over_time_path, bbox_inches='tight')
        plt.show()

    def show_mean_panic_distribution(self) -> None:
        """Displays a histogram showing the distribution of mean panic levels across agents."""
        flat_panic = [np.mean(panics) for panics in self.agent_panic]
        plt.hist(flat_panic, bins=20, color='green', edgecolor='black')
        plt.xlabel('Panic Level')
        plt.ylabel('Frequency')
        plt.title('Distribution of Mean Panic Levels')
        plt.show()

    def save_metrics(self, save_directory:str='runs', filename:str=None) -> None:
        """
        Saves agent metrics to a CSV file.

        Parameters:
            save_directory (str): Directory to save the CSV file.
            filename (str): Optional filename for saving; defaults to run_name.
        """
        import os
        if not filename:
            filename = self.run_name
        
        os.makedirs(save_directory, exist_ok=True)
        save_filename = os.path.join(save_directory, filename)
        with open(save_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Agent ID', 'Ticks to Exit', 'Average Panic Level'])
            for agent_id in range(self.number_of_agents):
                avg_panic = (
                    sum(self.agent_panic[agent_id]) / len(self.agent_panic[agent_id])
                    if self.agent_panic[agent_id] else 0
                )
                writer.writerow([agent_id, self.agent_ticks[agent_id], avg_panic])

def plot_boxplots_from_runs(csv_files:list, save_directory:str='plots'):
    """
    Plots and saves boxplots of escape times and mean panic levels from multiple runs.

    Parameters:
        csv_files (list): List of CSV file paths.
        save_directory (str): Directory to save the plots.
    """
    import os
    os.makedirs(save_directory, exist_ok=True)
    escape_times_runs = []
    average_panic_levels_runs = []

    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        escape_times = df['Ticks to Exit'].tolist()
        average_panic_levels = df['Average Panic Level'].tolist()

        print(f"Mean escape Time for {csv_file}: {sum(escape_times)/len(escape_times)}")
        print(f"Average Panic Level for {csv_file}: {sum(average_panic_levels)/len(average_panic_levels)}")

        escape_times_runs.append(escape_times)
        average_panic_levels_runs.append(average_panic_levels)

    plt.figure(figsize=(12, 6))
    plt.boxplot(escape_times_runs, patch_artist=True)
    #plt.xlabel('Experiment-Run')
    plt.ylabel('Ticks to Exit')
    plt.title('Escape Times Distribution Across Runs')
    plt.xticks(ticks=range(1, len(csv_files) + 1), labels=[f'Setup {i+1}' for i in range(len(csv_files))])
    plt.grid(True, linestyle='--', alpha=0.6)
    escape_plot_path = os.path.join(save_directory, 'escape_times_boxplot.png')
    plt.savefig(escape_plot_path, bbox_inches='tight')
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.boxplot(average_panic_levels_runs, patch_artist=True)
    #plt.xlabel('Experiments')
    plt.ylabel('Average Panic Level')
    plt.title('Average Panic Levels Across Runs')
    plt.xticks(ticks=range(1, len(csv_files) + 1), labels=[f'Setup {i+1}' for i in range(len(csv_files))])
    plt.grid(True, linestyle='--', alpha=0.6)
    panic_plot_path = os.path.join(save_directory, 'average_panic_levels_boxplot.png')
    plt.savefig(panic_plot_path, bbox_inches='tight')
    plt.show()

    print(f"Plots saved to {save_directory}")

def average_over_subruns(file_names:list) -> None:
    """
    Averages data over subruns for each main file and saves the result.

    Parameters:
        file_names (list): List of main file names to average over their subruns.
    """
    for file_name in file_names:
        sub_run_files = glob.glob(f"{file_name[:-4]}_subrun_*")
        subrun_dfs = []

        for subrun_file in sub_run_files:
            df = pd.read_csv(subrun_file)
            subrun_dfs.append(df)

        if not subrun_dfs:
            return None

        all_subruns_df = pd.concat(subrun_dfs)
        averaged_df = all_subruns_df.groupby('Agent ID').mean()
        averaged_df.to_csv(file_name)

if __name__=="__main__":
    # search for csv files in run-folder
    #csv_files = glob.glob("runs/*.csv")

    # Hard-coded Version:
    #csv_files = ["runs/Experiment_1.csv", "runs/Experiment_2.csv", "runs/Experiment_3.csv", "runs/Experiment_4.csv"]
    csv_files = ["runs/Experiment_3.csv"]
    average_over_subruns(csv_files)
    plot_boxplots_from_runs(csv_files)