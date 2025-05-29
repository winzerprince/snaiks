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
FOOD_SPAWN_INTERVAL = 2 # seconds

# Snake properties
INITIAL_SNAKE_LENGTH = 3
SNAKE_SEGMENT_RADIUS = 8
# Speed and acceleration will be dynamic, these are base values
BASE_MAX_SPEED = 5.0  # Pixels per frame
BASE_ACCELERATION = 0.2 # Pixels per frame^2
# Factor by which speed/acceleration decreases with size.
# e.g. max_speed = BASE_MAX_SPEED / (1 + size * SIZE_SPEED_PENALTY_FACTOR)
SIZE_SPEED_PENALTY_FACTOR = 0.05
SIZE_ACCEL_PENALTY_FACTOR = 0.05

SNAKE_SPAWN_INTERVAL_MIN = 3 # seconds
SNAKE_SPAWN_INTERVAL_MAX = 10 # seconds
MAX_SNAKES_ON_SCREEN = 5 # Initial limit, can be adjusted

FOOD_TO_BECOME_HUNTER = 10
WINNING_SIZE = 50 # Example size to win

# AI Behavior Constants
FEAR_MARGIN = 5  # Segments larger a hunter must be to induce fear
WALL_AVOIDANCE_DISTANCE = SNAKE_SEGMENT_RADIUS * 4 # How far to "see" walls
THREAT_AVOIDANCE_DISTANCE = SNAKE_SEGMENT_RADIUS * 10 # How far to "see" threats
PROACTIVE_AVOIDANCE_STRENGTH = 0.5 # How strongly to steer away

# Logging Settings
import logging
LOG_LEVEL = logging.DEBUG # Level of messages to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FILE_PATH = "game_activity.log"
LOG_HISTORY_PATH = "game_history.log"  # Appended to, keeps all logs
ML_DATA_LOG_PATH = "ml_training_data.log"  # For ML training data (state, action, reward, next_state, done)

# ML settings (placeholders for now)
MODEL_PATH = "ml/models/snake_model.pth"

