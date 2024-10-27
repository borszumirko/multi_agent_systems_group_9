from simulation import Simulation
import cProfile
import pstats
import numpy as np
import random
from constants import CSV_FILE_NAME

def set_seed(seed: int):
    np.random.seed(seed)          # For numpy's RNG
    random.seed(seed)             # For Python's built-in RNG

def main():
    simulation = Simulation()
    simulation.main_loop()

def n_runs(n=30):
    for i in range(n):
        name = CSV_FILE_NAME[:-4] + f"_subrun_{i}.csv"
        simulation = Simulation(name, False)
        simulation.main_loop()

import random
if __name__=="__main__":
    #main()
    set_seed(42)
    n_runs(2)
    #cProfile.run('main()', 'profiling_stats')
    #p = pstats.Stats('profiling_stats')
    #p.sort_stats(pstats.SortKey.TIME).print_stats(10)  # Adjust the number to see more or fewer results
    




