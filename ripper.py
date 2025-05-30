# ripper.py: Defines the Ripper class - a honey badger-like entity that hunts hunter snakes
import pygame
from pygame.math import Vector2
from settings import *
import random
import time
import uuid

class Ripper:
    def __init__(self, initial_pos_x, initial_pos_y):
        self.id = str(uuid.uuid4())[:8]  # Unique ID for each ripper
        
        # Position and movement
        self.position = Vector2(initial_pos_x, initial_pos_y)
        self.velocity = Vector2(0, 0)
        
        # Ripper is extremely fast and agile
        self.max_speed = BASE_MAX_SPEED * 2.5  # Much faster than any snake
        self.acceleration_rate = BASE_ACCELERATION * 3.0  # Very high acceleration
        
        # Visual properties - honey badger appearance
        self.body_color = (40, 35, 30)      # Dark brownish-black
        self.stripe_color = (200, 180, 140)  # Light tan/cream stripe
        self.size = 15  # Larger than normal snakes
        self.length = 25  # Body length
        
        # State
        self.is_dead = False
        self.alive = True
        self.target_hunter = None
        self.last_target_update = time.time()
        
        # Hunting behavior
        self.detection_range = 150  # Can detect hunters from far away
        self.attack_range = 20  # Close enough to "kill" a hunter
        
    def update(self, hunter_snakes):
        """Update ripper behavior - hunt down hunter snakes"""
        if self.is_dead:
            return
            
        # Find and target the nearest hunter snake
        self.find_target(hunter_snakes)
        
        # Move towards target
        if self.target_hunter and not self.target_hunter.is_dead:
            self.move_towards_target()
        else:
            # Patrol randomly if no target
            self.patrol()
            
        # Handle screen boundaries
        self.handle_screen_wrap()
    
    def find_target(self, hunter_snakes):
        """Find the nearest hunter snake to target"""
        current_time = time.time()
        
        # Update target every 0.5 seconds or if current target is dead
        if (current_time - self.last_target_update > 0.5 or 
            not self.target_hunter or 
            self.target_hunter.is_dead):
            
            nearest_hunter = None
            min_distance = float('inf')
            
            for hunter in hunter_snakes:
                if hunter.is_dead or not hunter.is_hunter:
                    continue
                    
                distance = (self.position - hunter.head_position).length()
                if distance < self.detection_range and distance < min_distance:
                    min_distance = distance
                    nearest_hunter = hunter
            
            self.target_hunter = nearest_hunter
            self.last_target_update = current_time
    
    def move_towards_target(self):
        """Move aggressively towards the target hunter"""
        if not self.target_hunter or self.target_hunter.is_dead:
            return
            
        # Calculate direction to target
        direction = self.target_hunter.head_position - self.position
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
            self.velocity += random_direction * (self.acceleration_rate * 0.3)
            
            # Apply some drag when patrolling
            self.velocity *= 0.95
            
            # Cap patrol speed (slower than hunting)
            patrol_speed = self.max_speed * 0.4
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
    
    def check_collision_with_hunter(self, hunter):
        """Check if ripper is close enough to eliminate a hunter"""
        if self.is_dead or hunter.is_dead or not hunter.is_hunter:
            return False
            
        distance = (self.position - hunter.head_position).length()
        return distance < self.attack_range
    
    def die(self, reason="unknown"):
        """Mark ripper as dead"""
        if not self.is_dead:
            self.is_dead = True
            self.alive = False
            print(f"Ripper {self.id} died: {reason}")
    
    def draw(self, screen):
        """Draw the ripper as a honey badger-like creature"""
        if self.is_dead:
            return
            
        # Draw main body (dark brownish-black oval)
        body_rect = pygame.Rect(
            int(self.position.x - self.length // 2),
            int(self.position.y - self.size // 2),
            self.length,
            self.size
        )
        pygame.draw.ellipse(screen, self.body_color, body_rect)
        
        # Draw characteristic honey badger stripe (light tan/cream)
        stripe_rect = pygame.Rect(
            int(self.position.x - self.length // 2 + 3),
            int(self.position.y - self.size // 2 + 2),
            self.length - 6,
            self.size // 2
        )
        pygame.draw.ellipse(screen, self.stripe_color, stripe_rect)
        
        # Draw head (slightly darker)
        head_color = (30, 25, 20)
        head_rect = pygame.Rect(
            int(self.position.x + self.length // 2 - 8),
            int(self.position.y - 6),
            12,
            12
        )
        pygame.draw.ellipse(screen, head_color, head_rect)
        
        # Draw small eyes
        eye_color = (255, 50, 50)  # Red eyes for intimidation
        eye1_pos = (int(self.position.x + self.length // 2 - 2), int(self.position.y - 2))
        eye2_pos = (int(self.position.x + self.length // 2 - 2), int(self.position.y + 2))
        pygame.draw.circle(screen, eye_color, eye1_pos, 2)
        pygame.draw.circle(screen, eye_color, eye2_pos, 2)
        
        # Draw target line if hunting
        if self.target_hunter and not self.target_hunter.is_dead:
            pygame.draw.line(screen, (255, 100, 100), 
                           (int(self.position.x), int(self.position.y)),
                           (int(self.target_hunter.head_position.x), int(self.target_hunter.head_position.y)), 
                           1)
