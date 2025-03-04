"""
Main simulation module for the life simulation.
"""

import pygame
from config import FRAME_RATE, WINDOW_SIZE, CONTROL_PANEL_WIDTH, TITLE_BAR_HEIGHT
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
        self.paused = False
        self.simulation_speed = 1.0  # Speed multiplier
    
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
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self._handle_click(event.pos)
            
            # Update simulation state if not paused
            if not self.paused:
                self.grid.update()
            
            # Get current statistics
            stats = self.grid.get_population_stats()
            
            # Render current state
            self.renderer.draw(self.grid.grid, stats, self.simulation_speed, self.paused)
            
            # Control frame rate with speed multiplier
            self.clock.tick(FRAME_RATE * self.simulation_speed)
        
        pygame.quit()
    
    def _handle_click(self, pos):
        """Handle mouse clicks on UI elements."""
        # Check if click is in control panel
        if pos[0] > WINDOW_SIZE:
            action = self.renderer.handle_click(pos)
            if action == "slower":
                self.simulation_speed = max(0.25, self.simulation_speed - 0.25)
            elif action == "faster":
                self.simulation_speed = min(4.0, self.simulation_speed + 0.25)

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run() 