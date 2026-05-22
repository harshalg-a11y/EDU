"""
EduSphere Central - Calendar Attendance Matrix & OmniSearch Command Menu
Pure Python Reflex frontend with pristine calendar grid layout and universal command palette.
6 classroom rows × 24 academic calendar blocks with dynamic color-coding.
Google Gemini-inspired minimalistic search overlay with Cmd+K / Ctrl+K activation.
"""

import reflex as rx
from typing import List, Dict, Tuple, Optional
from enum import Enum as PyEnum
from dataclasses import dataclass


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
#    DATA STRUCTURES - Calendar & Search Configuration
# ============================================================================

class SchedulingDensity(str, PyEnum):
    """Traffic density levels for color coding."""
    LOW = "low"           # Emerald (underutilized)
    MEDIUM = "medium"     # Amber (optimal)
    HIGH = "high"         # Deep slate (overutilized)


@dataclass
class SearchResult:
    """Represents a single search result item."""
    id: str
    title: str
    description: str
    category: str  # "Student Tracks", "Room Optimization", "System Actions"
    icon: str
    action: Optional[str] = None


# ============================================================================
#    MOCK DATA - Search Index
# ============================================================================

STUDENT_TRACKS_INDEX = [
    SearchResult(
        id="student_001",
        title="View Harshal's Track",
        description="Academic pathway & progress overview",
        category="Jump to Student Tracks",
        icon="👤",
    ),
    SearchResult(
        id="student_002",
        title="Student Roster",
        description="Browse all enrolled students",
        category="Jump to Student Tracks",
        icon="👥",
    ),
    SearchResult(
        id="student_003",
        title="Graduation Audits",
        description="Check degree requirements & status",
        category="Jump to Student Tracks",
        icon="🎓",
    ),
    SearchResult(
        id="student_004",
        title="Transcript View",
        description="Academic records & GPA tracking",
        category="Jump to Student Tracks",
        icon="📋",
    ),
]

ROOM_OPTIMIZATION_INDEX = [
    SearchResult(
        id="room_001",
        title="Room 403 - Capacity Check",
        description="Verify current utilization & availability",
        category="Optimize Rooms",
        icon="🏫",
    ),
    SearchResult(
        id="room_002",
        title="Room 405 - Schedule View",
        description="Display weekly timetable & assignments",
        category="Optimize Rooms",
        icon="📅",
    ),
    SearchResult(
        id="room_003",
        title="Conflict Resolution",
        description="Trigger scheduling conflict solver",
        category="Optimize Rooms",
        icon="⚡",
    ),
    SearchResult(
        id="room_004",
        title="Asset Inventory",
        description="View all classroom resources & equipment",
        category="Optimize Rooms",
        icon="📦",
    ),
]

SYSTEM_ACTIONS_INDEX = [
    SearchResult(
        id="action_001",
        title="Run Solver",
        description="Execute constraint satisfaction algorithm",
        category="System Action Functions",
        icon="🔧",
    ),
    SearchResult(
        id="action_002",
        title="Export Report",
        description="Generate PDF/CSV scheduling report",
        category="System Action Functions",
        icon="📥",
    ),
    SearchResult(
        id="action_003",
        title="Refresh Cache",
        description="Clear and regenerate system cache",
        category="System Action Functions",
        icon="🔄",
    ),
    SearchResult(
        id="action_004",
        title="System Status",
        description="View uptime, metrics, and health indicators",
        category="System Action Functions",
        icon="📊",
    ),
    SearchResult(
        id="action_005",
        title="Settings",
        description="Configure dashboard preferences",
        category="System Action Functions",
        icon="⚙️",
    ),
]

# Combined search index
GLOBAL_SEARCH_INDEX = STUDENT_TRACKS_INDEX + ROOM_OPTIMIZATION_INDEX + SYSTEM_ACTIONS_INDEX


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
#    OMNISEARCH STATE MANAGEMENT
# ============================================================================

