"""
Grid configuration parameters.
"""

# Grid dimensions and cell size
GRID_SIZE = 100
CELL_SIZE = 8
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# Movement settings
MOVEMENT_DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
] 