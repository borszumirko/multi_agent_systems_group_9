# Env constants
SCALING = 2
RENDER = True

CORR_WIDTH = 150 // SCALING
OBSTACLE_WIDTH = 50 // SCALING
OBSTACLE_HEIGHT = 870 // SCALING
BIG_OBSTACLE_H = 760 // SCALING
BIG_OBSTACLE_W = 100 // SCALING

CSV_FILE_NAME = "Experiment.csv"
# Column names for the CSV
COLUMN_NAMES = ["sep_threshold","avg_speed","sigma","avg_evac_time","avg_panic"]
WIDTH, HEIGHT = 2700 // SCALING, 1400 // SCALING
BOX_WIDTH, BOX_HEIGHT = 2080 // SCALING, 1180 // SCALING
BOX_LEFT = (WIDTH - BOX_WIDTH) // 2
BOX_TOP = (HEIGHT - BOX_HEIGHT) // 2
EXIT_WIDTH = 180 // SCALING
ENV_LENGTH = BOX_WIDTH

EXIT_HEIGHT = 15
EXITS = [
    {"position": (BOX_LEFT + ((1250+450)//SCALING), BOX_TOP - EXIT_HEIGHT), "width": EXIT_WIDTH, "height": EXIT_HEIGHT},
    # Comment or uncomment second exit
    # {"position": (BOX_LEFT + ((1250+450)//SCALING), BOX_TOP + BOX_HEIGHT), "width": EXIT_WIDTH, "height": EXIT_HEIGHT},
]

# Clock Box dimensions
CLOCK_BOX_WIDTH = 120
CLOCK_BOX_HEIGHT = 56
CLOCK_BOX_LEFT = (BOX_LEFT + BOX_WIDTH) + int((BOX_LEFT - CLOCK_BOX_WIDTH)/2)  # Right Box border + half of free space on the right side of the screen
CLOCK_BOX_TOP = BOX_TOP

# Agent constants
AGENT_AVG_SPEED = 1.67
AGENT_SPEED_SIGMA = 0.01
AGENT_RADIUS = 19 // SCALING
AGENT_COUNT = 240
AGENT_COLOR = (255, 255, 255)
SEPARATION_THRESHOLD = 2.0

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOX_COLOR = (208, 187, 48)
EXIT_COLOR = (202, 174, 152)

# Subgoal Zones
SUBGOAL_N = 2
VISUALIZE_SUBGOALS = False
SUBGOAL_ZONES = {
    0:[
        {"left": BOX_LEFT, "top": BOX_TOP, "width": OBSTACLE_WIDTH * 29 + 75, "height": CORR_WIDTH, "color": (0, 255, 0)},
        {"left": BOX_LEFT, "top": BOX_TOP+CORR_WIDTH+OBSTACLE_HEIGHT, "width": OBSTACLE_WIDTH * 29 + 75, "height": CORR_WIDTH, "color": (0, 255, 0)}
    ],
    1:[
        # The pre-goal-zone is wide as the whole classroom
        #{"position":(ex["position"][0]+EXIT_WIDTH//2, HEIGHT//2), "w":EXIT_WIDTH, "h":BOX_HEIGHT} for ex in EXITS 
        {"left": BOX_LEFT + OBSTACLE_WIDTH * 29 + 75, "top": BOX_TOP, "width": BOX_WIDTH - (OBSTACLE_WIDTH * 29 + 75), "height": BOX_HEIGHT, "color": (0, 0, 255)}
    ],
}
#BASE_ZONE = {"position": (sum([c[0] for c in centers])//len(centers), sum([c[1] for c in centers])//len(centers)), "w": obstacle_zone_x_span, "h": obstacle_zone_y_span}
BASE_ZONE = {"left": BOX_LEFT, "top": BOX_TOP + CORR_WIDTH, "width": OBSTACLE_WIDTH * 29 + 75, "height": OBSTACLE_HEIGHT, "color": (255, 0, 0)}