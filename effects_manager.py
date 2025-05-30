# effects_manager.py: Manages all environmental effects in the game
import time
import random
from settings import *
from pygame.math import Vector2

# Import effect classes conditionally based on settings
if ENABLE_EFFECTS:
    from environmental_effect import BlackHoleEffect, SpeedZoneEffect, FoodMagnetEffect

class EffectsManager:
    """Manages all environmental effects in the game"""
    
    def __init__(self):
        # Effect lists - always initialize as lists, but only populate if enabled
        self.black_holes = []
        self.speed_zones = []
        self.food_magnets = []
        
        # Timing for effect spawning
        self.last_black_hole_spawn_time = time.time()
        self.last_speed_zone_spawn_time = time.time()
        self.last_food_magnet_spawn_time = time.time()
        
        print(f"EffectsManager initialized:")
        print(f"  - Environmental Effects: {'Enabled' if ENABLE_EFFECTS else 'Disabled'}")
        if ENABLE_EFFECTS:
            print(f"  - Black Holes: {'Enabled' if ENABLE_BLACK_HOLES else 'Disabled'}")
            print(f"  - Speed Zones: {'Enabled' if ENABLE_SPEED_ZONES else 'Disabled'}")
            print(f"  - Food Magnets: {'Enabled' if ENABLE_FOOD_MAGNETS else 'Disabled'}")

    def update(self, snakes, food_items, creatures):
        """Update all active environmental effects"""
        if not ENABLE_EFFECTS:
            return
            
        current_time = time.time()
        
        # Update black holes if enabled
        if ENABLE_BLACK_HOLES:
            self._update_black_holes(snakes, food_items, creatures, current_time)
        
        # Update speed zones if enabled
        if ENABLE_SPEED_ZONES:
            self._update_speed_zones(snakes, food_items, creatures, current_time)
        
        # Update food magnets if enabled
        if ENABLE_FOOD_MAGNETS:
            self._update_food_magnets(snakes, food_items, creatures, current_time)

    def _update_black_holes(self, snakes, food_items, creatures, current_time):
        """Update black hole effects"""
        # Spawn new black holes periodically
        if (len(self.black_holes) < MAX_BLACK_HOLES and 
            current_time - self.last_black_hole_spawn_time > BLACK_HOLE_SPAWN_INTERVAL):
            self._spawn_black_hole()
            self.last_black_hole_spawn_time = current_time
        
        # Update existing black holes and remove expired ones
        for black_hole in self.black_holes[:]:
            if black_hole.is_expired():
                self.black_holes.remove(black_hole)
                print(f"Black hole {black_hole.id} expired")
            else:
                black_hole.update(snakes, food_items, creatures)

    def _update_speed_zones(self, snakes, food_items, creatures, current_time):
        """Update speed zone effects"""
        # Spawn new speed zones periodically
        if (len(self.speed_zones) < MAX_SPEED_ZONES and 
            current_time - self.last_speed_zone_spawn_time > SPEED_ZONE_SPAWN_INTERVAL):
            self._spawn_speed_zone()
            self.last_speed_zone_spawn_time = current_time
        
        # Update existing speed zones and remove expired ones
        for speed_zone in self.speed_zones[:]:
            if speed_zone.is_expired():
                # Restore original speeds for affected entities
                self._restore_entity_speeds(snakes, creatures)
                self.speed_zones.remove(speed_zone)
                print(f"Speed zone {speed_zone.id} expired")
            else:
                speed_zone.update(snakes, food_items, creatures)

    def _update_food_magnets(self, snakes, food_items, creatures, current_time):
        """Update food magnet effects"""
        # Spawn new food magnets periodically
        if (len(self.food_magnets) < MAX_FOOD_MAGNETS and 
            current_time - self.last_food_magnet_spawn_time > FOOD_MAGNET_SPAWN_INTERVAL):
            self._spawn_food_magnet()
            self.last_food_magnet_spawn_time = current_time
        
        # Update existing food magnets and remove expired ones
        for food_magnet in self.food_magnets[:]:
            if food_magnet.is_expired():
                self.food_magnets.remove(food_magnet)
                print(f"Food magnet {food_magnet.id} expired")
            else:
                food_magnet.update(snakes, food_items, creatures)

    def _spawn_black_hole(self):
        """Spawn a new black hole at a valid position"""
        if not ENABLE_EFFECTS or not ENABLE_BLACK_HOLES:
            return
            
        # Try to find a good position that doesn't overlap with existing black holes
        for attempt in range(10):  # Max 10 attempts
            x = random.randint(BLACK_HOLE_RADIUS + 50, SCREEN_WIDTH - BLACK_HOLE_RADIUS - 50)
            y = random.randint(BLACK_HOLE_RADIUS + 50, SCREEN_HEIGHT - BLACK_HOLE_RADIUS - 50)
            
            # Check if position is valid (not too close to other black holes)
            position_valid = True
            for existing_hole in self.black_holes:
                distance = (Vector2(x, y) - existing_hole.position).length()
                if distance < BLACK_HOLE_MIN_DISTANCE:
                    position_valid = False
                    break
            
            if position_valid:
                new_black_hole = BlackHoleEffect(x, y)
                self.black_holes.append(new_black_hole)
                print(f"Black hole {new_black_hole.id} spawned at ({x}, {y})")
                return
        
        print("Failed to find valid position for black hole after 10 attempts")

    def _spawn_speed_zone(self):
        """Spawn a new speed zone at a random position"""
        if not ENABLE_EFFECTS or not ENABLE_SPEED_ZONES:
            return
            
        # Generate random spawn position
        x = random.randint(SPEED_ZONE_RADIUS + 30, SCREEN_WIDTH - SPEED_ZONE_RADIUS - 30)
        y = random.randint(SPEED_ZONE_RADIUS + 30, SCREEN_HEIGHT - SPEED_ZONE_RADIUS - 30)
        
        # Randomly choose between fast and slow zone
        is_fast_zone = random.choice([True, False])
        
        new_speed_zone = SpeedZoneEffect(x, y, is_fast_zone)
        self.speed_zones.append(new_speed_zone)
        zone_type = "speed boost" if is_fast_zone else "slow"
        print(f"Speed zone {new_speed_zone.id} ({zone_type}) spawned at ({x}, {y})")

    def _spawn_food_magnet(self):
        """Spawn a new food magnet at a random position"""
        if not ENABLE_EFFECTS or not ENABLE_FOOD_MAGNETS:
            return
            
        # Generate random spawn position
        x = random.randint(FOOD_MAGNET_RADIUS + 40, SCREEN_WIDTH - FOOD_MAGNET_RADIUS - 40)
        y = random.randint(FOOD_MAGNET_RADIUS + 40, SCREEN_HEIGHT - FOOD_MAGNET_RADIUS - 40)
        
        new_food_magnet = FoodMagnetEffect(x, y)
        self.food_magnets.append(new_food_magnet)
        print(f"Food magnet {new_food_magnet.id} spawned at ({x}, {y})")

    def _restore_entity_speeds(self, snakes, creatures):
        """Restore original speeds for all entities when speed zones expire"""
        # Restore snake speeds
        for snake in snakes:
            if hasattr(snake, '_original_max_speed'):
                snake.max_speed = snake._original_max_speed
                delattr(snake, '_original_max_speed')
        
        # Restore creature speeds
        all_creatures = []
        if hasattr(creatures, 'get_all_creatures'):
            all_creatures = creatures.get_all_creatures()
            
        for creature in all_creatures:
            if hasattr(creature, '_original_max_speed'):
                creature.max_speed = creature._original_max_speed
                delattr(creature, '_original_max_speed')

    def draw(self, screen):
        """Draw all active environmental effects"""
        if not ENABLE_EFFECTS:
            return
        
        # Draw black holes
        if ENABLE_BLACK_HOLES:
            for black_hole in self.black_holes:
                black_hole.draw(screen)
        
        # Draw speed zones
        if ENABLE_SPEED_ZONES:
            for speed_zone in self.speed_zones:
                speed_zone.draw(screen)
        
        # Draw food magnets
        if ENABLE_FOOD_MAGNETS:
            for food_magnet in self.food_magnets:
                food_magnet.draw(screen)

    def get_effect_counts(self):
        """Get counts of all active effects for stats"""
        counts = {}
        
        if ENABLE_EFFECTS:
            counts['black_holes'] = len([bh for bh in self.black_holes if bh.is_active])
            counts['speed_zones'] = len([sz for sz in self.speed_zones if sz.is_active])
            counts['food_magnets'] = len([fm for fm in self.food_magnets if fm.is_active])
        else:
            counts['black_holes'] = 0
            counts['speed_zones'] = 0
            counts['food_magnets'] = 0
            
        return counts

    def get_all_effects(self):
        """Get all effect instances for external processing"""
        effects = []
        
        if ENABLE_EFFECTS:
            if ENABLE_BLACK_HOLES:
                effects.extend(self.black_holes)
            if ENABLE_SPEED_ZONES:
                effects.extend(self.speed_zones)
            if ENABLE_FOOD_MAGNETS:
                effects.extend(self.food_magnets)
                
        return effects

    def clear_all_effects(self):
        """Clear all active effects (useful for cleanup or reset)"""
        self.black_holes.clear()
        self.speed_zones.clear()
        self.food_magnets.clear()
        print("All environmental effects cleared")

    def force_spawn_effect(self, effect_type, x=None, y=None):
        """Force spawn a specific effect type at given coordinates (for testing)"""
        if not ENABLE_EFFECTS:
            print("Environmental effects are disabled")
            return
            
        if x is None:
            x = random.randint(100, SCREEN_WIDTH - 100)
        if y is None:
            y = random.randint(100, SCREEN_HEIGHT - 100)
            
        if effect_type == "black_hole" and ENABLE_BLACK_HOLES:
            new_effect = BlackHoleEffect(x, y)
            self.black_holes.append(new_effect)
            print(f"Force spawned black hole at ({x}, {y})")
        elif effect_type == "speed_zone" and ENABLE_SPEED_ZONES:
            is_fast = random.choice([True, False])
            new_effect = SpeedZoneEffect(x, y, is_fast)
            self.speed_zones.append(new_effect)
            print(f"Force spawned speed zone at ({x}, {y})")
        elif effect_type == "food_magnet" and ENABLE_FOOD_MAGNETS:
            new_effect = FoodMagnetEffect(x, y)
            self.food_magnets.append(new_effect)
            print(f"Force spawned food magnet at ({x}, {y})")
        else:
            print(f"Cannot spawn effect type '{effect_type}' - disabled or invalid")
