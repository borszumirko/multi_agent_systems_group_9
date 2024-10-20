# Env constants
CSV_FILE_NAME = "Experiment_3.csv"
WIDTH, HEIGHT = 1500, 1000
BOX_WIDTH, BOX_HEIGHT = 1200, 900
BOX_LEFT = (WIDTH - BOX_WIDTH) // 2
BOX_TOP = (HEIGHT - BOX_HEIGHT) // 2
EXIT_WIDTH = 35
ENV_LENGTH = BOX_WIDTH
EXITS = [
    {"position": (BOX_LEFT + BOX_WIDTH, BOX_TOP + (BOX_HEIGHT // 2) - EXIT_WIDTH // 2 + 350), "width": EXIT_WIDTH},
    {"position": (BOX_LEFT - 15, BOX_TOP + (BOX_HEIGHT // 2) - EXIT_WIDTH // 2 + 350), "width": EXIT_WIDTH},
    # Add more exits as needed
]

# Clock Box dimensions
CLOCK_BOX_WIDTH = 120
CLOCK_BOX_HEIGHT = 56
CLOCK_BOX_LEFT = (BOX_LEFT + BOX_WIDTH) + int((BOX_LEFT - CLOCK_BOX_WIDTH)/2)  # Right Box border + half of free space on the right side of the screen
CLOCK_BOX_TOP = BOX_TOP

# Agent constants
AGENT_MAX_SPEED = 2
AGENT_MAX_FORCE = 5
AGENT_PERCEPTION = 4
AGENT_RADIUS = 15
AGENT_COUNT = 150
AGENT_COLOR = (255, 255, 255)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOX_COLOR = (208, 187, 48)
EXIT_COLOR = (202, 174, 152)


# Obstacles -> TODO: No single source of truth and not dynamic (Are hardcoded in the simulation) 
y_min = 100000
y_max = 0
for i in range(10):
    center = (BOX_LEFT + 100 + (1000 // 2), BOX_TOP + (i+1) * 60 + 50 + 20 // 2)
    if center[1] + 10 > y_max:
        y_max = center[1] + 10
    if center[1] - 10 < y_min:
        y_min = center[1] - 10
        print(y_min)

obstacle_zone_y_span = y_max - y_min
# Subgoal Zones
SUBGOAL_N = 2
SUBGOAL_ZONES = {
    0:[
        {"position": (BOX_LEFT + 50, obstacle_zone_y_span//2 + y_min), "w": 100, "h": obstacle_zone_y_span+150},
        {"position": (BOX_LEFT + 1150, obstacle_zone_y_span//2 + y_min), "w": 100, "h": obstacle_zone_y_span+150}
    ],
    1:[
        # The pre-goal-zone is wide as the whole calssroom
        # It is as high as the exit itself plus 50 pixels (So it embedds the exit)
        {"position":(WIDTH//2, ex["position"][1]), "w":BOX_WIDTH, "h":EXIT_WIDTH + 100} for ex in EXITS 
    ],
}