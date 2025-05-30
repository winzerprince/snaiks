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

# Starvation System
ENABLE_STARVATION = True  # Enable/disable starvation death
STARVATION_TIME = 10.0  # Seconds without food before snake dies of starvation
STARVATION_WARNING_TIME = 8.0  # Seconds when snake starts showing starvation warning

# ===== ENVIRONMENTAL EFFECTS SYSTEM =====
# Enable/Disable switches for different environmental effects
ENABLE_EFFECTS = True  # Master switch for all environmental effects
ENABLE_BLACK_HOLES = True  # Enable Black Hole effects that pull entities
ENABLE_SPEED_ZONES = True  # Enable zones that modify movement speed
ENABLE_FOOD_MAGNETS = True  # Enable zones that attract food items

# Black Hole Effect Settings
MAX_BLACK_HOLES = 2  # Maximum number of black holes on screen
BLACK_HOLE_SPAWN_INTERVAL = 20.0  # Seconds between black hole spawn attempts
BLACK_HOLE_LIFETIME = 15.0  # Seconds before black hole disappears
BLACK_HOLE_RADIUS = 60  # Visual radius of black hole
BLACK_HOLE_PULL_RADIUS = 120  # Range at which entities are affected
BLACK_HOLE_PULL_STRENGTH = 1.5  # How strong the gravitational pull is
BLACK_HOLE_MIN_DISTANCE = 150  # Minimum distance between black holes

# Speed Zone Effect Settings
MAX_SPEED_ZONES = 3  # Maximum number of speed zones on screen
SPEED_ZONE_SPAWN_INTERVAL = 25.0  # Seconds between speed zone spawn attempts
SPEED_ZONE_LIFETIME = 20.0  # Seconds before speed zone disappears
SPEED_ZONE_RADIUS = 80  # Radius of speed zone effect
SPEED_ZONE_SLOW_MULTIPLIER = 0.3  # Speed multiplier for slow zones
SPEED_ZONE_FAST_MULTIPLIER = 2.0  # Speed multiplier for fast zones

# Food Magnet Effect Settings
MAX_FOOD_MAGNETS = 1  # Maximum number of food magnets on screen
FOOD_MAGNET_SPAWN_INTERVAL = 30.0  # Seconds between food magnet spawn attempts
FOOD_MAGNET_LIFETIME = 12.0  # Seconds before food magnet disappears
FOOD_MAGNET_RADIUS = 40  # Visual radius of food magnet
FOOD_MAGNET_PULL_RADIUS = 100  # Range at which food is affected
FOOD_MAGNET_PULL_STRENGTH = 2.0  # How strong the food attraction is

# ===== SPECIAL FOOD SYSTEM =====
# Enable/Disable switches for different food types
ENABLE_SPECIAL_FOOD = True  # Master switch for special food types
ENABLE_SPEED_FOOD = True  # Enable speed boost food
ENABLE_SLOW_FOOD = True  # Enable speed reduction food  
ENABLE_IMMUNITY_FOOD = True  # Enable temporary immunity food
ENABLE_GROWTH_FOOD = True  # Enable instant growth food
ENABLE_SHRINK_FOOD = True  # Enable shrinking food

# Special Food Spawn Settings
SPECIAL_FOOD_SPAWN_CHANCE = 0.15  # 15% chance for special food instead of normal
SPECIAL_FOOD_EFFECT_DURATION = 8.0  # Default effect duration in seconds

# Speed Food Settings
SPEED_FOOD_COLOR = (0, 255, 255)  # Cyan
SPEED_FOOD_BOOST_MULTIPLIER = 2.5  # Speed multiplier
SPEED_FOOD_ACCEL_MULTIPLIER = 3.0  # Acceleration multiplier
SPEED_FOOD_DURATION = 6.0  # Effect duration

# Slow Food Settings  
SLOW_FOOD_COLOR = (128, 0, 128)  # Purple
SLOW_FOOD_REDUCTION_MULTIPLIER = 0.4  # Speed reduction multiplier
SLOW_FOOD_DURATION = 10.0  # Effect duration

# Immunity Food Settings
IMMUNITY_FOOD_COLOR = (255, 215, 0)  # Gold
IMMUNITY_FOOD_DURATION = 5.0  # Immunity duration
IMMUNITY_FOOD_FLASH_SPEED = 8  # How fast immunity visual flashes

# Growth Food Settings
GROWTH_FOOD_COLOR = (255, 165, 0)  # Orange
GROWTH_FOOD_SIZE_BONUS = 3  # Instant size increase

# Shrink Food Settings
SHRINK_FOOD_COLOR = (255, 20, 147)  # Deep pink
SHRINK_FOOD_SIZE_REDUCTION = 2  # Size reduction amount
SHRINK_FOOD_MIN_SIZE = 2  # Minimum size after shrinking

