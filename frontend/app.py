"""
EduSphere Central - Reflex Frontend Dashboard Application
Pure Python UI layer with Google Gemini-inspired minimalist dark mode aesthetic.
Asymmetric layout with fixed navigation sidebar and dynamic content canvas.
"""

import reflex as rx
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum as PyEnum


# ============================================================================
#    DESIGN SYSTEM - Color Palette & Typography
# ============================================================================

class ColorToken(str, PyEnum):
    """Gemini-inspired color palette."""
    BACKGROUND_DEEP = "#080A10"      # Deep space black (sidebar)
    CARD_SLATE = "#121622"            # Deep slate (content canvas)
    BORDER_LASER = "#1E1F2E"          # Thin divider accent
    TEXT_PRIMARY = "#FFFFFF"           # Pure white text
    TEXT_SECONDARY = "#A0A0A0"        # Muted gray
    ACCENT_PRIMARY = "#6B5AFF"        # Purple accent (Gemini-inspired)
    ACCENT_HOVER = "#7D6FFF"          # Hover state
    STATUS_SUCCESS = "#00D084"        # Success green
    STATUS_WARNING = "#FFA500"        # Warning amber
    STATUS_CRITICAL = "#FF6B6B"       # Critical red
    OVERLAY_SEMI = "rgba(18, 22, 34, 0.8)"  # Semi-transparent overlay


class FontFamily(str, PyEnum):
    """Typography stack."""
    PRIMARY = "Inter, system-ui, -apple-system, sans-serif"
    MONO = "Courier New, monospace"


# ============================================================================
#    STATE MANAGEMENT - Reactive Reflex State
# ============================================================================

@dataclass
class NavigationItem:
    """Navigation sidebar menu item."""
    label: str
    icon: str
    path: str
    description: str = ""


class AppState(rx.State):
    """
    Central reactive state container.
    
    Manages navigation, user session, dashboard data, and UI interactions.
    """
    
    # Navigation state
    active_route: str = "dashboard"
    navigation_expanded: bool = True
    
    # User session
    current_user_name: str = "Harshal Sah Gupta"
    current_user_role: str = "GLOBAL_ADMIN"
    current_user_avatar: str = "HG"
    
    # Dashboard data
    active_conflicts_count: int = 3
    students_count: int = 2847
    average_gpa: float = 3.72
    system_uptime: float = 99.98
    
    # UI interactions
    sidebar_hover_item: Optional[str] = None
    
    def navigate_to(self, route: str) -> None:
        """
        Navigate to specified route.
        
        Args:
            route: Route identifier
        """
        self.active_route = route
    
    def toggle_sidebar(self) -> None:
        """Toggle sidebar expansion state."""
        self.navigation_expanded = not self.navigation_expanded
    
    def on_sidebar_item_hover(self, item: str) -> None:
        """
        Handle sidebar item hover.
        
        Args:
            item: Item identifier
        """
        self.sidebar_hover_item = item
    
    def on_sidebar_item_leave(self) -> None:
        """Clear sidebar hover state."""
        self.sidebar_hover_item = None


# ============================================================================
#    COMPONENT LIBRARY - Reusable UI Primitives
# ============================================================================

def navbar_item(
    label: str,
    icon: str,
    is_active: bool = False,
    on_click: Optional[Any] = None,
) -> rx.Component:
    """
    Minimalist navigation item with hover animation.
    
    Args:
        label: Display label
        icon: Icon emoji/unicode
        is_active: Active state flag
        on_click: Click handler
        
    Returns:
        Reflex component
    """
    return rx.box(
        rx.hstack(
            # Icon
            rx.text(
                icon,
                font_size="1.25rem",
                color=ColorToken.ACCENT_PRIMARY if is_active else ColorToken.TEXT_SECONDARY,
                transition="color 0.2s ease",
            ),
            # Label
            rx.text(
                label,
                font_size="0.95rem",
                font_weight="500" if is_active else "400",
                color=ColorToken.TEXT_PRIMARY if is_active else ColorToken.TEXT_SECONDARY,
                transition="color 0.2s ease",
                font_family=FontFamily.PRIMARY,
            ),
            spacing="0.75rem",
            width="100%",
            align_items="center",
        ),
        padding="0.875rem 1rem",
        border_radius="0.5rem",
        background_color=(
            f"rgba({ColorToken.ACCENT_PRIMARY}, 0.1)" if is_active
            else "transparent"
        ),
        border_left=(
            f"3px solid {ColorToken.ACCENT_PRIMARY}" if is_active
            else "3px solid transparent"
        ),
        cursor="pointer",
        transition="all 0.2s ease",
        _hover={
            "background_color": f"rgba({ColorToken.ACCENT_PRIMARY}, 0.08)",
            "border_left_color": ColorToken.ACCENT_PRIMARY,
        },
        on_click=on_click,
        width="100%",
    )


