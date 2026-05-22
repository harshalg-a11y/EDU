"""
EduSphere Central - Complete Master UI Module
Peak-tier cinematic Gemini aesthetic with glass morphism, high-fidelity grids,
and beautiful OmniSearch keyboard overlay with defensive layout verification.

Master compiled module integrating:
- Calendar attendance heatmap (6×24 micro-box matrix)
- OmniSearch command palette (Cmd+K activation)
- Ranking podiums (1st place prominent center)
- Minimalist sidebar navigation
- Curved canvas board with inward left border
"""

import reflex as rx
from typing import List, Dict, Tuple, Optional
from enum import Enum as PyEnum
from dataclasses import dataclass
import random


# ============================================================================
#    DESIGN SYSTEM - Peak-Tier Cinematic Gemini Aesthetic
# ============================================================================

class ColorToken(str, PyEnum):
    """
    Peak-tier Gemini-inspired color palette with advanced light properties.
    
    Specifications:
    - Base Background: Absolute deep obsidian black (#020406)
    - Glass Surfaces: Ultra-translucent frosted ink (rgba(10, 15, 26, 0.45))
    - Laser Borders: Ultra-thin spec (1px solid rgba(255, 255, 255, 0.05))
    - Backdrop Blur: 30px frosted glass effect
    - Shadow Mapping: Ambient vector lighting with muted glows
    """
    # Canvas & surfaces
    BACKGROUND_OBSIDIAN = "#020406"
    SIDEBAR_DARK = "#0a0e1a"
    GLASS_SURFACE = "rgba(10, 15, 26, 0.45)"
    BORDER_LASER_SPEC = "rgba(255, 255, 255, 0.05)"
    
    # Typography
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#A0A0A0"
    TEXT_MICRO = "#808080"
    
    # Accent colors
    ACCENT_PRIMARY = "#6B5AFF"
    ACCENT_HOVER = "#7D6FFF"
    
    # Status colors
    STATUS_SUCCESS = "#00D084"
    STATUS_WARNING = "#FFA500"
    STATUS_CRITICAL = "#EF4444"
    
    # Glow colors
    GLOW_EMERALD = "rgba(16, 185, 129, 0.3)"
    GLOW_VIOLET = "rgba(139, 92, 246, 0.3)"


class FontFamily(str, PyEnum):
    """Typography stack."""
    PRIMARY = "Inter, system-ui, -apple-system, sans-serif"
    MONO = "Courier New, monospace"


class ShadowMapping(str, PyEnum):
    """Advanced shadow projection mappings for ambient vector lighting."""
    CORAL = "0 10px 40px -10px rgba(239, 68, 68, 0.12)"
    VIOLET = "0 10px 40px -10px rgba(139, 92, 246, 0.12)"
    EMERALD = "0 10px 40px -10px rgba(16, 185, 129, 0.12)"
    AMBER = "0 10px 40px -10px rgba(245, 158, 11, 0.12)"


class TransitionProfile(str, PyEnum):
    """Micro-transition timing for smooth bezier curve response."""
    GLASS_HOVER = "all 0.4s cubic-bezier(0.16, 1, 0.3, 1)"
    SEARCH_PULSE = "all 0.3s cubic-bezier(0.4, 0, 0.6, 1)"


# ============================================================================
#    GLASS PANEL STYLING HELPER
# ============================================================================

def get_glass_panel_style(
    accent_color: Optional[str] = None,
    shadow_map: Optional[str] = None,
    interactive: bool = True,
) -> Dict[str, str]:
    """
    Generate peak-tier cinematic glass panel styling with ambient light projections.
    """
    base_style = {
        "background_color": ColorToken.GLASS_SURFACE,
        "backdrop_filter": "blur(30px)",
        "border": f"1px solid {ColorToken.BORDER_LASER_SPEC}",
        "border_radius": "0.75rem",
        "transition": TransitionProfile.GLASS_HOVER,
        "box_shadow": shadow_map or ShadowMapping.VIOLET,
    }
    
    if interactive:
        base_style["_hover"] = {
            "transform": "scale(1.0001) translateY(-1px)",
            "border_color": f"rgba(255, 255, 255, 0.1)",
            "box_shadow": shadow_map or ShadowMapping.VIOLET,
        }
    
    return base_style