class OmniSearchState(rx.State):
    """
    Manages OmniSearch command menu state and filtering.
    """
    # Search input
    search_query: str = ""
    is_open: bool = False
    
    # Filtered results
    filtered_results: List[Dict[str, str]] = []
    selected_index: int = 0
    
    def toggle_search(self) -> None:
        """Toggle search panel visibility."""
        self.is_open = not self.is_open
        if not self.is_open:
            self.search_query = ""
            self.selected_index = 0
    
    def update_search(self, value: str) -> None:
        """
        Update search query and filter results dynamically.
        
        Args:
            value: Search query string
        """
        self.search_query = value.lower()
        self.selected_index = 0
        
        # Filter results
        if not self.search_query:
            self.filtered_results = [
                {
                    "id": r.id,
                    "title": r.title,
                    "description": r.description,
                    "category": r.category,
                    "icon": r.icon,
                }
                for r in GLOBAL_SEARCH_INDEX
            ]
        else:
            filtered = []
            for result in GLOBAL_SEARCH_INDEX:
                if (self.search_query in result.title.lower() or
                    self.search_query in result.description.lower() or
                    self.search_query in result.category.lower()):
                    filtered.append({
                        "id": result.id,
                        "title": result.title,
                        "description": result.description,
                        "category": result.category,
                        "icon": result.icon,
                    })
            self.filtered_results = filtered
    
    def handle_key_down(self, key: str) -> None:
        """
        Handle keyboard navigation in search results.
        
        Args:
            key: Key identifier
        """
        if key == "ArrowDown":
            self.selected_index = min(self.selected_index + 1, len(self.filtered_results) - 1)
        elif key == "ArrowUp":
            self.selected_index = max(self.selected_index - 1, 0)
        elif key == "Enter":
            # Execute selected result
            if self.filtered_results and self.selected_index < len(self.filtered_results):
                result = self.filtered_results[self.selected_index]
                self.execute_action(result["id"])
                self.is_open = False
        elif key == "Escape":
            self.is_open = False
    
    def execute_action(self, result_id: str) -> None:
        """
        Execute a search result action.
        
        Args:
            result_id: ID of result to execute
        """
        # Placeholder: would navigate/execute based on result_id
        print(f"Executing action: {result_id}")


# ============================================================================
#    OMNISEARCH COMPONENT - Sleek Command Palette
# ============================================================================

