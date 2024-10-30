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
    simulation = Simulation()
    simulation.main_loop()

if __name__=="__main__":
    main()
    




