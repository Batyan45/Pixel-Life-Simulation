import pygame
import numpy as np
import random
from config import *

# Initialize Pygame
pygame.init()
pygame.font.init()

class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.stats_font = pygame.font.SysFont('Arial', STATS_FONT_SIZE)
        self.frame_count = 0
        
        # Initialize grid with zeros (empty cells)
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        
        # Place each species in their respective areas
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
        stats = {}
        unique, counts = np.unique(self.grid, return_counts=True)
        for species_id in SPECIES.keys():
            stats[species_id] = 0
        for value, count in zip(unique, counts):
            if value != 0:  # Skip empty cells
                stats[value] = count
        return stats
    
    def update(self):
        new_grid = self.grid.copy()
        
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                species_id = self.grid[x, y]
                if species_id != 0:  # If cell is not empty
                    species_data = SPECIES[species_id]
                    
                    # Movement
                    if random.random() < species_data['movement_chance']:
                        dx, dy = random.choice(MOVEMENT_DIRECTIONS)
                        new_x = (x + dx) % GRID_SIZE
                        new_y = (y + dy) % GRID_SIZE
                        
                        # If target cell is empty, move there
                        if new_grid[new_x, new_y] == 0:
                            new_grid[new_x, new_y] = species_id
                            new_grid[x, y] = 0
                        
                        # If target cell contains different species, fight
                        elif new_grid[new_x, new_y] != species_id:
                            opponent_id = new_grid[new_x, new_y]
                            attacker_strength = species_data['combat_strength']
                            defender_strength = SPECIES[opponent_id]['combat_strength']
                            
                            # Combat outcome based on relative strengths
                            if random.random() < attacker_strength / (attacker_strength + defender_strength):
                                new_grid[new_x, new_y] = species_id
                    
                    # Reproduction
                    if random.random() < species_data['reproduction_chance']:
                        # Find empty neighbor cell
                        random.shuffle(MOVEMENT_DIRECTIONS)
                        for dx, dy in MOVEMENT_DIRECTIONS:
                            reproduce_x = (x + dx) % GRID_SIZE
                            reproduce_y = (y + dy) % GRID_SIZE
                            if new_grid[reproduce_x, reproduce_y] == 0:
                                new_grid[reproduce_x, reproduce_y] = species_id
                                break
        
        self.grid = new_grid
        self.frame_count += 1
    
    def draw_stats(self):
        if not SHOW_STATS or self.frame_count % STATS_UPDATE_RATE != 0:
            return
            
        stats = self.get_population_stats()
        y_offset = 10
        
        for species_id, count in stats.items():
            species_data = SPECIES[species_id]
            text = f"{species_data['name']}: {count}"
            text_surface = self.stats_font.render(text, True, species_data['color'])
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += STATS_FONT_SIZE + 5
    
    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw grid lines if enabled
        if SHOW_GRID:
            for x in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, WINDOW_SIZE))
                pygame.draw.line(self.screen, GRID_COLOR, (0, x), (WINDOW_SIZE, x))
        
        # Draw species
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                species_id = self.grid[x, y]
                if species_id != 0:
                    color = SPECIES[species_id]['color']
                    pygame.draw.rect(self.screen, color,
                                   (y * CELL_SIZE, x * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
        
        # Draw statistics
        self.draw_stats()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.update()
            self.draw()
            self.clock.tick(FRAME_RATE)
        
        pygame.quit()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run() 