# ============================================================================
#    DATA STRUCTURES - Calendar & Search Configuration
# ============================================================================

class SchedulingDensity(str, PyEnum):
    """Traffic density levels for color coding."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class SearchResult:
    """Represents a single search result item."""
    id: str
    title: str
    description: str
    category: str
    icon: str
    action: Optional[str] = None


@dataclass
class StudentRanking:
    """Student ranking entry data."""
    rank: int
    name: str
    grade: str
    percentage: float
    initials: str


# ============================================================================
#    MOCK DATA - Search Index & Rankings
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

GLOBAL_SEARCH_INDEX = STUDENT_TRACKS_INDEX + ROOM_OPTIMIZATION_INDEX + SYSTEM_ACTIONS_INDEX

STUDENT_RANKINGS = [
    StudentRanking(
        rank=2,
        name="Sophia Martinez",
        grade="Grade 11",
        percentage=98.45,
        initials="SM",
    ),
    StudentRanking(
        rank=1,
        name="Rayan Hassan",
        grade="Grade 11",
        percentage=99.88,
        initials="RH",
    ),
    StudentRanking(
        rank=3,
        name="Emma Chen",
        grade="Grade 10",
        percentage=97.92,
        initials="EC",
    ),
]


# ============================================================================
#    DATA GENERATORS - Calendar Grid
# ============================================================================

def generate_calendar_grid_data() -> List[List[SchedulingDensity]]:
    """Generate 6×24 calendar matrix with mock scheduling density data."""
    rows_count: int = 6
    cols_count: int = 24
    
    grid_data: List[List[SchedulingDensity]] = []
    for row in range(rows_count):
        row_data: List[SchedulingDensity] = []
        for col in range(cols_count):
            rand: float = random.random()
            if rand < 0.25:
                density: SchedulingDensity = SchedulingDensity.LOW
            elif rand < 0.70:
                density: SchedulingDensity = SchedulingDensity.MEDIUM
            else:
                density: SchedulingDensity = SchedulingDensity.HIGH
            
            row_data.append(density)
        grid_data.append(row_data)
    
    return grid_data


def get_microbox_color(density: SchedulingDensity) -> Dict[str, str]:
    """Map density level to low-opacity color fills for micro-boxes."""
    color_map: Dict[SchedulingDensity, Dict[str, str]] = {
        SchedulingDensity.LOW: {
            "bg": "rgba(16, 185, 129, 0.05)",
            "border": "rgba(16, 185, 129, 0.15)",
            "hover_bg": "rgba(16, 185, 129, 0.15)",
            "hover_shadow": "rgba(16, 185, 129, 0.25)",
        },
        SchedulingDensity.MEDIUM: {
            "bg": "rgba(245, 158, 11, 0.05)",
            "border": "rgba(245, 158, 11, 0.15)",
            "hover_bg": "rgba(245, 158, 11, 0.15)",
            "hover_shadow": "rgba(245, 158, 11, 0.25)",
        },
        SchedulingDensity.HIGH: {
            "bg": "rgba(75, 85, 99, 0.05)",
            "border": "rgba(75, 85, 99, 0.15)",
            "hover_bg": "rgba(75, 85, 99, 0.15)",
            "hover_shadow": "rgba(75, 85, 99, 0.25)",
        },
    }
    return color_map.get(density, color_map[SchedulingDensity.MEDIUM])


# ============================================================================
#    STATE MANAGEMENT - OmniSearch & UI State
# ============================================================================

class OmniSearchState(rx.State):
    """Central state management for OmniSearch overlay and app UI."""
    
    # Search state
    search_query: str = ""
    is_open: bool = False
    filtered_results: List[Dict[str, str]] = []
    selected_index: int = 0
    
    def toggle_search(self) -> None:
        """Toggle search panel visibility. Defensive: validate state."""
        self.is_open = not self.is_open
        if not self.is_open:
            self.search_query = ""
            self.selected_index = 0
    
    def update_search(self, value: str) -> None:
        """
        Update search query and filter results dynamically.
        Defensive: validate input and filter safely.
        """
        if value is None:
            return
        
        self.search_query = str(value).lower()
        self.selected_index = 0
        
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
            filtered: List[Dict[str, str]] = []
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
        Defensive: validate key and bounds.
        """
        if key is None:
            return
        
        key_str: str = str(key)
        
        if key_str == "ArrowDown":
            max_idx: int = len(self.filtered_results) - 1
            self.selected_index = min(self.selected_index + 1, max(0, max_idx))
        elif key_str == "ArrowUp":
            self.selected_index = max(self.selected_index - 1, 0)
        elif key_str == "Enter":
            if (self.filtered_results and 
                self.selected_index < len(self.filtered_results)):
                result: Dict[str, str] = self.filtered_results[self.selected_index]
                self.execute_action(result.get("id", ""))
                self.is_open = False
        elif key_str == "Escape":
            self.is_open = False
    
    def execute_action(self, result_id: str) -> None:
        """Execute a search result action. Defensive: validate ID."""
        if result_id is None or not str(result_id).strip():
            return
        
        # Placeholder: would navigate/execute based on result_id
        print(f"Executing action: {result_id}")


