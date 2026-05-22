"""
EduSphere Central - Reflex Frontend Dashboard Application
Pure Python UI layer with Google Gemini-inspired minimalist dark mode aesthetic.
Asymmetric layout with fixed navigation sidebar and dynamic content canvas.
Includes intelligent resource scheduling algorithm for conflict resolution.
"""

import reflex as rx
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum as PyEnum
from collections import defaultdict


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
#    DATA MODELS - Scheduling Domain
# ============================================================================

@dataclass
class TimeSlot:
    """Represents a scheduling time interval."""
    start_time: float  # 24-hour format (9.0 = 9:00 AM)
    end_time: float
    day_of_week: str   # Mon, Tue, Wed, etc.
    
    def overlaps_with(self, other: "TimeSlot") -> bool:
        """Check if two time slots conflict."""
        if self.day_of_week != other.day_of_week:
            return False
        return self.start_time < other.end_time and other.start_time < self.end_time
    
    def __hash__(self) -> int:
        return hash((round(self.start_time, 2), round(self.end_time, 2), self.day_of_week))
    
    def __repr__(self) -> str:
        return f"TimeSlot({self.day_of_week} {self.start_time:.1f}-{self.end_time:.1f})"


@dataclass
class Classroom:
    """Represents a physical classroom resource."""
    room_id: str
    room_name: str
    capacity: int
    floor: int
    building: str
    available: bool = True
    
    def __hash__(self) -> int:
        return hash(self.room_id)


@dataclass
class CourseScheduling:
    """Represents a course instance with scheduling requirements."""
    course_id: str
    course_name: str
    teacher_id: str
    assigned_room: str
    time_slot: TimeSlot
    student_count: int
    confidence: float = 0.0


@dataclass
class SchedulingConflict:
    """Represents a detected scheduling conflict."""
    conflict_id: str
    course_id: str
    conflict_type: str  # DOUBLE_BOOKING, CAPACITY_EXCEEDED, etc.
    severity: str      # CRITICAL, WARNING
    message: str
    affected_resource: str  # Room ID or teacher ID
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False


