# basic_behavior.py: Basic behavior system for snakes
import random
import math
from pygame.math import Vector2
from settings import *

class BasicBehavior:
    """Handles AI decision making for snakes"""
    
    @staticmethod
    def calculate_direction(snake, food_items, other_snakes):
        """Calculate optimal direction for a snake based on current game state"""
        if snake.is_dead:
            return Vector2(0, 0)
        
        # Find nearest food
        nearest_food = BasicBehavior.find_nearest_food(snake, food_items)
        
        # Find threats (larger snakes if current snake is a hunter target)
        threats = BasicBehavior.find_threats(snake, other_snakes)
        
        # Find prey (smaller snakes if current snake is a hunter)
        prey = BasicBehavior.find_prey(snake, other_snakes)
        
        # Calculate desired direction based on priorities
        direction = BasicBehavior.calculate_behavior_vector(snake, nearest_food, threats, prey)
        
        return direction
    
    @staticmethod
    def find_nearest_food(snake, food_items):
        """Find the nearest food item to the snake"""
        if not food_items:
            return None
            
        nearest_food = None
        min_distance = float('inf')
        
        for food in food_items:
            distance = snake.head_position.distance_to(food.position)
            if distance < min_distance:
                min_distance = distance
                nearest_food = food
                
        return nearest_food
    
    @staticmethod
    def find_threats(snake, other_snakes):
        """Find threatening snakes (hunters larger than current snake)"""
        threats = []
        
        for other_snake in other_snakes:
            if other_snake == snake or other_snake.is_dead:
                continue
                
            # A threat is a hunter that's larger than current snake + fear margin
            if (other_snake.is_hunter and 
                other_snake.size > snake.size + FEAR_MARGIN and
                snake.head_position.distance_to(other_snake.head_position) < THREAT_AVOIDANCE_DISTANCE):
                threats.append(other_snake)
                
        return threats
    
    @staticmethod
    def find_prey(snake, other_snakes):
        """Find potential prey (smaller snakes if current snake is hunter)"""
        if not snake.is_hunter:
            return []
            
        prey = []
        
        for other_snake in other_snakes:
            if other_snake == snake or other_snake.is_dead:
                continue
                
            # Prey is a smaller snake within hunting range
            if (other_snake.size < snake.size - FEAR_MARGIN and
                snake.head_position.distance_to(other_snake.head_position) < THREAT_AVOIDANCE_DISTANCE):
                prey.append(other_snake)
                
        return prey
    
    @staticmethod
    def calculate_behavior_vector(snake, nearest_food, threats, prey):
        """Calculate the final movement vector based on all factors"""
        final_direction = Vector2(0, 0)
        
        # 1. Avoid threats (highest priority)
        if threats:
            threat_avoidance = BasicBehavior.calculate_threat_avoidance(snake, threats)
            final_direction += threat_avoidance * 3.0  # High weight
        
        # 2. Hunt prey (medium-high priority for hunters)
        elif prey and snake.is_hunter:
            prey_pursuit = BasicBehavior.calculate_prey_pursuit(snake, prey)
            final_direction += prey_pursuit * 2.0  # Medium-high weight
        
        # 3. Seek food (medium priority)
        elif nearest_food:
            food_seeking = BasicBehavior.calculate_food_seeking(snake, nearest_food)
            final_direction += food_seeking * 1.5  # Medium weight
        
        # 4. Avoid walls (always active)
        wall_avoidance = BasicBehavior.calculate_wall_avoidance(snake)
        final_direction += wall_avoidance * 1.0  # Base weight
        
        # 5. Random exploration if no other stimulus
        if final_direction.length_squared() < 0.1:
            final_direction = BasicBehavior.calculate_random_movement(snake)
        
        # Normalize and return
        if final_direction.length_squared() > 0:
            final_direction.normalize_ip()
            
        return final_direction
    
    @staticmethod
    def calculate_threat_avoidance(snake, threats):
        """Calculate direction to avoid threats"""
        avoidance_vector = Vector2(0, 0)
        
        for threat in threats:
            # Vector from threat to snake (direction to flee)
            flee_direction = snake.head_position - threat.head_position
            if flee_direction.length_squared() > 0:
                # Closer threats have more influence
                distance = flee_direction.length()
                flee_direction.normalize_ip()
                # Inverse relationship: closer = stronger avoidance
                strength = THREAT_AVOIDANCE_DISTANCE / max(distance, 1)
                avoidance_vector += flee_direction * strength
                
        return avoidance_vector
    
    @staticmethod
    def calculate_prey_pursuit(snake, prey):
        """Calculate direction to pursue prey"""
        if not prey:
            return Vector2(0, 0)
            
        # Target the closest prey
        closest_prey = min(prey, key=lambda p: snake.head_position.distance_to(p.head_position))
        
        # Vector from snake to prey
        pursuit_direction = closest_prey.head_position - snake.head_position
        
        if pursuit_direction.length_squared() > 0:
            pursuit_direction.normalize_ip()
            
        return pursuit_direction
    
    @staticmethod
    def calculate_food_seeking(snake, food):
        """Calculate direction to seek food"""
        if not food:
            return Vector2(0, 0)
            
        # Vector from snake to food
        food_direction = food.position - snake.head_position
        
        if food_direction.length_squared() > 0:
            food_direction.normalize_ip()
            
        return food_direction
    
    @staticmethod
    def calculate_wall_avoidance(snake):
        """Calculate direction to avoid walls"""
        avoidance = Vector2(0, 0)
        pos = snake.head_position
        
        # Check distance to each wall
        dist_to_left = pos.x
        dist_to_right = SCREEN_WIDTH - pos.x
        dist_to_top = pos.y
        dist_to_bottom = SCREEN_HEIGHT - pos.y
        
        # Apply avoidance force if too close to walls
        if dist_to_left < WALL_AVOIDANCE_DISTANCE:
            avoidance.x += (WALL_AVOIDANCE_DISTANCE - dist_to_left) / WALL_AVOIDANCE_DISTANCE
            
        if dist_to_right < WALL_AVOIDANCE_DISTANCE:
            avoidance.x -= (WALL_AVOIDANCE_DISTANCE - dist_to_right) / WALL_AVOIDANCE_DISTANCE
            
        if dist_to_top < WALL_AVOIDANCE_DISTANCE:
            avoidance.y += (WALL_AVOIDANCE_DISTANCE - dist_to_top) / WALL_AVOIDANCE_DISTANCE
            
        if dist_to_bottom < WALL_AVOIDANCE_DISTANCE:
            avoidance.y -= (WALL_AVOIDANCE_DISTANCE - dist_to_bottom) / WALL_AVOIDANCE_DISTANCE
            
        return avoidance * PROACTIVE_AVOIDANCE_STRENGTH
    
    @staticmethod
    def calculate_random_movement(snake):
        """Calculate random movement direction"""
        # Use snake's current velocity as a basis for momentum
        if snake.velocity.length_squared() > 0:
            # Add some randomness to current direction
            current_dir = snake.velocity.normalize()
            random_offset = Vector2(
                random.uniform(-0.3, 0.3),
                random.uniform(-0.3, 0.3)
            )
            return current_dir + random_offset
        else:
            # Completely random direction
            return Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )
