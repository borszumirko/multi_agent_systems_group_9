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

```RENDER = True```
Enables or disabler rendering
```EXITS = [
    {"position": (BOX_LEFT + ((1250+450)//SCALING), BOX_TOP - EXIT_HEIGHT), "width": EXIT_WIDTH, "height": EXIT_HEIGHT},
    # Comment or uncomment second exit
    # {"position": (BOX_LEFT + ((1250+450)//SCALING), BOX_TOP + BOX_HEIGHT), "width": EXIT_WIDTH, "height": EXIT_HEIGHT},
]```
Comment or uncomment second exit
``AGENT_AVG_SPEED = 1.67```
Mean of the uniform distribution from which the agent speed are sampled
```AGENT_SPEED_SIGMA = 0.01```
Distribution boundaries are given by [AGENT_AVG_SPEED-AGENT_SPEED_SIGMA*AGENT_AVG_SPEED, AGENT_AVG_SPEED+AGENT_SPEED_SIGMA*AGENT_AVG_SPEED]
```SEPARATION_THRESHOLD = 2.0```
Controls how much overlap is allowed between agents


