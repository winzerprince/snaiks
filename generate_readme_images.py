#!/usr/bin/env python3
"""
Generate images for README documentation of all game effects and systems.
This script creates visual representations of various game features.
"""

import pygame
import math
import os
from pygame.math import Vector2
from settings import *

# Initialize pygame
pygame.init()

# Create assets directory if it doesn't exist
ASSETS_DIR = "assets"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

def create_surface(width=400, height=300, bg_color=(20, 30, 40)):
    """Create a surface with the game's background color"""
    surface = pygame.Surface((width, height))
    surface.fill(bg_color)
    return surface

def draw_snake(surface, segments, body_color, head_color, segment_radius=8):
    """Draw a snake on the surface"""
    for i, segment in enumerate(segments):
        if i == 0:  # Head
            pygame.draw.circle(surface, head_color, (int(segment.x), int(segment.y)), segment_radius)
            # Inner circle for detail
            pygame.draw.circle(surface, (min(255, head_color[0]+30), min(255, head_color[1]+30), min(255, head_color[2]+30)), 
                             (int(segment.x), int(segment.y)), segment_radius - 3)
        else:  # Body
            pygame.draw.circle(surface, body_color, (int(segment.x), int(segment.y)), segment_radius)
            # Inner circle for detail
            inner_color = (max(0, body_color[0]-30), max(0, body_color[1]-30), max(0, body_color[2]-30))
            pygame.draw.circle(surface, inner_color, (int(segment.x), int(segment.y)), segment_radius - 3)

def draw_food(surface, pos, color, radius=7):
    """Draw food item"""
    pygame.draw.circle(surface, color, (int(pos.x), int(pos.y)), radius)
    # Inner highlight
    highlight_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
    pygame.draw.circle(surface, highlight_color, (int(pos.x - 2), int(pos.y - 2)), radius - 3)

def generate_snake_types_image():
    """Generate image showing different snake types"""
    surface = create_surface(600, 400)
    
    # Normal snake
    normal_segments = [Vector2(100, 100), Vector2(92, 100), Vector2(84, 100), Vector2(76, 100)]
    draw_snake(surface, normal_segments, NORMAL_SNAKE_BODY_COLOR, NORMAL_SNAKE_HEAD_COLOR)
    
    # Hunter snake
    hunter_segments = [Vector2(100, 200), Vector2(92, 200), Vector2(84, 200), Vector2(76, 200), Vector2(68, 200)]
    draw_snake(surface, hunter_segments, HUNTER_SNAKE_BODY_COLOR, HUNTER_SNAKE_HEAD_COLOR)
    
    # Starving snake (pulsing effect approximation)
    starving_segments = [Vector2(100, 300), Vector2(92, 300), Vector2(84, 300)]
    starving_color = (200, 200, 0)  # Yellow for starving
    draw_snake(surface, starving_segments, starving_color, (255, 255, 0))
    
    # Add labels
    font = pygame.font.Font(None, 36)
    
    # Normal snake label
    text = font.render("Normal Snake", True, (255, 255, 255))
    surface.blit(text, (150, 90))
    
    # Hunter snake label
    text = font.render("Hunter Snake (10+ food eaten)", True, (255, 255, 255))
    surface.blit(text, (150, 190))
    
    # Starving snake label
    text = font.render("Starving Snake (8+ seconds without food)", True, (255, 255, 255))
    surface.blit(text, (150, 290))
    
    # Add description
    desc_font = pygame.font.Font(None, 24)
    descriptions = [
        "• Seeks food, avoids hunters",
        "• Can hunt smaller snakes",
        "• Pulsing yellow warning"
    ]
    
    for i, desc in enumerate(descriptions):
        text = desc_font.render(desc, True, (200, 200, 200))
        surface.blit(text, (150, 110 + i * 100))
    
    pygame.image.save(surface, f"{ASSETS_DIR}/snake_types.png")
    print("Generated: snake_types.png")

