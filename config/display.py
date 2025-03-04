"""
Display configuration parameters.
"""

# Window settings
WINDOW_TITLE = "Life Simulation"

# Visual settings
SHOW_GRID = False
GRID_COLOR = (45, 49, 58)  # Slightly lighter modern gray
BACKGROUND_COLOR = (22, 27, 34)  # GitHub Dark theme inspired background
PANEL_COLOR = (33, 38, 45, 230)  # More opaque dark panel
PANEL_BORDER_COLOR = (48, 54, 61)  # Subtle border
GRADIENT_TOP = (22, 27, 34)  # Top color for background gradient
GRADIENT_BOTTOM = (13, 17, 23)  # Bottom color for background gradient

# UI Elements
TITLE_BAR_HEIGHT = 48  # Slightly taller for better spacing
CONTROL_PANEL_WIDTH = 240  # Wider panel for better layout
BORDER_RADIUS = 8  # More pronounced rounded corners
PADDING = 16  # Standard padding for elements

# Statistics display settings
SHOW_STATS = True
STATS_UPDATE_RATE = 30
STATS_FONT_SIZE = 14
STATS_TITLE_FONT_SIZE = 18
STATS_FONT = "Arial"  # Changed from Segoe UI for better compatibility
STATS_COLOR = (201, 209, 217)  # Softer text color
STATS_TITLE_COLOR = (255, 255, 255)
STATS_GRAPH_HEIGHT = 100  # Height for population graphs
STATS_HISTORY_LENGTH = 100  # Number of data points to keep

# Control panel settings
BUTTON_COLOR = (33, 138, 255)  # Modern blue
BUTTON_HOVER_COLOR = (56, 152, 255)  # Lighter blue on hover
BUTTON_DISABLED_COLOR = (48, 54, 61)  # Disabled state
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_HEIGHT = 36
BUTTON_ICON_SIZE = 16
SLIDER_COLOR = (48, 54, 61)
SLIDER_HANDLE_COLOR = (33, 138, 255)
SLIDER_HOVER_COLOR = (56, 152, 255)

# Tooltip settings
TOOLTIP_BACKGROUND = (48, 54, 61, 230)
TOOLTIP_TEXT_COLOR = (201, 209, 217)
TOOLTIP_PADDING = 8
TOOLTIP_FONT_SIZE = 12
TOOLTIP_DELAY = 0.5  # Seconds before showing tooltip

# Animation
ENABLE_ANTIALIASING = True
TRANSITION_SPEED = 0.15  # Seconds for smooth transitions
HOVER_TRANSITION_SPEED = 0.1  # Faster transitions for hover effects 