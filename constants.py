# Env constants
WIDTH, HEIGHT = 1500, 1000
BOX_WIDTH, BOX_HEIGHT = 1200, 900
BOX_LEFT = (WIDTH - BOX_WIDTH) // 2
BOX_TOP = (HEIGHT - BOX_HEIGHT) // 2
EXIT_WIDTH = 75
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