def generate_special_food_image():
    """Generate image showing all special food types"""
    surface = create_surface(800, 500)
    
    # Food positions and types
    foods = [
        (Vector2(100, 100), SPEED_FOOD_COLOR, "Speed Boost", "Cyan - 2.5x speed for 6s"),
        (Vector2(300, 100), SLOW_FOOD_COLOR, "Slow Effect", "Purple - 0.4x speed for 10s"),
        (Vector2(500, 100), IMMUNITY_FOOD_COLOR, "Immunity", "Gold - 5s immunity from hunters"),
        (Vector2(100, 300), GROWTH_FOOD_COLOR, "Growth", "Orange - Instant +3 size"),
        (Vector2(300, 300), SHRINK_FOOD_COLOR, "Shrink", "Pink - Reduces size by 2"),
        (Vector2(500, 300), FOOD_COLOR, "Normal Food", "Red - +1 size")
    ]
    
    font = pygame.font.Font(None, 28)
    desc_font = pygame.font.Font(None, 20)
    
    for pos, color, name, description in foods:
        # Draw food with pulsing effect
        base_radius = 12
        pulse_radius = base_radius + int(3 * math.sin(pygame.time.get_ticks() * 0.01))
        draw_food(surface, pos, color, pulse_radius)
        
        # Add name
        text = font.render(name, True, (255, 255, 255))
        surface.blit(text, (pos.x - 40, pos.y + 30))
        
        # Add description
        desc_text = desc_font.render(description, True, (200, 200, 200))
        surface.blit(text, (pos.x - 60, pos.y + 55))
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Special Food Types", True, (255, 255, 255))
    surface.blit(title, (250, 20))
    
    pygame.image.save(surface, f"{ASSETS_DIR}/special_food_types.png")
    print("Generated: special_food_types.png")

def generate_visual_effects_image():
    """Generate image showing visual effects on snakes"""
    surface = create_surface(800, 600)
    
    # Speed boost snake with cyan tint and speed lines
    speed_segments = [Vector2(150, 100), Vector2(142, 100), Vector2(134, 100), Vector2(126, 100)]
    speed_color = (100, 255, 255)  # Cyan tint
    draw_snake(surface, speed_segments, speed_color, (150, 255, 255))
    
    # Draw speed lines around head
    head_pos = speed_segments[0]
    for i in range(6):
        angle = i * 60
        line_length = 25
        end_x = head_pos.x + line_length * math.cos(math.radians(angle))
        end_y = head_pos.y + line_length * math.sin(math.radians(angle))
        pygame.draw.line(surface, (0, 255, 255), (head_pos.x, head_pos.y), (end_x, end_y), 3)
    
    # Immunity snake with golden aura
    immunity_segments = [Vector2(150, 250), Vector2(142, 250), Vector2(134, 250), Vector2(126, 250)]
    draw_snake(surface, immunity_segments, NORMAL_SNAKE_BODY_COLOR, (255, 215, 0))
    
    # Draw golden aura
    aura_radius = 35
    aura_color = (255, 215, 0, 100)
    aura_surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(aura_surface, aura_color, (aura_radius, aura_radius), aura_radius, 4)
    surface.blit(aura_surface, (immunity_segments[0].x - aura_radius, immunity_segments[0].y - aura_radius))
    
    # Slow snake with purple tint
    slow_segments = [Vector2(150, 400), Vector2(142, 400), Vector2(134, 400), Vector2(126, 400)]
    slow_color = (150, 50, 150)  # Purple tint
    draw_snake(surface, slow_segments, slow_color, (180, 80, 180))
    
    # Add labels
    font = pygame.font.Font(None, 32)
    labels = [
        ("Speed Boost Effect", 250, 90),
        ("Immunity Effect", 250, 240),
        ("Slow Effect", 250, 390)
    ]
    
    for label, x, y in labels:
        text = font.render(label, True, (255, 255, 255))
        surface.blit(text, (x, y))
    
    # Add descriptions
    desc_font = pygame.font.Font(None, 24)
    descriptions = [
        ("Cyan tint + rotating speed lines", 250, 120),
        ("Golden head + pulsing aura", 250, 270),
        ("Purple tint on body and head", 250, 420)
    ]
    
    for desc, x, y in descriptions:
        text = desc_font.render(desc, True, (200, 200, 200))
        surface.blit(text, (x, y))
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Visual Effects System", True, (255, 255, 255))
    surface.blit(title, (200, 20))
    
    pygame.image.save(surface, f"{ASSETS_DIR}/visual_effects.png")
    print("Generated: visual_effects.png")