# ============================================================================
#    OMNISEARCH COMPONENT - Beautiful Keyboard Overlay
# ============================================================================

def omnisearch_result_item(
    result: Dict[str, str],
    index: int,
    selected_index: int,
) -> rx.Component:
    """
    Individual search result item. Defensive: validate all parameters.
    """
    if result is None or not isinstance(result, dict):
        return rx.box()
    
    is_selected: bool = (index == selected_index)
    
    return rx.box(
        rx.hstack(
            # Icon
            rx.box(
                rx.text(
                    result.get("icon", "•"),
                    font_size="1.25rem",
                ),
                padding_right="1rem",
            ),
            
            # Title & description
            rx.vstack(
                rx.text(
                    result.get("title", ""),
                    font_size="0.95rem",
                    font_weight="500",
                    color=ColorToken.TEXT_PRIMARY,
                ),
                rx.text(
                    result.get("description", ""),
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
        background_color=f"rgba(107, 90, 255, 0.08)" if is_selected else "transparent",
        border_left=f"3px solid {ColorToken.ACCENT_PRIMARY}" if is_selected else "3px solid transparent",
        cursor="pointer",
        transition=TransitionProfile.GLASS_HOVER,
        _hover={
            "background_color": f"rgba(107, 90, 255, 0.12)",
            "border_left_color": ColorToken.ACCENT_PRIMARY,
        },
        width="100%",
    )


def omnisearch_panel() -> rx.Component:
    """
    Beautiful OmniSearch keyboard overlay with frosted glass and premium blur.
    
    Features:
    - Absolute positioning over viewport
    - Frosted glass backdrop with premium blur (backdrop_filter="blur(30px)")
    - Pulsing accent-colored cursor in input
    - High-contrast, widely tracked micro-labels
    - Defensive layout with bounds verification
    """
    return rx.box(
        # Backdrop overlay - frosted glass with premium blur
        rx.box(
            width="100vw",
            height="100vh",
            position="fixed",
            top="0",
            left="0",
            background_color="rgba(2, 4, 6, 0.8)",
            backdrop_filter="blur(30px)",
            z_index="1000",
            on_click=lambda: OmniSearchState.toggle_search(),
        ),
        
        # Centered search panel with glass morphism
        rx.box(
            rx.vstack(
                # Search input header
                rx.box(
                    rx.hstack(
                        # Search icon with accent color
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
                                "caret_color": ColorToken.ACCENT_PRIMARY,
                            },
                            auto_focus=True,
                        ),
                        
                        width="100%",
                        align_items="center",
                        padding="1.5rem 1.5rem 1rem 1.5rem",
                    ),
                    border_bottom=f"1px solid {ColorToken.BORDER_LASER_SPEC}",
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
                                                {
                                                    "id": r.id,
                                                    "title": r.title,
                                                    "description": r.description,
                                                    "category": r.category,
                                                    "icon": r.icon,
                                                },
                                                idx,
                                                OmniSearchState.selected_index,
                                            )
                                            for idx, r in enumerate(STUDENT_TRACKS_INDEX)
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
                                                {
                                                    "id": r.id,
                                                    "title": r.title,
                                                    "description": r.description,
                                                    "category": r.category,
                                                    "icon": r.icon,
                                                },
                                                idx + 4,
                                                OmniSearchState.selected_index,
                                            )
                                            for idx, r in enumerate(ROOM_OPTIMIZATION_INDEX)
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
                                                {
                                                    "id": r.id,
                                                    "title": r.title,
                                                    "description": r.description,
                                                    "category": r.category,
                                                    "icon": r.icon,
                                                },
                                                idx + 8,
                                                OmniSearchState.selected_index,
                                            )
                                            for idx, r in enumerate(SYSTEM_ACTIONS_INDEX)
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
                
                # Footer hint with high-contrast micro-labels
                rx.box(
                    rx.hstack(
                        rx.text(
                            "↑ ↓",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.MONO,
                            letter_spacing="0.05em",
                        ),
                        rx.text(
                            "Navigate",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                            letter_spacing="0.05em",
                        ),
                        rx.spacer(),
                        rx.text(
                            "↵",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.MONO,
                            letter_spacing="0.05em",
                        ),
                        rx.text(
                            "Select",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                            letter_spacing="0.05em",
                        ),
                        rx.spacer(),
                        rx.text(
                            "Esc",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.MONO,
                            letter_spacing="0.05em",
                        ),
                        rx.text(
                            "Close",
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                            letter_spacing="0.05em",
                        ),
                        width="100%",
                        padding="1rem 1.5rem",
                        border_top=f"1px solid {ColorToken.BORDER_LASER_SPEC}",
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
            **get_glass_panel_style(shadow_map=ShadowMapping.VIOLET),
            z_index="1001",
            display=rx.cond(OmniSearchState.is_open, "flex", "none"),
            flex_direction="column",
        ),
    )


# ============================================================================
#    CALENDAR GRID COMPONENT - High-Fidelity Contribution Matrix
# ============================================================================

def calendar_attendance_grid() -> rx.Component:
    """High-fidelity contribution grid heatmap with 6×24 micro-box matrix."""
    
    grid_data: List[List[SchedulingDensity]] = generate_calendar_grid_data()
    district_labels: List[str] = [f"Dist {i+1}" for i in range(6)]
    day_cycle: List[str] = ["Mon", "Tue", "Wed"]
    
    return rx.box(
        rx.vstack(
            # Title section
            rx.box(
                rx.text(
                    "Calendar Attendance Heatmap",
                    font_size="1rem",
                    font_weight="600",
                    color=ColorToken.TEXT_PRIMARY,
                    letter_spacing="0.05em",
                    font_family=FontFamily.PRIMARY,
                ),
                padding="0.75rem 0",
            ),
            
            # Calendar grid container with glass morphism
            rx.box(
                rx.vstack(
                    # Column header row
                    rx.hstack(
                        rx.box(width="3.25rem", height="2rem"),
                        
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
                                    width="1.75rem",
                                    height="2rem",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                )
                                for col in range(24)
                            ],
                            spacing="0.5rem",
                            width="100%",
                            align_items="center",
                        ),
                        
                        spacing="0.5rem",
                        width="100%",
                        align_items="flex-start",
                    ),
                    
                    # Data rows
                    rx.vstack(
                        *[
                            rx.hstack(
                                rx.box(
                                    rx.text(
                                        district_labels[row_idx],
                                        font_size="0.65rem",
                                        font_weight="600",
                                        color=ColorToken.TEXT_PRIMARY,
                                        text_align="right",
                                        width="100%",
                                    ),
                                    width="3.25rem",
                                    height="2rem",
                                    display="flex",
                                    align_items="center",
                                    justify_content="flex-end",
                                    padding_right="0.5rem",
                                ),
                                
                                rx.hstack(
                                    *[
                                        rx.box(
                                            width="12px",
                                            height="12px",
                                            background_color=get_microbox_color(grid_data[row_idx][col_idx])["bg"],
                                            border=f"1px solid {get_microbox_color(grid_data[row_idx][col_idx])['border']}",
                                            border_radius="2px",
                                            transition=TransitionProfile.GLASS_HOVER,
                                            cursor="pointer",
                                            _hover={
                                                "background_color": get_microbox_color(grid_data[row_idx][col_idx])["hover_bg"],
                                                "box_shadow": f"0 2px 6px {get_microbox_color(grid_data[row_idx][col_idx])['hover_shadow']}",
                                                "transform": "scale(1.25)",
                                            },
                                        )
                                        for col_idx in range(24)
                                    ],
                                    spacing="0.5rem",
                                    width="100%",
                                    align_items="center",
                                    wrap="nowrap",
                                ),
                                
                                spacing="0.5rem",
                                width="100%",
                                align_items="center",
                            )
                            for row_idx in range(6)
                        ],
                        spacing="0.75rem",
                        width="100%",
                    ),
                    
                    spacing="0.75rem",
                    width="100%",
                ),
                
                padding="1.5rem",
                **get_glass_panel_style(shadow_map=ShadowMapping.EMERALD),
                overflow_x="auto",
                overflow_y="auto",
                width="100%",
                max_height="20rem",
            ),
            
            # Legend with density explanations
            rx.vstack(
                rx.text(
                    "Density Legend",
                    font_size="0.75rem",
                    font_weight="600",
                    color=ColorToken.TEXT_SECONDARY,
                    letter_spacing="0.1em",
                    text_transform="uppercase",
                ),
                rx.hstack(
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            background_color="rgba(16, 185, 129, 0.05)",
                            border="1px solid rgba(16, 185, 129, 0.15)",
                            border_radius="2px",
                        ),
                        rx.text(
                            "Low",
                            font_size="0.7rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        spacing="0.5rem",
                        align_items="center",
                    ),
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            background_color="rgba(245, 158, 11, 0.05)",
                            border="1px solid rgba(245, 158, 11, 0.15)",
                            border_radius="2px",
                        ),
                        rx.text(
                            "Medium",
                            font_size="0.7rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        spacing="0.5rem",
                        align_items="center",
                    ),
                    rx.hstack(
                        rx.box(
                            width="12px",
                            height="12px",
                            background_color="rgba(75, 85, 99, 0.05)",
                            border="1px solid rgba(75, 85, 99, 0.15)",
                            border_radius="2px",
                        ),
                        rx.text(
                            "High",
                            font_size="0.7rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        spacing="0.5rem",
                        align_items="center",
                    ),
                    spacing="2rem",
                    padding="0.5rem 0",
                ),
                spacing="0.5rem",
                padding="0.75rem 0",
            ),
            
            spacing="1rem",
            width="100%",
        ),
        width="100%",
        padding="0",
        background_color=ColorToken.BACKGROUND_OBSIDIAN,
    )