def status_badge(
    label: str,
    value: str | float,
    status: str = "neutral",
    unit: str = "",
) -> rx.Component:
    """
    Minimalist status indicator badge.
    
    Args:
        label: Badge label
        value: Metric value
        status: Status type (neutral, success, warning, critical)
        unit: Unit suffix
        
    Returns:
        Reflex component
    """
    status_colors = {
        "success": ColorToken.STATUS_SUCCESS,
        "warning": ColorToken.STATUS_WARNING,
        "critical": ColorToken.STATUS_CRITICAL,
        "neutral": ColorToken.TEXT_SECONDARY,
    }
    
    return rx.box(
        rx.vstack(
            # Label
            rx.text(
                label,
                font_size="0.75rem",
                color=ColorToken.TEXT_SECONDARY,
                font_weight="500",
                letter_spacing="0.05em",
                text_transform="uppercase",
                font_family=FontFamily.PRIMARY,
            ),
            # Value
            rx.hstack(
                rx.text(
                    str(value),
                    font_size="1.5rem",
                    font_weight="700",
                    color=ColorToken.TEXT_PRIMARY,
                    font_family=FontFamily.MONO,
                ),
                rx.text(
                    unit,
                    font_size="0.875rem",
                    color=ColorToken.TEXT_SECONDARY,
                    font_family=FontFamily.MONO,
                ),
                spacing="0.25rem",
                align_items="baseline",
            ),
            spacing="0.25rem",
        ),
        padding="1rem",
        border_radius="0.75rem",
        background_color=ColorToken.CARD_SLATE,
        border=f"1px solid {ColorToken.BORDER_LASER}",
        width="100%",
    )


def metric_card(
    title: str,
    value: str | float,
    icon: str,
    trend: Optional[str] = None,
    color: str = ColorToken.ACCENT_PRIMARY,
) -> rx.Component:
    """
    Dashboard metric card with icon and trend.
    
    Args:
        title: Card title
        value: Metric value
        icon: Icon emoji
        trend: Trend indicator (e.g., "+5.2%")
        color: Accent color
        
    Returns:
        Reflex component
    """
    return rx.box(
        rx.vstack(
            # Header with icon
            rx.hstack(
                rx.text(icon, font_size="1.5rem"),
                rx.spacer(),
                rx.text(
                    title,
                    font_size="0.875rem",
                    color=ColorToken.TEXT_SECONDARY,
                    font_family=FontFamily.PRIMARY,
                ),
                width="100%",
            ),
            # Value
            rx.text(
                str(value),
                font_size="2rem",
                font_weight="700",
                color=ColorToken.TEXT_PRIMARY,
                font_family=FontFamily.MONO,
            ),
            # Trend (optional)
            rx.cond(
                trend,
                rx.text(
                    trend,
                    font_size="0.75rem",
                    color=color,
                    font_family=FontFamily.MONO,
                ),
                rx.spacer(),
            ),
            spacing="0.75rem",
        ),
        padding="1.5rem",
        border_radius="1rem",
        background_color=ColorToken.CARD_SLATE,
        border=f"1px solid {ColorToken.BORDER_LASER}",
        width="100%",
        transition="all 0.3s ease",
        _hover={
            "border_color": color,
            "box_shadow": f"0 8px 24px rgba(107, 90, 255, 0.1)",
        },
    )


def laser_divider(orientation: str = "horizontal") -> rx.Component:
    """
    Clean laser-thin divider.
    
    Args:
        orientation: "horizontal" or "vertical"
        
    Returns:
        Reflex component
    """
    if orientation == "horizontal":
        return rx.box(
            width="100%",
            height="1px",
            background_color=ColorToken.BORDER_LASER,
        )
    else:
        return rx.box(
            width="1px",
            height="100%",
            background_color=ColorToken.BORDER_LASER,
        )


# ============================================================================
#    LAYOUT COMPONENTS - Structural Canvas
# ============================================================================

