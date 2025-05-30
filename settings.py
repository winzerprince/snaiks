# settings.py: Game constants

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Colors
BG_COLOR = (20, 30, 40) # Dark grayish blue
FOOD_COLOR = (255, 100, 100) # Light red

# Snake Color Schemes
NORMAL_SNAKE_BODY_COLOR = (50, 200, 50)  # Green
NORMAL_SNAKE_HEAD_COLOR = (70, 220, 70)  # Lighter Green
HUNTER_SNAKE_BODY_COLOR = (200, 50, 50)  # Red
HUNTER_SNAKE_HEAD_COLOR = (220, 70, 70)  # Lighter Red
DEAD_SNAKE_COLOR = (100, 100, 100) # Grey for when they die (optional visual)

# Game mechanics
FPS = 60
WALL_BEHAVIOR = "wraparound"  # "wraparound" or "destructive"

# Food
FOOD_RADIUS = 7
MAX_FOOD_ON_SCREEN = 15
FOOD_SPAWN_INTERVAL = 0.5 # seconds

# Snake properties
INITIAL_SNAKE_LENGTH = 3
SNAKE_SEGMENT_RADIUS = 8
# Speed and acceleration will be dynamic, these are base values
BASE_MAX_SPEED = 5.0  # Pixels per frame
BASE_ACCELERATION = 0.2 # Pixels per frame^2
# Factor by which speed/acceleration decreases with size.
# e.g. max_speed = BASE_MAX_SPEED / (1 + size * SIZE_SPEED_PENALTY_FACTOR)
SIZE_SPEED_PENALTY_FACTOR = 0.0
SIZE_ACCEL_PENALTY_FACTOR = 0.0

SNAKE_SPAWN_INTERVAL_MIN = 2 # seconds
SNAKE_SPAWN_INTERVAL_MAX = 2 # seconds
MAX_SNAKES_ON_SCREEN = 20 # Initial limit, can be adjusted

FOOD_TO_BECOME_HUNTER = 10
WINNING_SIZE = 50 # Example size to win

# AI Behavior Constants
FEAR_MARGIN = 5  # Segments larger a hunter must be to induce fear
WALL_AVOIDANCE_DISTANCE = SNAKE_SEGMENT_RADIUS * 4 # How far to "see" walls
THREAT_AVOIDANCE_DISTANCE = SNAKE_SEGMENT_RADIUS * 10 # How far to "see" threats
PROACTIVE_AVOIDANCE_STRENGTH = 0.5 # How strongly to steer away

# ===== CREATURE SYSTEM =====
# Enable/Disable switches for different creatures
ENABLE_RIPPERS = True  # Enable Ripper entities that hunt hunters
ENABLE_SCAVENGERS = True  # Enable Scavenger entities (competes for food)
ENABLE_GUARDIANS = False  # Enable Guardian entities (future creature)

# Ripper Entity Settings
MAX_RIPPERS_ON_SCREEN = 3  # Maximum number of rippers allowed
RIPPER_SPAWN_INTERVAL = 5.0  # Seconds between ripper spawn checks
HUNTER_POPULATION_THRESHOLD = 0.5  # 50% hunters triggers ripper spawning
RIPPER_DESPAWN_DELAY = 10.0  # Seconds before ripper despawns when hunter population drops

# Scavenger Entity Settings
MAX_SCAVENGERS_ON_SCREEN = 2  # Maximum number of scavengers allowed
SCAVENGER_SPAWN_INTERVAL = 8.0  # Seconds between scavenger spawn checks
FOOD_ABUNDANCE_THRESHOLD = 10  # Minimum food count to trigger scavenger spawning

