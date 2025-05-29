# snake.py: Defines the Snake class
import pygame
from settings import *
from pygame.math import Vector2
import uuid # For unique snake IDs
import logging # For logging within the class
import json
import time
from logger_setup import ml_data_logger, log_ml_training_data

class Snake:
    def __init__(self, initial_pos_x, initial_pos_y, logger, color=None, initial_length=INITIAL_SNAKE_LENGTH):
        self.id = str(uuid.uuid4())[:8] # Unique ID for each snake
        self.logger = logger
        self.log_extra = {'snake_id': self.id} # Prepares extra dict for logger

        self.body_segments = [] # List of Vector2 positions for each segment
        self.head_position = Vector2(initial_pos_x, initial_pos_y)

        self.is_hunter = False # Initialize first
        self.body_color = NORMAL_SNAKE_BODY_COLOR
        self.head_color = NORMAL_SNAKE_HEAD_COLOR
        if color: # Allow specific color override if provided, though hunter status will change it
            self.body_color = color
            self.head_color = (min(255,color[0]+20), min(255,color[1]+20), min(255,color[2]+20))

        self.initial_length = initial_length

        self.velocity = Vector2(0, 0) # Current velocity
        self.max_speed = BASE_MAX_SPEED
        self.acceleration_rate = BASE_ACCELERATION

        self.size = initial_length # Number of segments including head
        self.food_eaten = 0
        self.is_dead = False

        self.last_decision_time = time.time()
        self.alive = True

        # Initialize body
        for i in range(self.initial_length):
            # Segments initially overlap by half their radius for a connected look
            self.body_segments.append(Vector2(self.head_position.x - i * SNAKE_SEGMENT_RADIUS * 1.0, self.head_position.y))
        if self.body_segments:
            self.head_position = self.body_segments[0]

        self.logger.info(f"Created. Pos:({initial_pos_x:.1f},{initial_pos_y:.1f}), Initial Size:{self.size}, Color:{self.body_color}", extra=self.log_extra)
        self.update_dynamic_properties()

    def update_dynamic_properties(self):
        """Updates speed and acceleration based on size."""
        # Inverse relationship: larger snake, slower and less agile
        self.max_speed = BASE_MAX_SPEED / (1 + (self.size - self.initial_length) * SIZE_SPEED_PENALTY_FACTOR)
        self.acceleration_rate = BASE_ACCELERATION / (1 + (self.size - self.initial_length) * SIZE_ACCEL_PENALTY_FACTOR)
        # Ensure they don't go to zero or negative
        self.max_speed = max(0.5, self.max_speed) # Minimum speed
        self.acceleration_rate = max(0.05, self.acceleration_rate) # Minimum acceleration

    def move(self, target_direction: Vector2 = None, nearest_food=None, nearest_hunter=None, min_food_dist=None, min_hunter_dist=None):
        if self.is_dead:
            return

        # Log every move decision for ML
        state = {
            'pos': (self.head_position.x, self.head_position.y),
            'velocity': (self.velocity.x, self.velocity.y),
            'size': self.size,
            'is_hunter': self.is_hunter,
            'food_eaten': self.food_eaten,
            'nearest_food': tuple(nearest_food) if nearest_food is not None else None,
            'nearest_hunter': tuple(nearest_hunter) if nearest_hunter is not None else None,
            'min_food_dist': min_food_dist,
            'min_hunter_dist': min_hunter_dist
        }
        action = {
            'target_direction': (target_direction.x, target_direction.y) if target_direction else None,
            'current_velocity': (self.velocity.x, self.velocity.y)
        }
        self.log_event(
            event_type="move_decision",
            state=state,
            action=action,
            outcome=None
        )

        if target_direction and target_direction.length_squared() > 0:
            desired_velocity = target_direction.normalize() * self.max_speed
            steering = (desired_velocity - self.velocity)
            if steering.length_squared() > 0:
                 steering = steering.normalize() * self.acceleration_rate
            self.velocity += steering

        # Cap speed
        if self.velocity.length_squared() > self.max_speed * self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # Update head position
        new_head_position = self.head_position + self.velocity

        # Move body segments
        self.body_segments.insert(0, new_head_position)
        if len(self.body_segments) > self.size:
            self.body_segments.pop()

        self.head_position = self.body_segments[0]
        self.handle_screen_wrap()
        if not self.is_dead:
            pass

    def grow(self, amount=1, reason="ate food"):
        if self.is_dead: return
        old_size = self.size
        self.size += amount
        self.logger.info(f"Grew by {amount} from {old_size} to {self.size}. Reason: {reason}. Food Eaten: {self.food_eaten}", extra=self.log_extra)

        if not self.is_hunter:
            if reason == "ate food":
                self.food_eaten += amount
            if self.food_eaten >= FOOD_TO_BECOME_HUNTER:
                self.is_hunter = True
                self.body_color = HUNTER_SNAKE_BODY_COLOR
                self.head_color = HUNTER_SNAKE_HEAD_COLOR
                self.logger.info(f"Became HUNTER at size {self.size}. Food eaten total: {self.food_eaten}", extra=self.log_extra)
        self.update_dynamic_properties()

    def handle_screen_wrap(self):
        if self.is_dead: return
        original_pos = self.head_position.copy()

        if WALL_BEHAVIOR == "wraparound":
            wrapped = False
            if self.head_position.x > SCREEN_WIDTH + SNAKE_SEGMENT_RADIUS: # Allow going slightly off before wrap
                self.head_position.x = -SNAKE_SEGMENT_RADIUS
                wrapped = True
            elif self.head_position.x < -SNAKE_SEGMENT_RADIUS:
                self.head_position.x = SCREEN_WIDTH + SNAKE_SEGMENT_RADIUS
                wrapped = True
            if self.head_position.y > SCREEN_HEIGHT + SNAKE_SEGMENT_RADIUS:
                self.head_position.y = -SNAKE_SEGMENT_RADIUS
                wrapped = True
            elif self.head_position.y < -SNAKE_SEGMENT_RADIUS:
                self.head_position.y = SCREEN_HEIGHT + SNAKE_SEGMENT_RADIUS
                wrapped = True

            if wrapped:
                self.logger.debug(f"Wrapped screen from ({original_pos.x:.1f},{original_pos.y:.1f}) to ({self.head_position.x:.1f},{self.head_position.y:.1f})", extra=self.log_extra)
                self.body_segments[0] = self.head_position

        elif WALL_BEHAVIOR == "destructive":
            # Check if center of head is out of bounds
            if not (0 <= self.head_position.x <= SCREEN_WIDTH and \
                    0 <= self.head_position.y <= SCREEN_HEIGHT):
                self.logger.info(f"Hit wall at ({self.head_position.x:.1f},{self.head_position.y:.1f}). Screen limits: W={SCREEN_WIDTH}, H={SCREEN_HEIGHT}", extra=self.log_extra)
                self.die(reason="hit wall")

    def check_self_collision(self):
        # Self-collision is disabled for now; always return False
        return False

    def die(self, reason="unknown"):
        if not self.is_dead:
            self.is_dead = True
            self.body_color = DEAD_SNAKE_COLOR
            self.head_color = DEAD_SNAKE_COLOR
            self.logger.info(f"Died. Reason: {reason}. Final size: {self.size}. Pos:({self.head_position.x:.1f},{self.head_position.y:.1f})", extra=self.log_extra)
            self.log_event(
                event_type="death",
                state={"pos": (self.head_position.x, self.head_position.y)},
                action=None,
                outcome=reason,
                extra={"final_size": self.size}
            )

    def log_event(self, event_type, state=None, action=None, outcome=None, extra=None):
        now = time.time()
        time_since_last = now - getattr(self, 'last_decision_time', now)
        self.last_decision_time = now

        # Continue with the detailed JSON logging for the general game activity log
        event = {
            'timestamp': now,
            'snake_id': self.id,
            'event_type': event_type,
            'state': state if state is not None else {},
            'action': action,
            'outcome': outcome,
            'time_since_last_decision': time_since_last,
            'is_hunter': self.is_hunter,
            'size': self.size,
            'food_eaten': self.food_eaten,
            'alive': not self.is_dead,
        }
        if extra:
            event.update(extra)

        # Only log to ML training data for move decisions with valid actions
        if event_type == "move_decision" and action and action.get('target_direction'):
            # Calculate features for ML training

            # 1. Current direction (normalized velocity)
            current_dir = (0, 0)
            if self.velocity.length_squared() > 0:
                norm_vel = self.velocity.normalize()
                current_dir = (norm_vel.x, norm_vel.y)

            # 2. Distance to nearest food (if available in state)
            food_dist = (0, 0)
            if 'nearest_food' in state and state['nearest_food'] is not None:
                food_pos = state['nearest_food']
                food_dist = (food_pos[0] - self.head_position.x, food_pos[1] - self.head_position.y)

            # 3. Distance to walls
            wall_dist = (
                self.head_position.y,                          # Distance to top wall
                SCREEN_WIDTH - self.head_position.x,           # Distance to right wall
                SCREEN_HEIGHT - self.head_position.y,          # Distance to bottom wall
                self.head_position.x                           # Distance to left wall
            )

            # 4. Distance to self (simplified, just using a constant for now)
            self_dist = 100.0  # Placeholder

            # 5. Distance to nearest hunter snake
            hunter_dist = 9999.0
            hunter_vec = (0, 0)
            if 'nearest_hunter' in state and state['nearest_hunter'] is not None:
                hunter_vec = (state['nearest_hunter'][0] - self.head_position.x, state['nearest_hunter'][1] - self.head_position.y)
                hunter_dist = (hunter_vec[0] ** 2 + hunter_vec[1] ** 2) ** 0.5

            # 6. Action taken (direction chosen)
            action_dir = action['target_direction']
            if action_dir[0] > 0 and abs(action_dir[0]) > abs(action_dir[1]):
                action_label = "RIGHT"
            elif action_dir[0] < 0 and abs(action_dir[0]) > abs(action_dir[1]):
                action_label = "LEFT"
            elif action_dir[1] > 0 and abs(action_dir[1]) > abs(action_dir[0]):
                action_label = "DOWN"
            elif action_dir[1] < 0 and abs(action_dir[1]) > abs(action_dir[0]):
                action_label = "UP"
            else:
                action_label = "NONE"

            # Log in scikit-learn friendly format (now with hunter info)
            log_ml_training_data(
                snake_direction=current_dir,
                distance_to_food=food_dist,
                distance_to_wall=wall_dist,
                distance_to_self=self_dist,
                action_taken=action_label,
                hunter_distance=hunter_dist,
                hunter_vector=hunter_vec
            )

        # Keep the original JSON logging for debugging and analysis
        ml_data_logger.info(json.dumps(event))

    def draw(self, screen):
        if self.is_dead and len(self.body_segments) == 0: # Don't draw if truly gone
            return

        # Draw body segments first
        for i, segment_pos in enumerate(reversed(self.body_segments)):
            # If dead, draw all segments in dead color
            color_to_use = self.body_color if not self.is_dead else DEAD_SNAKE_COLOR
            pygame.draw.circle(screen, color_to_use, (int(segment_pos.x), int(segment_pos.y)), SNAKE_SEGMENT_RADIUS)
            # Inner circle for detail
            inner_color_detail = (max(0,color_to_use[0]-30), max(0,color_to_use[1]-30), max(0,color_to_use[2]-30))
            pygame.draw.circle(screen, inner_color_detail, (int(segment_pos.x), int(segment_pos.y)), SNAKE_SEGMENT_RADIUS - 3)

        # Draw head on top, potentially with a different color
        if self.body_segments: # Ensure there's a head to draw
            head_draw_pos = self.body_segments[0]
            actual_head_color = self.head_color if not self.is_dead else DEAD_SNAKE_COLOR
            pygame.draw.circle(screen, actual_head_color, (int(head_draw_pos.x), int(head_draw_pos.y)), SNAKE_SEGMENT_RADIUS)
            # Inner circle for head
            inner_head_detail = (max(0,actual_head_color[0]-30), max(0,actual_head_color[1]-30), max(0,actual_head_color[2]-30))
            pygame.draw.circle(screen, inner_head_detail, (int(head_draw_pos.x), int(head_draw_pos.y)), SNAKE_SEGMENT_RADIUS - 3)

            # Draw eyes on the head if not dead
            if not self.is_dead and self.velocity.length_squared() > 0:
                direction_vector = self.velocity.normalize()
                perp_vector = Vector2(-direction_vector.y, direction_vector.x) * (SNAKE_SEGMENT_RADIUS * 0.4)
                eye_offset_forward = direction_vector * (SNAKE_SEGMENT_RADIUS * 0.3)

                eye1_pos = head_draw_pos + eye_offset_forward + perp_vector
                eye2_pos = head_draw_pos + eye_offset_forward - perp_vector

                eye_radius = SNAKE_SEGMENT_RADIUS * 0.25 # Slightly larger eyes
                pupil_radius = eye_radius * 0.5

                pygame.draw.circle(screen, (255,255,255), (int(eye1_pos.x), int(eye1_pos.y)), int(eye_radius))
                pygame.draw.circle(screen, (255,255,255), (int(eye2_pos.x), int(eye2_pos.y)), int(eye_radius))
                pygame.draw.circle(screen, (0,0,0), (int(eye1_pos.x), int(eye1_pos.y)), int(pupil_radius))
                pygame.draw.circle(screen, (0,0,0), (int(eye2_pos.x), int(eye2_pos.y)), int(pupil_radius))
