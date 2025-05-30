# food_effects.py: Handles temporary effects from special food
import time
from settings import *

class FoodEffect:
    """Base class for food effects"""
    
    def __init__(self, duration):
        self.start_time = time.time()
        self.duration = duration
        self.is_active = True
        self.effect_type = "base"
        
    def is_expired(self):
        """Check if effect has expired"""
        return time.time() - self.start_time > self.duration
        
    def apply_effect(self, snake):
        """Apply effect to snake - override in subclasses"""
        pass
        
    def remove_effect(self, snake):
        """Remove effect from snake - override in subclasses"""
        pass

class SpeedBoostEffect(FoodEffect):
    """Speed boost effect from speed food"""
    
    def __init__(self):
        super().__init__(SPEED_FOOD_DURATION)
        self.effect_type = "speed_boost"
        self.speed_multiplier = SPEED_FOOD_BOOST_MULTIPLIER
        self.accel_multiplier = SPEED_FOOD_ACCEL_MULTIPLIER
        
    def apply_effect(self, snake):
        """Apply speed boost to snake"""
        if not hasattr(snake, '_original_speed_values'):
            snake._original_speed_values = {
                'max_speed': snake.max_speed,
                'acceleration_rate': snake.acceleration_rate
            }
            
        snake.max_speed = snake._original_speed_values['max_speed'] * self.speed_multiplier
        snake.acceleration_rate = snake._original_speed_values['acceleration_rate'] * self.accel_multiplier
        
    def remove_effect(self, snake):
        """Remove speed boost from snake"""
        if hasattr(snake, '_original_speed_values'):
            snake.max_speed = snake._original_speed_values['max_speed']
            snake.acceleration_rate = snake._original_speed_values['acceleration_rate']
            delattr(snake, '_original_speed_values')

class SlowEffect(FoodEffect):
    """Slow effect from slow food"""
    
    def __init__(self):
        super().__init__(SLOW_FOOD_DURATION)
        self.effect_type = "slow"
        self.speed_multiplier = SLOW_FOOD_REDUCTION_MULTIPLIER
        
    def apply_effect(self, snake):
        """Apply slow effect to snake"""
        if not hasattr(snake, '_original_slow_speed'):
            snake._original_slow_speed = snake.max_speed
            
        snake.max_speed = snake._original_slow_speed * self.speed_multiplier
        
    def remove_effect(self, snake):
        """Remove slow effect from snake"""
        if hasattr(snake, '_original_slow_speed'):
            snake.max_speed = snake._original_slow_speed
            delattr(snake, '_original_slow_speed')

class ImmunityEffect(FoodEffect):
    """Immunity effect from immunity food"""
    
    def __init__(self):
        super().__init__(IMMUNITY_FOOD_DURATION)
        self.effect_type = "immunity"
        
    def apply_effect(self, snake):
        """Apply immunity to snake"""
        snake.is_immune = True
        
    def remove_effect(self, snake):
        """Remove immunity from snake"""
        snake.is_immune = False

class FoodEffectsManager:
    """Manages all active food effects on snakes"""
    
    def __init__(self):
        self.active_effects = {}  # snake_id -> list of effects
        
    def apply_food_effect(self, snake, food_type):
        """Apply appropriate effect based on food type"""
        if food_type == "normal":
            return  # No special effect
            
        snake_id = snake.id
        
        # Initialize effects list for snake if needed
        if snake_id not in self.active_effects:
            self.active_effects[snake_id] = []
            
        # Create appropriate effect
        effect = None
        if food_type == "speed" and ENABLE_SPEED_FOOD:
            effect = SpeedBoostEffect()
            
        elif food_type == "slow" and ENABLE_SLOW_FOOD:
            effect = SlowEffect()
            
        elif food_type == "immunity" and ENABLE_IMMUNITY_FOOD:
            effect = ImmunityEffect()
            
        elif food_type == "growth" and ENABLE_GROWTH_FOOD:
            # Instant effect - no duration needed
            snake.grow(GROWTH_FOOD_SIZE_BONUS, reason="ate growth food")
            print(f"Snake {snake_id} grew by {GROWTH_FOOD_SIZE_BONUS} segments from growth food!")
            return
            
        elif food_type == "shrink" and ENABLE_SHRINK_FOOD:
            # Instant effect - no duration needed
            old_size = snake.size
            snake.size = max(SHRINK_FOOD_MIN_SIZE, snake.size - SHRINK_FOOD_SIZE_REDUCTION)
            
            # Adjust body segments if snake shrunk
            if snake.size < old_size:
                segments_to_remove = old_size - snake.size
                for _ in range(segments_to_remove):
                    if len(snake.body_segments) > snake.size:
                        snake.body_segments.pop()
                        
                snake.update_dynamic_properties()
                print(f"Snake {snake_id} shrunk from {old_size} to {snake.size} segments!")
            return
            
        # Add effect to snake if it was created
        if effect:
            # Remove any existing effects of the same type
            self.active_effects[snake_id] = [
                e for e in self.active_effects[snake_id] 
                if e.effect_type != effect.effect_type
            ]
            
            # Add new effect
            self.active_effects[snake_id].append(effect)
            effect.apply_effect(snake)
            print(f"Snake {snake_id} gained {effect.effect_type} effect for {effect.duration}s")
            
    def update_effects(self, snakes):
        """Update all active effects and remove expired ones"""
        for snake in snakes:
            if snake.is_dead:
                # Clean up effects for dead snakes
                if snake.id in self.active_effects:
                    del self.active_effects[snake.id]
                continue
                
            snake_id = snake.id
            if snake_id not in self.active_effects:
                continue
                
            # Update effects for this snake
            for effect in self.active_effects[snake_id][:]:
                if effect.is_expired():
                    # Remove expired effect
                    effect.remove_effect(snake)
                    self.active_effects[snake_id].remove(effect)
                    print(f"Snake {snake_id} {effect.effect_type} effect expired")
                    
            # Remove empty effect lists
            if not self.active_effects[snake_id]:
                del self.active_effects[snake_id]
                
    def get_snake_effects(self, snake_id):
        """Get list of active effects for a snake"""
        return self.active_effects.get(snake_id, [])
        
    def clear_snake_effects(self, snake):
        """Clear all effects from a snake (useful when snake dies)"""
        snake_id = snake.id
        if snake_id in self.active_effects:
            # Remove all effects
            for effect in self.active_effects[snake_id]:
                effect.remove_effect(snake)
            del self.active_effects[snake_id]
            
    def get_effect_counts(self):
        """Get counts of active effects for stats"""
        counts = {
            'speed_boost': 0,
            'slow': 0,
            'immunity': 0,
            'total_effects': 0
        }
        
        for snake_effects in self.active_effects.values():
            for effect in snake_effects:
                if effect.effect_type in counts:
                    counts[effect.effect_type] += 1
                counts['total_effects'] += 1
                
        return counts
