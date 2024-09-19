# Constants
WIDTH, HEIGHT = 1600, 800
BOX_WIDTH, BOX_HEIGHT = 1200, 600
BOX_LEFT = (WIDTH - BOX_WIDTH) // 2
BOX_TOP = (HEIGHT - BOX_HEIGHT) // 2
EXIT_WIDTH = 60
EXIT_POSITION = (BOX_LEFT + BOX_WIDTH, BOX_TOP + (BOX_HEIGHT // 2) - EXIT_WIDTH // 2)

AGENT_MAX_SPEED = 3
AGENT_MAX_FORCE = 0.3
AGENT_PERCEPTION = 4

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOID_COLOR = (0, 255, 0)
BOX_COLOR = (255, 0, 0)
EXIT_COLOR = (0, 0, 255)
BOID_COUNT = 50
BOID_RADIUS = 15