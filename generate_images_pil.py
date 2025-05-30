#!/usr/bin/env python3
"""
Generate images for README documentation using PIL/Pillow.
This script creates visual representations of various game features.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Create assets directory if it doesn't exist
ASSETS_DIR = "assets"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Colors (RGB tuples)
BG_COLOR = (20, 30, 40)
NORMAL_SNAKE_BODY_COLOR = (50, 200, 50)
NORMAL_SNAKE_HEAD_COLOR = (70, 220, 70)
HUNTER_SNAKE_BODY_COLOR = (200, 50, 50)
HUNTER_SNAKE_HEAD_COLOR = (220, 70, 70)
DEAD_SNAKE_COLOR = (100, 100, 100)
FOOD_COLOR = (255, 100, 100)
SPEED_FOOD_COLOR = (0, 255, 255)
SLOW_FOOD_COLOR = (128, 0, 128)
IMMUNITY_FOOD_COLOR = (255, 215, 0)
GROWTH_FOOD_COLOR = (255, 165, 0)
SHRINK_FOOD_COLOR = (255, 20, 147)

def create_image(width=800, height=600, bg_color=BG_COLOR):
    """Create a new image with background color"""
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_snake_segment(draw, x, y, color, radius=8):
    """Draw a snake segment"""
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color, outline=(255, 255, 255), width=1)

def draw_food_item(draw, x, y, color, radius=7):
    """Draw a food item"""
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color, outline=(255, 255, 255), width=1)

def generate_snake_types_image():
    """Generate image showing different snake types"""
    img, draw = create_image(800, 500)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 32)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((250, 20), "Snake Types", fill=(255, 255, 255), font=font_large)
    
    # Normal snake
    snake_y = 120
    for i in range(4):
        draw_snake_segment(draw, 100 + i*16, snake_y, NORMAL_SNAKE_BODY_COLOR if i > 0 else NORMAL_SNAKE_HEAD_COLOR)
    
    draw.text((200, 110), "Normal Snake", fill=(255, 255, 255), font=font_small)
    draw.text((200, 135), "• Seeks food, avoids hunters", fill=(200, 200, 200), font=font_small)
    draw.text((200, 155), "• Becomes hunter after 10 food", fill=(200, 200, 200), font=font_small)
    
    # Hunter snake
    snake_y = 250
    for i in range(5):
        draw_snake_segment(draw, 100 + i*16, snake_y, HUNTER_SNAKE_BODY_COLOR if i > 0 else HUNTER_SNAKE_HEAD_COLOR)
    
    draw.text((200, 240), "Hunter Snake", fill=(255, 255, 255), font=font_small)
    draw.text((200, 265), "• Can hunt smaller snakes", fill=(200, 200, 200), font=font_small)
    draw.text((200, 285), "• Gains 1/3 of prey's size", fill=(200, 200, 200), font=font_small)
    
    # Starving snake
    snake_y = 380
    starving_color = (255, 255, 0)  # Yellow
    for i in range(3):
        draw_snake_segment(draw, 100 + i*16, snake_y, starving_color)
    
    draw.text((200, 370), "Starving Snake", fill=(255, 255, 255), font=font_small)
    draw.text((200, 395), "• Pulsing yellow after 8s without food", fill=(200, 200, 200), font=font_small)
    draw.text((200, 415), "• Dies after 10s without food", fill=(200, 200, 200), font=font_small)
    
    img.save(f"{ASSETS_DIR}/snake_types.png")
    print("Generated: snake_types.png")

def generate_special_food_image():
    """Generate image showing all special food types"""
    img, draw = create_image(900, 600)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((300, 20), "Special Food Types", fill=(255, 255, 255), font=font_large)
    
    # Food types with descriptions
    foods = [
        (150, 120, SPEED_FOOD_COLOR, "Speed Boost", "2.5x speed for 6 seconds"),
        (450, 120, SLOW_FOOD_COLOR, "Slow Effect", "0.4x speed for 10 seconds"),
        (750, 120, IMMUNITY_FOOD_COLOR, "Immunity", "5s protection from hunters"),
        (150, 300, GROWTH_FOOD_COLOR, "Growth Food", "Instant +3 size increase"),
        (450, 300, SHRINK_FOOD_COLOR, "Shrink Food", "Reduces size by 2"),
        (750, 300, FOOD_COLOR, "Normal Food", "Standard +1 size increase")
    ]
    
    for x, y, color, name, description in foods:
        # Draw food item
        draw_food_item(draw, x, y, color, 15)
        
        # Add name
        draw.text((x - 50, y + 30), name, fill=(255, 255, 255), font=font_medium)
        
        # Add description
        draw.text((x - 70, y + 55), description, fill=(200, 200, 200), font=font_small)
    
    # Add spawn chance info
    draw.text((50, 500), "Special food has 15% spawn chance instead of normal food", fill=(200, 200, 200), font=font_small)
    draw.text((50, 525), "Effects are temporary except for growth/shrink", fill=(200, 200, 200), font=font_small)
    
    img.save(f"{ASSETS_DIR}/special_food_types.png")
    print("Generated: special_food_types.png")

def generate_visual_effects_image():
    """Generate image showing visual effects on snakes"""
    img, draw = create_image(800, 600)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((250, 20), "Visual Effects System", fill=(255, 255, 255), font=font_large)
    
    # Speed boost effect
    y_pos = 120
    speed_color = (100, 255, 255)  # Cyan tint
    for i in range(4):
        draw_snake_segment(draw, 100 + i*16, y_pos, speed_color)
    
    # Speed lines around head
    head_x, head_y = 100, y_pos
    for i in range(6):
        angle = i * 60
        line_length = 25
        end_x = head_x + line_length * math.cos(math.radians(angle))
        end_y = head_y + line_length * math.sin(math.radians(angle))
        draw.line([head_x, head_y, end_x, end_y], fill=(0, 255, 255), width=3)
    
    draw.text((200, 110), "Speed Boost Effect", fill=(255, 255, 255), font=font_medium)
    draw.text((200, 135), "• Cyan tint on entire snake", fill=(200, 200, 200), font=font_small)
    draw.text((200, 155), "• Rotating speed lines around head", fill=(200, 200, 200), font=font_small)
    
    # Immunity effect
    y_pos = 280
    for i in range(4):
        color = (255, 215, 0) if i == 0 else NORMAL_SNAKE_BODY_COLOR  # Golden head
        draw_snake_segment(draw, 100 + i*16, y_pos, color)
    
    # Golden aura around head
    aura_x, aura_y = 100, y_pos
    draw.ellipse([aura_x-25, aura_y-25, aura_x+25, aura_y+25], outline=(255, 215, 0), width=4)
    
    draw.text((200, 270), "Immunity Effect", fill=(255, 255, 255), font=font_medium)
    draw.text((200, 295), "• Golden pulsing head", fill=(200, 200, 200), font=font_small)
    draw.text((200, 315), "• Golden aura around head", fill=(200, 200, 200), font=font_small)
    
    # Slow effect
    y_pos = 440
    slow_color = (150, 50, 150)  # Purple tint
    for i in range(4):
        draw_snake_segment(draw, 100 + i*16, y_pos, slow_color)
    
    draw.text((200, 430), "Slow Effect", fill=(255, 255, 255), font=font_medium)
    draw.text((200, 455), "• Purple tint on entire snake", fill=(200, 200, 200), font=font_small)
    draw.text((200, 475), "• Reduced movement speed", fill=(200, 200, 200), font=font_small)
    
    img.save(f"{ASSETS_DIR}/visual_effects.png")
    print("Generated: visual_effects.png")

def generate_environmental_effects_image():
    """Generate image showing environmental effects"""
    img, draw = create_image(900, 600)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((250, 20), "Environmental Effects", fill=(255, 255, 255), font=font_large)
    
    # Black hole
    bh_x, bh_y = 150, 150
    draw.ellipse([bh_x-30, bh_y-30, bh_x+30, bh_y+30], fill=(10, 10, 10), outline=(100, 0, 100), width=3)
    draw.ellipse([bh_x-45, bh_y-45, bh_x+45, bh_y+45], outline=(50, 0, 50), width=2)
    
    # Snake being pulled
    snake_x, snake_y = 220, 120
    for i in range(3):
        draw_snake_segment(draw, snake_x + i*12, snake_y, NORMAL_SNAKE_BODY_COLOR if i > 0 else NORMAL_SNAKE_HEAD_COLOR, 6)
    
    # Pull lines
    for i in range(3):
        start_x = snake_x + i * 8
        start_y = snake_y + i * 3
        draw.line([start_x, start_y, bh_x + 20, bh_y - 10], fill=(150, 50, 150), width=2)
    
    draw.text((50, 220), "Black Hole", fill=(255, 255, 255), font=font_medium)
    draw.text((50, 245), "Pulls nearby entities", fill=(200, 200, 200), font=font_small)
    
    # Speed zone
    sz_x, sz_y = 500, 150
    draw.ellipse([sz_x-60, sz_y-60, sz_x+60, sz_y+60], outline=(0, 255, 0), width=5)
    draw.ellipse([sz_x-40, sz_y-40, sz_x+40, sz_y+40], outline=(0, 200, 0), width=3)
    
    # Fast snake in zone
    for i in range(3):
        draw_snake_segment(draw, sz_x + i*12, sz_y, (100, 255, 100) if i > 0 else (150, 255, 150), 6)
    
    draw.text((450, 220), "Speed Zone", fill=(255, 255, 255), font=font_medium)
    draw.text((450, 245), "2x speed boost inside", fill=(200, 200, 200), font=font_small)
    
    # Food magnet
    fm_x, fm_y = 150, 400
    draw.ellipse([fm_x-20, fm_y-20, fm_x+20, fm_y+20], fill=(255, 100, 0), outline=(255, 150, 50), width=3)
    draw.ellipse([fm_x-35, fm_y-35, fm_x+35, fm_y+35], outline=(255, 150, 50), width=2)
    
    # Food being attracted
    food_x, food_y = 220, 370
    draw_food_item(draw, food_x, food_y, FOOD_COLOR, 6)
    
    # Attraction lines
    for i in range(3):
        start_x = food_x - i * 4
        start_y = food_y + i * 2
        draw.line([start_x, start_y, fm_x + 15, fm_y - 5], fill=(255, 200, 100), width=2)
    
    draw.text((50, 470), "Food Magnet", fill=(255, 255, 255), font=font_medium)
    draw.text((50, 495), "Attracts food items", fill=(200, 200, 200), font=font_small)
    
    img.save(f"{ASSETS_DIR}/environmental_effects.png")
    print("Generated: environmental_effects.png")

def generate_creatures_image():
    """Generate image showing special creatures"""
    img, draw = create_image(800, 500)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((250, 20), "Special Creatures", fill=(255, 255, 255), font=font_large)
    
    # Ripper
    ripper_x, ripper_y = 150, 150
    ripper_color = (200, 0, 200)
    draw.ellipse([ripper_x-15, ripper_y-15, ripper_x+15, ripper_y+15], fill=ripper_color, outline=(255, 255, 255), width=2)
    
    # Spikes around ripper
    for i in range(8):
        angle = i * 45
        spike_length = 20
        end_x = ripper_x + spike_length * math.cos(math.radians(angle))
        end_y = ripper_y + spike_length * math.sin(math.radians(angle))
        draw.line([ripper_x, ripper_y, end_x, end_y], fill=ripper_color, width=3)
    
    # Hunter being chased
    hunter_x, hunter_y = 280, 130
    for i in range(4):
        draw_snake_segment(draw, hunter_x + i*12, hunter_y, HUNTER_SNAKE_BODY_COLOR if i > 0 else HUNTER_SNAKE_HEAD_COLOR, 8)
    
    # Chase line
    draw.line([ripper_x + 15, ripper_y, hunter_x - 8, hunter_y], fill=(255, 100, 100), width=3)
    
    draw.text((300, 120), "Ripper", fill=(255, 255, 255), font=font_medium)
    draw.text((300, 145), "• Hunts hunter snakes", fill=(200, 200, 200), font=font_small)
    draw.text((300, 165), "• Spawns when >50% hunters", fill=(200, 200, 200), font=font_small)
    
    # Scavenger
    scav_x, scav_y = 150, 350
    scav_color = (150, 75, 0)
    
    # Scavenger body
    for i in range(4):
        radius = 12 - i * 2
        draw.ellipse([scav_x + i*8 - radius, scav_y - radius, 
                     scav_x + i*8 + radius, scav_y + radius], 
                    fill=scav_color, outline=(255, 255, 255), width=1)
    
    # Food being stolen
    food_x, food_y = 250, 350
    draw_food_item(draw, food_x, food_y, FOOD_COLOR, 7)
    
    # Steal line
    draw.line([scav_x + 12, scav_y, food_x - 7, food_y], fill=(255, 200, 0), width=3)
    
    draw.text((300, 340), "Scavenger", fill=(255, 255, 255), font=font_medium)
    draw.text((300, 365), "• Steals food from snakes", fill=(200, 200, 200), font=font_small)
    draw.text((300, 385), "• Spawns when 10+ food present", fill=(200, 200, 200), font=font_small)
    
    img.save(f"{ASSETS_DIR}/special_creatures.png")
    print("Generated: special_creatures.png")

def generate_ai_behavior_image():
    """Generate image showing AI decision making"""
    img, draw = create_image(800, 600)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((250, 20), "AI Decision Making", fill=(255, 255, 255), font=font_large)
    
    # Decision tree visualization
    # Root node
    draw.rectangle([340, 80, 460, 110], fill=(100, 100, 200), outline=(255, 255, 255), width=2)
    draw.text((380, 90), "Is Hunter?", fill=(255, 255, 255), font=font_small)
    
    # Level 2 nodes
    draw.rectangle([200, 160, 350, 190], fill=(100, 100, 200), outline=(255, 255, 255), width=2)
    draw.text((210, 170), "Nearby smaller snake?", fill=(255, 255, 255), font=font_small)
    
    draw.rectangle([450, 160, 580, 190], fill=(100, 100, 200), outline=(255, 255, 255), width=2)
    draw.text((465, 170), "Hunter approaching?", fill=(255, 255, 255), font=font_small)
    
    # Action nodes
    action_color = (200, 100, 100)
    draw.ellipse([80, 240, 180, 270], fill=action_color, outline=(255, 255, 255), width=2)
    draw.text((110, 250), "HUNT", fill=(255, 255, 255), font=font_small)
    
    draw.ellipse([220, 240, 330, 270], fill=action_color, outline=(255, 255, 255), width=2)
    draw.text((245, 250), "SEEK FOOD", fill=(255, 255, 255), font=font_small)
    
    draw.ellipse([520, 240, 620, 270], fill=action_color, outline=(255, 255, 255), width=2)
    draw.text((555, 250), "FLEE", fill=(255, 255, 255), font=font_small)
    
    # Connection lines
    connections = [
        ((400, 110), (275, 160)),  # Root to left branch
        ((400, 110), (515, 160)),  # Root to right branch
        ((275, 190), (130, 240)),  # Left branch to HUNT
        ((275, 190), (275, 240)),  # Left branch to SEEK FOOD
        ((515, 190), (570, 240))   # Right branch to FLEE
    ]
    
    for start, end in connections:
        draw.line([start[0], start[1], end[0], end[1]], fill=(255, 255, 255), width=2)
    
    # YES/NO labels
    draw.text((320, 130), "YES", fill=(200, 255, 200), font=font_small)
    draw.text((420, 130), "NO", fill=(255, 200, 200), font=font_small)
    draw.text((200, 210), "YES", fill=(200, 255, 200), font=font_small)
    draw.text((290, 210), "NO", fill=(255, 200, 200), font=font_small)
    draw.text((540, 210), "YES", fill=(200, 255, 200), font=font_small)
    
    # Explanation
    explanation_y = 320
    explanations = [
        "AI snakes use Decision Tree machine learning",
        "Each decision based on current game state",
        "Model learns from successful behaviors",
        "Improves over time with more training data"
    ]
    
    for i, text in enumerate(explanations):
        draw.text((50, explanation_y + i * 25), f"• {text}", fill=(200, 200, 200), font=font_small)
    
    img.save(f"{ASSETS_DIR}/ai_behavior.png")
    print("Generated: ai_behavior.png")

def generate_starvation_system_image():
    """Generate image showing starvation system progression"""
    img, draw = create_image(800, 400)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 32)
        font_medium = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 20)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((250, 20), "Starvation System", fill=(255, 255, 255), font=font_large)
    
    # Timeline
    timeline_y = 200
    timeline_start = 100
    timeline_end = 700
    
    # Draw timeline
    draw.line([timeline_start, timeline_y, timeline_end, timeline_y], fill=(255, 255, 255), width=3)
    
    # Timeline markers
    markers = [
        (150, "0s", "Snake eats food", (100, 255, 100)),
        (300, "8s", "Starvation warning", (255, 255, 0)),
        (450, "10s", "Death by starvation", (255, 100, 100)),
        (600, "Reset", "Cycle restarts", (100, 255, 100))
    ]
    
    for x, time_text, desc, color in markers:
        # Draw marker
        draw.ellipse([x-8, timeline_y-8, x+8, timeline_y+8], fill=color, outline=(255, 255, 255), width=2)
        draw.line([x, timeline_y-20, x, timeline_y+20], fill=color, width=2)
        
        # Time label
        draw.text((x-15, timeline_y-40), time_text, fill=(255, 255, 255), font=font_medium)
        
        # Description
        draw.text((x-50, timeline_y+30), desc, fill=(200, 200, 200), font=font_small)
    
    # Draw example snakes at different stages
    # Normal snake
    for i in range(3):
        draw_snake_segment(draw, 150 + i*12, 120, NORMAL_SNAKE_BODY_COLOR if i > 0 else NORMAL_SNAKE_HEAD_COLOR, 6)
    
    # Warning snake (yellow)
    warning_color = (255, 255, 0)
    for i in range(3):
        draw_snake_segment(draw, 300 + i*12, 120, warning_color, 6)
    
    # Dead snake
    for i in range(3):
        draw_snake_segment(draw, 450 + i*12, 120, DEAD_SNAKE_COLOR, 6)
    
    # Explanation
    explanation_y = 320
    explanations = [
        "Snakes must eat regularly to survive",
        "Warning phase: Yellow pulsing effect after 8 seconds",
        "Death occurs after 10 seconds without food",
        "Timer resets when snake eats any food"
    ]
    
    for i, text in enumerate(explanations):
        draw.text((50, explanation_y + i * 25), f"• {text}", fill=(200, 200, 200), font=font_small)
    
    img.save(f"{ASSETS_DIR}/starvation_system.png")
    print("Generated: starvation_system.png")

def generate_game_overview_image():
    """Generate overview image showing the complete game"""
    img, draw = create_image(900, 700)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 36)
        font_medium = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Title
    draw.text((300, 20), "SNAIKS Game Overview", fill=(255, 255, 255), font=font_large)
    
    # Multiple snakes
    # Normal snake
    for i in range(4):
        draw_snake_segment(draw, 100 + i*15, 120, NORMAL_SNAKE_BODY_COLOR if i > 0 else NORMAL_SNAKE_HEAD_COLOR)
    
    # Hunter snake
    for i in range(5):
        draw_snake_segment(draw, 350 + i*15, 150, HUNTER_SNAKE_BODY_COLOR if i > 0 else HUNTER_SNAKE_HEAD_COLOR)
    
    # Speed boost snake
    speed_color = (100, 255, 255)
    for i in range(4):
        draw_snake_segment(draw, 600 + i*15, 100, speed_color)
    
    # Various food items
    foods = [
        (200, 200, FOOD_COLOR),
        (400, 180, SPEED_FOOD_COLOR),
        (650, 220, IMMUNITY_FOOD_COLOR),
        (300, 250, GROWTH_FOOD_COLOR),
        (500, 280, SHRINK_FOOD_COLOR)
    ]
    
    for x, y, color in foods:
        draw_food_item(draw, x, y, color)
    
    # Environmental effects
    # Black hole
    bh_x, bh_y = 150, 350
    draw.ellipse([bh_x-25, bh_y-25, bh_x+25, bh_y+25], fill=(10, 10, 10), outline=(100, 0, 100), width=3)
    
    # Speed zone
    sz_x, sz_y = 500, 380
    draw.ellipse([sz_x-40, sz_y-40, sz_x+40, sz_y+40], outline=(0, 255, 0), width=3)
    
    # Ripper creature
    ripper_x, ripper_y = 750, 350
    draw.ellipse([ripper_x-12, ripper_y-12, ripper_x+12, ripper_y+12], fill=(200, 0, 200))
    
    # Feature list
    features_y = 480
    features = [
        "🐍 AI-controlled snakes with machine learning",
        "🎯 Hunt or be hunted mechanics",
        "⚡ Special food with temporary effects",
        "🌀 Environmental effects (black holes, speed zones)",
        "👾 Special creatures (rippers, scavengers)",
        "⏰ Starvation system for survival pressure",
        "🎨 Rich visual effects and indicators",
        "📊 Performance tracking and learning curves"
    ]
    
    for i, feature in enumerate(features):
        draw.text((50, features_y + i * 25), feature, fill=(200, 220, 255), font=font_small)
    
    img.save(f"{ASSETS_DIR}/game_overview.png")
    print("Generated: game_overview.png")

def main():
    """Generate all README images"""
    print("Generating README images with PIL...")
    
    generate_game_overview_image()
    generate_snake_types_image()
    generate_special_food_image()
    generate_visual_effects_image()
    generate_environmental_effects_image()
    generate_creatures_image()
    generate_ai_behavior_image()
    generate_starvation_system_image()
    
    print(f"\nAll images generated successfully in '{ASSETS_DIR}' directory!")
    print("Images created:")
    for filename in os.listdir(ASSETS_DIR):
        if filename.endswith('.png'):
            print(f"  - {filename}")

if __name__ == "__main__":
    main()
