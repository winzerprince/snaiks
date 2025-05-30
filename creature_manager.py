# creature_manager.py: Modular system for managing different creature types
import time
import random
from settings import *
from pygame.math import Vector2

# Import creature classes conditionally based on settings
if ENABLE_RIPPERS:
    from ripper import Ripper
if ENABLE_SCAVENGERS:
    from scavenger import Scavenger

class CreatureManager:
    """Manages all non-snake creatures in the game"""
    
    def __init__(self):
        # Creature lists - always initialize as lists, but only populate if enabled
        self.rippers = []
        self.scavengers = []
        self.guardians = []
        
        # Timing for creature spawning
        self.last_ripper_check_time = time.time()
        self.last_scavenger_check_time = time.time()
        self.last_guardian_check_time = time.time()
        
        print(f"CreatureManager initialized:")
        print(f"  - Rippers: {'Enabled' if ENABLE_RIPPERS else 'Disabled'}")
        print(f"  - Scavengers: {'Enabled' if ENABLE_SCAVENGERS else 'Disabled'}")
        print(f"  - Guardians: {'Enabled' if ENABLE_GUARDIANS else 'Disabled'}")

    def update(self, snakes, food_items):
        """Update all active creature types"""
        current_time = time.time()
        
        # Update rippers if enabled
        if ENABLE_RIPPERS:
            self._update_rippers(snakes, current_time)
        
        # Update scavengers if enabled
        if ENABLE_SCAVENGERS:
            self._update_scavengers(snakes, food_items, current_time)
        
        # Future: Update guardians if enabled
        if ENABLE_GUARDIANS:
            self._update_guardians(snakes, current_time)

    def _update_rippers(self, snakes, current_time):
        """Update ripper entities"""
        # Calculate hunter population percentage
        alive_snakes = [s for s in snakes if not s.is_dead]
        hunters = [s for s in alive_snakes if s.is_hunter]
        hunter_percentage = len(hunters) / len(alive_snakes) if alive_snakes else 0
        
        # Spawn rippers when hunter population exceeds threshold
        if (hunter_percentage >= HUNTER_POPULATION_THRESHOLD and 
            len(self.rippers) < MAX_RIPPERS_ON_SCREEN and 
            current_time - self.last_ripper_check_time > RIPPER_SPAWN_INTERVAL):
            self._spawn_ripper()
            self.last_ripper_check_time = current_time
        
        # Update rippers and handle collisions
        for ripper in self.rippers[:]:
            if ripper.is_dead:
                self.rippers.remove(ripper)
            else:
                ripper.update(hunters)
                
                # Check for ripper-hunter collisions
                for hunter in hunters[:]:
                    if ripper.check_collision_with_hunter(hunter):
                        hunter.die(reason="killed by ripper")
                        print(f"Ripper {ripper.id} eliminated hunter snake")
        
        # Remove rippers if hunter population drops significantly
        if hunter_percentage < HUNTER_POPULATION_THRESHOLD * 0.7:  # 70% of threshold
            for ripper in self.rippers[:]:
                if hasattr(ripper, 'despawn_timer'):
                    if current_time - ripper.despawn_timer > RIPPER_DESPAWN_DELAY:
                        ripper.die("hunter population decreased")
                        self.rippers.remove(ripper)
                else:
                    ripper.despawn_timer = current_time

    def _update_scavengers(self, snakes, food_items, current_time):
        """Update scavenger entities"""
        # Spawn scavengers when there's abundant food
        if (len(food_items) >= FOOD_ABUNDANCE_THRESHOLD and 
            len(self.scavengers) < MAX_SCAVENGERS_ON_SCREEN and 
            current_time - self.last_scavenger_check_time > SCAVENGER_SPAWN_INTERVAL):
            self._spawn_scavenger()
            self.last_scavenger_check_time = current_time
        
        # Update scavengers and handle food competition
        for scavenger in self.scavengers[:]:
            if scavenger.is_dead:
                self.scavengers.remove(scavenger)
            else:
                scavenger.update(food_items)
                
                # Check for scavenger-food collisions
                for food in food_items[:]:
                    if scavenger.check_collision_with_food(food):
                        scavenger.eat_food()
                        food_items.remove(food)  # Scavenger steals the food
                        print(f"Scavenger {scavenger.id} stole food from snakes!")

    def _update_guardians(self, snakes, current_time):
        """Update guardian entities - placeholder for future implementation"""
        # TODO: Implement guardian logic
        # Guardians might protect smaller snakes from hunters
        pass

    def _spawn_ripper(self):
        """Spawn a new ripper at a random position"""
        if not ENABLE_RIPPERS:
            return
            
        # Generate random spawn position away from edges
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Create new ripper instance
        new_ripper = Ripper(x, y)
        self.rippers.append(new_ripper)
        print(f"Ripper {new_ripper.id} spawned at ({x}, {y}) - Hunter population too high!")

    def _spawn_scavenger(self):
        """Spawn a new scavenger at a random position"""
        if not ENABLE_SCAVENGERS:
            return
            
        # Generate random spawn position away from edges
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Create new scavenger instance
        new_scavenger = Scavenger(x, y)
        self.scavengers.append(new_scavenger)
        print(f"Scavenger {new_scavenger.id} spawned at ({x}, {y}) - Abundant food detected!")

    def draw(self, screen):
        """Draw all active creatures"""
        # Draw rippers
        if ENABLE_RIPPERS:
            for ripper in self.rippers:
                ripper.draw(screen)
        
        # Draw scavengers
        if ENABLE_SCAVENGERS:
            for scavenger in self.scavengers:
                scavenger.draw(screen)
        
        # Future: Draw guardians
        if ENABLE_GUARDIANS:
            for guardian in self.guardians:
                guardian.draw(screen)

    def get_creature_counts(self):
        """Get counts of all active creatures for stats"""
        counts = {}
        
        if ENABLE_RIPPERS:
            counts['rippers'] = len([r for r in self.rippers if not r.is_dead])
        else:
            counts['rippers'] = 0
            
        if ENABLE_SCAVENGERS:
            counts['scavengers'] = len([s for s in self.scavengers if not s.is_dead])
        else:
            counts['scavengers'] = 0
            
        if ENABLE_GUARDIANS:
            counts['guardians'] = len([g for g in self.guardians if not g.is_dead])
        else:
            counts['guardians'] = 0
            
        return counts

    def get_all_creatures(self):
        """Get all creature instances for external processing"""
        creatures = []
        
        if ENABLE_RIPPERS:
            creatures.extend(self.rippers)
        if ENABLE_SCAVENGERS:
            creatures.extend(self.scavengers)
        if ENABLE_GUARDIANS:
            creatures.extend(self.guardians)
            
        return creatures
