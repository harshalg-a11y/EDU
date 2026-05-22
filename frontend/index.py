"""
EduSphere Central - Peak Layout Asymmetry Index
Master viewport assembly with minimalist sidebar and curved canvas board.
High-fidelity student ranking podiums with floating structural decks.
"""

import reflex as rx
from typing import List, Dict, Optional
from enum import Enum as PyEnum
from dataclasses import dataclass


# ============================================================================
#    DESIGN SYSTEM - Peak Asymmetry Aesthetic
# ============================================================================

class LayoutColor(str, PyEnum):
    """Layout color palette for asymmetric viewport design."""
    BACKGROUND_OBSIDIAN = "#020406"
    SIDEBAR_DARK = "#0a0e1a"
    CANVAS_GLASS = "rgba(10, 15, 26, 0.45)"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#A0A0A0"
    ACCENT_VIOLET = "#6B5AFF"
    ACCENT_HOVER = "#7D6FFF"
    LASER_BORDER = "rgba(255, 255, 255, 0.05)"
    GLOW_EMERALD = "rgba(16, 185, 129, 0.3)"
    GLOW_VIOLET = "rgba(139, 92, 246, 0.3)"


class FontFamily(str, PyEnum):
    """Typography stack."""
    PRIMARY = "Inter, system-ui, -apple-system, sans-serif"
    MONO = "Courier New, monospace"


# ============================================================================
#    STUDENT RANKING DATA STRUCTURES
# ============================================================================

@dataclass
class StudentRanking:
    """Student ranking entry data."""
    rank: int  # 1, 2, or 3
    name: str
    grade: str
    percentage: float
    initials: str  # For avatar placeholder


# Mock student ranking data
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
#    SIDEBAR NAVIGATION COMPONENT - Minimalist Profile
# ============================================================================

class SidebarNavItem:
    """Navigation item data."""
    def __init__(self, icon: str, label: str, path: str = "#"):
        self.icon = icon
        self.label = label
        self.path = path


SIDEBAR_ITEMS = [
    SidebarNavItem("📊", "Dashboard"),
    SidebarNavItem("📚", "Courses"),
    SidebarNavItem("👥", "Students"),
    SidebarNavItem("🎛️", "Scheduler"),
    SidebarNavItem("⚙️", "Settings"),
]


def sidebar_nav_button(item: SidebarNavItem, is_active: bool = False) -> rx.Component:
    """
    Minimalist sidebar navigation button with subtle hover effects.
    
    Features:
    - Tight, compact layout
    - Icon-centric design
    - Subtle hover color shifts
    - Text tracking scales on interaction
    
    Args:
        item: Navigation item data
        is_active: Whether button is currently active
        
    Returns:
        Reflex component for nav button
    """
    return rx.button(
        rx.vstack(
            rx.text(
                item.icon,
                font_size="1.5rem",
            ),
            rx.text(
                item.label,
                font_size="0.65rem",
                font_weight="600",
                letter_spacing="0.05em",
                color=LayoutColor.TEXT_PRIMARY if is_active else LayoutColor.TEXT_SECONDARY,
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
        transition="all 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
        _hover={
            "color": LayoutColor.ACCENT_VIOLET,
            "transform": "scale(1.02)",
        },
        _active={
            "color": LayoutColor.ACCENT_VIOLET,
        },
    )


def sidebar_navigation() -> rx.Component:
    """
    Minimalist left navigation sidebar with tight spacing.
    
    Design:
    - Vertical stack of icon-label buttons
    - Subtle hover color shifts (text secondary → accent violet)
    - Text tracking scales on interaction
    - Clean, professional appearance
    - Tight layout profile
    
    Returns:
        Reflex component for sidebar navigation
    """
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
                border_bottom=f"1px solid {LayoutColor.LASER_BORDER}",
            ),
            
            # Navigation buttons
            rx.vstack(
                *[
                    sidebar_nav_button(
                        item,
                        is_active=(i == 0),
                    )
                    for i, item in enumerate(SIDEBAR_ITEMS)
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
                border_top=f"1px solid {LayoutColor.LASER_BORDER}",
            ),
            
            spacing="0",
            width="100%",
            height="100vh",
        ),
        width="4.5rem",
        background_color=LayoutColor.SIDEBAR_DARK,
        border_right=f"1px solid {LayoutColor.LASER_BORDER}",
        padding="0",
    )


