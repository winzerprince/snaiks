# game_manager.py: Handles game logic, spawning, collisions, state
import pygame
import random
import time
from settings import *
from snake import Snake
from pygame.math import Vector2
from basic_behavior import BasicBehavior
from resource_manager import ResourceManager
from creature_manager import CreatureManager

class GameManager:
    def __init__(self):
        self.snakes = []
        self.food_items = []
        self.score = 0
        self.game_over = False
        self.winner = None
        self.last_food_spawn_time = time.time()
        self.last_snake_spawn_time = time.time()
        
        # Resource management
        self.resource_manager = ResourceManager()
        
        # Creature management - modular system
        self.creature_manager = CreatureManager()
        
        # Performance tracking
        self.frame_count = 0
        self.last_performance_update = time.time()
        
        # Spawn initial food items
        self.spawn_initial_food()

    def update(self):
        """Update game state, including snakes and food."""
        self.resource_manager.start_frame()
        
        # Update snakes with AI behavior
        for snake in self.snakes[:]:  # Use slice copy to allow safe removal
            if snake.is_dead:
                continue
                
            # Calculate basic behavior direction for snake
            ai_direction = BasicBehavior.calculate_direction(snake, self.food_items, self.snakes)
            
            # Move snake with AI direction
            snake.move(ai_direction)
        
        # Update spatial grid for efficient collision detection
        self.resource_manager.update_spatial_grid(self.snakes, self.food_items)
        
        # Check for collisions and update game state
        self.check_collisions()
        
        # Clean up dead snakes periodically
        if self.resource_manager.should_cleanup():
            self.cleanup_dead_snakes()

        # Spawn food if needed - spawn multiple at once to reach target
        if len(self.food_items) < MAX_FOOD_ON_SCREEN:
            if time.time() - self.last_food_spawn_time > FOOD_SPAWN_INTERVAL:
                # Spawn multiple food items to quickly reach the target
                food_to_spawn = min(5, MAX_FOOD_ON_SCREEN - len(self.food_items))
                for _ in range(food_to_spawn):
                    self.spawn_food()
                self.last_food_spawn_time = time.time()

        # Spawn new snakes if needed
        if len(self.snakes) < MAX_SNAKES_ON_SCREEN and time.time() - self.last_snake_spawn_time > random.uniform(SNAKE_SPAWN_INTERVAL_MIN, SNAKE_SPAWN_INTERVAL_MAX):
            self.spawn_snake()
            self.last_snake_spawn_time = time.time()
        
        # Update creatures using the modular creature manager
        self.creature_manager.update(self.snakes, self.food_items)
        
        self.resource_manager.mark_update_complete()
        
        # Print performance stats occasionally
        self.frame_count += 1
        if self.frame_count % 300 == 0:  # Every 5 seconds at 60 FPS
            self.print_performance_stats()

    def check_collisions(self):
        """Check for collisions between snakes and food, and snake-to-snake collisions."""
        # Food collisions
        for snake in self.snakes:
            if snake.is_dead:
                continue
                
            for food in self.food_items[:]:  # Use slice copy for safe removal
                if snake.head_position.distance_to(food.position) < (SNAKE_SEGMENT_RADIUS + food.radius):
                    snake.grow()
                    self.food_items.remove(food)
                    self.resource_manager.return_food_to_pool(food)
        
        # Snake-to-snake collisions (hunter eating smaller snakes)
        for hunter in self.snakes:
            if not hunter.is_hunter or hunter.is_dead:
                continue
                
            for prey in self.snakes:
                if prey == hunter or prey.is_dead:
                    continue
                
                # Hunter can eat smaller snakes
                if (prey.size < hunter.size - FEAR_MARGIN and
                    hunter.head_position.distance_to(prey.head_position) < SNAKE_SEGMENT_RADIUS * 2):
                    
                    # Hunter grows by 1/3 of prey's size
                    growth_amount = max(1, prey.size // 3)
                    hunter.grow(growth_amount, reason="ate snake")
                    prey.die(reason="eaten by hunter")
                    break  # Hunter can only eat one snake per frame

    def spawn_food(self):
        """Spawn a new food item using object pool."""
        food = self.resource_manager.get_food_from_pool()
        self.food_items.append(food)
    
    def spawn_initial_food(self):
        """Spawn initial food items to populate the screen"""
        for _ in range(MAX_FOOD_ON_SCREEN):
            self.spawn_food()

    def spawn_snake(self):
        """Spawn a new snake at a random position with random color."""
        # Generate random position
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)

        # Generate random color variation for visual diversity
        color_variation = (
            random.randint(-20, 20),
            random.randint(-20, 20),
            random.randint(-20, 20)
        )

        # Create base color - either use normal snake color or a random variation
        if random.random() < 0.8:  # 80% chance of normal color
            base_color = NORMAL_SNAKE_BODY_COLOR
        else:
            # Generate a completely random color
            base_color = (
                random.randint(50, 200),
                random.randint(50, 200),
                random.randint(50, 200)
            )

        # Apply variation to the base color
        color = (
            max(0, min(255, base_color[0] + color_variation[0])),
            max(0, min(255, base_color[1] + color_variation[1])),
            max(0, min(255, base_color[2] + color_variation[2]))
        )

        # Create and add the snake
        new_snake = Snake(x, y, color)

        # Give random initial direction
        direction = Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        )
        if direction.length_squared() > 0:
            direction.normalize_ip()
            new_snake.move(direction)

        self.snakes.append(new_snake)
    
    def cleanup_dead_snakes(self):
        """Remove dead snakes that have been dead for a while"""
        current_time = time.time()
        
        # Remove snakes that have been dead for more than 3 seconds
        self.snakes = [snake for snake in self.snakes 
                      if not snake.is_dead or (current_time - getattr(snake, 'death_time', current_time)) < 3.0]
    
    def print_performance_stats(self):
        """Print performance statistics to console"""
        stats = self.resource_manager.get_performance_stats()
        creature_counts = self.creature_manager.get_creature_counts()
        
        print(f"FPS: {stats.get('fps', 0):.1f}, "
              f"Snakes: {len([s for s in self.snakes if not s.is_dead])}, "
              f"Food: {len(self.food_items)}, "
              f"Rippers: {creature_counts.get('rippers', 0)}, "
              f"Scavengers: {creature_counts.get('scavengers', 0)}, "
              f"Update: {stats.get('update_time_ms', 0):.1f}ms")

    def draw(self, screen):
        """Draw all game elements on the screen."""
        # Draw food items
        for food in self.food_items:
            food.draw(screen)

        # Draw snakes
        for snake in self.snakes:
            snake.draw(screen)

        # Draw creatures using the modular creature manager
        self.creature_manager.draw(screen)
        
        self.resource_manager.mark_draw_complete()