def generate_environmental_effects_image():
    """Generate image showing environmental effects"""
    surface = create_surface(800, 600)
    
    # Black hole effect
    black_hole_pos = Vector2(150, 150)
    
    # Draw black hole (dark center with swirling effect)
    pygame.draw.circle(surface, (10, 10, 10), (int(black_hole_pos.x), int(black_hole_pos.y)), 30)
    pygame.draw.circle(surface, (50, 0, 50), (int(black_hole_pos.x), int(black_hole_pos.y)), 40, 5)
    pygame.draw.circle(surface, (100, 0, 100), (int(black_hole_pos.x), int(black_hole_pos.y)), 60, 3)
    
    # Draw snake being pulled
    snake_pos = Vector2(220, 120)
    pull_segments = [snake_pos, snake_pos + Vector2(-8, 0), snake_pos + Vector2(-16, 0)]
    draw_snake(surface, pull_segments, NORMAL_SNAKE_BODY_COLOR, NORMAL_SNAKE_HEAD_COLOR, 6)
    
    # Draw pull effect lines
    for i in range(5):
        start_x = snake_pos.x + i * 10
        start_y = snake_pos.y + i * 5
        end_x = black_hole_pos.x + 20
        end_y = black_hole_pos.y - 10
        pygame.draw.line(surface, (150, 50, 150), (start_x, start_y), (end_x, end_y), 2)
    
    # Speed zone (fast)
    speed_zone_pos = Vector2(500, 150)
    pygame.draw.circle(surface, (0, 255, 0, 50), (int(speed_zone_pos.x), int(speed_zone_pos.y)), 80, 5)
    pygame.draw.circle(surface, (0, 200, 0), (int(speed_zone_pos.x), int(speed_zone_pos.y)), 70, 3)
    
    # Snake in speed zone
    fast_snake_pos = Vector2(500, 150)
    fast_segments = [fast_snake_pos, fast_snake_pos + Vector2(-8, 0), fast_snake_pos + Vector2(-16, 0)]
    draw_snake(surface, fast_segments, (100, 255, 100), (150, 255, 150), 6)
    
    # Food magnet
    magnet_pos = Vector2(150, 400)
    pygame.draw.circle(surface, (255, 100, 0), (int(magnet_pos.x), int(magnet_pos.y)), 20)
    pygame.draw.circle(surface, (255, 150, 50), (int(magnet_pos.x), int(magnet_pos.y)), 40, 3)
    
    # Food being attracted
    food_pos = Vector2(220, 370)
    draw_food(surface, food_pos, FOOD_COLOR, 6)
    
    # Attraction lines
    for i in range(3):
        start_x = food_pos.x - i * 5
        start_y = food_pos.y + i * 3
        end_x = magnet_pos.x + 15
        end_y = magnet_pos.y - 5
        pygame.draw.line(surface, (255, 200, 100), (start_x, start_y), (end_x, end_y), 2)
    
    # Labels
    font = pygame.font.Font(None, 32)
    labels = [
        ("Black Hole", 50, 250),
        ("Speed Zone", 450, 250),
        ("Food Magnet", 50, 500)
    ]
    
    for label, x, y in labels:
        text = font.render(label, True, (255, 255, 255))
        surface.blit(text, (x, y))
    
    # Descriptions
    desc_font = pygame.font.Font(None, 24)
    descriptions = [
        ("Pulls nearby entities", 50, 280),
        ("2x speed boost inside", 450, 280),
        ("Attracts food items", 50, 530)
    ]
    
    for desc, x, y in descriptions:
        text = desc_font.render(desc, True, (200, 200, 200))
        surface.blit(text, (x, y))
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Environmental Effects", True, (255, 255, 255))
    surface.blit(title, (200, 20))
    
    pygame.image.save(surface, f"{ASSETS_DIR}/environmental_effects.png")
    print("Generated: environmental_effects.png")

