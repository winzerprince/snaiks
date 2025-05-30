# scavenger.py: Defines the Scavenger class - a creature that competes for food
import pygame
from pygame.math import Vector2
from settings import *
import random
import time
import uuid

class Scavenger:
    def __init__(self, initial_pos_x, initial_pos_y):
        self.id = str(uuid.uuid4())[:8]  # Unique ID for each scavenger
        
        # Position and movement
        self.position = Vector2(initial_pos_x, initial_pos_y)
        self.velocity = Vector2(0, 0)
        
        # Scavenger is fast but not as fast as rippers
        self.max_speed = BASE_MAX_SPEED * 1.8  # Faster than snakes, slower than rippers
        self.acceleration_rate = BASE_ACCELERATION * 2.0  # Good acceleration
        
        # Visual properties - crow/raven appearance
        self.body_color = (20, 20, 30)      # Very dark grayish-black
        self.beak_color = (180, 180, 50)    # Yellow-orange beak
        self.size = 12  # Medium size
        self.wing_span = 20  # Wing span for drawing
        
        # State
        self.is_dead = False
        self.alive = True
        self.target_food = None
        self.last_target_update = time.time()
        self.satiation = 0  # How much food eaten
        
        # Behavior
        self.detection_range = 120  # Can detect food from distance
        self.eating_range = 8  # Close enough to "eat" food
        
    def update(self, food_items):
        """Update scavenger behavior - compete for food with snakes"""
        if self.is_dead:
            return
            
        # Find and target the nearest food
        self.find_target(food_items)
        
        # Move towards target
        if self.target_food:
            self.move_towards_target()
        else:
            # Patrol randomly if no target
            self.patrol()
        
        # Handle screen boundaries
        self.handle_screen_wrap()
    
    def find_target(self, food_items):
        """Find the nearest food item to target"""
        current_time = time.time()
        
        # Update target every 0.3 seconds or if current target is gone
        if (current_time - self.last_target_update > 0.3 or 
            not self.target_food or 
            self.target_food not in food_items):
            
            nearest_food = None
            min_distance = float('inf')
            
            for food in food_items:
                distance = (self.position - food.position).length()
                if distance < self.detection_range and distance < min_distance:
                    min_distance = distance
                    nearest_food = food
            
            self.target_food = nearest_food
            self.last_target_update = current_time
    
    def move_towards_target(self):
        """Move towards the target food"""
        if not self.target_food:
            return
            
        # Calculate direction to target
        direction = self.target_food.position - self.position
        if direction.length_squared() > 0:
            direction = direction.normalize()
            
            # Apply acceleration towards target
            self.velocity += direction * self.acceleration_rate
            
            # Cap speed
            if self.velocity.length_squared() > self.max_speed * self.max_speed:
                self.velocity = self.velocity.normalize() * self.max_speed
        
        # Update position
        self.position += self.velocity
    
    def patrol(self):
        """Random patrol movement when no target is available"""
        # Add some random movement to prevent getting stuck
        random_direction = Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )
        
        if random_direction.length_squared() > 0:
            random_direction = random_direction.normalize()
            self.velocity += random_direction * (self.acceleration_rate * 0.2)
            
            # Apply some drag when patrolling
            self.velocity *= 0.92
            
            # Cap patrol speed (slower than hunting)
            patrol_speed = self.max_speed * 0.3
            if self.velocity.length_squared() > patrol_speed * patrol_speed:
                self.velocity = self.velocity.normalize() * patrol_speed
        
        self.position += self.velocity
    
    def handle_screen_wrap(self):
        """Handle screen boundaries"""
        if WALL_BEHAVIOR == "wraparound":
            if self.position.x < 0:
                self.position.x = SCREEN_WIDTH
            elif self.position.x > SCREEN_WIDTH:
                self.position.x = 0
                
            if self.position.y < 0:
                self.position.y = SCREEN_HEIGHT
            elif self.position.y > SCREEN_HEIGHT:
                self.position.y = 0
        elif WALL_BEHAVIOR == "destructive":
            if (self.position.x < 0 or self.position.x > SCREEN_WIDTH or 
                self.position.y < 0 or self.position.y > SCREEN_HEIGHT):
                self.die("hit wall")
    
    def check_collision_with_food(self, food):
        """Check if scavenger is close enough to eat food"""
        if self.is_dead:
            return False
            
        distance = (self.position - food.position).length()
        return distance < self.eating_range
    
    def eat_food(self):
        """Scavenger eats food and gains satiation"""
        self.satiation += 1
        if self.satiation >= 10:  # After eating 10 food items, scavenger flies away
            self.die("satisfied and flew away")
    
    def die(self, reason="unknown"):
        """Mark scavenger as dead"""
        if not self.is_dead:
            self.is_dead = True
            self.alive = False
            print(f"Scavenger {self.id} {reason}")
    
    def draw(self, screen):
        """Draw the scavenger as a crow/raven-like creature"""
        if self.is_dead:
            return
            
        # Draw body (dark oval)
        body_rect = pygame.Rect(
            int(self.position.x - self.size // 2),
            int(self.position.y - self.size // 2),
            self.size,
            self.size
        )
        pygame.draw.ellipse(screen, self.body_color, body_rect)
        
        # Draw wings (extended when moving fast)
        speed = self.velocity.length()
        if speed > self.max_speed * 0.3:  # Wings out when moving
            wing_color = (40, 40, 50)
            # Left wing
            left_wing = [
                (int(self.position.x - self.wing_span // 2), int(self.position.y)),
                (int(self.position.x - self.size // 2), int(self.position.y - self.size // 3)),
                (int(self.position.x - self.size // 2), int(self.position.y + self.size // 3))
            ]
            pygame.draw.polygon(screen, wing_color, left_wing)
            
            # Right wing
            right_wing = [
                (int(self.position.x + self.wing_span // 2), int(self.position.y)),
                (int(self.position.x + self.size // 2), int(self.position.y - self.size // 3)),
                (int(self.position.x + self.size // 2), int(self.position.y + self.size // 3))
            ]
            pygame.draw.polygon(screen, wing_color, right_wing)
        
        # Draw beak (pointing toward target)
        beak_length = 6
        if self.target_food:
            # Point beak toward food
            direction = (self.target_food.position - self.position).normalize()
        else:
            # Default forward direction
            direction = Vector2(1, 0)
        
        beak_end = self.position + direction * beak_length
        pygame.draw.line(screen, self.beak_color, 
                        (int(self.position.x), int(self.position.y)),
                        (int(beak_end.x), int(beak_end.y)), 3)
        
        # Draw small eyes
        eye_color = (255, 255, 100)  # Yellow eyes
        eye1_pos = (int(self.position.x - 2), int(self.position.y - 2))
        eye2_pos = (int(self.position.x + 2), int(self.position.y - 2))
        pygame.draw.circle(screen, eye_color, eye1_pos, 1)
        pygame.draw.circle(screen, eye_color, eye2_pos, 1)
        
        # Draw target line if hunting food (faint)
        if self.target_food:
            pygame.draw.line(screen, (100, 100, 150), 
                           (int(self.position.x), int(self.position.y)),
                           (int(self.target_food.position.x), int(self.target_food.position.y)), 
                           1)
