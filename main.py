from simulation import Simulation
import cProfile
import pstats
import numpy as np
import matplotlib.pyplot as plt

def float_range(start, stop, step):
    while start < stop:
        yield round(start, 10)
        start += step

def main():
    avg_speed = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
    # avg_speed = [10, 11]
    # sigma = [0.1]
    sigma = [0.5]
    evac_times = {}
    panics = {}
    num_runs = 10
    for s in sigma:
        print(f"=========== Sigma {s} ===========")
        evac_times_same_sigma = np.zeros(len(avg_speed), dtype=np.float64)
        panics_same_sigma = np.zeros(len(avg_speed), dtype=np.float64)
        for i in range(num_runs):
            if s==0 and i != 0:
                continue
            print(f"=========== RUN {i} ===========")
            evac_times_same_sigma_one_run = []
            panics_same_sigma_one_run = []
            for speed in avg_speed:
                simulation = Simulation()
                avg_evac_time, avg_panic = simulation.main_loop(avg_speed=speed, sigma=s)
                evac_times_same_sigma_one_run.append(avg_evac_time)
                panics_same_sigma_one_run.append(avg_panic)
            if evac_times_same_sigma_one_run != []:
                evac_times_same_sigma += np.array(evac_times_same_sigma_one_run)
                panics_same_sigma += np.array(panics_same_sigma_one_run)
        if s != 0:
            evac_times_same_sigma /= num_runs
            panics_same_sigma /= num_runs
        evac_times[str(s*100) + '%'] = evac_times_same_sigma.tolist()
        panics[str(s*100) + '%'] = panics_same_sigma.tolist()
        
    return evac_times, avg_speed,  panics
    

if __name__=="__main__":
    data, avg_speed, panics = main()
    #cProfile.run('main()', 'profiling_stats')
    #p = pstats.Stats('profiling_stats')
    #p.sort_stats(pstats.SortKey.TIME).print_stats(10)  # Adjust the number to see more or fewer results
    # Create a plot

    
    for key, values in data.items():
        plt.plot(avg_speed, values, label='speed diff:+-' + key)
    # Add labels and title
    plt.xlabel('Avg speed')  # You can customize this
    plt.ylabel('Mean evac time')  # You can customize this
    plt.title('Mean evac time for differnt avg speeds and speed ditributions')
    plt.legend()  # Show legend
    plt.grid(True)  # Optional: add a grid

    # Show the plot
    plt.savefig('plots/evac_times_one_door.pdf', format="pdf")
    plt.show()
    

    for key, values in panics.items():
        plt.plot(avg_speed, values, label='speed diff:+-' + key)
    # Add labels and title
    plt.xlabel('Avg speed')  # You can customize this
    plt.ylabel('Mean panic level')  # You can customize this
    plt.title('Mean panic for differnt avg speeds and speed ditributions')
    plt.legend()  # Show legend
    plt.grid(True)  # Optional: add a grid

    # Show the plot
    plt.savefig('plots/panics_one_door.pdf', format="pdf")
    plt.show()


        




