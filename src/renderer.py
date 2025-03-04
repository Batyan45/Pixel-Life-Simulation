"""
Visualization module for the life simulation.
"""

import pygame
import pygame.gfxdraw
import numpy as np
from config import (
    WINDOW_SIZE, WINDOW_TITLE, GRID_SIZE, CELL_SIZE,
    GRID_COLOR, BACKGROUND_COLOR, PANEL_COLOR,
    PANEL_BORDER_COLOR, BORDER_RADIUS, TITLE_BAR_HEIGHT,
    CONTROL_PANEL_WIDTH, STATS_UPDATE_RATE,
    STATS_FONT_SIZE, STATS_TITLE_FONT_SIZE, STATS_FONT,
    STATS_COLOR, STATS_TITLE_COLOR, BUTTON_COLOR,
    BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, SLIDER_COLOR,
    SLIDER_HANDLE_COLOR, ENABLE_ANTIALIASING, SPECIES,
    GRADIENT_TOP, GRADIENT_BOTTOM, PADDING, BUTTON_HEIGHT,
    STATS_GRAPH_HEIGHT, STATS_HISTORY_LENGTH,
    TOOLTIP_BACKGROUND, TOOLTIP_TEXT_COLOR, TOOLTIP_PADDING,
    TOOLTIP_FONT_SIZE, TOOLTIP_DELAY, BUTTON_DISABLED_COLOR,
    SLIDER_HOVER_COLOR, HOVER_TRANSITION_SPEED, SHOW_GRID,
    EXTINCT_COLOR
)
from src.ui.button import Button
from src.ui.tooltip import Tooltip
from src.ui.graph import PopulationGraph

