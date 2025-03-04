"""
Main simulation module for the life simulation.
"""

import pygame
from config import FRAME_RATE
from src.grid import Grid
from src.renderer import Renderer

class Simulation:
    def __init__(self):
        """Initialize the simulation."""
        pygame.init()
        pygame.font.init()
        
        self.grid = Grid()
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
    
    def run(self):
        """Run the main simulation loop."""
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update simulation state
            self.grid.update()
            
            # Get current statistics
            stats = self.grid.get_population_stats()
            
            # Render current state
            self.renderer.draw(self.grid.grid, stats)
            
            # Control frame rate
            self.clock.tick(FRAME_RATE)
        
        pygame.quit()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run() 