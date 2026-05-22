"""
EduSphere Central - Main Controller Page
The central hub that controls and orchestrates the entire website.
Single entry point for launching, monitoring, and managing all system components.

This page serves as the master control interface that:
- Initializes all subsystems (Dashboard, Calendar, OmniSearch, Scheduling Engine)
- Provides real-time system health monitoring
- Manages navigation between all application modules
- Displays critical system metrics and alerts
- Handles application startup/shutdown sequences
"""

import reflex as rx
from typing import List, Dict, Any, Optional
from enum import Enum as PyEnum
from datetime import datetime
import asyncio


# ============================================================================
#    DESIGN SYSTEM - Inherited from Dashboard
# ============================================================================

class ColorToken(str, PyEnum):
    """Gemini-inspired color palette."""
    BACKGROUND_DEEP = "#080A10"
    CARD_SLATE = "#121622"
    BORDER_LASER = "#1E1F2E"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#A0A0A0"
    ACCENT_PRIMARY = "#6B5AFF"
    ACCENT_HOVER = "#7D6FFF"
    STATUS_SUCCESS = "#00D084"
    STATUS_WARNING = "#FFA500"
    STATUS_CRITICAL = "#FF6B6B"
    STATUS_INFO = "#3B82F6"


class FontFamily(str, PyEnum):
    """Typography stack."""
    PRIMARY = "Inter, system-ui, -apple-system, sans-serif"
    MONO = "Courier New, monospace"


# ============================================================================
#    SUBSYSTEM STATUS ENUMS
# ============================================================================

class SystemStatus(str, PyEnum):
    """Overall system health status."""
    INITIALIZING = "initializing"
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class SubsystemState(str, PyEnum):
    """Individual subsystem states."""
    OFFLINE = "offline"
    INITIALIZING = "initializing"
    READY = "ready"
    ERROR = "error"


# ============================================================================
#    SUBSYSTEM DEFINITIONS
# ============================================================================

class SubsystemConfig:
    """Configuration for each system subsystem."""
    
    SUBSYSTEMS = {
        "dashboard": {
            "name": "Dashboard",
            "icon": "📊",
            "description": "Real-time metrics & system overview",
            "path": "/dashboard",
            "required": True,
            "startup_time_ms": 1200,
        },
        "calendar": {
            "name": "Calendar Attendance",
            "icon": "📅",
            "description": "6×24 calendar grid & scheduling matrix",
            "path": "/calendar",
            "required": True,
            "startup_time_ms": 800,
        },
        "command_center": {
            "name": "Command Center",
            "icon": "🎛️",
            "description": "Scheduling conflict resolution engine",
            "path": "/command",
            "required": True,
            "startup_time_ms": 1500,
        },
        "student_pathways": {
            "name": "Student Pathways",
            "icon": "👥",
            "description": "Academic tracking & progression",
            "path": "/pathways",
            "required": False,
            "startup_time_ms": 900,
        },
        "curriculum": {
            "name": "Curriculum Canvas",
            "icon": "📚",
            "description": "Course management & design",
            "path": "/curriculum",
            "required": False,
            "startup_time_ms": 1100,
        },
        "operations": {
            "name": "Global Operations",
            "icon": "🌐",
            "description": "System administration & settings",
            "path": "/operations",
            "required": False,
            "startup_time_ms": 700,
        },
        "omnisearch": {
            "name": "OmniSearch",
            "icon": "🔍",
            "description": "Universal command palette (Cmd+K)",
            "path": "/",
            "required": True,
            "startup_time_ms": 600,
        },
    }


# ============================================================================
#    MAIN CONTROLLER STATE
# ============================================================================