def sidebar_navigation() -> rx.Component:
    """
    Left fixed navigation sidebar with deep space black background.
    
    Features:
    - Fixed width (280px)
    - Deep space black background (#080A10)
    - Clean navigation links with hover animations
    - User profile status badge at base
    - Widely-tracked typography
    
    Returns:
        Reflex vstack component
    """
    return rx.box(
        rx.vstack(
            # Branding header
            rx.vstack(
                rx.text(
                    "EduSphere",
                    font_size="1.25rem",
                    font_weight="700",
                    color=ColorToken.TEXT_PRIMARY,
                    letter_spacing="0.05em",
                    font_family=FontFamily.PRIMARY,
                ),
                rx.text(
                    "Central",
                    font_size="0.875rem",
                    color=ColorToken.ACCENT_PRIMARY,
                    letter_spacing="0.1em",
                    text_transform="uppercase",
                    font_weight="600",
                    font_family=FontFamily.PRIMARY,
                ),
                spacing="0.25rem",
                padding="1.5rem 1rem",
            ),
            
            # Divider
            laser_divider(),
            
            # Navigation items
            rx.vstack(
                navbar_item("📊 Dashboard", "📊", AppState.active_route == "dashboard", on_click=lambda: AppState.navigate_to("dashboard")),
                navbar_item("🎛️ Command Center", "🎛️", AppState.active_route == "command_center", on_click=lambda: AppState.navigate_to("command_center")),
                navbar_item("👥 Student Pathways", "👥", AppState.active_route == "pathways", on_click=lambda: AppState.navigate_to("pathways")),
                navbar_item("📚 Curriculum Canvas", "📚", AppState.active_route == "curriculum", on_click=lambda: AppState.navigate_to("curriculum")),
                navbar_item("🌐 Global Operations", "🌐", AppState.active_route == "operations", on_click=lambda: AppState.navigate_to("operations")),
                navbar_item("💼 Asset Ledger", "💼", AppState.active_route == "assets", on_click=lambda: AppState.navigate_to("assets")),
                spacing="0.5rem",
                padding="1rem",
            ),
            
            # Spacer to push profile to bottom
            rx.spacer(),
            
            # Divider before profile
            laser_divider(),
            
            # User profile status badge
            rx.box(
                rx.vstack(
                    # Avatar
                    rx.box(
                        rx.text(
                            AppState.current_user_avatar,
                            font_size="1rem",
                            font_weight="700",
                            color=ColorToken.TEXT_PRIMARY,
                        ),
                        padding="0.75rem 1rem",
                        border_radius="0.5rem",
                        background_color=f"rgba({ColorToken.ACCENT_PRIMARY}, 0.2)",
                        width="100%",
                        text_align="center",
                    ),
                    # User info
                    rx.vstack(
                        rx.text(
                            AppState.current_user_name,
                            font_size="0.875rem",
                            font_weight="600",
                            color=ColorToken.TEXT_PRIMARY,
                            font_family=FontFamily.PRIMARY,
                            no_of_lines=1,
                        ),
                        rx.text(
                            AppState.current_user_role,
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            letter_spacing="0.05em",
                            font_family=FontFamily.PRIMARY,
                        ),
                        spacing="0.25rem",
                    ),
                    spacing="0.75rem",
                ),
                padding="1rem",
                border_radius="0.75rem",
                background_color=f"rgba({ColorToken.ACCENT_PRIMARY}, 0.08)",
                border=f"1px solid {ColorToken.BORDER_LASER}",
                width="100%",
            ),
            
            spacing="0",
            width="280px",
            height="100vh",
            background_color=ColorToken.BACKGROUND_DEEP,
            padding="0",
            position="fixed",
            left="0",
            top="0",
            overflow_y="auto",
        ),
        width="280px",
        height="100vh",
        background_color=ColorToken.BACKGROUND_DEEP,
    )