def generate_creatures_image():
    """Generate image showing special creatures"""
    surface = create_surface(800, 500)
    
    # Ripper creature
    ripper_pos = Vector2(150, 150)
    ripper_color = (200, 0, 200)  # Purple
    pygame.draw.circle(surface, ripper_color, (int(ripper_pos.x), int(ripper_pos.y)), 15)
    # Spikes around ripper
    for i in range(8):
        angle = i * 45
        spike_length = 20
        end_x = ripper_pos.x + spike_length * math.cos(math.radians(angle))
        end_y = ripper_pos.y + spike_length * math.sin(math.radians(angle))
        pygame.draw.line(surface, ripper_color, (ripper_pos.x, ripper_pos.y), (end_x, end_y), 3)
    
    # Hunter snake being chased
    hunter_segments = [Vector2(250, 130), Vector2(242, 130), Vector2(234, 130), Vector2(226, 130)]
    draw_snake(surface, hunter_segments, HUNTER_SNAKE_BODY_COLOR, HUNTER_SNAKE_HEAD_COLOR, 8)
    
    # Chase line
    pygame.draw.line(surface, (255, 100, 100), (ripper_pos.x + 15, ripper_pos.y), (hunter_segments[0].x - 8, hunter_segments[0].y), 3)
    
    # Scavenger creature
    scavenger_pos = Vector2(150, 350)
    scavenger_color = (150, 75, 0)  # Brown
    pygame.draw.circle(surface, scavenger_color, (int(scavenger_pos.x), int(scavenger_pos.y)), 12)
    # Body segments
    for i in range(3):
        segment_pos = Vector2(scavenger_pos.x - (i + 1) * 10, scavenger_pos.y)
        pygame.draw.circle(surface, scavenger_color, (int(segment_pos.x), int(segment_pos.y)), 10 - i * 2)
    
    # Food being stolen
    food_pos = Vector2(220, 350)
    draw_food(surface, food_pos, FOOD_COLOR, 7)
    
    # Steal line
    pygame.draw.line(surface, (255, 200, 0), (scavenger_pos.x + 12, scavenger_pos.y), (food_pos.x - 7, food_pos.y), 3)
    
    # Labels
    font = pygame.font.Font(None, 32)
    labels = [
        ("Ripper", 300, 120),
        ("Scavenger", 300, 320)
    ]
    
    for label, x, y in labels:
        text = font.render(label, True, (255, 255, 255))
        surface.blit(text, (x, y))
    
    # Descriptions
    desc_font = pygame.font.Font(None, 24)
    descriptions = [
        ("Hunts hunter snakes when population > 50%", 300, 150),
        ("Spawns when 10+ food items present", 300, 180),
        ("Steals food from snakes", 300, 350),
        ("Competes for resources", 300, 380)
    ]
    
    for desc, x, y in descriptions:
        text = desc_font.render(desc, True, (200, 200, 200))
        surface.blit(text, (x, y))
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Special Creatures", True, (255, 255, 255))
    surface.blit(title, (250, 20))
    
    pygame.image.save(surface, f"{ASSETS_DIR}/special_creatures.png")
    print("Generated: special_creatures.png")

def generate_ai_behavior_image():
    """Generate image showing AI decision making"""
    surface = create_surface(800, 600)
    
    # Create a simple decision tree visualization
    font = pygame.font.Font(None, 24)
    
    # Decision nodes
    decisions = [
        ("Is Hunter?", 400, 100),
        ("Nearby smaller snake?", 250, 200),
        ("Larger threat nearby?", 450, 200),
        ("HUNT", 150, 300),
        ("EVALUATE RISK", 350, 300),
        ("SEEK FOOD", 550, 300),
        ("Hunter approaching?", 600, 200),
        ("FLEE", 700, 300)
    ]
    
    # Draw decision tree
    for i, (text, x, y) in enumerate(decisions):
        if i < 3 or i == 6:  # Decision nodes
            pygame.draw.rect(surface, (100, 100, 200), (x - 60, y - 15, 120, 30))
            pygame.draw.rect(surface, (255, 255, 255), (x - 60, y - 15, 120, 30), 2)
        else:  # Action nodes
            pygame.draw.ellipse(surface, (200, 100, 100), (x - 60, y - 15, 120, 30))
            pygame.draw.ellipse(surface, (255, 255, 255), (x - 60, y - 15, 120, 30), 2)
        
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, text_rect)
    
    # Draw connections
    connections = [
        ((400, 115), (250, 185)),  # Is Hunter -> Nearby smaller
        ((400, 115), (600, 185)),  # Is Hunter -> Hunter approaching
        ((250, 215), (150, 285)),  # Nearby smaller -> Hunt
        ((250, 215), (350, 285)),  # Nearby smaller -> Evaluate risk
        ((450, 215), (550, 285)),  # Larger threat -> Seek food
        ((600, 215), (700, 285))   # Hunter approaching -> Flee
    ]
    
    for start, end in connections:
        pygame.draw.line(surface, (255, 255, 255), start, end, 2)
    
    # Add YES/NO labels
    labels = [
        ("YES", 320, 150),
        ("NO", 500, 150),
        ("YES", 200, 250),
        ("NO", 300, 250),
        ("YES", 650, 250)
    ]
    
    label_font = pygame.font.Font(None, 20)
    for text, x, y in labels:
        text_surface = label_font.render(text, True, (200, 255, 200))
        surface.blit(text_surface, (x, y))
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("AI Decision Making", True, (255, 255, 255))
    surface.blit(title, (250, 20))
    
    # Add explanation
    explanation = [
        "Snakes use Decision Tree AI to make movement choices",
        "Each decision is based on current game state and nearby entities",
        "Model learns from successful snake behaviors over time"
    ]
    
    exp_font = pygame.font.Font(None, 24)
    for i, text in enumerate(explanation):
        text_surface = exp_font.render(text, True, (200, 200, 200))
        surface.blit(text_surface, (50, 450 + i * 30))
    
    pygame.image.save(surface, f"{ASSETS_DIR}/ai_behavior.png")
    print("Generated: ai_behavior.png")