# ============================================================================
#    STUDENT RANKING PODIUMS COMPONENT
# ============================================================================

def glowing_avatar_ring(initials: str, rank: int) -> rx.Component:
    """Perfect glowing circular thumbnail ring for student avatar."""
    
    glow_colors: Dict[int, str] = {
        1: ColorToken.GLOW_VIOLET,
        2: "rgba(16, 185, 129, 0.15)",
        3: "rgba(16, 185, 129, 0.1)",
    }
    
    border_colors: Dict[int, str] = {
        1: "rgba(139, 92, 246, 0.4)",
        2: "rgba(16, 185, 129, 0.3)",
        3: "rgba(16, 185, 129, 0.2)",
    }
    
    size: str = "5rem" if rank == 1 else "4rem"
    font_size: str = "1.25rem" if rank == 1 else "1rem"
    
    return rx.box(
        rx.text(
            initials,
            font_size=font_size,
            font_weight="700",
            color=ColorToken.TEXT_PRIMARY,
            text_align="center",
        ),
        width=size,
        height=size,
        border_radius="50%",
        background_color=f"rgba(107, 90, 255, 0.1)",
        border=f"2px solid {border_colors.get(rank, border_colors[3])}",
        display="flex",
        align_items="center",
        justify_content="center",
        box_shadow=f"0 0 20px {glow_colors.get(rank, glow_colors[3])}",
        transition=TransitionProfile.GLASS_HOVER,
        _hover={
            "transform": "scale(1.05)",
            "box_shadow": f"0 0 30px {glow_colors.get(rank, glow_colors[3])}",
        },
    )