def main_content_canvas() -> rx.Component:
    """
    Main content workspace with deep slate background and curved left border.
    
    Features:
    - Background: Deep slate (#121622)
    - Inward-curving left border (border_radius="2.5rem 0 0 2.5rem")
    - Asymmetric layout slipping underneath sidebar
    - No overflow (clean frame)
    
    Returns:
        Reflex component
    """
    return rx.box(
        rx.vstack(
            # Header section
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.text(
                            rx.cond(
                                AppState.active_route == "dashboard",
                                "Dashboard",
                                rx.cond(
                                    AppState.active_route == "command_center",
                                    "Command Center",
                                    rx.cond(
                                        AppState.active_route == "pathways",
                                        "Student Pathways",
                                        "Content",
                                    ),
                                ),
                            ),
                            font_size="2rem",
                            font_weight="700",
                            color=ColorToken.TEXT_PRIMARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        rx.text(
                            "Real-time system monitoring and control",
                            font_size="0.875rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.PRIMARY,
                        ),
                        spacing="0.5rem",
                    ),
                    rx.spacer(),
                    # Header actions (placeholder)
                    rx.hstack(
                        rx.text("⌘K", font_size="0.875rem", color=ColorToken.TEXT_SECONDARY),
                        spacing="1rem",
                    ),
                    width="100%",
                    align_items="center",
                ),
                padding="2rem",
            ),
            
            # Divider
            laser_divider(),
            
            # Content grid - Metrics
            rx.vstack(
                rx.text(
                    "Live Metrics",
                    font_size="0.875rem",
                    color=ColorToken.TEXT_SECONDARY,
                    letter_spacing="0.1em",
                    text_transform="uppercase",
                    font_weight="600",
                    font_family=FontFamily.PRIMARY,
                ),
                rx.grid(
                    metric_card(
                        "Total Students",
                        AppState.students_count,
                        "👥",
                        "+12.5%",
                        ColorToken.ACCENT_PRIMARY,
                    ),
                    metric_card(
                        "Average GPA",
                        f"{AppState.average_gpa:.2f}",
                        "📊",
                        "+0.12",
                        ColorToken.STATUS_SUCCESS,
                    ),
                    metric_card(
                        "Active Conflicts",
                        AppState.active_conflicts_count,
                        "⚠️",
                        "3 Critical",
                        ColorToken.STATUS_CRITICAL,
                    ),
                    metric_card(
                        "System Uptime",
                        f"{AppState.system_uptime:.2f}%",
                        "✓",
                        "+0.01%",
                        ColorToken.STATUS_SUCCESS,
                    ),
                    columns="4",
                    spacing="1rem",
                    width="100%",
                ),
                spacing="1rem",
                padding="2rem",
            ),
            
            # Content divider
            laser_divider(),
            
            # Dynamic content section
            rx.box(
                rx.vstack(
                    rx.text(
                        "Scheduling Status",
                        font_size="0.875rem",
                        color=ColorToken.TEXT_SECONDARY,
                        letter_spacing="0.1em",
                        text_transform="uppercase",
                        font_weight="600",
                        font_family=FontFamily.PRIMARY,
                    ),
                    rx.text(
                        "All courses are optimally scheduled. 0 conflicts detected.",
                        font_size="0.95rem",
                        color=ColorToken.TEXT_PRIMARY,
                        font_family=FontFamily.PRIMARY,
                    ),
                    rx.text(
                        "Last solver run: 2.4ms • Confidence: 98.5%",
                        font_size="0.75rem",
                        color=ColorToken.TEXT_SECONDARY,
                        font_family=FontFamily.MONO,
                    ),
                    spacing="0.75rem",
                ),
                padding="2rem",
            ),
            
            spacing="0",
            width="100%",
            height="100%",
            overflow_y="auto",
        ),
        margin_left="280px",
        width="calc(100vw - 280px)",
        height="100vh",
        background_color=ColorToken.CARD_SLATE,
        border_radius="2.5rem 0 0 2.5rem",
        overflow="hidden",
    )


def dashboard_layout() -> rx.Component:
    """
    Master dashboard layout combining sidebar and canvas.
    
    Asymmetric structure:
    - Left: Fixed navigation sidebar (280px)
    - Right: Main content with curved inward border
    
    Returns:
        Reflex component
    """
    return rx.box(
        rx.hstack(
            sidebar_navigation(),
            main_content_canvas(),
            spacing="0",
            width="100%",
            height="100vh",
            overflow="hidden",
        ),
        width="100%",
        height="100vh",
        background_color=ColorToken.BACKGROUND_DEEP,
        overflow="hidden",
    )


# ============================================================================
#    APPLICATION INITIALIZATION
# ============================================================================

def create_app() -> rx.App:
    """
    Create and configure Reflex application instance.
    
    Returns:
        Configured Reflex app
    """
    # Initialize app
    app = rx.App()
    
    # Register state
    app.add_page(dashboard_layout, path="/")
    
    return app


# Create app instance
app = create_app()

# ============================================================================
#    ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """Run the application."""
    app.compile()
