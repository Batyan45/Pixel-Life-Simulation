"""
Modern button component with hover effects and tooltips.
"""

import pygame
import pygame.gfxdraw
from config import (
    BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR,
    BUTTON_HEIGHT, BUTTON_DISABLED_COLOR, BORDER_RADIUS,
    HOVER_TRANSITION_SPEED
)

class Button:
    def __init__(self, text, action, tooltip=None, icon=None, disabled=False):
        """Initialize a modern button."""
        self.text = text
        self.action = action
        self.tooltip = tooltip
        self.icon = icon
        self.disabled = disabled
        self.hover = 0.0  # Hover animation progress (0.0 to 1.0)
        self.rect = None
        
    def draw(self, surface, pos, font, width):
        """Draw the button with hover effects."""
        x, y = pos
        self.rect = pygame.Rect(x, y, width, BUTTON_HEIGHT)
        
        # Update hover animation
        mouse_pos = pygame.mouse.get_pos()
        target_hover = 1.0 if self.is_hovered(mouse_pos) and not self.disabled else 0.0
        self.hover += (target_hover - self.hover) * HOVER_TRANSITION_SPEED
        
        # Calculate current color based on hover state
        if self.disabled:
            color = BUTTON_DISABLED_COLOR
        else:
            color = tuple(
                int(BUTTON_COLOR[i] * (1 - self.hover) + BUTTON_HOVER_COLOR[i] * self.hover)
                for i in range(3)
            )
        
        # Draw button background with rounded corners
        pygame.draw.rect(
            surface,
            color,
            self.rect,
            border_radius=BORDER_RADIUS
        )
        
        # Draw text with icon
        text_surface = font.render(
            f"{self.icon + ' ' if self.icon else ''}{self.text}",
            True,
            BUTTON_TEXT_COLOR
        )
        
        # Center text
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (BUTTON_HEIGHT - text_surface.get_height()) // 2
        
        # Draw text shadow for depth
        shadow_surface = font.render(
            f"{self.icon + ' ' if self.icon else ''}{self.text}",
            True,
            (0, 0, 0, 100)
        )
        surface.blit(shadow_surface, (text_x, text_y + 1))
        surface.blit(text_surface, (text_x, text_y))
        
        # Draw hover highlight
        if self.hover > 0 and not self.disabled:
            highlight = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            pygame.draw.rect(
                highlight,
                (255, 255, 255, int(30 * self.hover)),
                highlight.get_rect(),
                border_radius=BORDER_RADIUS
            )
            surface.blit(highlight, self.rect)
    
    def is_hovered(self, pos):
        """Check if the mouse is over the button."""
        return self.rect is not None and self.rect.collidepoint(pos)
    
    def is_clicked(self, pos):
        """Check if the button was clicked."""
        return not self.disabled and self.is_hovered(pos)
    
    def get_tooltip(self):
        """Get the button's tooltip text."""
        return self.tooltip if self.is_hovered(pygame.mouse.get_pos()) else None 