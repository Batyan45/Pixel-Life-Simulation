"""
Configuration file for the life simulation parameters
"""

# Grid parameters
GRID_SIZE = 100
CELL_SIZE = 8
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FRAME_RATE = 30

# Species definitions
SPECIES = {
    1: {
        'name': 'Red Runners',
        'color': (255, 0, 0),
        'initial_count': 400,
        'movement_chance': 1.0,    # Fast movement
        'reproduction_chance': 0.005,  # Low reproduction
        'combat_strength': 0.6,    # Strong in combat
        'start_area': (0, 0, GRID_SIZE//2, GRID_SIZE//2),  # Top-left
    },
    2: {
        'name': 'Blue Breeders',
        'color': (0, 0, 255),
        'initial_count': 300,
        'movement_chance': 0.7,    # Slower movement
        'reproduction_chance': 0.02,  # High reproduction
        'combat_strength': 0.4,    # Weak in combat
        'start_area': (GRID_SIZE//2, 0, GRID_SIZE, GRID_SIZE//2),  # Top-right
    },
    3: {
        'name': 'Green Guardians',
        'color': (0, 255, 0),
        'initial_count': 200,
        'movement_chance': 0.5,    # Slowest movement
        'reproduction_chance': 0.01,  # Medium reproduction
        'combat_strength': 0.7,    # Strongest in combat
        'start_area': (0, GRID_SIZE//2, GRID_SIZE//2, GRID_SIZE),  # Bottom-left
    },
    4: {
        'name': 'Yellow Yielders',
        'color': (255, 255, 0),
        'initial_count': 350,
        'movement_chance': 0.8,    # Medium-fast movement
        'reproduction_chance': 0.015,  # Medium-high reproduction
        'combat_strength': 0.45,   # Medium-weak in combat
        'start_area': (GRID_SIZE//2, GRID_SIZE//2, GRID_SIZE, GRID_SIZE),  # Bottom-right
    }
}

SPECIES_COUNT = len(SPECIES)

# Display settings
WINDOW_TITLE = "Life Simulation"
SHOW_GRID = False
GRID_COLOR = (50, 50, 50)  # Dark gray
BACKGROUND_COLOR = (0, 0, 0)  # Black

# Movement settings
MOVEMENT_DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

# Statistics settings
SHOW_STATS = True  # Show population statistics
STATS_UPDATE_RATE = 30  # Update stats every N frames
STATS_FONT_SIZE = 20
STATS_COLOR = (255, 255, 255)  # White 