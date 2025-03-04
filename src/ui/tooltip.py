"""
Tooltip component for displaying hover information.
"""

import pygame
import pygame.gfxdraw

class Tooltip:
    @staticmethod
    def draw(surface, pos, text, font, bg_color, text_color, padding):
        """Draw a modern tooltip at the specified position."""
        # Render text
        text_surface = font.render(text, True, text_color)
        text_width, text_height = text_surface.get_size()
        
        # Calculate tooltip dimensions
        tooltip_width = text_width + padding * 2
        tooltip_height = text_height + padding * 2
        
        # Calculate position (try to keep tooltip on screen)
        x, y = pos
        screen_width, screen_height = surface.get_size()
        
        # Adjust x position if tooltip would go off screen
        if x + tooltip_width + 10 > screen_width:
            x = screen_width - tooltip_width - 10
        else:
            x += 10
            
        # Adjust y position if tooltip would go off screen
        if y + tooltip_height + 10 > screen_height:
            y = y - tooltip_height - 5
        else:
            y += 10
            
        # Create tooltip surface with alpha
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        
        # Draw rounded rectangle background
        rect = pygame.Rect(0, 0, tooltip_width, tooltip_height)
        pygame.draw.rect(tooltip_surface, bg_color, rect, border_radius=4)
        
        # Draw text
        text_x = padding
        text_y = padding
        tooltip_surface.blit(text_surface, (text_x, text_y))
        
        # Draw tooltip on main surface
        surface.blit(tooltip_surface, (x, y)) 