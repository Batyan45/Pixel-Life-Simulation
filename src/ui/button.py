"""
Button UI element for the simulation.
"""

import pygame
import pygame.gfxdraw
from config import (
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    BORDER_RADIUS,
    ENABLE_ANTIALIASING
)

class Button:
    def __init__(self, text, action, width=None, height=30):
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        self.rect = None
        self.font = None
        
    def draw(self, surface, pos, font, width=None):
        """Draw the button on the surface."""
        self.font = font
        button_width = width if width is not None else self.width
        button_rect = pygame.Rect(pos[0], pos[1], button_width, self.height)
        self.rect = button_rect
        
        # Get mouse position and check hover
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Draw button background
        color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        self._draw_rounded_rect(surface, button_rect, color)
        
        # Draw button text
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        """Check if button was clicked."""
        return self.rect is not None and self.rect.collidepoint(pos)
    
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