# ============================================================================
#    STUDENT RANKING PODIUM COMPONENTS
# ============================================================================

def glowing_avatar_ring(initials: str, rank: int) -> rx.Component:
    """
    Perfect glowing circular thumbnail ring for student avatar.
    
    Features:
    - Circular ring with glowing border
    - Minimalist placeholder text (initials)
    - Rank-based glow color (1st: violet, 2nd/3rd: muted)
    - Smooth hover animations
    
    Args:
        initials: Student initials for fallback text
        rank: Ranking position (1, 2, or 3)
        
    Returns:
        Reflex component for avatar ring
    """
    # Glow colors based on rank
    glow_colors = {
        1: LayoutColor.GLOW_VIOLET,
        2: "rgba(16, 185, 129, 0.15)",
        3: "rgba(16, 185, 129, 0.1)",
    }
    
    border_colors = {
        1: "rgba(139, 92, 246, 0.4)",
        2: "rgba(16, 185, 129, 0.3)",
        3: "rgba(16, 185, 129, 0.2)",
    }
    
    size = "5rem" if rank == 1 else "4rem"
    font_size = "1.25rem" if rank == 1 else "1rem"
    
    return rx.box(
        rx.text(
            initials,
            font_size=font_size,
            font_weight="700",
            color=LayoutColor.TEXT_PRIMARY,
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
        transition="all 0.4s cubic-bezier(0.16, 1, 0.3, 1)",
        _hover={
            "transform": "scale(1.05)",
            "box_shadow": f"0 0 30px {glow_colors.get(rank, glow_colors[3])}",
        },
    )


def ranking_podium_card(student: StudentRanking) -> rx.Component:
    """
    Floating structural podium deck for student ranking.
    
    Design:
    - 1st place card is taller and centered
    - 2nd and 3rd cards flank the 1st place card
    - Glowing laser band border for 1st place
    - Glass morphism surfaces
    - Professional typography
    
    Args:
        student: Student ranking data
        
    Returns:
        Reflex component for ranking podium
    """
    is_first = student.rank == 1
    
    # Height based on rank
    height_map = {
        1: "24rem",  # Prominently taller
        2: "20rem",
        3: "20rem",
    }
    
    # Border colors - 1st place gets glowing laser band
    border_color_map = {
        1: f"2px solid {LayoutColor.GLOW_EMERALD}",
        2: f"1px solid {LayoutColor.LASER_BORDER}",
        3: f"1px solid {LayoutColor.LASER_BORDER}",
    }
    
    # Shadow mapping
    shadow_map = {
        1: f"0 0 30px {LayoutColor.GLOW_EMERALD}",
        2: "0 10px 40px -10px rgba(139, 92, 246, 0.12)",
        3: "0 10px 40px -10px rgba(139, 92, 246, 0.12)",
    }
    
    return rx.box(
        rx.vstack(
            # Rank badge
            rx.box(
                rx.text(
                    f"#{student.rank}",
                    font_size="0.85rem" if is_first else "0.75rem",
                    font_weight="700",
                    color=LayoutColor.TEXT_PRIMARY,
                    letter_spacing="0.05em",
                ),
                padding="0.5rem 1rem" if is_first else "0.375rem 0.75rem",
                background_color="rgba(107, 90, 255, 0.2)" if is_first else "rgba(107, 90, 255, 0.1)",
                border=f"1px solid {LayoutColor.ACCENT_VIOLET}",
                border_radius="0.5rem",
            ),
            
            # Avatar with glowing ring
            glowing_avatar_ring(student.initials, student.rank),
            
            # Student name
            rx.text(
                student.name,
                font_size="1rem" if is_first else "0.9rem",
                font_weight="700",
                color=LayoutColor.TEXT_PRIMARY,
                text_align="center",
            ),
            
            # Grade/level
            rx.text(
                student.grade,
                font_size="0.75rem",
                color=LayoutColor.TEXT_SECONDARY,
                text_align="center",
            ),
            
            # Performance percentage - razor sharp
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
        height=height_map[student.rank],
        background_color=LayoutColor.CANVAS_GLASS,
        border=border_color_map[student.rank],
        border_radius="1.25rem",
        box_shadow=shadow_map[student.rank],
        transition="all 0.4s cubic-bezier(0.16, 1, 0.3, 1)",
        _hover={
            "transform": "translateY(-4px)" if is_first else "translateY(-2px)",
            "box_shadow": f"0 0 40px {LayoutColor.GLOW_VIOLET}" if is_first else shadow_map[student.rank],
        },
    )


def student_ranking_podiums() -> rx.Component:
    """
    3-column ranking podium layout with 1st place prominently centered.
    
    Design:
    - 1st Place (Rayan Hassan, 99.88%) in the middle, structurally taller
    - 2nd Place (Sophia Martinez, 98.45%) on the left
    - 3rd Place (Emma Chen, 97.92%) on the right
    - Clean spacing and professional alignment
    
    Returns:
        Reflex component with ranking podiums
    """
    # Sort by rank for proper layout order
    sorted_students = sorted(STUDENT_RANKINGS, key=lambda x: x.rank)
    
    # Reorder to [2nd, 1st, 3rd] for visual center placement
    display_order = [sorted_students[1], sorted_students[0], sorted_students[2]]
    
    return rx.box(
        rx.vstack(
            # Title
            rx.text(
                "Top Performers",
                font_size="1.5rem",
                font_weight="700",
                color=LayoutColor.TEXT_PRIMARY,
                letter_spacing="0.02em",
            ),
            
            # Ranking podiums grid
            rx.hstack(
                *[
                    ranking_podium_card(student)
                    for student in display_order
                ],
                spacing="2rem",
                width="100%",
                align_items="flex-end",  # Align bottoms
            ),
            
            spacing="2rem",
            width="100%",
        ),
        padding="2rem",
        width="100%",
    )


# ============================================================================
#    MAIN CONTENT CANVAS - Curved Left Border
# ============================================================================

def canvas_content_board() -> rx.Component:
    """
    Massive right content board with sweeping inward left-side border contour.
    
    Design:
    - Explicit curved inward left border: border_radius="2.5rem 0 0 2.5rem"
    - Overlays dark sidebar region beneath
    - Glass morphism background
    - Houses ranking podiums and other content
    
    Returns:
        Reflex component for main canvas board
    """
    return rx.box(
        rx.vstack(
            # Canvas content
            student_ranking_podiums(),
            
            spacing="0",
            width="100%",
        ),
        flex="1",
        background_color=LayoutColor.BACKGROUND_OBSIDIAN,
        border_radius="2.5rem 0 0 2.5rem",
        border_left=f"1px solid {LayoutColor.LASER_BORDER}",
        overflow_y="auto",
        overflow_x="hidden",
    )


# ============================================================================
#    MAIN INDEX LAYOUT - Peak Asymmetry Assembly
# ============================================================================

def index_layout() -> rx.Component:
    """
    Peak layout asymmetry viewport assembly.
    
    Structure:
    - Minimalist left sidebar (4.5rem wide) with navigation
    - Massive right canvas board with curved inward border (2.5rem)
    - Clean asymmetric visual hierarchy
    - Professional, cinematic appearance
    
    Returns:
        Reflex component with complete layout
    """
    return rx.box(
        rx.hstack(
            # Left minimalist sidebar
            sidebar_navigation(),
            
            # Right curved canvas board
            canvas_content_board(),
            
            spacing="0",
            width="100%",
            height="100vh",
        ),
        background_color=LayoutColor.BACKGROUND_OBSIDIAN,
        width="100%",
        height="100%",
    )


# ============================================================================
#    EXPORT FUNCTIONS
# ============================================================================

def get_index_layout() -> rx.Component:
    """Export main index layout for app integration."""
    return index_layout()


def get_sidebar_navigation() -> rx.Component:
    """Export sidebar navigation component."""
    return sidebar_navigation()


def get_student_ranking_podiums() -> rx.Component:
    """Export student ranking podiums component."""
    return student_ranking_podiums()


def get_canvas_board() -> rx.Component:
    """Export canvas content board component."""
    return canvas_content_board()
