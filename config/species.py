"""
Species configuration parameters.
"""

from .grid import GRID_SIZE

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

# Total number of species
SPECIES_COUNT = len(SPECIES) 