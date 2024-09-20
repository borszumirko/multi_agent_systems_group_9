from simulation import Simulation
import cProfile
import pstats
import numpy as np


def main():
    simulation = Simulation()
    simulation.main_loop()


if __name__=="__main__":
    main()
    # cProfile.run('main()', 'profiling_stats')
    # p = pstats.Stats('profiling_stats')
    # p.sort_stats(pstats.SortKey.TIME).print_stats(10)  # Adjust the number to see more or fewer results
    