def generate_starvation_system_image():
    """Generate image showing starvation system progression"""
    surface = create_surface(800, 400)
    
    # Timeline showing starvation progression
    timeline_y = 200
    timeline_start = 100
    timeline_end = 700
    
    # Draw timeline
    pygame.draw.line(surface, (255, 255, 255), (timeline_start, timeline_y), (timeline_end, timeline_y), 3)
    
    # Timeline markers
    markers = [
        (150, "0s", "Snake eats food", (100, 255, 100)),
        (300, "8s", "Starvation warning", (255, 255, 0)),
        (450, "10s", "Death by starvation", (255, 100, 100)),
        (600, "Reset", "Cycle restarts", (100, 255, 100))
    ]
    
    font = pygame.font.Font(None, 24)
    for x, time_text, desc, color in markers:
        # Draw marker
        pygame.draw.circle(surface, color, (x, timeline_y), 8)
        pygame.draw.line(surface, color, (x, timeline_y - 20), (x, timeline_y + 20), 2)
        
        # Time label
        time_surface = font.render(time_text, True, (255, 255, 255))
        surface.blit(time_surface, (x - 15, timeline_y - 40))
        
        # Description
        desc_surface = font.render(desc, True, (200, 200, 200))
        surface.blit(desc_surface, (x - 50, timeline_y + 30))
    
    # Draw example snakes at different stages
    # Normal snake
    normal_segments = [Vector2(150, 120), Vector2(142, 120), Vector2(134, 120)]
    draw_snake(surface, normal_segments, NORMAL_SNAKE_BODY_COLOR, NORMAL_SNAKE_HEAD_COLOR, 6)
    
    # Warning snake (yellow pulse)
    warning_segments = [Vector2(300, 120), Vector2(292, 120), Vector2(284, 120)]
    warning_color = (255, 255, 0)
    draw_snake(surface, warning_segments, warning_color, (255, 255, 100), 6)
    
    # Dead snake
    dead_segments = [Vector2(450, 120), Vector2(442, 120), Vector2(434, 120)]
    draw_snake(surface, dead_segments, DEAD_SNAKE_COLOR, DEAD_SNAKE_COLOR, 6)
    
    # Title
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Starvation System", True, (255, 255, 255))
    surface.blit(title, (250, 20))
    
    # Add explanation
    explanation = [
        "Snakes must eat regularly to survive",
        "Warning phase: Yellow pulsing effect after 8 seconds",
        "Death occurs after 10 seconds without food"
    ]
    
    exp_font = pygame.font.Font(None, 24)
    for i, text in enumerate(explanation):
        text_surface = exp_font.render(text, True, (200, 200, 200))
        surface.blit(text_surface, (50, 320 + i * 25))
    
    pygame.image.save(surface, f"{ASSETS_DIR}/starvation_system.png")
    print("Generated: starvation_system.png")

def main():
    """Generate all README images"""
    print("Generating README images...")
    
    generate_snake_types_image()
    generate_special_food_image()
    generate_visual_effects_image()
    generate_environmental_effects_image()
    generate_creatures_image()
    generate_ai_behavior_image()
    generate_starvation_system_image()
    
    print(f"All images generated successfully in '{ASSETS_DIR}' directory!")
    pygame.quit()

if __name__ == "__main__":
    main()
