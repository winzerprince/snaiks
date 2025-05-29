# logger_setup.py
import logging
import sys
from settings import LOG_FILE_PATH, LOG_LEVEL, LOG_HISTORY_PATH, ML_DATA_LOG_PATH

def setup_logger():
    logger = logging.getLogger("SnakeGame")
    logger.setLevel(LOG_LEVEL)

    # Session log (overwritten each run)
    fh = logging.FileHandler(LOG_FILE_PATH, mode='w')
    fh.setLevel(LOG_LEVEL)
    # Persistent log (appended)
    hist_fh = logging.FileHandler(LOG_HISTORY_PATH, mode='a')
    hist_fh.setLevel(LOG_LEVEL)
    # ML data log (appended, INFO level only)
    ml_fh = logging.FileHandler(ML_DATA_LOG_PATH, mode='a')
    ml_fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - SnakeID:%(snake_id)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    class SnakeIDFilter(logging.Filter):
        def filter(self, record):
            if not hasattr(record, 'snake_id'):
                record.snake_id = 'N/A'
            return True
    logger.addFilter(SnakeIDFilter())

    fh.setFormatter(formatter)
    hist_fh.setFormatter(formatter)
    ml_fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(hist_fh)
    logger.addHandler(ml_fh)

    logger.info("Logging initialized.", extra={'snake_id': 'SYSTEM'})
    return logger

# For ML data logging convenience
ml_data_logger = logging.getLogger("MLData")
ml_data_logger.setLevel(logging.INFO)
ml_fh = logging.FileHandler(ML_DATA_LOG_PATH, mode='a')
ml_fh.setFormatter(logging.Formatter('%(message)s'))
ml_data_logger.addHandler(ml_fh)

# New function for scikit-learn friendly ML data logging
def log_ml_training_data(snake_direction, distance_to_food, distance_to_wall,
                         distance_to_self, action_taken, hunter_distance=None, hunter_vector=None):
    """
    Log essential snake game data in a format suitable for scikit-learn.
    Logs a single line of comma-separated values with the following format:

    direction_x,direction_y,food_distance_x,food_distance_y,wall_distance_up,wall_distance_right,
    wall_distance_down,wall_distance_left,self_collision_distance,hunter_distance,hunter_vec_x,hunter_vec_y,action_taken

    Parameters:
    - snake_direction: tuple (x, y) of current snake direction
    - distance_to_food: tuple (x, y) of distance to nearest food
    - distance_to_wall: tuple (up, right, down, left) distances to walls
    - distance_to_self: distance to nearest self-collision point
    - action_taken: the action/direction chosen ("UP", "RIGHT", "DOWN", "LEFT")
    - hunter_distance: distance to nearest hunter snake
    - hunter_vector: vector (x, y) to nearest hunter snake
    """
    features = [
        snake_direction[0],                # Current direction X
        snake_direction[1],                # Current direction Y
        distance_to_food[0],               # Food distance X
        distance_to_food[1],               # Food distance Y
        distance_to_wall[0],               # Wall distance up
        distance_to_wall[1],               # Wall distance right
        distance_to_wall[2],               # Wall distance down
        distance_to_wall[3],               # Wall distance left
        distance_to_self,                  # Self collision distance
        hunter_distance if hunter_distance is not None else 9999.0,
        hunter_vector[0] if hunter_vector is not None else 0,
        hunter_vector[1] if hunter_vector is not None else 0,
        action_taken                       # Action/direction chosen
    ]

    # Convert all values to strings and join with commas
    log_line = ','.join(str(feature) for feature in features)
    ml_data_logger.info(log_line)