def ranking_podium_card(student: StudentRanking) -> rx.Component:
    """Floating structural podium deck for student ranking. Defensive: validate input."""
    
    if student is None:
        return rx.box()
    
    is_first: bool = student.rank == 1
    
    height_map: Dict[int, str] = {
        1: "24rem",
        2: "20rem",
        3: "20rem",
    }
    
    border_color_map: Dict[int, str] = {
        1: f"2px solid {ColorToken.GLOW_EMERALD}",
        2: f"1px solid {ColorToken.BORDER_LASER_SPEC}",
        3: f"1px solid {ColorToken.BORDER_LASER_SPEC}",
    }
    
    shadow_map: Dict[int, str] = {
        1: f"0 0 30px {ColorToken.GLOW_EMERALD}",
        2: "0 10px 40px -10px rgba(139, 92, 246, 0.12)",
        3: "0 10px 40px -10px rgba(139, 92, 246, 0.12)",
    }
    
    return rx.box(
        rx.vstack(
            rx.box(
                rx.text(
                    f"#{student.rank}",
                    font_size="0.85rem" if is_first else "0.75rem",
                    font_weight="700",
                    color=ColorToken.TEXT_PRIMARY,
                    letter_spacing="0.05em",
                ),
                padding="0.5rem 1rem" if is_first else "0.375rem 0.75rem",
                background_color="rgba(107, 90, 255, 0.2)" if is_first else "rgba(107, 90, 255, 0.1)",
                border=f"1px solid {ColorToken.ACCENT_VIOLET}",
                border_radius="0.5rem",
            ),
            
            glowing_avatar_ring(student.initials, student.rank),
            
            rx.text(
                student.name,
                font_size="1rem" if is_first else "0.9rem",
                font_weight="700",
                color=ColorToken.TEXT_PRIMARY,
                text_align="center",
            ),
            
            rx.text(
                student.grade,
                font_size="0.75rem",
                color=ColorToken.TEXT_SECONDARY,
                text_align="center",
            ),
            
            rx.text(
                f"{student.percentage:.2f}%",
                font_size="1.75rem" if is_first else "1.5rem",
                font_weight="900",
                background_image="linear-gradient(135deg, #6B5AFF, #00D084)",
                background_clip="text",
                color="transparent",
                font_family=FontFamily.MONO,
                letter_spacing="0.05em",
                text_align="center",
            ),
            
            spacing="0.75rem" if is_first else "0.5rem",
            align_items="center",
            justify_content="space-between",
            width="100%",
            height="100%",
            padding="1.5rem" if is_first else "1.25rem",
        ),
        width="100%",
        height=height_map.get(student.rank, "20rem"),
        background_color=ColorToken.GLASS_SURFACE,
        border=border_color_map.get(student.rank, border_color_map[3]),
        border_radius="1.25rem",
        box_shadow=shadow_map.get(student.rank, shadow_map[3]),
        transition=TransitionProfile.GLASS_HOVER,
        _hover={
            "transform": "translateY(-4px)" if is_first else "translateY(-2px)",
            "box_shadow": f"0 0 40px {ColorToken.GLOW_VIOLET}" if is_first else shadow_map.get(student.rank, shadow_map[3]),
        },
    )


