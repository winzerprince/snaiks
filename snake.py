# snake.py: Defines the Snake class
import pygame
import math
import time
import uuid # For unique snake IDs
from pygame.math import Vector2
from settings import *

class Snake:
    def __init__(self, initial_pos_x, initial_pos_y, color=None, initial_length=INITIAL_SNAKE_LENGTH):
        self.id = str(uuid.uuid4())[:8] # Unique ID for each snake

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
        
        # Starvation tracking
        self.last_food_time = time.time()  # Track when snake last ate food
        self.is_starving = False  # Visual indicator for starvation warning
        
        # Food effects and immunity
        self.is_immune = False  # Temporary immunity from hunters
        self.recent_growth_time = 0  # Track recent growth for visual effect
        self.recent_shrink_time = 0  # Track recent shrinking for visual effect

        self.last_decision_time = time.time()
        self.alive = True

        # Initialize body
        for i in range(self.initial_length):
            # Segments initially overlap by half their radius for a connected look
            self.body_segments.append(Vector2(self.head_position.x - i * SNAKE_SEGMENT_RADIUS * 1.0, self.head_position.y))
        if self.body_segments:
            self.head_position = self.body_segments[0]

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

    def grow(self, amount=1, reason="ate food"):
        if self.is_dead: return
        self.size += amount

        # Reset starvation timer when eating food
        if reason == "ate food":
            self.last_food_time = time.time()
            self.is_starving = False
            
        # Track recent growth for visual effects
        if amount > 1:  # Special food growth
            self.recent_growth_time = time.time()

        if not self.is_hunter:
            if reason == "ate food":
                self.food_eaten += amount
            if self.food_eaten >= FOOD_TO_BECOME_HUNTER:
                self.is_hunter = True
                self.body_color = HUNTER_SNAKE_BODY_COLOR
                self.head_color = HUNTER_SNAKE_HEAD_COLOR
        self.update_dynamic_properties()

    def handle_screen_wrap(self):
        if self.is_dead: return

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
                self.body_segments[0] = self.head_position

        elif WALL_BEHAVIOR == "destructive":
            # Check if center of head is out of bounds
            if not (0 <= self.head_position.x <= SCREEN_WIDTH and \
                    0 <= self.head_position.y <= SCREEN_HEIGHT):
                self.die(reason="hit wall")

    def check_self_collision(self):
        # Self-collision is disabled for now; always return False
        return False

    def check_starvation(self):
        """Check if snake is starving and handle starvation death"""
        if self.is_dead or not ENABLE_STARVATION:
            return
        
        current_time = time.time()
        time_since_food = current_time - self.last_food_time
        
        # Check if snake should die from starvation
        if time_since_food >= STARVATION_TIME:
            self.die(reason="starvation")
            return
        
        # Check if snake is entering starvation warning state
        if time_since_food >= STARVATION_WARNING_TIME:
            self.is_starving = True
        else:
            self.is_starving = False

    def die(self, reason="unknown"):
        if not self.is_dead:
            self.is_dead = True
            self.death_time = time.time()  # Track when snake died
            self.body_color = DEAD_SNAKE_COLOR
            self.head_color = DEAD_SNAKE_COLOR

    def draw(self, screen, active_effects=None):
        if self.is_dead and len(self.body_segments) == 0: # Don't draw if truly gone
            return

        # Get active effects for visual indicators
        effects = active_effects or []
        
        # Draw body segments first
        for segment_pos in reversed(self.body_segments):
            # If dead, draw all segments in dead color
            if self.is_dead:
                color_to_use = DEAD_SNAKE_COLOR
            elif self.is_starving:
                # Starving snakes get a pulsing orange/yellow color
                pulse = int(128 + 127 * math.sin(time.time() * 8))  # Fast pulsing
                if self.is_hunter:
                    color_to_use = (pulse, pulse//2, 0)  # Orange pulse for starving hunters
                else:
                    color_to_use = (pulse, pulse, 0)  # Yellow pulse for starving normal snakes
            else:
                # Check for active food effects and modify color accordingly
                color_to_use = self.body_color
                for effect in effects:
                    if effect.effect_type == "speed_boost":
                        # Cyan tint for speed boost
                        boost_pulse = int(50 + 50 * math.sin(time.time() * 12))
                        color_to_use = (
                            max(0, min(255, self.body_color[0] + boost_pulse)),
                            max(0, min(255, self.body_color[1] + boost_pulse)),
                            max(0, min(255, self.body_color[2] + 100 + boost_pulse))
                        )
                        break
                    elif effect.effect_type == "slow":
                        # Purple tint for slow effect
                        color_to_use = (
                            max(0, min(255, self.body_color[0] + 50)),
                            max(0, min(255, self.body_color[1] - 50)),
                            max(0, min(255, self.body_color[2] + 80))
                        )
                        break
                
            pygame.draw.circle(screen, color_to_use, (int(segment_pos.x), int(segment_pos.y)), SNAKE_SEGMENT_RADIUS)
            # Inner circle for detail
            inner_color_detail = (max(0,color_to_use[0]-30), max(0,color_to_use[1]-30), max(0,color_to_use[2]-30))
            pygame.draw.circle(screen, inner_color_detail, (int(segment_pos.x), int(segment_pos.y)), SNAKE_SEGMENT_RADIUS - 3)

        # Draw head on top, potentially with a different color
        if self.body_segments: # Ensure there's a head to draw
            head_draw_pos = self.body_segments[0]
            
            if self.is_dead:
                actual_head_color = DEAD_SNAKE_COLOR
            elif self.is_starving:
                # Starving heads get a brighter pulse effect
                pulse = int(128 + 127 * math.sin(time.time() * 8))
                if self.is_hunter:
                    actual_head_color = (255, pulse//2, 0)  # Bright orange pulse for starving hunters
                else:
                    actual_head_color = (255, pulse, 0)  # Bright yellow pulse for starving normal snakes
            else:
                # Check for active effects on head
                actual_head_color = self.head_color
                for effect in effects:
                    if effect.effect_type == "immunity":
                        # Golden pulsing effect for immunity
                        immunity_pulse = int(150 + 105 * math.sin(time.time() * IMMUNITY_FOOD_FLASH_SPEED))
                        actual_head_color = (immunity_pulse, max(0, immunity_pulse - 50), 0)
                        break
                    elif effect.effect_type == "speed_boost":
                        # Bright cyan for speed boost
                        speed_pulse = int(100 + 100 * math.sin(time.time() * 15))
                        actual_head_color = (speed_pulse, 255, 255)
                        break
                    elif effect.effect_type == "slow":
                        # Dark purple for slow effect
                        actual_head_color = (128, 0, 128)
                        break
                
            pygame.draw.circle(screen, actual_head_color, (int(head_draw_pos.x), int(head_draw_pos.y)), SNAKE_SEGMENT_RADIUS)
            # Inner circle for head
            inner_head_detail = (max(0,actual_head_color[0]-30), max(0,actual_head_color[1]-30), max(0,actual_head_color[2]-30))
            pygame.draw.circle(screen, inner_head_detail, (int(head_draw_pos.x), int(head_draw_pos.y)), SNAKE_SEGMENT_RADIUS - 3)

            # Draw special effect auras around the head
            for effect in effects:
                if effect.effect_type == "immunity":
                    # Golden aura around immune snakes
                    aura_radius = SNAKE_SEGMENT_RADIUS + 8 + int(3 * math.sin(time.time() * 6))
                    aura_alpha = int(100 + 50 * math.sin(time.time() * 4))
                    aura_color = (255, 215, 0, aura_alpha)
                    aura_surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(aura_surface, aura_color, (aura_radius, aura_radius), aura_radius, 3)
                    screen.blit(aura_surface, (head_draw_pos.x - aura_radius, head_draw_pos.y - aura_radius))
                    
                elif effect.effect_type == "speed_boost":
                    # Speed lines around fast snakes
                    for i in range(6):
                        angle = time.time() * 15 + i * 60
                        line_length = SNAKE_SEGMENT_RADIUS + 12
                        end_x = head_draw_pos.x + line_length * math.cos(math.radians(angle))
                        end_y = head_draw_pos.y + line_length * math.sin(math.radians(angle))
                        line_color = (0, 255, 255, 150)
                        line_surface = pygame.Surface((3, int(line_length * 2)), pygame.SRCALPHA)
                        pygame.draw.line(line_surface, line_color, (1, int(line_length)), (1, int(line_length * 1.5)), 2)
                        # Rotate and blit the line (simplified approach)
                        pygame.draw.line(screen, (0, 255, 255), 
                                       (int(head_draw_pos.x), int(head_draw_pos.y)),
                                       (int(end_x), int(end_y)), 2)

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
