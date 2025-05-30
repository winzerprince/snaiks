# resource_manager.py: Efficient resource management for game objects
import time
from collections import deque

class ObjectPool:
    """Generic object pool for efficient memory management"""
    
    def __init__(self, factory_func, reset_func, initial_size=10):
        self.factory_func = factory_func
        self.reset_func = reset_func
        self.available_objects = deque()
        self.active_objects = set()
        
        # Pre-populate pool
        for _ in range(initial_size):
            obj = self.factory_func()
            self.available_objects.append(obj)
    
    def get_object(self, *args, **kwargs):
        """Get an object from the pool"""
        if self.available_objects:
            obj = self.available_objects.popleft()
            self.reset_func(obj, *args, **kwargs)
        else:
            obj = self.factory_func(*args, **kwargs)
        
        self.active_objects.add(obj)
        return obj
    
    def return_object(self, obj):
        """Return an object to the pool"""
        if obj in self.active_objects:
            self.active_objects.remove(obj)
            self.available_objects.append(obj)
    
    def get_active_count(self):
        """Get number of active objects"""
        return len(self.active_objects)
    
    def get_available_count(self):
        """Get number of available objects"""
        return len(self.available_objects)

class PerformanceMonitor:
    """Monitor game performance and resource usage"""
    
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.frame_times = deque(maxlen=window_size)
        self.update_times = deque(maxlen=window_size)
        self.draw_times = deque(maxlen=window_size)
        self.last_time = time.time()
    
    def start_frame(self):
        """Mark the start of a frame"""
        current_time = time.time()
        if hasattr(self, 'last_time'):
            frame_time = current_time - self.last_time
            self.frame_times.append(frame_time)
        self.last_time = current_time
        self.frame_start_time = current_time
    
    def mark_update_time(self):
        """Mark the end of update phase"""
        self.update_end_time = time.time()
        update_time = self.update_end_time - self.frame_start_time
        self.update_times.append(update_time)
    
    def mark_draw_time(self):
        """Mark the end of draw phase"""
        draw_end_time = time.time()
        draw_time = draw_end_time - self.update_end_time
        self.draw_times.append(draw_time)
    
    def get_stats(self):
        """Get performance statistics"""
        if not self.frame_times:
            return {}
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        avg_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        
        stats = {
            'fps': avg_fps,
            'frame_time_ms': avg_frame_time * 1000,
        }
        
        if self.update_times:
            avg_update_time = sum(self.update_times) / len(self.update_times)
            stats['update_time_ms'] = avg_update_time * 1000
        
        if self.draw_times:
            avg_draw_time = sum(self.draw_times) / len(self.draw_times)
            stats['draw_time_ms'] = avg_draw_time * 1000
        
        return stats

class SpatialGrid:
    """Spatial partitioning for efficient collision detection"""
    
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = int(width // cell_size) + 1
        self.rows = int(height // cell_size) + 1
        self.clear()
    
    def clear(self):
        """Clear all objects from the grid"""
        self.grid = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
    
    def _get_grid_pos(self, x, y):
        """Convert world position to grid coordinates"""
        col = max(0, min(self.cols - 1, int(x // self.cell_size)))
        row = max(0, min(self.rows - 1, int(y // self.cell_size)))
        return col, row
    
    def add_object(self, obj, x, y):
        """Add object to grid at position"""
        col, row = self._get_grid_pos(x, y)
        self.grid[row][col].append(obj)
    
    def get_nearby_objects(self, x, y, radius=None):
        """Get objects near the given position"""
        if radius is None:
            radius = self.cell_size
        
        # Calculate range of cells to check
        min_col = max(0, int((x - radius) // self.cell_size))
        max_col = min(self.cols - 1, int((x + radius) // self.cell_size))
        min_row = max(0, int((y - radius) // self.cell_size))
        max_row = min(self.rows - 1, int((y + radius) // self.cell_size))
        
        nearby_objects = []
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                nearby_objects.extend(self.grid[row][col])
        
        return nearby_objects

class ResourceManager:
    """Central resource manager for the game"""
    
    def __init__(self):
        self.performance_monitor = PerformanceMonitor()
        
        # Initialize spatial grid for collision detection
        self.spatial_grid = SpatialGrid(
            width=1000,  # SCREEN_WIDTH
            height=800,  # SCREEN_HEIGHT
            cell_size=100  # Reasonable cell size
        )
        
        # Object pools for memory efficiency
        from food import Food
        from snake import Snake
        
        def create_food():
            return Food()
        
        def reset_food(food, *args, **kwargs):
            food.__init__()
        
        self.food_pool = ObjectPool(create_food, reset_food, initial_size=20)
        
        # Cleanup tracking
        self.cleanup_interval = 5.0  # seconds
        self.last_cleanup_time = time.time()
    
    def start_frame(self):
        """Start frame timing"""
        self.performance_monitor.start_frame()
        self.spatial_grid.clear()
    
    def mark_update_complete(self):
        """Mark update phase complete"""
        self.performance_monitor.mark_update_time()
    
    def mark_draw_complete(self):
        """Mark draw phase complete"""
        self.performance_monitor.mark_draw_time()
    
    def get_food_from_pool(self):
        """Get a food object from the pool"""
        return self.food_pool.get_object()
    
    def return_food_to_pool(self, food):
        """Return a food object to the pool"""
        self.food_pool.return_object(food)
    
    def update_spatial_grid(self, snakes, food_items):
        """Update spatial grid with current objects"""
        self.spatial_grid.clear()
        
        # Add snakes to grid
        for snake in snakes:
            if not snake.is_dead:
                self.spatial_grid.add_object(
                    snake, 
                    snake.head_position.x, 
                    snake.head_position.y
                )
        
        # Add food to grid
        for food in food_items:
            self.spatial_grid.add_object(
                food,
                food.position.x,
                food.position.y
            )
    
    def get_nearby_objects(self, x, y, radius=50):
        """Get objects near position using spatial grid"""
        return self.spatial_grid.get_nearby_objects(x, y, radius)
    
    def should_cleanup(self):
        """Check if cleanup should be performed"""
        current_time = time.time()
        if current_time - self.last_cleanup_time > self.cleanup_interval:
            self.last_cleanup_time = current_time
            return True
        return False
    
    def get_performance_stats(self):
        """Get current performance statistics"""
        stats = self.performance_monitor.get_stats()
        stats['active_food'] = self.food_pool.get_active_count()
        stats['pooled_food'] = self.food_pool.get_available_count()
        return stats
