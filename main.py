from simulation import Simulation
import random
import numpy as np

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

def run_experiments():
    '''
    Multipe runs with the values to be tested
    '''
    avg_speeds = [1.4, 1.6, 2.0]
    for run in range(10):
        print(f"RUN: {run+1}")
        for threshold in [2.0, 1.5]:
            for sigma in [0.01, 0.5]:
                for speed in avg_speeds:
                    simulation = Simulation()
                    simulation.main_loop(avg_speed=speed, sigma=sigma, sep_threshold = threshold)

if __name__=="__main__":
    set_seed(42)  # Set seed for reproducibility

    # Uncomment to run a multiple experiments
    # run_experiments()
    main()
    
    

    




