# environmental_effect.py: Base class for environmental effects
import pygame
from pygame.math import Vector2
from settings import *
import time
import uuid

class EnvironmentalEffect:
    """Base class for all environmental effects"""
    
    def __init__(self, x, y, lifetime=10.0):
        self.id = str(uuid.uuid4())[:8]  # Unique ID for each effect
        self.position = Vector2(x, y)
        self.creation_time = time.time()
        self.lifetime = lifetime
        self.is_active = True
        self.effect_type = "base"
        
    def update(self, snakes, food_items, creatures):
        """Update effect - override in subclasses"""
        # Check if effect should expire
        if time.time() - self.creation_time > self.lifetime:
            self.is_active = False
            
    def apply_effect(self, entities):
        """Apply effect to entities - override in subclasses"""
        pass
        
    def draw(self, screen):
        """Draw effect - override in subclasses"""
        pass
        
    def is_expired(self):
        """Check if effect has expired"""
        return not self.is_active or (time.time() - self.creation_time > self.lifetime)

class BlackHoleEffect(EnvironmentalEffect):
    """Black hole that pulls entities toward its center"""
    
    def __init__(self, x, y):
        super().__init__(x, y, BLACK_HOLE_LIFETIME)
        self.effect_type = "black_hole"
        self.radius = BLACK_HOLE_RADIUS
        self.pull_radius = BLACK_HOLE_PULL_RADIUS
        self.pull_strength = BLACK_HOLE_PULL_STRENGTH
        
        # Visual effects
        self.rotation = 0.0
        self.pulse_phase = 0.0
        
    def update(self, snakes, food_items, creatures):
        """Update black hole and apply gravitational effects"""
        super().update(snakes, food_items, creatures)
        
        if not self.is_active:
            return
            
        # Update visual effects
        self.rotation += 5.0  # Rotation speed
        self.pulse_phase += 0.2
        
        # Apply gravitational pull to snakes
        for snake in snakes:
            if snake.is_dead:
                continue
            self._apply_gravitational_pull(snake)
            
        # Apply gravitational pull to food items
        for food in food_items:
            self._apply_gravitational_pull_to_food(food)
            
        # Apply gravitational pull to creatures
        all_creatures = []
        if hasattr(creatures, 'get_all_creatures'):
            all_creatures = creatures.get_all_creatures()
        elif hasattr(creatures, 'rippers'):
            all_creatures.extend(creatures.rippers)
        elif hasattr(creatures, 'scavengers'):
            all_creatures.extend(creatures.scavengers)
            
        for creature in all_creatures:
            if hasattr(creature, 'is_dead') and creature.is_dead:
                continue
            self._apply_gravitational_pull(creature)
    
    def _apply_gravitational_pull(self, entity):
        """Apply gravitational pull to an entity (snake or creature)"""
        # Calculate distance to black hole
        distance_vector = self.position - entity.head_position if hasattr(entity, 'head_position') else self.position - entity.position
        distance = distance_vector.length()
        
        # Only apply effect if within pull radius
        if distance < self.pull_radius and distance > 5:  # Avoid division by zero
            # Calculate pull force (stronger when closer)
            pull_force = self.pull_strength * (self.pull_radius - distance) / self.pull_radius
            
            # Normalize direction vector
            pull_direction = distance_vector.normalize()
            
            # Apply pull to entity's velocity
            if hasattr(entity, 'velocity'):
                entity.velocity += pull_direction * pull_force * 0.3  # Dampen effect
                
    def _apply_gravitational_pull_to_food(self, food):
        """Apply gravitational pull to food items"""
        distance_vector = self.position - food.position
        distance = distance_vector.length()
        
        # Only apply effect if within pull radius
        if distance < self.pull_radius and distance > 5:
            # Calculate pull force
            pull_force = self.pull_strength * (self.pull_radius - distance) / self.pull_radius
            
            # Normalize direction vector
            pull_direction = distance_vector.normalize()
            
            # Move food toward black hole
            food.position += pull_direction * pull_force * 0.1
    
    def draw(self, screen):
        """Draw the black hole with visual effects"""
        if not self.is_active:
            return
            
        import math
        
        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)  # Fade out over time
        
        # Draw gravitational field (faint outer ring)
        field_alpha = int(30 * age_factor)
        field_color = (50, 0, 50, field_alpha)
        field_surface = pygame.Surface((self.pull_radius * 2, self.pull_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(field_surface, field_color, 
                          (self.pull_radius, self.pull_radius), 
                          self.pull_radius, 2)
        screen.blit(field_surface, 
                   (self.position.x - self.pull_radius, self.position.y - self.pull_radius))
        
        # Draw main black hole body
        main_radius = int(self.radius * age_factor)
        if main_radius > 0:
            # Pulsing dark center
            pulse = int(50 + 30 * math.sin(self.pulse_phase))
            center_color = (pulse, 0, pulse)
            pygame.draw.circle(screen, center_color, 
                             (int(self.position.x), int(self.position.y)), 
                             main_radius)
            
            # Darker inner circle
            inner_radius = int(main_radius * 0.7)
            pygame.draw.circle(screen, (20, 0, 20), 
                             (int(self.position.x), int(self.position.y)), 
                             inner_radius)
            
            # Rotating accretion disk effect
            for i in range(8):
                angle = self.rotation + i * 45
                ring_radius = main_radius + 10 + i * 3
                ring_x = self.position.x + ring_radius * math.cos(math.radians(angle))
                ring_y = self.position.y + ring_radius * math.sin(math.radians(angle))
                
                ring_alpha = int(100 * age_factor * (8 - i) / 8)
                ring_color = (ring_alpha, 0, ring_alpha // 2)
                
                if ring_alpha > 0:
                    pygame.draw.circle(screen, ring_color, 
                                     (int(ring_x), int(ring_y)), 3)

class SpeedZoneEffect(EnvironmentalEffect):
    """Zone that modifies movement speed of entities within it"""
    
    def __init__(self, x, y, is_fast_zone=True):
        super().__init__(x, y, SPEED_ZONE_LIFETIME)
        self.effect_type = "speed_zone"
        self.radius = SPEED_ZONE_RADIUS
        self.is_fast_zone = is_fast_zone
        self.speed_multiplier = SPEED_ZONE_FAST_MULTIPLIER if is_fast_zone else SPEED_ZONE_SLOW_MULTIPLIER
        
        # Visual effects
        self.pulse_phase = 0.0
        
    def update(self, snakes, food_items, creatures):
        """Update speed zone effects"""
        super().update(snakes, food_items, creatures)
        
        if not self.is_active:
            return
            
        self.pulse_phase += 0.1
        
        # Apply speed effects to snakes
        for snake in snakes:
            if snake.is_dead:
                continue
            self._apply_speed_effect(snake)
            
        # Apply speed effects to creatures
        all_creatures = []
        if hasattr(creatures, 'get_all_creatures'):
            all_creatures = creatures.get_all_creatures()
            
        for creature in all_creatures:
            if hasattr(creature, 'is_dead') and creature.is_dead:
                continue
            self._apply_speed_effect(creature)
    
    def _apply_speed_effect(self, entity):
        """Apply speed modification to entity if within zone"""
        entity_pos = entity.head_position if hasattr(entity, 'head_position') else entity.position
        distance = (self.position - entity_pos).length()
        
        if distance < self.radius:
            # Temporarily modify entity's max speed
            if hasattr(entity, 'max_speed'):
                # Store original speed if not already stored
                if not hasattr(entity, '_original_max_speed'):
                    entity._original_max_speed = entity.max_speed
                    
                entity.max_speed = entity._original_max_speed * self.speed_multiplier
        else:
            # Restore original speed when outside zone
            if hasattr(entity, '_original_max_speed'):
                entity.max_speed = entity._original_max_speed
                delattr(entity, '_original_max_speed')
    
    def draw(self, screen):
        """Draw the speed zone with visual effects"""
        if not self.is_active:
            return
            
        import math
        
        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)
        
        # Pulsing effect
        pulse = 0.5 + 0.3 * math.sin(self.pulse_phase)
        
        # Different colors for fast vs slow zones
        if self.is_fast_zone:
            base_color = (0, 255, 100)  # Green for speed boost
        else:
            base_color = (255, 100, 0)  # Orange for speed reduction
            
        # Draw zone boundary
        alpha = int(80 * age_factor * pulse)
        zone_color = (*base_color, alpha)
        zone_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(zone_surface, zone_color, 
                          (self.radius, self.radius), 
                          self.radius, 3)
        screen.blit(zone_surface, 
                   (self.position.x - self.radius, self.position.y - self.radius))
        
        # Draw center indicator
        center_radius = int(8 * pulse)
        pygame.draw.circle(screen, base_color, 
                         (int(self.position.x), int(self.position.y)), 
                         center_radius)

class FoodMagnetEffect(EnvironmentalEffect):
    """Effect that attracts food items to a central point"""
    
    def __init__(self, x, y):
        super().__init__(x, y, FOOD_MAGNET_LIFETIME)
        self.effect_type = "food_magnet"
        self.radius = FOOD_MAGNET_RADIUS
        self.pull_radius = FOOD_MAGNET_PULL_RADIUS
        self.pull_strength = FOOD_MAGNET_PULL_STRENGTH
        
        # Visual effects
        self.pulse_phase = 0.0
        
    def update(self, snakes, food_items, creatures):
        """Update food magnet and attract food"""
        super().update(snakes, food_items, creatures)
        
        if not self.is_active:
            return
            
        self.pulse_phase += 0.15
        
        # Apply attraction to food items
        for food in food_items:
            self._attract_food(food)
    
    def _attract_food(self, food):
        """Attract food item toward magnet center"""
        distance_vector = self.position - food.position
        distance = distance_vector.length()
        
        # Only apply effect if within pull radius
        if distance < self.pull_radius and distance > 10:  # Keep some minimum distance
            # Calculate attraction force
            attraction_force = self.pull_strength * (self.pull_radius - distance) / self.pull_radius
            
            # Normalize direction vector
            pull_direction = distance_vector.normalize()
            
            # Move food toward magnet
            food.position += pull_direction * attraction_force * 0.2
    
    def draw(self, screen):
        """Draw the food magnet with visual effects"""
        if not self.is_active:
            return
            
        import math
        
        # Calculate age-based effects
        age = time.time() - self.creation_time
        age_factor = max(0, 1.0 - age / self.lifetime)
        
        # Pulsing effect
        pulse = 0.6 + 0.4 * math.sin(self.pulse_phase)
        
        # Draw attraction field
        field_alpha = int(40 * age_factor * pulse)
        field_color = (255, 200, 0, field_alpha)
        field_surface = pygame.Surface((self.pull_radius * 2, self.pull_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(field_surface, field_color, 
                          (self.pull_radius, self.pull_radius), 
                          self.pull_radius, 2)
        screen.blit(field_surface, 
                   (self.position.x - self.pull_radius, self.position.y - self.pull_radius))
        
        # Draw magnet core
        core_radius = int(self.radius * age_factor * pulse)
        if core_radius > 0:
            pygame.draw.circle(screen, (255, 200, 0), 
                             (int(self.position.x), int(self.position.y)), 
                             core_radius)
            
            # Inner sparkle effect
            inner_radius = int(core_radius * 0.5)
            pygame.draw.circle(screen, (255, 255, 150), 
                             (int(self.position.x), int(self.position.y)), 
                             inner_radius)