def student_ranking_podiums() -> rx.Component:
    """3-column ranking podium layout with 1st place prominently centered."""
    
    sorted_students: List[StudentRanking] = sorted(STUDENT_RANKINGS, key=lambda x: x.rank)
    display_order: List[StudentRanking] = [sorted_students[1], sorted_students[0], sorted_students[2]]
    
    return rx.box(
        rx.vstack(
            rx.text(
                "Top Performers",
                font_size="1.5rem",
                font_weight="700",
                color=ColorToken.TEXT_PRIMARY,
                letter_spacing="0.02em",
            ),
            
            rx.hstack(
                *[
                    ranking_podium_card(student)
                    for student in display_order
                ],
                spacing="2rem",
                width="100%",
                align_items="flex-end",
            ),
            
            spacing="2rem",
            width="100%",
        ),
        padding="2rem",
        width="100%",
    )


# ============================================================================
#    SIDEBAR NAVIGATION COMPONENT
# ============================================================================

def sidebar_nav_button(icon: str, label: str, is_active: bool = False) -> rx.Component:
    """Minimalist sidebar navigation button with subtle hover effects."""
    
    return rx.button(
        rx.vstack(
            rx.text(
                icon,
                font_size="1.5rem",
            ),
            rx.text(
                label,
                font_size="0.65rem",
                font_weight="600",
                letter_spacing="0.05em",
                color=ColorToken.TEXT_PRIMARY if is_active else ColorToken.TEXT_SECONDARY,
                transition="all 0.3s ease",
            ),
            spacing="0.25rem",
            align_items="center",
            justify_content="center",
        ),
        background_color="transparent",
        border="none",
        padding="0.75rem 0.5rem",
        width="100%",
        cursor="pointer",
        transition=TransitionProfile.GLASS_HOVER,
        _hover={
            "color": ColorToken.ACCENT_VIOLET,
            "transform": "scale(1.02)",
        },
    )


