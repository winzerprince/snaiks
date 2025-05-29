# game_manager.py: Handles game logic, spawning, collisions, state
import pygame
import random
import time
import logging # For logging within the class
from settings import *
from snake import Snake
from food import Food
from pygame.math import Vector2
from ml.agent import SnakeAgent
import os

class GameManager:
    def __init__(self, logger):
        self.logger = logger
        self.snakes = []
        self.food_items = []
        self.score = 0 # Or track per snake
        self.game_over = False
        self.winner = None
        self.last_food_spawn_time = time.time()
        self.last_snake_spawn_time = time.time()
        self.next_snake_spawn_delay = random.uniform(SNAKE_SPAWN_INTERVAL_MIN, SNAKE_SPAWN_INTERVAL_MAX)

        # Load ML model if it exists
        model_path = "trained_snake_model.joblib"
        self.ml_agent = None
        if os.path.exists(model_path):
            try:
                self.ml_agent = SnakeAgent(model_path)
                self.logger.info(f"Loaded ML model from {model_path}", extra={'snake_id': 'SYSTEM'})
            except Exception as e:
                self.logger.error(f"Failed to load ML model: {e}", extra={'snake_id': 'SYSTEM'})

        # Initial food
        for _ in range(MAX_FOOD_ON_SCREEN // 2):
            self.spawn_food()

        # Initial snake
        self.spawn_snake()

    def spawn_food(self):
        """Create and add a new food item to the game."""
        if len(self.food_items) < MAX_FOOD_ON_SCREEN:
            self.food_items.append(Food())

    def spawn_snake(self, is_ai_controlled=None):
        """Create and add a new snake to the game."""
        if len(self.snakes) < MAX_SNAKES_ON_SCREEN:
            x = random.randint(SNAKE_SEGMENT_RADIUS * INITIAL_SNAKE_LENGTH, SCREEN_WIDTH - SNAKE_SEGMENT_RADIUS * INITIAL_SNAKE_LENGTH)
            y = random.randint(SNAKE_SEGMENT_RADIUS * INITIAL_SNAKE_LENGTH, SCREEN_HEIGHT - SNAKE_SEGMENT_RADIUS * INITIAL_SNAKE_LENGTH)
            random_body_color = (random.randint(50,150), random.randint(100,200), random.randint(50,150))
            # Pass self.logger to the Snake constructor
            new_snake = Snake(x, y, self.logger, color=random_body_color)

            # Set AI control flag based on parameter or randomly if model exists
            if is_ai_controlled is None:
                is_ai_controlled = self.ml_agent is not None and random.random() < 0.7  # 70% chance if model exists

            new_snake.is_ai_controlled = is_ai_controlled

            self.snakes.append(new_snake)
            # Updated log message to include AI status
            self.logger.info(f"Spawned new {'AI-controlled' if is_ai_controlled else 'random'} snake {new_snake.id} at ({x:.1f},{y:.1f}). Total snakes: {len(self.snakes)}", extra={'snake_id': 'SYSTEM'})

    def update(self):
        """Update game state, including snake movement and collisions."""
        if self.game_over:
            return

        # Spawn new food
        current_time = time.time()
        if current_time - self.last_food_spawn_time > FOOD_SPAWN_INTERVAL and len(self.food_items) < MAX_FOOD_ON_SCREEN:
            self.spawn_food()
            self.last_food_spawn_time = current_time

        # Randomly spawn new snakes over time
        if current_time - self.last_snake_spawn_time > self.next_snake_spawn_delay and len(self.snakes) < MAX_SNAKES_ON_SCREEN:
            self.spawn_snake()
            self.last_snake_spawn_time = current_time
            self.next_snake_spawn_delay = random.uniform(SNAKE_SPAWN_INTERVAL_MIN, SNAKE_SPAWN_INTERVAL_MAX)

        # Update snakes
        for snake in self.snakes:
            if snake.is_dead:
                continue

            # --- Awareness: Find nearest food ---
            nearest_food = None
            min_food_dist = float('inf')
            for food in self.food_items:
                dist = (snake.head_position - food.position).length()
                if dist < min_food_dist:
                    min_food_dist = dist
                    nearest_food = food

            # --- Awareness: Find nearest hunter snake (excluding self) ---
            nearest_hunter = None
            min_hunter_dist = float('inf')
            for other in self.snakes:
                if other is snake or other.is_dead or not other.is_hunter:
                    continue
                dist = (snake.head_position - other.head_position).length()
                if dist < min_hunter_dist:
                    min_hunter_dist = dist
                    nearest_hunter = other

            # --- Awareness: Find nearest prey snake (for hunters) ---
            nearest_prey = None
            min_prey_dist = float('inf')
            if snake.is_hunter:  # Only hunters look for prey
                for other in self.snakes:
                    if other is snake or other.is_dead:
                        continue
                    # Only target snakes that are smaller by at least 1 unit
                    if other.size < snake.size:
                        dist = (snake.head_position - other.head_position).length()
                        if dist < min_prey_dist:
                            min_prey_dist = dist
                            nearest_prey = other

            # --- Awareness: Find nearest threat (larger hunter) ---
            nearest_threat = None
            min_threat_dist = float('inf')
            for other in self.snakes:
                if other is snake or other.is_dead:
                    continue
                # Feared if other is hunter and larger by FEAR_MARGIN or more
                if other.is_hunter and other.size >= snake.size + FEAR_MARGIN:
                    dist = (snake.head_position - other.head_position).length()
                    if dist < min_threat_dist:
                        min_threat_dist = dist
                        nearest_threat = other

            # --- Direction to nearest food ---
            if nearest_food:
                direction_to_food = (nearest_food.position - snake.head_position)
            else:
                direction_to_food = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

            # Determine the move direction
            move_direction = None

            # Use ML model for AI-controlled snakes if available
            if hasattr(snake, 'is_ai_controlled') and snake.is_ai_controlled and self.ml_agent is not None:
                try:
                    # Prepare features for ML model
                    current_dir = (0, 0)
                    if snake.velocity.length_squared() > 0:
                        norm_vel = snake.velocity.normalize()
                        current_dir = (norm_vel.x, norm_vel.y)

                    food_dist = (0, 0)
                    if nearest_food:
                        food_dist = (nearest_food.position.x - snake.head_position.x,
                                      nearest_food.position.y - snake.head_position.y)

                    wall_dist = (
                        snake.head_position.y,                     # Distance to top wall
                        SCREEN_WIDTH - snake.head_position.x,      # Distance to right wall
                        SCREEN_HEIGHT - snake.head_position.y,     # Distance to bottom wall
                        snake.head_position.x                      # Distance to left wall
                    )

                    self_dist = 100.0  # Placeholder

                    hunter_dist = 9999.0
                    hunter_vec = (0, 0)
                    if nearest_hunter:
                        hunter_vec = (nearest_hunter.head_position.x - snake.head_position.x,
                                       nearest_hunter.head_position.y - snake.head_position.y)
                        hunter_dist = (hunter_vec[0] ** 2 + hunter_vec[1] ** 2) ** 0.5

                    # Collect all features in the format expected by the model
                    features = [
                        current_dir[0], current_dir[1],
                        food_dist[0], food_dist[1],
                        wall_dist[0], wall_dist[1], wall_dist[2], wall_dist[3],
                        self_dist,
                        hunter_dist, hunter_vec[0], hunter_vec[1]
                    ]

                    # Get model prediction
                    action = self.ml_agent.predict(features)
                    self.logger.debug(f"AI snake {snake.id} chose action: {action}", extra=snake.log_extra)

                    # Convert action to direction
                    if action == "UP":
                        move_direction = Vector2(0, -1)
                    elif action == "RIGHT":
                        move_direction = Vector2(1, 0)
                    elif action == "DOWN":
                        move_direction = Vector2(0, 1)
                    elif action == "LEFT":
                        move_direction = Vector2(-1, 0)
                    else:
                        # Fallback if prediction is invalid
                        self.logger.warning(f"Invalid ML prediction: {action} for snake {snake.id}", extra=snake.log_extra)
                        move_direction = None

                except Exception as e:
                    self.logger.error(f"Error using ML model for snake {snake.id}: {e}", extra=snake.log_extra)
                    move_direction = None

            # If no valid ML direction or not AI-controlled, use traditional logic
            if move_direction is None:
                # --- Determine movement direction based on snake status ---
                if snake.is_hunter:
                    # Hunter behavior: prioritize hunting smaller snakes if available
                    if nearest_prey and min_prey_dist < 200:
                        direction_to_prey = (nearest_prey.head_position - snake.head_position)
                        move_direction = direction_to_prey
                        # Still be cautious of much larger snakes
                        if nearest_threat and min_threat_dist < 150:
                            direction_away_threat = (snake.head_position - nearest_threat.head_position)
                            # Blend: hunt prey but avoid threats
                            move_direction = direction_to_prey + direction_away_threat * 1.5
                    else:
                        # No prey nearby, fallback to food seeking
                        move_direction = direction_to_food
                        # Still avoid larger threats
                        if nearest_threat and min_threat_dist < 150:
                            direction_away_threat = (snake.head_position - nearest_threat.head_position)
                            move_direction = direction_to_food + direction_away_threat * 1.5
                else:
                    # Normal snake behavior: avoid hunters
                    if nearest_hunter and min_hunter_dist < 200:
                        # Move away from hunter if close
                        direction_away_hunter = (snake.head_position - nearest_hunter.head_position)
                        # Combine: move towards food, but away from hunter
                        move_direction = direction_to_food + direction_away_hunter * 2
                    else:
                        move_direction = direction_to_food

            # --- Move snake with awareness ---
            snake.move(
                move_direction,
                nearest_food=nearest_food.position if nearest_food else None,
                nearest_hunter=nearest_hunter.head_position if nearest_hunter else None,
                min_food_dist=min_food_dist,
                min_hunter_dist=min_hunter_dist
            )

            # Check collision with food
            for food in self.food_items:
                distance = (snake.head_position - food.position).length()
                if distance < (SNAKE_SEGMENT_RADIUS + FOOD_RADIUS):
                    snake.grow(amount=1, reason="ate food")
                    self.logger.info(
                        f"Snake {snake.id} ate food at ({food.position.x},{food.position.y}) | FoodDist:{min_food_dist:.1f} | HunterDist:{min_hunter_dist:.1f}",
                        extra=snake.log_extra
                    )
                    self.food_items.remove(food)
                    self.spawn_food()
                    break

            # Check hunter snake collisions with smaller snakes
            if snake.is_hunter:
                for other in self.snakes:
                    if other is snake or other.is_dead or other.size >= snake.size:
                        continue

                    # Check for collision with other snake's head
                    head_distance = (snake.head_position - other.head_position).length()
                    if head_distance < (SNAKE_SEGMENT_RADIUS * 2):
                        # Hunter snake consumed smaller snake
                        growth_amount = max(1, other.size // 3)  # Grow by 1/3 of the prey's size
                        snake.grow(amount=growth_amount, reason=f"ate snake {other.id}")
                        self.logger.info(
                            f"Hunter snake {snake.id} consumed snake {other.id} | Size gain: {growth_amount}",
                            extra=snake.log_extra
                        )
                        other.die(reason=f"eaten by hunter snake {snake.id}")
                        break

                    # Check for collision with any body segment of the other snake
                    for segment_pos in other.body_segments:
                        segment_distance = (snake.head_position - segment_pos).length()
                        if segment_distance < (SNAKE_SEGMENT_RADIUS * 2):
                            # Hunter snake consumed smaller snake by hitting its body
                            growth_amount = max(1, other.size // 3)  # Grow by 1/3 of the prey's size
                            snake.grow(amount=growth_amount, reason=f"ate snake {other.id} body")
                            self.logger.info(
                                f"Hunter snake {snake.id} consumed snake {other.id} by hitting its body | Size gain: {growth_amount}",
                                extra=snake.log_extra
                            )
                            other.die(reason=f"body eaten by hunter snake {snake.id}")
                            break

                    # If the other snake is already dead from body collision, break the outer loop too
                    if other.is_dead:
                        break

        # Remove dead snakes
        self.snakes = [s for s in self.snakes if not s.is_dead]

    def draw(self, screen):
        """Draw all game elements to the screen."""
        # Draw food
        for food in self.food_items:
            food.draw(screen)

        # Draw snakes
        for snake in self.snakes:
            snake.draw(screen)
