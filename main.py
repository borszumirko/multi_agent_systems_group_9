from simulation import Simulation

def float_range(start, stop, step):
    while start < stop:
        yield round(start, 10)
        start += step

def run_experiments():
    '''
    Multipe runs the values to be tested
    '''
    avg_speeds = [1.4, 1.6, 2.0]
    for run in range(10):
        print(f"RUN: {run+1}")
        for threshold in [2.0, 1.5]:
            for sigma in [0.01, 0.5]:
                for speed in avg_speeds:
                    simulation = Simulation()
                    simulation.main_loop(avg_speed=speed, sigma=sigma, sep_threshold = threshold)
                
def main():
    # Run ne experiment with the default settings
import cProfile
import pstats
import numpy as np
import random
from constants import CSV_FILE_NAME

def set_seed(seed: int) -> None:
    """
    Sets the random seed for both numpy and Python's built-in random generators.

    Parameters:
        seed (int): The seed value for reproducibility.
    """
    np.random.seed(seed)          # For numpy's RNG
    random.seed(seed)             # For Python's built-in RNG

def main() -> None:
    """Runs a single simulation loop."""
    simulation = Simulation()
    simulation.main_loop()

def n_runs(n:int=30) -> None:
    """
    Executes multiple simulation runs and saves each run's results in separate files.

    Parameters:
        n (int): The number of simulation runs. Default is 30.
    """
    for i in range(n):
        name = CSV_FILE_NAME[:-4] + f"_subrun_{i}.csv"
        simulation = Simulation(name, False)
        simulation.main_loop()

def n_runs(n:int=30) -> None:
    """
    Executes multiple simulation runs and saves each run's results in separate files.

    Parameters:
        n (int): The number of simulation runs. Default is 30.
    """
    for i in range(n):
        name = CSV_FILE_NAME[:-4] + f"_subrun_{i}.csv"
        simulation = Simulation(name, False)
        simulation.main_loop()

if __name__=="__main__":
    set_seed(42)  # Set seed for reproducibility

    # Uncomment to run a single simulation loop
    # main()
    
    n_runs(2)     # Run several simulations

    




