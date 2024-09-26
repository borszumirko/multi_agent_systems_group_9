# Env constants
WIDTH, HEIGHT = 1600, 800
BOX_WIDTH, BOX_HEIGHT = 1200, 600
BOX_LEFT = (WIDTH - BOX_WIDTH) // 2
BOX_TOP = (HEIGHT - BOX_HEIGHT) // 2
EXIT_WIDTH = 80
EXIT_POSITION = (BOX_LEFT + BOX_WIDTH, BOX_TOP + (BOX_HEIGHT // 2) - EXIT_WIDTH // 2)
ENV_LENGTH = BOX_WIDTH

# Agent constants
AGENT_MAX_SPEED = 3
AGENT_MAX_FORCE = 0.1
AGENT_PERCEPTION = 4
AGENT_RADIUS = 15
AGENT_COUNT = 300
AGENT_COLOR = (255, 255, 255)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOX_COLOR = (0, 0, 255)
EXIT_COLOR = (0, 255, 0)