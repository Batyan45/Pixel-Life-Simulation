"""
Graph component for displaying population statistics.
"""

import pygame
import numpy as np

class PopulationGraph:
    def __init__(self, width, height, history_length):
        """Initialize the population graph."""
        self.width = width
        self.height = height
        self.history_length = history_length
        self.graph_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.max_scale = 10000  # Fixed maximum scale for Y-axis
        
    def draw(self, surface, pos, population_history, species_data):
        """Draw the population graph with clear lines."""
        self.graph_surface.fill((0, 0, 0, 0))  # Clear with transparency
        
        if not population_history or not any(population_history.values()):
            return
            
        # Draw background
        pygame.draw.rect(
            self.graph_surface,
            (30, 33, 39, 200),  # More opaque background
            (0, 0, self.width, self.height),
            border_radius=4
        )
        
        # Draw grid lines for better readability
        self._draw_grid()
        
        # Find the maximum length of history across all species
        max_history_length = max(len(history) for history in population_history.values() if history)
        if max_history_length == 0:
            return
        
        # Draw population lines for each species
        for species_id, history in population_history.items():
            if not history:
                continue
                
            color = species_data[species_id]['color']
            points = self._get_curve_points(history, max_history_length)
            
            if len(points) > 1:
                # Draw thicker line for better visibility
                pygame.draw.lines(
                    self.graph_surface,
                    color,
                    False,
                    points,
                    width=2
                )
            
            # Always draw the last point
            if points:
                end_point = points[-1]
                pygame.draw.circle(
                    self.graph_surface,
                    color,
                    (int(end_point[0]), int(end_point[1])),
                    4
                )
        
        # Draw the graph on the target surface
        surface.blit(self.graph_surface, pos)
        
    def _draw_grid(self):
        """Draw background grid lines."""
        grid_color = (100, 100, 100, 50)  # Light gray, semi-transparent
        
        # Draw horizontal grid lines
        num_lines = 4
        for i in range(num_lines + 1):
            y = int(self.height * (1 - i / num_lines))
            pygame.draw.line(
                self.graph_surface,
                grid_color,
                (0, y),
                (self.width, y)
            )
    
    def _get_curve_points(self, history, max_history_length):
        """Convert population history to graph points."""
        if not history:
            return []
            
        points = []
        
        # Add small padding to the graph edges
        padding = 0.05
        usable_width = self.width * (1 - 2 * padding)
        
        # Handle single point case
        if max_history_length == 1:
            x = self.width / 2  # Center point
            value = history[0]
            scaled_value = min(value / self.max_scale, 1.0)
            v_padding = 0.1
            usable_height = self.height * (1 - 2 * v_padding)
            y = (self.height * v_padding) + (usable_height * (1 - scaled_value))
            return [(x, y)]
        
        # Calculate points using actual history length for x-scale
        for i, value in enumerate(history):
            # Scale x position based on current history length
            x = (self.width * padding) + (i * usable_width / (max_history_length - 1))
            
            # Scale value based on fixed maximum
            scaled_value = min(value / self.max_scale, 1.0)
            
            # Add padding to vertical scale
            v_padding = 0.1
            usable_height = self.height * (1 - 2 * v_padding)
            y = (self.height * v_padding) + (usable_height * (1 - scaled_value))
            
            points.append((x, y))
            
        return points 