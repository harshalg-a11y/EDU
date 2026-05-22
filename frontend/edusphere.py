"""
EduSphere Central - Calendar Attendance Matrix Component
Pure Python Reflex frontend with pristine calendar grid layout.
6 classroom rows × 24 academic calendar blocks with dynamic color-coding.
"""

import reflex as rx
from typing import List, Dict, Tuple
from enum import Enum as PyEnum


# ============================================================================
#    DESIGN SYSTEM - Color Palette & Typography
# ============================================================================

class ColorToken(str, PyEnum):
    """Gemini-inspired color palette."""
    BACKGROUND_DEEP = "#080A10"           # Deep space black (sidebar)
    CARD_SLATE = "#121622"                # Deep slate (content canvas)
    BORDER_LASER = "#1E1F2E"              # Thin divider accent
    TEXT_PRIMARY = "#FFFFFF"              # Pure white text
    TEXT_SECONDARY = "#A0A0A0"            # Muted gray
    ACCENT_PRIMARY = "#6B5AFF"            # Purple accent (Gemini-inspired)
    ACCENT_HOVER = "#7D6FFF"              # Hover state
    STATUS_SUCCESS = "#00D084"            # Success green
    STATUS_WARNING = "#FFA500"            # Warning amber
    STATUS_CRITICAL = "#FF6B6B"           # Critical red
    
    # Calendar grid color variants (emerald, amber, deep slate)
    GRID_EMERALD_100 = "#10B981"          # Emerald at 10% opacity
    GRID_EMERALD_50 = "#059669"           # Emerald at 5% opacity
    GRID_AMBER_100 = "#F59E0B"            # Amber at 10% opacity
    GRID_AMBER_50 = "#D97706"             # Amber at 5% opacity
    GRID_SLATE_100 = "#4B5563"            # Deep slate at 10% opacity
    GRID_SLATE_50 = "#2D3748"             # Deep slate at 5% opacity


class FontFamily(str, PyEnum):
    """Typography stack."""
    PRIMARY = "Inter, system-ui, -apple-system, sans-serif"
    MONO = "Courier New, monospace"


# ============================================================================
#    DATA STRUCTURES - Calendar Grid Configuration
# ============================================================================

class SchedulingDensity(str, PyEnum):
    """Traffic density levels for color coding."""
    LOW = "low"           # Emerald (underutilized)
    MEDIUM = "medium"     # Amber (optimal)
    HIGH = "high"         # Deep slate (overutilized)