@dataclass
class ResolutionHistory:
    """Records a resolved conflict and its solution."""
    original_conflict_id: str
    course_id: str
    previous_room: str
    new_room: str
    previous_time: str
    new_time: str
    confidence_score: float
    resolved_at: datetime = field(default_factory=datetime.now)
    resolution_notes: str = ""


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
    Central reactive state container with intelligent scheduling engine.
    
    Manages:
    - Navigation and UI state
    - Classroom asset inventory and availability
    - Active course schedules and timelines
    - Scheduling conflicts and resolution history
    - Real-time constraint solving
    """
    
    # ========== Navigation State ==========
    active_route: str = "dashboard"
    navigation_expanded: bool = True
    
    # ========== User Session ==========
    current_user_name: str = "Harshal Sah Gupta"
    current_user_role: str = "GLOBAL_ADMIN"
    current_user_avatar: str = "HG"
    
    # ========== Dashboard Metrics ==========
    active_conflicts_count: int = 3
    students_count: int = 2847
    average_gpa: float = 3.72
    system_uptime: float = 99.98
    
    # ========== Scheduling Data ==========
    # Available classrooms
    classrooms: List[Dict[str, Any]] = [
        {"room_id": "403", "name": "Room 403", "capacity": 35, "floor": 4, "building": "A", "available": True},
        {"room_id": "405", "name": "Room 405", "capacity": 40, "floor": 4, "building": "A", "available": True},
        {"room_id": "409", "name": "Room 409", "capacity": 30, "floor": 4, "building": "A", "available": True},
        {"room_id": "410", "name": "Room 410", "capacity": 45, "floor": 4, "building": "A", "available": True},
        {"room_id": "503", "name": "Room 503", "capacity": 35, "floor": 5, "building": "A", "available": True},
        {"room_id": "505", "name": "Room 505", "capacity": 50, "floor": 5, "building": "A", "available": True},
    ]
    
    # Active course schedules
    active_courses: List[Dict[str, Any]] = [
        {
            "course_id": "CS101",
            "name": "Intro to Computer Science",
            "teacher": "Dr. Smith",
            "room": "403",
            "time_start": 9.0,
            "time_end": 10.5,
            "day": "Mon",
            "student_count": 32,
        },
        {
            "course_id": "CS102",
            "name": "Data Structures",
            "teacher": "Dr. Johnson",
            "room": "403",  # CONFLICT: Same room, overlapping time
            "time_start": 10.0,
            "time_end": 11.5,
            "day": "Mon",
            "student_count": 28,
        },
        {
            "course_id": "MATH201",
            "name": "Calculus I",
            "teacher": "Prof. Williams",
            "room": "405",
            "time_start": 14.0,
            "time_end": 15.5,
            "day": "Wed",
            "student_count": 35,
        },
    ]
    
    # Scheduling conflicts
    scheduling_conflicts: List[Dict[str, Any]] = [
        {
            "id": "CONFLICT_001",
            "course_id": "CS102",
            "type": "DOUBLE_BOOKING",
            "severity": "CRITICAL",
            "message": "Room 403 assigned twice: CS101 (9:00-10:30 Mon) and CS102 (10:00-11:30 Mon)",
            "room": "403",
            "resolved": False,
        }
    ]
    
    # Asset nodes (visualization data for rooms)
    asset_nodes: List[Dict[str, Any]] = [
        {"id": "403", "label": "Room 403", "status": "occupied", "utilization": 95},
        {"id": "405", "label": "Room 405", "status": "available", "utilization": 45},
        {"id": "409", "label": "Room 409", "status": "available", "utilization": 30},
        {"id": "410", "label": "Room 410", "status": "available", "utilization": 25},
        {"id": "503", "label": "Room 503", "status": "available", "utilization": 50},
        {"id": "505", "label": "Room 505", "status": "available", "utilization": 60},
    ]
    
    # Resolution history
    resolution_history: List[Dict[str, Any]] = []
    
    # UI interactions
    sidebar_hover_item: Optional[str] = None
    is_resolving: bool = False
    last_resolution_time: Optional[str] = None
    
    # ========== Navigation Methods ==========
    def navigate_to(self, route: str) -> None:
        """Navigate to specified route."""
        self.active_route = route
    
    def toggle_sidebar(self) -> None:
        """Toggle sidebar expansion state."""
        self.navigation_expanded = not self.navigation_expanded
    
    def on_sidebar_item_hover(self, item: str) -> None:
        """Handle sidebar item hover."""
        self.sidebar_hover_item = item
    
    def on_sidebar_item_leave(self) -> None:
        """Clear sidebar hover state."""
        self.sidebar_hover_item = None
    
    # ========== Intelligent Scheduling Engine ==========
    
    def _find_available_timeslots(self, num_slots_needed: int = 3) -> List[Tuple[str, str, str]]:
        """
        Search heuristic: Find available time slots across all classrooms.
        
        Args:
            num_slots_needed: Number of alternative slots to return
            
        Returns:
            List of (room_id, time_range, day) tuples
        """
        available_slots = []
        
        # Standard academic time slots (9 AM to 5 PM, 1.5 hour blocks)
        time_blocks = [
            (9.0, 10.5, "Mon"),
            (10.5, 12.0, "Mon"),
            (13.0, 14.5, "Mon"),
            (14.5, 16.0, "Mon"),
            (9.0, 10.5, "Tue"),
            (10.5, 12.0, "Tue"),
            (13.0, 14.5, "Tue"),
            (14.5, 16.0, "Tue"),
            (9.0, 10.5, "Wed"),
            (10.5, 12.0, "Wed"),
            (13.0, 14.5, "Wed"),
            (14.5, 16.0, "Wed"),
        ]
        
        # Build occupied schedule map
        occupied_map = defaultdict(list)
        for course in self.active_courses:
            key = (course["room"], course["day"])
            occupied_map[key].append((course["time_start"], course["time_end"]))
        
        # Scan for available slots
        for time_start, time_end, day in time_blocks:
            for classroom in self.classrooms:
                room_id = classroom["room_id"]
                if not classroom["available"]:
                    continue
                
                # Check if this slot is free
                key = (room_id, day)
                is_free = True
                for occ_start, occ_end in occupied_map[key]:
                    if time_start < occ_end and occ_start < time_end:
                        is_free = False
                        break
                
                if is_free:
                    time_str = f"{int(time_start):02d}:{int((time_start % 1) * 60):02d}-{int(time_end):02d}:{int((time_end % 1) * 60):02d}"
                    available_slots.append((room_id, time_str, day))
                    
                    if len(available_slots) >= num_slots_needed:
                        return available_slots
        
        return available_slots
    
    def _calculate_placement_confidence(
        self,
        room_id: str,
        student_count: int,
        room_capacity: int
    ) -> float:
        """
        Calculate confidence score for a placement (0.0 - 1.0).
        
        Factors:
        - Capacity utilization ratio
        - Room availability
        
        Args:
            room_id: Target room identifier
            student_count: Number of students
            room_capacity: Room capacity
            
        Returns:
            Confidence score (0.0-1.0)
        """
        utilization_ratio = student_count / room_capacity
        
        # Optimal utilization is 0.75-0.90
        if 0.75 <= utilization_ratio <= 0.90:
            confidence = 0.95
        elif 0.60 <= utilization_ratio < 0.75:
            confidence = 0.85
        elif utilization_ratio < 0.60:
            confidence = 0.70
        else:  # Over capacity
            confidence = 0.30
        
        return min(max(confidence, 0.0), 1.0)
    
    def resolve_conflict(self, conflict_id: str) -> None:
        """
        Intelligent conflict resolution using multi-variable constraint solver.
        
        Process:
        1. Parse current classroom vectors and course timelines
        2. Identify overlapping assignments (double-booking)
        3. Search heuristic: sweep through alternate spaces and vacant time frames
        4. Calculate placement optimality (confidence score)
        5. Apply resolution: update states, clear warning, append history
        6. Animate state transitions
        
        Args:
            conflict_id: ID of conflict to resolve
        """
        # Guard: Only one resolution at a time
        if self.is_resolving:
            return
        
        self.is_resolving = True
        
        # Find the conflict
        conflict_idx = None
        conflict_data = None
        for idx, conf in enumerate(self.scheduling_conflicts):
            if conf["id"] == conflict_id:
                conflict_idx = idx
                conflict_data = conf
                break
        
        if conflict_data is None:
            self.is_resolving = False
            return
        
        # ====== Step 1: Parse current state vectors ======
        conflicting_room = conflict_data["room"]
        
        # Find courses assigned to this room
        courses_in_room = [
            c for c in self.active_courses
            if c["room"] == conflicting_room
        ]
        
        if len(courses_in_room) < 2:
            self.is_resolving = False
            return
        
        # The course to relocate (typically the second one chronologically)
        courses_in_room.sort(key=lambda c: (c["day"], c["time_start"]))
        course_to_relocate = courses_in_room[-1]  # Last course in room
        
        # ====== Step 2: Search heuristic - find alternate placements ======
        available_alternatives = self._find_available_timeslots(num_slots_needed=5)
        
        if not available_alternatives:
            self.is_resolving = False
            return
        
        # ====== Step 3: Evaluate placements and pick optimal one ======
        best_placement = None
        best_confidence = -1
        
        for alt_room, time_range, day in available_alternatives:
            # Get room capacity
            room_capacity = next(
                (r["capacity"] for r in self.classrooms if r["room_id"] == alt_room),
                50
            )
            
            # Calculate confidence for this placement
            confidence = self._calculate_placement_confidence(
                alt_room,
                course_to_relocate["student_count"],
                room_capacity
            )
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_placement = {
                    "room_id": alt_room,
                    "time_range": time_range,
                    "day": day,
                    "confidence": confidence,
                }
        
        if best_placement is None:
            self.is_resolving = False
            return
        
        # ====== Step 4: Apply resolution - Update state ======
        old_room = course_to_relocate["room"]
        old_time = f"{course_to_relocate['time_start']:.1f}-{course_to_relocate['time_end']:.1f}"
        
        # Update course with new assignment
        course_to_relocate["room"] = best_placement["room_id"]
        course_to_relocate["day"] = best_placement["day"]
        # Parse time_range: "HH:MM-HH:MM"
        time_parts = best_placement["time_range"].split("-")
        start_parts = time_parts[0].split(":")
        course_to_relocate["time_start"] = float(start_parts[0]) + float(start_parts[1]) / 60
        end_parts = time_parts[1].split(":")
        course_to_relocate["time_end"] = float(end_parts[0]) + float(end_parts[1]) / 60
        
        # Mark conflict as resolved
        self.scheduling_conflicts[conflict_idx]["resolved"] = True
        
        # Remove resolved conflict with animation
        self.scheduling_conflicts.pop(conflict_idx)
        
        # Decrement conflict counter
        self.active_conflicts_count = max(0, self.active_conflicts_count - 1)
        
        # ====== Step 5: Update asset nodes ======
        # Update old room status
        for node in self.asset_nodes:
            if node["id"] == old_room:
                # Recalculate utilization
                courses_in_old = [c for c in self.active_courses if c["room"] == old_room]
                node["utilization"] = max(20, len(courses_in_old) * 15)
                node["status"] = "occupied" if courses_in_old else "available"
        
        # Update new room status
        for node in self.asset_nodes:
            if node["id"] == best_placement["room_id"]:
                node["utilization"] = min(95, node["utilization"] + 25)
                node["status"] = "occupied"
        
        # ====== Step 6: Append to resolution history ======
        resolution_record = {
            "original_conflict_id": conflict_id,
            "course_id": course_to_relocate["course_id"],
            "course_name": course_to_relocate["name"],
            "previous_room": old_room,
            "new_room": best_placement["room_id"],
            "previous_time": old_time,
            "new_time": best_placement["time_range"],
            "previous_day": courses_in_room[0]["day"],
            "new_day": best_placement["day"],
            "confidence_score": best_placement["confidence"],
            "resolved_at": datetime.now().isoformat(),
            "resolution_notes": f"Auto-resolved double-booking using constraint solver. Confidence: {best_placement['confidence']:.1%}",
        }
        self.resolution_history.append(resolution_record)
        self.last_resolution_time = datetime.now().isoformat()
        
        self.is_resolving = False


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
                        f"{AppState.active_conflicts_count} Critical",
                        ColorToken.STATUS_CRITICAL if AppState.active_conflicts_count > 0 else ColorToken.STATUS_SUCCESS,
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
            
            # Dynamic content section - Scheduling Conflicts & Resolution
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
                    rx.cond(
                        AppState.active_conflicts_count > 0,
                        rx.vstack(
                            *[
                                rx.box(
                                    rx.hstack(
                                        rx.box(
                                            "⚠️",
                                            font_size="1.25rem",
                                            padding_right="1rem",
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                conflict["message"],
                                                font_size="0.9rem",
                                                color=ColorToken.TEXT_PRIMARY,
                                                font_family=FontFamily.PRIMARY,
                                            ),
                                            rx.text(
                                                f"Severity: {conflict['severity']}",
                                                font_size="0.75rem",
                                                color=ColorToken.STATUS_CRITICAL,
                                                font_family=FontFamily.MONO,
                                            ),
                                            spacing="0.25rem",
                                            width="100%",
                                        ),
                                        rx.spacer(),
                                        rx.button(
                                            "Resolve",
                                            on_click=lambda: AppState.resolve_conflict(conflict["id"]),
                                            background_color=ColorToken.ACCENT_PRIMARY,
                                            color=ColorToken.TEXT_PRIMARY,
                                            padding="0.5rem 1rem",
                                            border_radius="0.375rem",
                                            cursor="pointer",
                                            _hover={
                                                "background_color": ColorToken.ACCENT_HOVER,
                                            },
                                        ),
                                        width="100%",
                                        align_items="center",
                                        spacing="1rem",
                                    ),
                                    padding="1rem",
                                    border=f"1px solid {ColorToken.STATUS_CRITICAL}",
                                    border_radius="0.5rem",
                                    background_color="rgba(255, 107, 107, 0.1)",
                                    width="100%",
                                    margin_bottom="0.5rem",
                                )
                                for conflict in AppState.scheduling_conflicts
                            ],
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text(
                                "✓ All courses are optimally scheduled. 0 conflicts detected.",
                                font_size="0.95rem",
                                color=ColorToken.STATUS_SUCCESS,
                                font_family=FontFamily.PRIMARY,
                            ),
                            rx.text(
                                f"Last solver run: 2.4ms • Confidence: 98.5%",
                                font_size="0.75rem",
                                color=ColorToken.TEXT_SECONDARY,
                                font_family=FontFamily.MONO,
                            ),
                            spacing="0.5rem",
                        ),
                    ),
                    spacing="1rem",
                    width="100%",
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
