"""
Grid management for the life simulation.
"""

import numpy as np
import random
from config import GRID_SIZE, MOVEMENT_DIRECTIONS, SPECIES

class Grid:
    def __init__(self):
        # Initialize grid with zeros (empty cells)
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self._initialize_species()
    
    def _initialize_species(self):
        """Place initial species in their respective areas."""
        for species_id, species_data in SPECIES.items():
            placed = 0
            x_start, y_start, x_end, y_end = species_data['start_area']
            while placed < species_data['initial_count']:
                x = random.randint(x_start, x_end - 1)
                y = random.randint(y_start, y_end - 1)
                if self.grid[x, y] == 0:
                    self.grid[x, y] = species_id
                    placed += 1
    
    def get_population_stats(self):
        """Get current population statistics for each species."""
        stats = {species_id: 0 for species_id in SPECIES.keys()}
        unique, counts = np.unique(self.grid, return_counts=True)
        for value, count in zip(unique, counts):
            if value != 0:  # Skip empty cells
                stats[value] = count
        return stats
    
    def update(self):
        """Update the grid state for one simulation step."""
        new_grid = self.grid.copy()
        
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                species_id = self.grid[x, y]
                if species_id != 0:  # If cell is not empty
                    self._process_cell(x, y, species_id, new_grid)
        
        self.grid = new_grid
    
    def _process_cell(self, x, y, species_id, new_grid):
        """Process movement and reproduction for a single cell."""
        species_data = SPECIES[species_id]
        
        # Movement
        if random.random() < species_data['movement_chance']:
            self._try_movement(x, y, species_id, species_data, new_grid)
        
        # Reproduction
        if random.random() < species_data['reproduction_chance']:
            self._try_reproduction(x, y, species_id, new_grid)
    
    def _try_movement(self, x, y, species_id, species_data, new_grid):
        """Attempt to move a creature to a new cell."""
        dx, dy = random.choice(MOVEMENT_DIRECTIONS)
        new_x = (x + dx) % GRID_SIZE
        new_y = (y + dy) % GRID_SIZE
        
        # If target cell is empty, move there
        if new_grid[new_x, new_y] == 0:
            new_grid[new_x, new_y] = species_id
            new_grid[x, y] = 0
        
        # If target cell contains different species, fight
        elif new_grid[new_x, new_y] != species_id:
            self._resolve_combat(species_id, species_data, new_x, new_y, new_grid)
    
    def _resolve_combat(self, attacker_id, attacker_data, x, y, new_grid):
        """Resolve combat between two creatures."""
        defender_id = new_grid[x, y]
        attacker_strength = attacker_data['combat_strength']
        defender_strength = SPECIES[defender_id]['combat_strength']
        
        # Combat outcome based on relative strengths
        if random.random() < attacker_strength / (attacker_strength + defender_strength):
            new_grid[x, y] = attacker_id
    
    def _try_reproduction(self, x, y, species_id, new_grid):
        """Attempt to reproduce into an adjacent empty cell."""
        directions = list(MOVEMENT_DIRECTIONS)
        random.shuffle(directions)
        for dx, dy in directions:
            reproduce_x = (x + dx) % GRID_SIZE
            reproduce_y = (y + dy) % GRID_SIZE
            if new_grid[reproduce_x, reproduce_y] == 0:
                new_grid[reproduce_x, reproduce_y] = species_id
                break 