def generate_calendar_grid_data() -> List[List[Tuple[str, SchedulingDensity]]]:
    """
    Generate 6×24 calendar matrix with mock scheduling density data.
    
    Returns:
        6 rows × 24 columns matrix with (block_label, density) tuples
    """
    import random
    
    rows_count = 6
    cols_count = 24
    
    grid_data = []
    for row in range(rows_count):
        row_data = []
        for col in range(cols_count):
            # Generate block label (Week1-Mon, Week2-Tue, etc.)
            week_num = (col // 3) + 1
            days = ["Mon", "Tue", "Wed"]
            day_label = days[col % 3]
            block_label = f"W{week_num}-{day_label}"
            
            # Assign random density with bias toward medium
            rand = random.random()
            if rand < 0.25:
                density = SchedulingDensity.LOW
            elif rand < 0.70:
                density = SchedulingDensity.MEDIUM
            else:
                density = SchedulingDensity.HIGH
            
            row_data.append((block_label, density))
        grid_data.append(row_data)
    
    return grid_data


def get_density_color(density: SchedulingDensity) -> Tuple[str, str]:
    """
    Map density level to color and opacity.
    
    Args:
        density: SchedulingDensity enum value
        
    Returns:
        Tuple of (background_color, border_color)
    """
    color_map = {
        SchedulingDensity.LOW: (
            "rgba(16, 185, 129, 0.15)",    # Emerald with 15% opacity
            "rgba(16, 185, 129, 0.4)"      # Emerald border
        ),
        SchedulingDensity.MEDIUM: (
            "rgba(245, 158, 11, 0.15)",    # Amber with 15% opacity
            "rgba(245, 158, 11, 0.4)"      # Amber border
        ),
        SchedulingDensity.HIGH: (
            "rgba(75, 85, 99, 0.15)",      # Deep slate with 15% opacity
            "rgba(75, 85, 99, 0.4)"        # Deep slate border
        ),
    }
    return color_map.get(density, color_map[SchedulingDensity.MEDIUM])


# ============================================================================
#    CALENDAR GRID COMPONENT - Pristine Matrix Layout
# ============================================================================

def calendar_attendance_grid() -> rx.Component:
    """
    Pristine calendar attendance matrix grid component.
    
    Features:
    - 6 classroom rows (Dist 1-6) × 24 academic calendar blocks (Week×Day)
    - Dynamic color-coding by scheduling traffic density
    - Row labels on left (Dist 1, Dist 2, etc.)
    - Column headers with Mon/Tue/Wed pattern
    - High-contrast micro-boxes with sharp rendering
    - Fixed height without overflow in card container
    
    Returns:
        Reflex component with fully populated grid
    """
    
    # Generate calendar data
    grid_data = generate_calendar_grid_data()
    
    # District/classroom row labels
    district_labels = [f"Dist {i+1}" for i in range(6)]
    
    # Week and day headers (simplified for first few weeks)
    week_headers = []
    for week in range(8):  # 24 columns = 8 weeks × 3 days
        week_headers.append(f"W{week+1}")
    
    day_cycle = ["Mon", "Tue", "Wed"]
    
    return rx.box(
        rx.vstack(
            # Title section
            rx.box(
                rx.text(
                    "Calendar Attendance",
                    font_size="1rem",
                    font_weight="600",
                    color=ColorToken.TEXT_PRIMARY,
                    letter_spacing="0.05em",
                    font_family=FontFamily.PRIMARY,
                ),
                padding="0.75rem 0",
            ),
            
            # Calendar grid container
            rx.box(
                # Main grid wrapper
                rx.vstack(
                    # Column header row with day labels
                    rx.hstack(
                        # Empty corner cell for row labels
                        rx.box(width="3.5rem", height="1.75rem"),
                        
                        # Day of week headers (Mon, Tue, Wed repeated)
                        rx.hstack(
                            *[
                                rx.box(
                                    rx.text(
                                        day_cycle[col % 3],
                                        font_size="0.65rem",
                                        font_weight="600",
                                        color=ColorToken.TEXT_SECONDARY,
                                        text_align="center",
                                        width="100%",
                                    ),
                                    width="2.5rem",
                                    height="1.75rem",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                )
                                for col in range(24)
                            ],
                            spacing="0.25rem",
                            width="100%",
                        ),
                        
                        spacing="0.5rem",
                        width="100%",
                        align_items="center",
                    ),
                    
                    # Data rows (6 classrooms)
                    rx.vstack(
                        *[
                            rx.hstack(
                                # Row label (District)
                                rx.box(
                                    rx.text(
                                        district_labels[row_idx],
                                        font_size="0.7rem",
                                        font_weight="600",
                                        color=ColorToken.TEXT_PRIMARY,
                                        text_align="center",
                                        width="100%",
                                    ),
                                    width="3.5rem",
                                    height="2rem",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    border_right=f"1px solid {ColorToken.BORDER_LASER}",
                                    padding_right="0.5rem",
                                ),
                                
                                # Grid cells for this row (24 columns)
                                rx.hstack(
                                    *[
                                        rx.box(
                                            rx.vstack(
                                                rx.text(
                                                    grid_data[row_idx][col_idx][0],
                                                    font_size="0.55rem",
                                                    font_weight="500",
                                                    color=ColorToken.TEXT_PRIMARY,
                                                    text_align="center",
                                                    width="100%",
                                                    no_of_lines=1,
                                                ),
                                                spacing="0",
                                            ),
                                            width="2.5rem",
                                            height="2rem",
                                            background_color=get_density_color(grid_data[row_idx][col_idx][1])[0],
                                            border=f"1px solid {get_density_color(grid_data[row_idx][col_idx][1])[1]}",
                                            border_radius="0.375rem",
                                            display="flex",
                                            align_items="center",
                                            justify_content="center",
                                            padding="0.25rem",
                                            transition="all 0.2s ease",
                                            _hover={
                                                "background_color": get_density_color(grid_data[row_idx][col_idx][1])[1],
                                                "box_shadow": f"0 2px 8px {get_density_color(grid_data[row_idx][col_idx][1])[1]}",
                                            },
                                            cursor="pointer",
                                        )
                                        for col_idx in range(24)
                                    ],
                                    spacing="0.25rem",
                                    width="100%",
                                    wrap="nowrap",
                                ),
                                
                                spacing="0.5rem",
                                width="100%",
                                align_items="center",
                            )
                            for row_idx in range(6)
                        ],
                        spacing="0.5rem",
                        width="100%",
                    ),
                    
                    spacing="0.5rem",
                    width="100%",
                ),
                
                padding="1.25rem",
                background_color=ColorToken.CARD_SLATE,
                border=f"1px solid {ColorToken.BORDER_LASER}",
                border_radius="0.75rem",
                overflow_x="auto",
                overflow_y="hidden",
                width="100%",
                max_height="16rem",  # Fixed height to prevent overflow
            ),
            
            # Legend
            rx.hstack(
                rx.hstack(
                    rx.box(
                        width="0.75rem",
                        height="0.75rem",
                        background_color="rgba(16, 185, 129, 0.4)",
                        border_radius="0.25rem",
                    ),
                    rx.text(
                        "Low Density",
                        font_size="0.7rem",
                        color=ColorToken.TEXT_SECONDARY,
                        font_family=FontFamily.PRIMARY,
                    ),
                    spacing="0.5rem",
                ),
                rx.hstack(
                    rx.box(
                        width="0.75rem",
                        height="0.75rem",
                        background_color="rgba(245, 158, 11, 0.4)",
                        border_radius="0.25rem",
                    ),
                    rx.text(
                        "Medium Density",
                        font_size="0.7rem",
                        color=ColorToken.TEXT_SECONDARY,
                        font_family=FontFamily.PRIMARY,
                    ),
                    spacing="0.5rem",
                ),
                rx.hstack(
                    rx.box(
                        width="0.75rem",
                        height="0.75rem",
                        background_color="rgba(75, 85, 99, 0.4)",
                        border_radius="0.25rem",
                    ),
                    rx.text(
                        "High Density",
                        font_size="0.7rem",
                        color=ColorToken.TEXT_SECONDARY,
                        font_family=FontFamily.PRIMARY,
                    ),
                    spacing="0.5rem",
                ),
                spacing="1.5rem",
                padding="0.75rem 0",
                justify_content="flex-start",
            ),
            
            spacing="1rem",
            width="100%",
        ),
        width="100%",
        padding="0",
    )


# ============================================================================
#    CONTAINER EXPORT
# ============================================================================

def get_calendar_attendance_component() -> rx.Component:
    """
    Export calendar attendance grid for integration into dashboard.
    
    Returns:
        Reflex component ready for embedding
    """
    return calendar_attendance_grid()
