"""
Visualization module for the life simulation.
"""

import pygame
from config import (
    WINDOW_SIZE, WINDOW_TITLE, GRID_SIZE, CELL_SIZE,
    SHOW_GRID, GRID_COLOR, BACKGROUND_COLOR,
    SHOW_STATS, STATS_UPDATE_RATE, STATS_FONT_SIZE,
    STATS_COLOR, SPECIES
)

class Renderer:
    def __init__(self):
        """Initialize the renderer."""
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)
        self.stats_font = pygame.font.SysFont('Arial', STATS_FONT_SIZE)
        self.frame_count = 0
    
    def draw(self, grid, stats):
        """Draw the current state of the simulation."""
        self.screen.fill(BACKGROUND_COLOR)
        
        self._draw_grid_lines()
        self._draw_species(grid)
        self._draw_stats(stats)
        
        pygame.display.flip()
        self.frame_count += 1
    
    def _draw_grid_lines(self):
        """Draw grid lines if enabled."""
        if not SHOW_GRID:
            return
            
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_SIZE))
            pygame.draw.line(self.screen, GRID_COLOR, (0, x), (WINDOW_SIZE, x))
    
    def _draw_species(self, grid):
        """Draw all species on the grid."""
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                species_id = grid[x, y]
                if species_id != 0:
                    color = SPECIES[species_id]['color']
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
    
    def _draw_stats(self, stats):
        """Draw population statistics if enabled."""
        if not SHOW_STATS or self.frame_count % STATS_UPDATE_RATE != 0:
            return
            
        y_offset = 10
        for species_id, count in stats.items():
            species_data = SPECIES[species_id]
            text = f"{species_data['name']}: {count}"
            text_surface = self.stats_font.render(text, True, species_data['color'])
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += STATS_FONT_SIZE + 5 