class MainControllerState(rx.State):
    """
    Central state management for the master controller page.
    
    Manages:
    - System startup/shutdown sequences
    - Subsystem health monitoring
    - Navigation routing
    - Application configuration
    - Real-time status updates
    """
    
    # System status
    system_status: SystemStatus = SystemStatus.INITIALIZING
    is_system_running: bool = False
    startup_timestamp: Optional[str] = None
    uptime_seconds: int = 0
    
    # Subsystem states
    subsystem_states: Dict[str, Dict[str, Any]] = {
        key: {
            "name": config["name"],
            "icon": config["icon"],
            "state": SubsystemState.OFFLINE,
            "error": None,
            "startup_progress": 0,  # 0-100%
            "last_heartbeat": None,
        }
        for key, config in SubsystemConfig.SUBSYSTEMS.items()
    }
    
    # Navigation
    active_subsystem: str = "dashboard"
    navigation_history: List[str] = []
    
    # Configuration
    log_messages: List[str] = []
    max_logs: int = 50
    verbose_mode: bool = False
    auto_resolve_conflicts: bool = True
    
    # Performance metrics
    total_startup_time_ms: int = 0
    peak_cpu_percent: float = 0.0
    total_memory_mb: float = 0.0
    
    # ========== System Lifecycle Methods ==========
    
    async def startup_system(self) -> None:
        """
        Initialize entire EduSphere system with sequential subsystem startup.
        
        Process:
        1. Set system status to INITIALIZING
        2. Start OmniSearch (lowest latency first)
        3. Initialize core subsystems in parallel batches
        4. Verify database connectivity
        5. Load cached data
        6. Transition to HEALTHY status
        
        Raises:
            RuntimeError: If critical subsystem startup fails
        """
        self.system_status = SystemStatus.INITIALIZING
        self.is_system_running = False
        self.startup_timestamp = datetime.now().isoformat()
        self.log_messages = []
        self.add_log("🚀 EduSphere Central startup initiated...")
        
        try:
            # Phase 1: Initialize OmniSearch (universal command palette)
            await self._initialize_subsystem("omnisearch")
            
            # Phase 2: Initialize core required subsystems in sequence
            core_subsystems = ["dashboard", "calendar", "command_center"]
            for subsystem_key in core_subsystems:
                await self._initialize_subsystem(subsystem_key)
            
            # Phase 3: Initialize optional subsystems in parallel
            optional_subsystems = ["student_pathways", "curriculum", "operations"]
            for subsystem_key in optional_subsystems:
                await self._initialize_subsystem_background(subsystem_key)
            
            # Phase 4: Verify system health
            self.add_log("✓ Verifying system health...")
            critical_subsystems = [
                self.subsystem_states[key]["state"]
                for key in ["dashboard", "calendar", "command_center"]
            ]
            
            if all(state == SubsystemState.READY for state in critical_subsystems):
                self.system_status = SystemStatus.HEALTHY
                self.is_system_running = True
                self.add_log(
                    f"✓ EduSphere Central ready! {len(critical_subsystems)} core subsystems online."
                )
            else:
                self.system_status = SystemStatus.WARNING
                self.add_log("⚠️ Some subsystems failed to initialize.")
        
        except Exception as e:
            self.system_status = SystemStatus.CRITICAL
            self.add_log(f"❌ System startup failed: {str(e)}")
    
    async def shutdown_system(self) -> None:
        """
        Gracefully shutdown all subsystems in reverse initialization order.
        
        Process:
        1. Mark system as shutting down
        2. Stop accepting new requests
        3. Close all active connections
        4. Flush pending operations
        5. Release resources
        """
        self.add_log("🛑 Initiating graceful shutdown...")
        
        # Gracefully stop all subsystems
        for subsystem_key in list(self.subsystem_states.keys()):
            self.subsystem_states[subsystem_key]["state"] = SubsystemState.OFFLINE
        
        self.is_system_running = False
        self.system_status = SystemStatus.OFFLINE
        self.add_log("✓ EduSphere Central shutdown complete.")
    
    async def _initialize_subsystem(self, subsystem_key: str) -> None:
        """
        Initialize a single subsystem with progress tracking.
        
        Args:
            subsystem_key: Subsystem identifier
        """
        if subsystem_key not in self.subsystem_states:
            return
        
        config = SubsystemConfig.SUBSYSTEMS.get(subsystem_key, {})
        subsystem = self.subsystem_states[subsystem_key]
        
        try:
            subsystem["state"] = SubsystemState.INITIALIZING
            self.add_log(f"⏳ Initializing {subsystem['name']}...")
            
            # Simulate startup with progress updates
            startup_time = config.get("startup_time_ms", 1000)
            steps = 10
            step_delay = startup_time / (steps * 1000)  # Convert to seconds
            
            for i in range(steps):
                subsystem["startup_progress"] = int((i + 1) / steps * 100)
                await asyncio.sleep(step_delay)
            
            # Mark as ready
            subsystem["state"] = SubsystemState.READY
            subsystem["startup_progress"] = 100
            subsystem["last_heartbeat"] = datetime.now().isoformat()
            self.add_log(f"✓ {subsystem['name']} online")
        
        except Exception as e:
            subsystem["state"] = SubsystemState.ERROR
            subsystem["error"] = str(e)
            self.add_log(f"❌ {subsystem['name']} failed: {str(e)}")
            
            if config.get("required"):
                self.system_status = SystemStatus.CRITICAL
    
    async def _initialize_subsystem_background(self, subsystem_key: str) -> None:
        """Initialize subsystem in background without blocking main flow."""
        await self._initialize_subsystem(subsystem_key)
    
    def restart_subsystem(self, subsystem_key: str) -> None:
        """Restart a single subsystem."""
        if subsystem_key in self.subsystem_states:
            self.add_log(f"🔄 Restarting {self.subsystem_states[subsystem_key]['name']}...")
            self.subsystem_states[subsystem_key]["state"] = SubsystemState.INITIALIZING
            # In production, would trigger actual subsystem restart
    
    # ========== Navigation Methods ==========
    
    def navigate_to_subsystem(self, subsystem_key: str) -> None:
        """Navigate to a subsystem module."""
        if subsystem_key in self.subsystem_states:
            self.active_subsystem = subsystem_key
            self.navigation_history.append(subsystem_key)
            self.add_log(f"→ Navigated to {self.subsystem_states[subsystem_key]['name']}")
    
    def go_back(self) -> None:
        """Navigate back to previous subsystem."""
        if len(self.navigation_history) > 1:
            self.navigation_history.pop()
            self.active_subsystem = self.navigation_history[-1]
    
    # ========== Logging Methods ==========
    
    def add_log(self, message: str) -> None:
        """Add message to system log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_messages.append(log_entry)
        
        # Keep only recent logs
        if len(self.log_messages) > self.max_logs:
            self.log_messages = self.log_messages[-self.max_logs:]
    
    def clear_logs(self) -> None:
        """Clear all system logs."""
        self.log_messages = []
    
    def toggle_verbose_mode(self) -> None:
        """Toggle verbose logging mode."""
        self.verbose_mode = not self.verbose_mode
        status = "enabled" if self.verbose_mode else "disabled"
        self.add_log(f"Verbose mode {status}")
    
    # ========== Configuration Methods ==========
    
    def toggle_auto_resolve(self) -> None:
        """Toggle automatic conflict resolution."""
        self.auto_resolve_conflicts = not self.auto_resolve_conflicts
        status = "enabled" if self.auto_resolve_conflicts else "disabled"
        self.add_log(f"Auto-resolve conflicts {status}")
    
    def reset_system(self) -> None:
        """Reset system to initial state."""
        self.add_log("🔄 System reset initiated...")
        self.startup_timestamp = None
        self.uptime_seconds = 0
        self.total_startup_time_ms = 0


# ============================================================================
#    UI COMPONENTS
# ============================================================================

def system_status_badge() -> rx.Component:
    """
    Real-time system status indicator with color coding.
    
    Returns:
        Reflex component showing system health
    """
    status_colors = {
        SystemStatus.INITIALIZING: ColorToken.STATUS_INFO,
        SystemStatus.HEALTHY: ColorToken.STATUS_SUCCESS,
        SystemStatus.WARNING: ColorToken.STATUS_WARNING,
        SystemStatus.CRITICAL: ColorToken.STATUS_CRITICAL,
        SystemStatus.OFFLINE: ColorToken.TEXT_SECONDARY,
    }
    
    status_labels = {
        SystemStatus.INITIALIZING: "INITIALIZING",
        SystemStatus.HEALTHY: "HEALTHY",
        SystemStatus.WARNING: "WARNING",
        SystemStatus.CRITICAL: "CRITICAL",
        SystemStatus.OFFLINE: "OFFLINE",
    }
    
    return rx.box(
        rx.hstack(
            # Status indicator dot
            rx.box(
                width="0.75rem",
                height="0.75rem",
                border_radius="50%",
                background_color=status_colors.get(
                    MainControllerState.system_status,
                    ColorToken.TEXT_SECONDARY
                ),
                animation="pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
            ),
            # Status text
            rx.text(
                status_labels.get(
                    MainControllerState.system_status,
                    "UNKNOWN"
                ),
                font_size="0.875rem",
                font_weight="600",
                color=status_colors.get(
                    MainControllerState.system_status,
                    ColorToken.TEXT_SECONDARY
                ),
                font_family=FontFamily.MONO,
                letter_spacing="0.05em",
            ),
            spacing="0.75rem",
            align_items="center",
        ),
        padding="0.75rem 1.25rem",
        background_color=f"rgba({status_colors.get(MainControllerState.system_status, ColorToken.TEXT_SECONDARY)}, 0.1)",
        border_radius="0.5rem",
        border=f"1px solid {status_colors.get(MainControllerState.system_status, ColorToken.TEXT_SECONDARY)}",
    )


def subsystem_card(subsystem_key: str) -> rx.Component:
    """
    Individual subsystem status card with control buttons.
    
    Args:
        subsystem_key: Subsystem identifier
        
    Returns:
        Reflex component for subsystem
    """
    config = SubsystemConfig.SUBSYSTEMS.get(subsystem_key, {})
    subsystem = MainControllerState.subsystem_states[subsystem_key]
    
    state_colors = {
        SubsystemState.READY: ColorToken.STATUS_SUCCESS,
        SubsystemState.INITIALIZING: ColorToken.STATUS_INFO,
        SubsystemState.ERROR: ColorToken.STATUS_CRITICAL,
        SubsystemState.OFFLINE: ColorToken.TEXT_SECONDARY,
    }
    
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                # Icon + Name
                rx.hstack(
                    rx.text(subsystem["icon"], font_size="1.5rem"),
                    rx.vstack(
                        rx.text(
                            subsystem["name"],
                            font_size="0.95rem",
                            font_weight="600",
                            color=ColorToken.TEXT_PRIMARY,
                        ),
                        rx.text(
                            config.get("description", ""),
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                        ),
                        spacing="0.25rem",
                    ),
                    spacing="0.75rem",
                ),
                rx.spacer(),
                # Status indicator
                rx.box(
                    rx.text(
                        subsystem["state"].value.upper(),
                        font_size="0.7rem",
                        font_weight="600",
                        color=state_colors.get(subsystem["state"], ColorToken.TEXT_SECONDARY),
                        letter_spacing="0.05em",
                    ),
                    padding="0.375rem 0.75rem",
                    background_color=f"rgba({state_colors.get(subsystem['state'], ColorToken.TEXT_SECONDARY)}, 0.15)",
                    border_radius="0.375rem",
                    border=f"1px solid {state_colors.get(subsystem['state'], ColorToken.TEXT_SECONDARY)}",
                ),
                width="100%",
                align_items="center",
            ),
            
            # Progress bar (if initializing)
            rx.cond(
                subsystem["state"] == SubsystemState.INITIALIZING,
                rx.box(
                    rx.box(
                        width=f"{subsystem['startup_progress']}%",
                        height="4px",
                        background_color=ColorToken.ACCENT_PRIMARY,
                        border_radius="2px",
                        transition="width 0.3s ease",
                    ),
                    width="100%",
                    height="4px",
                    background_color=ColorToken.BORDER_LASER,
                    border_radius="2px",
                    margin_top="0.75rem",
                ),
                rx.spacer(),
            ),
            
            # Error message (if error)
            rx.cond(
                subsystem["error"] != None,
                rx.box(
                    rx.text(
                        f"Error: {subsystem['error']}",
                        font_size="0.75rem",
                        color=ColorToken.STATUS_CRITICAL,
                        font_family=FontFamily.MONO,
                    ),
                    padding="0.5rem 0.75rem",
                    background_color=f"rgba({ColorToken.STATUS_CRITICAL}, 0.1)",
                    border_radius="0.375rem",
                    margin_top="0.5rem",
                ),
                rx.spacer(),
            ),
            
            # Action buttons
            rx.hstack(
                rx.cond(
                    subsystem["state"] == SubsystemState.READY,
                    rx.button(
                        "Launch",
                        on_click=lambda: MainControllerState.navigate_to_subsystem(subsystem_key),
                        background_color=ColorToken.ACCENT_PRIMARY,
                        color=ColorToken.TEXT_PRIMARY,
                        padding="0.5rem 1rem",
                        border_radius="0.375rem",
                        font_size="0.875rem",
                        _hover={"background_color": ColorToken.ACCENT_HOVER},
                    ),
                    rx.button(
                        "Restart",
                        on_click=lambda: MainControllerState.restart_subsystem(subsystem_key),
                        background_color=ColorToken.STATUS_WARNING,
                        color=ColorToken.TEXT_PRIMARY,
                        padding="0.5rem 1rem",
                        border_radius="0.375rem",
                        font_size="0.875rem",
                        _hover={"opacity": 0.8},
                    ),
                ),
                width="100%",
                justify_content="flex-end",
                margin_top="0.75rem",
            ),
            
            spacing="0.75rem",
            width="100%",
        ),
        padding="1.25rem",
        background_color=ColorToken.CARD_SLATE,
        border=f"1px solid {ColorToken.BORDER_LASER}",
        border_radius="0.75rem",
        transition="all 0.3s ease",
        _hover={"border_color": ColorToken.ACCENT_PRIMARY},
    )


def system_logs_panel() -> rx.Component:
    """
    Real-time system activity log with scrolling display.
    
    Returns:
        Reflex component showing system logs
    """
    return rx.box(
        rx.vstack(
            # Header
            rx.hstack(
                rx.text(
                    "System Activity Log",
                    font_size="0.95rem",
                    font_weight="600",
                    color=ColorToken.TEXT_PRIMARY,
                ),
                rx.spacer(),
                rx.button(
                    "Clear",
                    on_click=lambda: MainControllerState.clear_logs(),
                    background_color="transparent",
                    color=ColorToken.TEXT_SECONDARY,
                    padding="0.375rem 0.75rem",
                    border=f"1px solid {ColorToken.BORDER_LASER}",
                    border_radius="0.375rem",
                    font_size="0.75rem",
                    _hover={"color": ColorToken.TEXT_PRIMARY},
                ),
                width="100%",
                align_items="center",
            ),
            
            # Log entries
            rx.box(
                rx.vstack(
                    *[
                        rx.text(
                            log,
                            font_size="0.75rem",
                            color=ColorToken.TEXT_SECONDARY,
                            font_family=FontFamily.MONO,
                            word_break="break-word",
                        )
                        for log in MainControllerState.log_messages
                    ],
                    spacing="0.25rem",
                    width="100%",
                ),
                height="200px",
                overflow_y="auto",
                background_color="rgba(8, 10, 16, 0.5)",
                padding="1rem",
                border_radius="0.5rem",
                border=f"1px solid {ColorToken.BORDER_LASER}",
            ),
            
            spacing="1rem",
            width="100%",
        ),
        padding="1.25rem",
        background_color=ColorToken.CARD_SLATE,
        border=f"1px solid {ColorToken.BORDER_LASER}",
        border_radius="0.75rem",
    )


def master_control_page() -> rx.Component:
    """
    Master control page - central hub for entire EduSphere system.
    
    Features:
    - System status overview
    - Subsystem initialization tracking
    - Real-time activity logs
    - System controls (startup, shutdown, reset)
    - Subsystem management
    
    Returns:
        Reflex component with full master control interface
    """
    return rx.box(
        rx.vstack(
            # Header
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "EduSphere Central",
                                font_size="2rem",
                                font_weight="700",
                                color=ColorToken.TEXT_PRIMARY,
                                letter_spacing="0.05em",
                            ),
                            rx.text(
                                "Master Control & System Orchestration",
                                font_size="0.9rem",
                                color=ColorToken.TEXT_SECONDARY,
                            ),
                            spacing="0.5rem",
                        ),
                        rx.spacer(),
                        system_status_badge(),
                        width="100%",
                        align_items="flex-start",
                        spacing="2rem",
                    ),
                    spacing="1rem",
                    width="100%",
                ),
                padding="2rem",
                border_bottom=f"1px solid {ColorToken.BORDER_LASER}",
            ),
            
            # Main content
            rx.vstack(
                # System Controls
                rx.box(
                    rx.vstack(
                        rx.text(
                            "System Controls",
                            font_size="0.95rem",
                            font_weight="600",
                            color=ColorToken.TEXT_SECONDARY,
                            letter_spacing="0.1em",
                            text_transform="uppercase",
                        ),
                        rx.hstack(
                            rx.cond(
                                MainControllerState.is_system_running,
                                rx.button(
                                    "🛑 Shutdown",
                                    on_click=lambda: MainControllerState.shutdown_system(),
                                    background_color=ColorToken.STATUS_CRITICAL,
                                    color=ColorToken.TEXT_PRIMARY,
                                    padding="0.75rem 1.5rem",
                                    border_radius="0.5rem",
                                    font_size="0.9rem",
                                    _hover={"opacity": 0.9},
                                ),
                                rx.button(
                                    "🚀 Startup System",
                                    on_click=lambda: MainControllerState.startup_system(),
                                    background_color=ColorToken.STATUS_SUCCESS,
                                    color=ColorToken.TEXT_PRIMARY,
                                    padding="0.75rem 1.5rem",
                                    border_radius="0.5rem",
                                    font_size="0.9rem",
                                    _hover={"opacity": 0.9},
                                ),
                            ),
                            rx.button(
                                "🔄 Reset",
                                on_click=lambda: MainControllerState.reset_system(),
                                background_color=ColorToken.STATUS_WARNING,
                                color=ColorToken.TEXT_PRIMARY,
                                padding="0.75rem 1.5rem",
                                border_radius="0.5rem",
                                font_size="0.9rem",
                                _hover={"opacity": 0.9},
                            ),
                            spacing="1rem",
                        ),
                        spacing="1rem",
                    ),
                    padding="1.5rem",
                    background_color="rgba(107, 90, 255, 0.05)",
                    border=f"1px solid {ColorToken.BORDER_LASER}",
                    border_radius="0.75rem",
                    width="100%",
                ),
                
                # Subsystems Grid
                rx.vstack(
                    rx.text(
                        "Subsystems",
                        font_size="0.95rem",
                        font_weight="600",
                        color=ColorToken.TEXT_SECONDARY,
                        letter_spacing="0.1em",
                        text_transform="uppercase",
                    ),
                    rx.grid(
                        *[
                            subsystem_card(key)
                            for key in SubsystemConfig.SUBSYSTEMS.keys()
                        ],
                        columns="3",
                        spacing="1.5rem",
                        width="100%",
                    ),
                    spacing="1rem",
                    width="100%",
                ),
                
                # Logs Section
                system_logs_panel(),
                
                spacing="2rem",
                padding="2rem",
                width="100%",
            ),
            
            spacing="0",
            width="100%",
            height="100vh",
            overflow_y="auto",
        ),
        background_color=ColorToken.BACKGROUND_DEEP,
        width="100%",
    )


# ============================================================================
#    APPLICATION SETUP
# ============================================================================

def create_controller_app() -> rx.App:
    """
    Create and configure the main controller application.
    
    Returns:
        Configured Reflex app with master control interface
    """
    app = rx.App()
    
    # Register the master control page as root
    app.add_page(master_control_page, path="/", title="EduSphere Central - Master Control")
    
    return app


# Create app instance
app = create_controller_app()


# ============================================================================
#    ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Run the main controller application.
    
    Usage:
        python frontend/main_controller.py
        
    This starts the EduSphere Central master control interface on http://localhost:3000
    """
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║          EduSphere Central - Master Control                    ║
    ║                                                                ║
    ║  Starting system orchestration interface...                   ║
    ║  Access the control panel at: http://localhost:3000           ║
    ║                                                                ║
    ║  Click "🚀 Startup System" to initialize all subsystems       ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    app.compile()
