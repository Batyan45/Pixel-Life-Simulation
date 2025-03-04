"""
Species configuration parameters.
"""

from .grid import GRID_SIZE

# Species definitions
SPECIES = {
    1: {
        'name': 'Sprinters',  # Fast but weak reproducers
        'color': (255, 0, 0),
        'initial_count': 400,
        'movement_chance': 1.0,    # Fastest movement
        'reproduction_chance': 0.005,  # Very low reproduction
        'combat_strength': 0.3,    # Below average combat
        'start_area': (0, 0, GRID_SIZE//2, GRID_SIZE//2),  # Top-left
    },
    2: {
        'name': 'Swarmers',  # Explosive breeders
        'color': (0, 0, 255),
        'initial_count': 300,
        'movement_chance': 0.7,    # High mobility
        'reproduction_chance': 0.6,  # Explosive reproduction
        'combat_strength': 0.4,    # Medium combat ability
        'start_area': (GRID_SIZE//2, 0, GRID_SIZE, GRID_SIZE//2),  # Top-right
    },
    3: {
        'name': 'Warriors',  # Combat specialists
        'color': (0, 255, 0),
        'initial_count': 50,
        'movement_chance': 0.5,    # Low mobility
        'reproduction_chance': 0.005,  # Very low reproduction
        'combat_strength': 0.7,    # Superior combat strength
        'start_area': (0, GRID_SIZE//2, GRID_SIZE//2, GRID_SIZE),  # Bottom-left
    },
    4: {
        'name': 'Scouts',  # Fast movers with moderate stats
        'color': (255, 255, 0),
        'initial_count': 350,
        'movement_chance': 0.8,    # Very high mobility
        'reproduction_chance': 0.015,  # Low-medium reproduction
        'combat_strength': 0.39,   # Medium combat ability
        'start_area': (GRID_SIZE//2, GRID_SIZE//2, GRID_SIZE, GRID_SIZE),  # Bottom-right
    }
}

# Total number of species
SPECIES_COUNT = len(SPECIES) 