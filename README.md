# Evacuation of a lecture hall with agent-based modelling

## Setup Instructions

### Install the required packages from the requirements.txt file (use a virtual environment)
```
pip install -r requirements.txt
```

## Usage
Run main.py to start the simulation
### Constants
Important parameters in constants.py:

```RENDER```
Enables or disables rendering

```EXIT_WIDTH```
Controls the width of the exit(s)

```EXITS```
This is a list of exits, you can comment or uncomment the second element to change the number of exits

```AGENT_AVG_SPEED```
Mean of the uniform distribution from which the agent speeds are sampled

```AGENT_SPEED_SIGMA```
Distribution boundaries are given by
```[AGENT_AVG_SPEED-AGENT_SPEED_SIGMA*AGENT_AVG_SPEED, AGENT_AVG_SPEED+AGENT_SPEED_SIGMA*AGENT_AVG_SPEED]```

```SEPARATION_THRESHOLD```
Decrease to allow some overlap between agents

### Experiment

With ```run_experiments``` in ```main.py```, you can run an experiment where multiple settings of ```AGENT_AVG_SPEED```, ```AGENT_SPEED_SIGMA``` and ```SEPARATION_THRESHOLD``` are tested.




