# food.py: Defines the Food class and special food types
import pygame
import random
import time
import math
from settings import *
from pygame.math import Vector2

class Food:
    def __init__(self, food_type="normal"):
        self.position = Vector2(random.randint(FOOD_RADIUS, SCREEN_WIDTH - FOOD_RADIUS),
                                random.randint(FOOD_RADIUS, SCREEN_HEIGHT - FOOD_RADIUS))
        self.radius = FOOD_RADIUS
        self.food_type = food_type
        self.creation_time = time.time()
        
        # Set properties based on food type
        self._setup_food_properties()
        
    def _setup_food_properties(self):
        """Setup visual and effect properties based on food type"""
        if self.food_type == "normal":
            self.color = FOOD_COLOR
            self.effect_description = "Basic nutrition"
            
        elif self.food_type == "speed":
            self.color = SPEED_FOOD_COLOR
            self.effect_description = f"Speed boost x{SPEED_FOOD_BOOST_MULTIPLIER} for {SPEED_FOOD_DURATION}s"
            
        elif self.food_type == "slow":
            self.color = SLOW_FOOD_COLOR  
            self.effect_description = f"Speed reduction x{SLOW_FOOD_REDUCTION_MULTIPLIER} for {SLOW_FOOD_DURATION}s"
            
        elif self.food_type == "immunity":
            self.color = IMMUNITY_FOOD_COLOR
            self.effect_description = f"Immunity from hunters for {IMMUNITY_FOOD_DURATION}s"
            
        elif self.food_type == "growth":
            self.color = GROWTH_FOOD_COLOR
            self.effect_description = f"Instant growth +{GROWTH_FOOD_SIZE_BONUS} segments"
            
        elif self.food_type == "shrink":
            self.color = SHRINK_FOOD_COLOR
            self.effect_description = f"Size reduction -{SHRINK_FOOD_SIZE_REDUCTION} segments"
            
        else:
            # Fallback to normal food
            self.color = FOOD_COLOR
            self.effect_description = "Basic nutrition"

    def draw(self, screen):
        """Draw the food with special effects for different types"""
        age = time.time() - self.creation_time
        
        if self.food_type == "normal":
            # Simple circle for normal food
            pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
            
        elif self.food_type == "speed":
            # Pulsing cyan food with speed lines
            pulse = 0.8 + 0.2 * math.sin(age * 8)
            radius = int(self.radius * pulse)
            pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), radius)
            
            # Speed lines around the food
            for i in range(4):
                angle = age * 10 + i * 90
                line_length = self.radius + 5
                end_x = self.position.x + line_length * math.cos(math.radians(angle))
                end_y = self.position.y + line_length * math.sin(math.radians(angle))
                pygame.draw.line(screen, self.color, 
                               (int(self.position.x), int(self.position.y)),
                               (int(end_x), int(end_y)), 2)
                               
        elif self.food_type == "slow":
            # Purple food with concentric circles
            for i in range(3):
                alpha = int(100 - i * 30)
                radius = self.radius + i * 3
                slow_color = (*self.color, alpha)
                slow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(slow_surface, slow_color, (radius, radius), radius)
                screen.blit(slow_surface, (self.position.x - radius, self.position.y - radius))
                
        elif self.food_type == "immunity":
            # Gold food with shimmering effect
            shimmer = int(200 + 55 * math.sin(age * 6))
            shimmer_color = (shimmer, shimmer - 50, 0)
            pygame.draw.circle(screen, shimmer_color, (int(self.position.x), int(self.position.y)), self.radius)
            
            # Golden aura
            aura_radius = self.radius + 3
            aura_alpha = int(80 + 40 * math.sin(age * 4))
            aura_color = (255, 215, 0, aura_alpha)
            aura_surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, aura_color, (aura_radius, aura_radius), aura_radius)
            screen.blit(aura_surface, (self.position.x - aura_radius, self.position.y - aura_radius))
            
        elif self.food_type == "growth":
            # Orange food with expanding rings
            pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)
            
            # Expanding rings
            for i in range(2):
                ring_phase = (age * 3 + i * 1.5) % 3
                ring_radius = self.radius + ring_phase * 8
                ring_alpha = int(100 * (1 - ring_phase / 3))
                if ring_alpha > 0:
                    ring_color = (*self.color, ring_alpha)
                    ring_surface = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(ring_surface, ring_color, (int(ring_radius), int(ring_radius)), int(ring_radius), 2)
                    screen.blit(ring_surface, (self.position.x - ring_radius, self.position.y - ring_radius))
                    
        elif self.food_type == "shrink":
            # Pink food with contracting effect
            contraction = 0.9 + 0.1 * math.sin(age * 10)
            radius = int(self.radius * contraction)
            pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), radius)
            
            # Contracting particles
            for i in range(6):
                angle = age * 15 + i * 60
                particle_distance = self.radius + 8 - (age * 2) % 16
                particle_x = self.position.x + particle_distance * math.cos(math.radians(angle))
                particle_y = self.position.y + particle_distance * math.sin(math.radians(angle))
                pygame.draw.circle(screen, self.color, (int(particle_x), int(particle_y)), 2)

def create_food(force_type=None):
    """Factory function to create food with appropriate type"""
    if not ENABLE_SPECIAL_FOOD or force_type == "normal":
        return Food("normal")
    
    if force_type:
        return Food(force_type)
    
    # Random chance for special food
    if random.random() < SPECIAL_FOOD_SPAWN_CHANCE:
        # Choose random special food type from enabled types
        available_types = []
        
        if ENABLE_SPEED_FOOD:
            available_types.append("speed")
        if ENABLE_SLOW_FOOD:
            available_types.append("slow")
        if ENABLE_IMMUNITY_FOOD:
            available_types.append("immunity")
        if ENABLE_GROWTH_FOOD:
            available_types.append("growth")
        if ENABLE_SHRINK_FOOD:
            available_types.append("shrink")
            
        if available_types:
            food_type = random.choice(available_types)
            return Food(food_type)
    
    # Default to normal food
    return Food("normal")