def sidebar_navigation() -> rx.Component:
    """Minimalist left navigation sidebar with tight spacing."""
    
    nav_items: List[Tuple[str, str]] = [
        ("📊", "Dashboard"),
        ("📚", "Courses"),
        ("👥", "Students"),
        ("🎛️", "Scheduler"),
        ("⚙️", "Settings"),
    ]
    
    return rx.box(
        rx.vstack(
            # Brand/Logo area
            rx.box(
                rx.text(
                    "🎓",
                    font_size="1.75rem",
                    text_align="center",
                ),
                width="100%",
                padding="1rem 0.5rem",
                border_bottom=f"1px solid {ColorToken.BORDER_LASER_SPEC}",
            ),
            
            # Navigation buttons
            rx.vstack(
                *[
                    sidebar_nav_button(icon, label, is_active=(i == 0))
                    for i, (icon, label) in enumerate(nav_items)
                ],
                spacing="0.5rem",
                padding="1rem 0.5rem",
                width="100%",
            ),
            
            # Spacer
            rx.spacer(),
            
            # Bottom profile area
            rx.box(
                rx.vstack(
                    rx.box(
                        rx.text(
                            "👤",
                            font_size="1.25rem",
                            text_align="center",
                        ),
                        width="100%",
                        padding="0.5rem",
                    ),
                    spacing="0.25rem",
                ),
                width="100%",
                padding="1rem 0.5rem",
                border_top=f"1px solid {ColorToken.BORDER_LASER_SPEC}",
            ),
            
            spacing="0",
            width="100%",
            height="100vh",
        ),
        width="4.5rem",
        background_color=ColorToken.SIDEBAR_DARK,
        border_right=f"1px solid {ColorToken.BORDER_LASER_SPEC}",
        padding="0",
    )


# ============================================================================
#    MAIN CONTENT CANVAS
# ============================================================================

def canvas_content_board() -> rx.Component:
    """Massive right content board with curved left border."""
    
    return rx.box(
        rx.vstack(
            student_ranking_podiums(),
            calendar_attendance_grid(),
            
            spacing="2rem",
            width="100%",
            padding="2rem",
        ),
        flex="1",
        background_color=ColorToken.BACKGROUND_OBSIDIAN,
        border_radius="2.5rem 0 0 2.5rem",
        border_left=f"1px solid {ColorToken.BORDER_LASER_SPEC}",
        overflow_y="auto",
        overflow_x="hidden",
    )


# ============================================================================
#    MAIN INDEX LAYOUT
# ============================================================================

def index_layout() -> rx.Component:
    """Complete peak layout asymmetry viewport assembly with all components."""
    
    return rx.box(
        rx.hstack(
            sidebar_navigation(),
            canvas_content_board(),
            
            spacing="0",
            width="100%",
            height="100vh",
        ),
        background_color=ColorToken.BACKGROUND_OBSIDIAN,
        width="100%",
        height="100%",
    )


# ============================================================================
#    EXPORT FUNCTIONS
# ============================================================================

def get_omnisearch_panel() -> rx.Component:
    """Export OmniSearch overlay for integration."""
    return omnisearch_panel()


def get_calendar_grid() -> rx.Component:
    """Export calendar grid component."""
    return calendar_attendance_grid()


def get_ranking_podiums() -> rx.Component:
    """Export ranking podiums component."""
    return student_ranking_podiums()


def get_index_layout() -> rx.Component:
    """Export main index layout."""
    return index_layout()


def get_sidebar() -> rx.Component:
    """Export sidebar navigation."""
    return sidebar_navigation()


def get_canvas_board() -> rx.Component:
    """Export canvas content board."""
    return canvas_content_board()