def omnisearch_panel() -> rx.Component:
    """
    Google Gemini-inspired OmniSearch command menu component.
    
    Features:
    - Keyboard activation (Cmd+K / Ctrl+K)
    - Translucent frosted background overlay
    - Pulsing violet text cursor
    - Dynamic result filtering
    - Categorized results (3 sections)
    - Arrow key navigation
    
    Returns:
        Reflex component with search overlay
    """
    return rx.box(
        # Backdrop overlay (translucent frosted background)
        rx.box(
            width="100vw",
            height="100vh",
            position="fixed",
            top="0",
            left="0",
            background_color="rgba(8, 10, 16, 0.7)",
            backdrop_filter="blur(12px)",
            z_index="1000",
            on_click=lambda: OmniSearchState.toggle_search(),
        ),
        
        # Centered search panel
        rx.box(
            rx.vstack(
                # Search input header
                rx.box(
                    rx.hstack(
                        # Search icon
                        rx.text(
                            "🔍",
                            font_size="1.25rem",
                            color=ColorToken.ACCENT_PRIMARY,
                            padding_right="0.75rem",
                        ),
                        
                        # Input field with pulsing cursor
                        rx.input(
                            placeholder="Search students, rooms, or actions...",
                            value=OmniSearchState.search_query,
                            on_change=lambda v: OmniSearchState.update_search(v),
                            on_key_down=lambda k: OmniSearchState.handle_key_down(k),
                            font_size="1rem",
                            padding="1rem",
                            background_color="transparent",
                            border="none",
                            color=ColorToken.TEXT_PRIMARY,
                            width="100%",
                            _placeholder={
                                "color": ColorToken.TEXT_SECONDARY,
                            },
                            _focus={
                                "outline": "none",
                            },
                            auto_focus=True,
                        ),
                        
                        width="100%",
                        align_items="center",
                        padding="1.5rem 1.5rem 1rem 1.5rem",
                    ),
                    border_bottom=f"1px solid {ColorToken.BORDER_LASER}",
                    width="100%",
                ),
                
                # Results section
                rx.box(
                    rx.vstack(
                        rx.cond(
                            OmniSearchState.search_query == "",
                            # Show organized categories when empty
                            rx.vstack(
                                # Jump to Student Tracks
                                rx.vstack(
                                    rx.text(
                                        "Jump to Student Tracks",
                                        font_size="0.75rem",
                                        font_weight="600",
                                        color=ColorToken.TEXT_SECONDARY,
                                        letter_spacing="0.1em",
                                        text_transform="uppercase",
                                        padding="1rem 1.5rem 0.5rem 1.5rem",
                                    ),
                                    rx.vstack(
                                        *[
                                            omnisearch_result_item(
                                                result,
                                                idx,
                                                OmniSearchState.selected_index,
                                            )
                                            for idx, result in enumerate(STUDENT_TRACKS_INDEX)
                                        ],
                                        width="100%",
                                    ),
                                    width="100%",
                                ),
                                
                                # Optimize Rooms
                                rx.vstack(
                                    rx.text(
                                        "Optimize Rooms",
                                        font_size="0.75rem",
                                        font_weight="600",
                                        color=ColorToken.TEXT_SECONDARY,
                                        letter_spacing="0.1em",
                                        text_transform="uppercase",
                                        padding="1rem 1.5rem 0.5rem 1.5rem",
                                    ),
                                    rx.vstack(
                                        *[
                                            omnisearch_result_item(
                                                result,
                                                idx + 4,
                                                OmniSearchState.selected_index,
                                            )
                                            for idx, result in enumerate(ROOM_OPTIMIZATION_INDEX)
                                        ],
                                        width="100%",
                                    ),
                                    width="100%",
                                ),
                                
                                # System Action Functions
                                rx.vstack(
                                    rx.text(
                                        "System Action Functions",
                                        font_size="0.75rem",
                                        font_weight="600",
                                        color=ColorToken.TEXT_SECONDARY,
                                        letter_spacing="0.1em",
                                        text_transform="uppercase",
                                        padding="1rem 1.5rem 0.5rem 1.5rem",
                                    ),
                                    rx.vstack(
                                        *[
                                            omnisearch_result_item(
                                                result,
                                                idx + 8,
                                                OmniSearchState.selected_index,
                                            )
                                            for idx, result in enumerate(SYSTEM_ACTIONS_INDEX)
                                        ],
                                        width="100%",
                                    ),
                                    width="100%",
                                ),
                                
                                spacing="0",
                                width="100%",
                            ),
                            # Show filtered results
                            rx.cond(
                                len(OmniSearchState.filtered_results) > 0,
                                rx.vstack(
                                    *[
                                        omnisearch_result_item(
                                            result,
                                            idx,
                                            OmniSearchState.selected_index,
                                        )
                                        for idx, result in enumerate(OmniSearchState.filtered_results)
                                    ],
                                    spacing="0",
                                    width="100%",
                                ),
                                rx.box(
                                    rx.text(
                                        "No results found",
                                        font_size="0.9rem",
                                        color=ColorToken.TEXT_SECONDARY,
                                        text_align="center",
                                    ),
                                    padding="2rem",
                                    width="100%",
                                ),
                            ),
                        ),
                        
                        max_height="400px",
                        overflow_y="auto",
                        spacing="0",
                        width="100%",
                    ),
                    width="100%",
                ),
                
                # Footer hint
                rx.box(
                    rx.hstack(
                        rx.text(
                            "↑ ↓",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.MONO,
                        ),
                        rx.text(
                            "Navigate",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        rx.spacer(),
                        rx.text(
                            "↵",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.MONO,
                        ),
                        rx.text(
                            "Select",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        rx.spacer(),
                        rx.text(
                            "Esc",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.MONO,
                        ),
                        rx.text(
                            "Close",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        width="100%",
                        padding="1rem 1.5rem",
                        border_top=f"1px solid {ColorToken.BORDER_LASER}",
                    ),
                ),
                
                spacing="0",
                width="100%",
            ),
            position="fixed",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            width="90%",
            max_width="600px",
            max_height="600px",
            background_color=ColorToken.CARD_SLATE,
            border=f"1px solid {ColorToken.BORDER_LASER}",
            border_radius="1rem",
            box_shadow="0 20px 60px rgba(0, 0, 0, 0.6)",
            z_index="1001",
            display=rx.cond(OmniSearchState.is_open, "flex", "none"),
            flex_direction="column",
        ),
    )


def omnisearch_result_item(
    result: Dict[str, str],
    index: int,
    selected_index: int,
) -> rx.Component:
    """
    Individual search result item in the command menu.
    
    Args:
        result: Result data dictionary
        index: Result index
        selected_index: Currently selected index
        
    Returns:
        Reflex component
    """
    is_selected = index == selected_index
    
    return rx.box(
        rx.hstack(
            # Icon
            rx.box(
                rx.text(
                    result["icon"],
                    font_size="1.25rem",
                ),
                padding_right="1rem",
            ),
            
            # Title & description
            rx.vstack(
                rx.text(
                    result["title"],
                    font_size="0.95rem",
                    font_weight="500",
                    color=ColorToken.TEXT_PRIMARY,
                ),
                rx.text(
                    result["description"],
                    font_size="0.8rem",
                    color=ColorToken.TEXT_SECONDARY,
                    font_family=FontFamily.PRIMARY,
                ),
                spacing="0.25rem",
                width="100%",
            ),
            
            width="100%",
            align_items="center",
            spacing="0.75rem",
        ),
        padding="0.75rem 1.5rem",
        background_color=f"rgba(107, 90, 255, 0.15)" if is_selected else "transparent",
        border_left=f"3px solid {ColorToken.ACCENT_PRIMARY}" if is_selected else "3px solid transparent",
        cursor="pointer",
        transition="all 0.15s ease",
        _hover={
            "background_color": f"rgba(107, 90, 255, 0.08)",
        },
        width="100%",
    )


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

def get_omnisearch_component() -> rx.Component:
    """
    Export OmniSearch command menu for integration into root layout.
    
    Returns:
        Reflex component with search overlay
    """
    return omnisearch_panel()


def get_calendar_attendance_component() -> rx.Component:
    """
    Export calendar attendance grid for integration into dashboard.
    
    Returns:
        Reflex component ready for embedding
    """
    return calendar_attendance_grid()