class Renderer:
    def __init__(self):
        """Initialize the renderer."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE + CONTROL_PANEL_WIDTH, WINDOW_SIZE))
        pygame.display.set_caption(WINDOW_TITLE)
        
        # Initialize fonts
        self.title_font = pygame.font.SysFont(STATS_FONT, STATS_TITLE_FONT_SIZE, bold=True)
        self.stats_font = pygame.font.SysFont(STATS_FONT, STATS_FONT_SIZE)
        self.tooltip_font = pygame.font.SysFont(STATS_FONT, TOOLTIP_FONT_SIZE)
        
        # Create surfaces
        self.simulation_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        self.control_panel = pygame.Surface((CONTROL_PANEL_WIDTH, WINDOW_SIZE), pygame.SRCALPHA)
        self.title_bar = pygame.Surface((WINDOW_SIZE + CONTROL_PANEL_WIDTH, TITLE_BAR_HEIGHT), pygame.SRCALPHA)
        
        # Initialize UI elements
        self.frame_count = 0
        self.last_stats = {}
        self.population_history = {species_id: [] for species_id in SPECIES.keys()}
        self.population_graph = PopulationGraph(
            CONTROL_PANEL_WIDTH - PADDING * 2,
            STATS_GRAPH_HEIGHT,
            STATS_HISTORY_LENGTH
        )
        
        # Create buttons with tooltips
        self.slower_button = Button(
            "Slower",
            "slower",
            tooltip="Decrease simulation speed (Left click)"
        )
        self.faster_button = Button(
            "Faster",
            "faster",
            tooltip="Increase simulation speed (Left click)"
        )
        self.grid_button = Button(
            "Toggle Grid",
            "toggle_grid",
            tooltip="Show/Hide grid lines"
        )
        
        # Grid visibility state
        self.show_grid = SHOW_GRID
        
        # Create gradient surface
        self.gradient_surface = self._create_gradient_surface()
        
    def draw(self, grid, stats, speed, paused, step_count, extinction_data):
        """Draw the current state of the simulation."""
        # Draw gradient background
        self.screen.blit(self.gradient_surface, (0, 0))
        
        # Clear main surfaces
        self.simulation_surface.fill(BACKGROUND_COLOR)
        self.control_panel.fill((0, 0, 0, 0))  # Clear with transparency
        self.title_bar.fill((0, 0, 0, 0))  # Clear with transparency
        
        # Draw simulation elements with modern cell styling
        self._draw_species(grid)
        
        # Update population history
        if self.frame_count % STATS_UPDATE_RATE == 0:
            self.last_stats = stats
            for species_id, count in stats.items():
                self.population_history[species_id].append(count)
                if len(self.population_history[species_id]) > STATS_HISTORY_LENGTH:
                    self.population_history[species_id].pop(0)
        
        # Draw UI elements with modern styling
        self._draw_title_bar(paused, step_count)
        self._draw_control_panel(stats, speed, extinction_data)
        
        # Combine surfaces with proper alpha blending
        self.screen.blit(self.title_bar, (0, 0))
        self.screen.blit(self.simulation_surface, (0, TITLE_BAR_HEIGHT))
        self.screen.blit(self.control_panel, (WINDOW_SIZE, TITLE_BAR_HEIGHT))
        
        # Draw tooltips last
        mouse_pos = pygame.mouse.get_pos()
        self._handle_tooltips(mouse_pos)
        
        pygame.display.flip()
        self.frame_count += 1
    
    def _create_gradient_surface(self):
        """Create a vertical gradient surface for the background."""
        surface = pygame.Surface((WINDOW_SIZE + CONTROL_PANEL_WIDTH, WINDOW_SIZE))
        for y in range(WINDOW_SIZE):
            progress = y / WINDOW_SIZE
            color = [
                int(GRADIENT_TOP[i] * (1 - progress) + GRADIENT_BOTTOM[i] * progress)
                for i in range(3)
            ]
            pygame.draw.line(surface, color, (0, y), (WINDOW_SIZE + CONTROL_PANEL_WIDTH, y))
        return surface
    
    def _draw_species(self, grid):
        """Draw all species on the grid with modern styling."""
        # Draw grid lines if enabled
        if self.show_grid:
            for x in range(GRID_SIZE + 1):
                pygame.draw.line(
                    self.simulation_surface,
                    GRID_COLOR,
                    (x * CELL_SIZE, 0),
                    (x * CELL_SIZE, WINDOW_SIZE)
                )
                pygame.draw.line(
                    self.simulation_surface,
                    GRID_COLOR,
                    (0, x * CELL_SIZE),
                    (WINDOW_SIZE, x * CELL_SIZE)
                )

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                species_id = grid[x, y]
                if species_id != 0:
                    color = SPECIES[species_id]['color']
                    rect = pygame.Rect(
                        y * CELL_SIZE + (1 if self.show_grid else 0),
                        x * CELL_SIZE + (1 if self.show_grid else 0),
                        CELL_SIZE - (2 if self.show_grid else 0),
                        CELL_SIZE - (2 if self.show_grid else 0)
                    )
                    if ENABLE_ANTIALIASING and CELL_SIZE > 4:
                        self._draw_rounded_rect(self.simulation_surface, rect, color)
                    else:
                        pygame.draw.rect(self.simulation_surface, color, rect)
    
    def _draw_title_bar(self, paused, step_count):
        """Draw the title bar with modern styling."""
        # Draw semi-transparent background
        pygame.draw.rect(
            self.title_bar,
            PANEL_COLOR,
            (0, 0, WINDOW_SIZE + CONTROL_PANEL_WIDTH, TITLE_BAR_HEIGHT)
        )
        
        # Draw title with step count (removed dash)
        title_text = f"{WINDOW_TITLE} {'(Paused)' if paused else ''} Step: {step_count:,}"
        title = self.title_font.render(title_text, True, STATS_TITLE_COLOR)
        self.title_bar.blit(title, (PADDING, (TITLE_BAR_HEIGHT - title.get_height()) // 2))
        
        # Draw subtle bottom border
        pygame.draw.line(
            self.title_bar,
            PANEL_BORDER_COLOR,
            (0, TITLE_BAR_HEIGHT - 1),
            (WINDOW_SIZE + CONTROL_PANEL_WIDTH, TITLE_BAR_HEIGHT - 1)
        )
    
    def _draw_control_panel(self, stats, speed, extinction_data):
        """Draw the control panel with modern styling."""
        # Draw panel background with rounded corners
        panel_rect = pygame.Rect(0, 0, CONTROL_PANEL_WIDTH, WINDOW_SIZE)
        pygame.draw.rect(self.control_panel, PANEL_COLOR, panel_rect, border_radius=BORDER_RADIUS)
        
        y_offset = PADDING
        
        # Draw statistics section
        stats_title = self.title_font.render("Statistics", True, STATS_TITLE_COLOR)
        self.control_panel.blit(stats_title, (PADDING, y_offset))
        y_offset += stats_title.get_height() + PADDING
        
        # Draw population graph
        if self.last_stats:
            self.population_graph.draw(
                self.control_panel,
                (PADDING, y_offset),
                self.population_history,
                SPECIES
            )
            y_offset += STATS_GRAPH_HEIGHT + PADDING
            
            # Draw species statistics with modern indicators
            for species_id, count in self.last_stats.items():
                species_data = SPECIES[species_id]
                
                # Draw species indicator with gradient
                indicator_rect = pygame.Rect(PADDING, y_offset, 12, 12)
                self._draw_rounded_rect(
                    self.control_panel,
                    indicator_rect,
                    species_data['color']
                )
                
                # Draw species name and count
                text = f"{species_data['name']}: {count:,}"
                if count == 0:
                    extinction_step = extinction_data.get(species_id, 0)
                    # Show extinction info on the same line
                    text += f" (†{extinction_step:,})"
                    text_surface = self.stats_font.render(text, True, EXTINCT_COLOR)
                    self.control_panel.blit(text_surface, (PADDING + 20, y_offset))
                else:
                    text_surface = self.stats_font.render(text, True, STATS_COLOR)
                    self.control_panel.blit(text_surface, (PADDING + 20, y_offset))
                
                y_offset += text_surface.get_height() + PADDING
        
        y_offset += PADDING
        
        # Draw speed control section
        speed_title = self.title_font.render("Controls", True, STATS_TITLE_COLOR)
        self.control_panel.blit(speed_title, (PADDING, y_offset))
        y_offset += speed_title.get_height() + PADDING // 2
        
        # Speed indicator with modern styling
        speed_text = f"Current Speed: {speed:.2f}x"
        speed_surface = self.stats_font.render(speed_text, True, STATS_COLOR)
        self.control_panel.blit(speed_surface, (PADDING, y_offset))
        y_offset += speed_surface.get_height() + PADDING
        
        # Draw speed control buttons
        button_width = CONTROL_PANEL_WIDTH - PADDING * 2
        self.slower_button.draw(
            self.control_panel,
            (PADDING, y_offset),
            self.stats_font,
            button_width
        )
        y_offset += BUTTON_HEIGHT + PADDING // 2
        self.faster_button.draw(
            self.control_panel,
            (PADDING, y_offset),
            self.stats_font,
            button_width
        )
        y_offset += BUTTON_HEIGHT + PADDING
        
        # Draw grid toggle button
        self.grid_button.text = "Hide Grid" if self.show_grid else "Show Grid"
        self.grid_button.draw(
            self.control_panel,
            (PADDING, y_offset),
            self.stats_font,
            button_width
        )
    
    def _handle_tooltips(self, mouse_pos):
        """Handle tooltip rendering for UI elements."""
        x = mouse_pos[0] - WINDOW_SIZE
        y = mouse_pos[1] - TITLE_BAR_HEIGHT
        
        # Check button tooltips
        for button in [self.slower_button, self.faster_button, self.grid_button]:
            if button.is_hovered((x, y)):
                tooltip_text = button.get_tooltip()
                if tooltip_text:
                    Tooltip.draw(
                        self.screen,
                        mouse_pos,
                        tooltip_text,
                        self.tooltip_font,
                        TOOLTIP_BACKGROUND,
                        TOOLTIP_TEXT_COLOR,
                        TOOLTIP_PADDING
                    )
                break
    
    def handle_click(self, pos):
        """Handle clicks on UI elements."""
        x = pos[0] - WINDOW_SIZE
        y = pos[1] - TITLE_BAR_HEIGHT
        click_pos = (x, y)
        
        if self.slower_button.is_clicked(click_pos):
            return "slower"
        elif self.faster_button.is_clicked(click_pos):
            return "faster"
        elif self.grid_button.is_clicked(click_pos):
            self.show_grid = not self.show_grid
            return "toggle_grid"
        
        return None
    
    def _draw_rounded_rect(self, surface, rect, color):
        """Draw a rounded rectangle with anti-aliasing and optional gradient."""
        if ENABLE_ANTIALIASING:
            pygame.gfxdraw.box(surface, rect, color)
            if rect.width > BORDER_RADIUS * 2 and rect.height > BORDER_RADIUS * 2:
                pygame.gfxdraw.aacircle(
                    surface,
                    rect.left + BORDER_RADIUS,
                    rect.top + BORDER_RADIUS,
                    BORDER_RADIUS,
                    color
                )
                pygame.gfxdraw.aacircle(
                    surface,
                    rect.right - BORDER_RADIUS - 1,
                    rect.top + BORDER_RADIUS,
                    BORDER_RADIUS,
                    color
                )
                pygame.gfxdraw.aacircle(
                    surface,
                    rect.left + BORDER_RADIUS,
                    rect.bottom - BORDER_RADIUS - 1,
                    BORDER_RADIUS,
                    color
                )
                pygame.gfxdraw.aacircle(
                    surface,
                    rect.right - BORDER_RADIUS - 1,
                    rect.bottom - BORDER_RADIUS - 1,
                    BORDER_RADIUS,
                    color
                )
        else:
            pygame.draw.rect(surface, color, rect) 