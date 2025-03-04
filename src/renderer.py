"""
Visualization module for the life simulation.
"""

import pygame
import pygame.gfxdraw
from config import (
    WINDOW_SIZE, WINDOW_TITLE, GRID_SIZE, CELL_SIZE,
    GRID_COLOR, BACKGROUND_COLOR, PANEL_COLOR,
    PANEL_BORDER_COLOR, BORDER_RADIUS, TITLE_BAR_HEIGHT,
    CONTROL_PANEL_WIDTH, STATS_UPDATE_RATE,
    STATS_FONT_SIZE, STATS_TITLE_FONT_SIZE, STATS_FONT,
    STATS_COLOR, STATS_TITLE_COLOR, BUTTON_COLOR,
    BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, SLIDER_COLOR,
    SLIDER_HANDLE_COLOR, ENABLE_ANTIALIASING, SPECIES
)
from src.ui.button import Button

class Renderer:
    def __init__(self):
        """Initialize the renderer."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE + CONTROL_PANEL_WIDTH, WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Initialize fonts
        self.title_font = pygame.font.SysFont(STATS_FONT, STATS_TITLE_FONT_SIZE, bold=True)
        self.stats_font = pygame.font.SysFont(STATS_FONT, STATS_FONT_SIZE)
        self.button_font = pygame.font.SysFont(STATS_FONT, STATS_FONT_SIZE)
        
        # Create surfaces
        self.simulation_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        self.control_panel = pygame.Surface((CONTROL_PANEL_WIDTH, WINDOW_SIZE))
        self.title_bar = pygame.Surface((WINDOW_SIZE + CONTROL_PANEL_WIDTH, TITLE_BAR_HEIGHT))
        
        self.frame_count = 0
        self.last_stats = {}
        
        # Create buttons
        self.slower_button = Button("- Slower", "slower")
        self.faster_button = Button("+ Faster", "faster")
        
    def draw(self, grid, stats, speed, paused):
        """Draw the current state of the simulation."""
        # Clear main surfaces
        self.screen.fill(BACKGROUND_COLOR)
        self.simulation_surface.fill(BACKGROUND_COLOR)
        self.control_panel.fill(PANEL_COLOR)
        self.title_bar.fill(PANEL_COLOR)
        
        # Draw simulation elements
        self._draw_species(grid)
        
        # Draw UI elements
        self._draw_title_bar(paused)
        self._draw_control_panel(stats, speed)
        
        # Combine surfaces
        self.screen.blit(self.title_bar, (0, 0))
        self.screen.blit(self.simulation_surface, (0, TITLE_BAR_HEIGHT))
        self.screen.blit(self.control_panel, (WINDOW_SIZE, TITLE_BAR_HEIGHT))
        
        pygame.display.flip()
        self.frame_count += 1
    
    def _draw_species(self, grid):
        """Draw all species on the grid with modern styling."""
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                species_id = grid[x, y]
                if species_id != 0:
                    color = SPECIES[species_id]['color']
                    rect = pygame.Rect(
                        y * CELL_SIZE,
                        x * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    if ENABLE_ANTIALIASING and CELL_SIZE > 4:
                        self._draw_rounded_rect(self.simulation_surface, rect, color)
                    else:
                        pygame.draw.rect(self.simulation_surface, color, rect)
    
    def _draw_title_bar(self, paused):
        """Draw the title bar with controls."""
        # Draw title
        title_text = f"{WINDOW_TITLE} {'(Paused)' if paused else ''}"
        title = self.title_font.render(title_text, True, STATS_TITLE_COLOR)
        self.title_bar.blit(title, (20, (TITLE_BAR_HEIGHT - title.get_height()) // 2))
        
        # Draw border line
        pygame.draw.line(
            self.title_bar,
            PANEL_BORDER_COLOR,
            (0, TITLE_BAR_HEIGHT - 1),
            (WINDOW_SIZE + CONTROL_PANEL_WIDTH, TITLE_BAR_HEIGHT - 1)
        )
    
    def _draw_control_panel(self, stats, speed):
        """Draw the control panel with statistics and controls."""
        y_offset = 20
        
        # Draw panel title
        stats_title = self.title_font.render("Statistics", True, STATS_TITLE_COLOR)
        self.control_panel.blit(stats_title, (20, y_offset))
        y_offset += stats_title.get_height() + 20
        
        # Update stats if it's time
        if self.frame_count % STATS_UPDATE_RATE == 0:
            self.last_stats = stats
        
        # Draw statistics for each species
        if self.last_stats:
            for species_id, count in self.last_stats.items():
                species_data = SPECIES[species_id]
                # Draw species color indicator
                pygame.draw.rect(
                    self.control_panel,
                    species_data['color'],
                    (20, y_offset, 12, 12),
                    border_radius=2
                )
                
                # Draw species name and count
                text = f"{species_data['name']}: {count}"
                text_surface = self.stats_font.render(text, True, STATS_COLOR)
                self.control_panel.blit(text_surface, (40, y_offset - 2))
                y_offset += 25
        
        y_offset += 20
        
        # Draw speed controls
        speed_title = self.title_font.render("Speed Control", True, STATS_TITLE_COLOR)
        self.control_panel.blit(speed_title, (20, y_offset))
        y_offset += speed_title.get_height() + 10
        
        # Speed indicator
        speed_text = f"Current Speed: {speed:.2f}x"
        speed_surface = self.stats_font.render(speed_text, True, STATS_COLOR)
        self.control_panel.blit(speed_surface, (20, y_offset))
        y_offset += 30
        
        # Draw speed control buttons
        button_width = CONTROL_PANEL_WIDTH - 40
        self.slower_button.draw(self.control_panel, (20, y_offset), self.button_font, button_width)
        y_offset += 40
        self.faster_button.draw(self.control_panel, (20, y_offset), self.button_font, button_width)
        
        # Draw border line
        pygame.draw.line(
            self.control_panel,
            PANEL_BORDER_COLOR,
            (0, 0),
            (0, WINDOW_SIZE)
        )
    
    def handle_click(self, pos):
        """Handle clicks on buttons."""
        x = pos[0] - WINDOW_SIZE
        y = pos[1] - TITLE_BAR_HEIGHT
        click_pos = (x, y)
        
        if self.slower_button.is_clicked(click_pos):
            return "slower"
        elif self.faster_button.is_clicked(click_pos):
            return "faster"
        
        return None
    
    def _draw_rounded_rect(self, surface, rect, color):
        """Draw a rounded rectangle with anti-aliasing."""
        if ENABLE_ANTIALIASING:
            pygame.gfxdraw.box(surface, rect, color)
            if rect.width > BORDER_RADIUS * 2 and rect.height > BORDER_RADIUS * 2:
                pygame.gfxdraw.aacircle(surface, rect.left + BORDER_RADIUS, rect.top + BORDER_RADIUS, BORDER_RADIUS, color)
                pygame.gfxdraw.aacircle(surface, rect.right - BORDER_RADIUS - 1, rect.top + BORDER_RADIUS, BORDER_RADIUS, color)
                pygame.gfxdraw.aacircle(surface, rect.left + BORDER_RADIUS, rect.bottom - BORDER_RADIUS - 1, BORDER_RADIUS, color)
                pygame.gfxdraw.aacircle(surface, rect.right - BORDER_RADIUS - 1, rect.bottom - BORDER_RADIUS - 1, BORDER_RADIUS, color)
        else:
            pygame.draw.rect(surface, color, rect) 