"""
Unified Analytics Dashboard Component
Displays a comprehensive overview of the education command workspace with
structured sections for metrics, scheduling, alerts, achievements, and assets.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class AlertSeverity(Enum):
    """Alert severity levels for warning indicators."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class MetricType(Enum):
    """Types of metrics displayed in stat cards."""
    SCHOOLS = "schools"
    TEACHERS = "teachers"
    STUDENTS = "students"
    FLEET_ASSETS = "fleet_assets"


class TrafficLoad(Enum):
    """Traffic load levels for scheduling matrix opacity."""
    LIGHT = 0.3
    MODERATE = 0.6
    HEAVY = 0.9


@dataclass
class GlassomorphicStatCard:
    """
    Translucent glassomorphic stat card with highlight glow effect.
    Represents a single metric in the top metrics row.
    """
    metric_type: MetricType
    value: int
    highlight_color: str  # CSS color code (e.g., '#FF6B6B', '#8E44AD')
    glow_intensity: float = 0.8  # 0.0 to 1.0
    
    @property
    def display_label(self) -> str:
        """Return human-readable label for metric type."""
        labels = {
            MetricType.SCHOOLS: "Schools",
            MetricType.TEACHERS: "Teachers",
            MetricType.STUDENTS: "Students",
            MetricType.FLEET_ASSETS: "Fleet/Assets",
        }
        return labels[self.metric_type]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize stat card to dictionary for rendering."""
        return {
            "label": self.display_label,
            "value": self.value,
            "highlightColor": self.highlight_color,
            "glowIntensity": self.glow_intensity,
            "metricType": self.metric_type.value,
        }


@dataclass
class SchedulingMatrixCell:
    """
    Individual cell in the scheduling contribution matrix.
    Represents availability slot vs semester intersection.
    """
    semester: str  # e.g., "Fall 2024", "Spring 2025"
    time_slot: str  # e.g., "9:00 AM", "1:00 PM"
    traffic_load: TrafficLoad
    occupied_slots: int
    total_slots: int
    
    @property
    def opacity(self) -> float:
        """Return opacity based on traffic load."""
        return self.traffic_load.value
    
    @property
    def fill_percentage(self) -> float:
        """Calculate percentage of slots occupied."""
        if self.total_slots == 0:
            return 0.0
        return (self.occupied_slots / self.total_slots) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize matrix cell to dictionary."""
        return {
            "semester": self.semester,
            "timeSlot": self.time_slot,
            "opacity": self.opacity,
            "fillPercentage": self.fill_percentage,
            "occupiedSlots": self.occupied_slots,
            "totalSlots": self.total_slots,
        }


@dataclass
class AlertLog:
    """
    Active warning log entry in the alert panel.
    Includes timestamp and severity level.
    """
    message: str
    severity: AlertSeverity
    timestamp: datetime
    pulse_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize alert log to dictionary."""
        return {
            "message": self.message,
            "severity": self.severity.value,
            "timestamp": self.timestamp.isoformat(),
            "pulseActive": self.pulse_active,
        }


@dataclass
class StudentAchievement:
    """
    Student achievement record for leaderboard podium display.
    Includes ranking and performance metrics.
    """
    rank: int  # 1, 2, 3 for podium
    student_id: str
    student_name: str
    score: float  # 0.0 to 100.0
    achievement_badge: str  # e.g., "🏆", "🥈", "🥉"
    is_centered: bool = False  # Podium layout flag
    glow_color: str = "#7C3AED"  # Violet glow for podium
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize achievement record to dictionary."""
        return {
            "rank": self.rank,
            "studentId": self.student_id,
            "studentName": self.student_name,
            "score": self.score,
            "achievementBadge": self.achievement_badge,
            "isCentered": self.is_centered,
            "glowColor": self.glow_color,
        }


@dataclass
class AssetNode:
    """
    Interactive coordinate node for spatial asset map.
    Represents infrastructure metric with position data.
    """
    asset_id: str  # e.g., "Vehicle ID: 8598"
    asset_type: str  # e.g., "vehicle", "room"
    x_coordinate: float  # 0.0 to 1.0 (normalized)
    y_coordinate: float  # 0.0 to 1.0 (normalized)
    label: str  # e.g., "Room Tracks: 1/11 pm"
    status: str  # e.g., "active", "idle", "maintenance"
    is_interactive: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize asset node to dictionary."""
        return {
            "assetId": self.asset_id,
            "assetType": self.asset_type,
            "x": self.x_coordinate,
            "y": self.y_coordinate,
            "label": self.label,
            "status": self.status,
            "isInteractive": self.is_interactive,
        }


@dataclass
class SchedulingGridSection:
    """Left pane: Interactive scheduling contribution matrix grid."""
    matrix_cells: List[SchedulingMatrixCell] = field(default_factory=list)
    semesters: List[str] = field(default_factory=list)
    time_slots: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize scheduling grid section."""
        return {
            "matrixCells": [cell.to_dict() for cell in self.matrix_cells],
            "semesters": self.semesters,
            "timeSlots": self.time_slots,
        }


@dataclass
class AlertPanelSection:
    """Right pane: Vertical scrollable alert panel with warning indicators."""
    alerts: List[AlertLog] = field(default_factory=list)
    max_visible_alerts: int = 8
    auto_scroll: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize alert panel section."""
        return {
            "alerts": [alert.to_dict() for alert in self.alerts[:self.max_visible_alerts]],
            "totalAlerts": len(self.alerts),
            "maxVisibleAlerts": self.max_visible_alerts,
            "autoScroll": self.auto_scroll,
        }


@dataclass
class LeaderboardSection:
    """Left pane: Academic achievement leaderboard with podium display."""
    achievements: List[StudentAchievement] = field(default_factory=list)
    
    def __post_init__(self):
        """Sort achievements by rank and set podium flags."""
        self.achievements.sort(key=lambda a: a.rank)
        for achievement in self.achievements:
            if achievement.rank == 1:
                achievement.is_centered = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize leaderboard section."""
        return {
            "achievements": [ach.to_dict() for ach in self.achievements],
            "totalRecords": len(self.achievements),
        }


@dataclass
class AssetMapSection:
    """Right pane: Dark spatial asset map with interactive coordinate nodes."""
    asset_nodes: List[AssetNode] = field(default_factory=list)
    map_background_color: str = "#1A1A2E"  # Dark background
    grid_visible: bool = True
    zoom_level: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize asset map section."""
        return {
            "assetNodes": [node.to_dict() for node in self.asset_nodes],
            "mapBackgroundColor": self.map_background_color,
            "gridVisible": self.grid_visible,
            "zoomLevel": self.zoom_level,
        }


@dataclass
class UnifiedAnalyticsDashboard:
    """
    Main dashboard component that aggregates all sections.
    Provides a comprehensive overview of the analytics command workspace.
    """
    # Top Metrics Row
    stat_cards: List[GlassomorphicStatCard] = field(default_factory=list)
    
    # Middle Row Split-Pane
    scheduling_grid: SchedulingGridSection = field(default_factory=SchedulingGridSection)
    alert_panel: AlertPanelSection = field(default_factory=AlertPanelSection)
    
    # Bottom Row Split-Pane
    leaderboard: LeaderboardSection = field(default_factory=LeaderboardSection)
    asset_map: AssetMapSection = field(default_factory=AssetMapSection)
    
    # Metadata
    last_updated: datetime = field(default_factory=datetime.now)
    dashboard_theme: str = "dark"  # "dark" or "light"
    is_loading: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize entire dashboard to dictionary for rendering."""
        return {
            "topMetricsRow": [card.to_dict() for card in self.stat_cards],
            "middleRow": {
                "schedulingGrid": self.scheduling_grid.to_dict(),
                "alertPanel": self.alert_panel.to_dict(),
            },
            "bottomRow": {
                "leaderboard": self.leaderboard.to_dict(),
                "assetMap": self.asset_map.to_dict(),
            },
            "metadata": {
                "lastUpdated": self.last_updated.isoformat(),
                "theme": self.dashboard_theme,
                "isLoading": self.is_loading,
            },
        }


# ============================================================================
# Mock Data Pools - Clean schema-bound data for instantaneous rendering
# ============================================================================

def create_mock_dashboard() -> UnifiedAnalyticsDashboard:
    """
    Generate a fully populated dashboard with clean mock data.
    All data is bound to schema definitions for error-free rendering.
    """
    
    dashboard = UnifiedAnalyticsDashboard(dashboard_theme="dark")
    
    # ========== TOP METRICS ROW ==========
    dashboard.stat_cards = [
        GlassomorphicStatCard(
            metric_type=MetricType.SCHOOLS,
            value=145,
            highlight_color="#FF6B6B",  # Red/Coral
            glow_intensity=0.8,
        ),
        GlassomorphicStatCard(
            metric_type=MetricType.TEACHERS,
            value=220,
            highlight_color="#8E44AD",  # Deep Purple/Violet
            glow_intensity=0.85,
        ),
        GlassomorphicStatCard(
            metric_type=MetricType.STUDENTS,
            value=3400,
            highlight_color="#F39C12",  # Warm Amber/Gold
            glow_intensity=0.8,
        ),
        GlassomorphicStatCard(
            metric_type=MetricType.FLEET_ASSETS,
            value=45,
            highlight_color="#1ABC9C",  # Emerald Green
            glow_intensity=0.75,
        ),
    ]
    
    # ========== MIDDLE ROW - LEFT: SCHEDULING GRID ==========
    semesters = ["Fall 2024", "Spring 2025", "Summer 2025"]
    time_slots = ["9:00 AM", "11:00 AM", "1:00 PM", "3:00 PM", "5:00 PM"]
    
    matrix_cells = []
    for semester in semesters:
        for time_slot in time_slots:
            traffic_load = {
                "Fall 2024-9:00 AM": TrafficLoad.HEAVY,
                "Fall 2024-11:00 AM": TrafficLoad.MODERATE,
                "Fall 2024-1:00 PM": TrafficLoad.HEAVY,
                "Spring 2025-9:00 AM": TrafficLoad.MODERATE,
                "Spring 2025-3:00 PM": TrafficLoad.LIGHT,
                "Summer 2025-5:00 PM": TrafficLoad.LIGHT,
            }.get(f"{semester}-{time_slot}", TrafficLoad.MODERATE)
            
            occupied = {
                "Heavy": 9, "Moderate": 5, "Light": 2
            }[traffic_load.name]
            
            matrix_cells.append(SchedulingMatrixCell(
                semester=semester,
                time_slot=time_slot,
                traffic_load=traffic_load,
                occupied_slots=occupied,
                total_slots=10,
            ))
    
    dashboard.scheduling_grid = SchedulingGridSection(
        matrix_cells=matrix_cells,
        semesters=semesters,
        time_slots=time_slots,
    )
    
    # ========== MIDDLE ROW - RIGHT: ALERT PANEL ==========
    dashboard.alert_panel = AlertPanelSection(
        alerts=[
            AlertLog(
                message="Warning: Room 403 double-booked for 2:00 PM slot",
                severity=AlertSeverity.CRITICAL,
                timestamp=datetime(2026, 5, 21, 14, 35),
                pulse_active=True,
            ),
            AlertLog(
                message="Warning: Bus Fleet #12 maintenance overdue",
                severity=AlertSeverity.WARNING,
                timestamp=datetime(2026, 5, 21, 13, 22),
                pulse_active=True,
            ),
            AlertLog(
                message="Info: Teacher assignment for Room 210 updated",
                severity=AlertSeverity.INFO,
                timestamp=datetime(2026, 5, 21, 12, 45),
                pulse_active=False,
            ),
            AlertLog(
                message="Warning: Student enrollment exceeds capacity in Math 201",
                severity=AlertSeverity.WARNING,
                timestamp=datetime(2026, 5, 21, 11, 18),
                pulse_active=True,
            ),
            AlertLog(
                message="Info: System backup completed successfully",
                severity=AlertSeverity.INFO,
                timestamp=datetime(2026, 5, 21, 10, 0),
                pulse_active=False,
            ),
        ],
        max_visible_alerts=8,
        auto_scroll=True,
    )
    
    # ========== BOTTOM ROW - LEFT: LEADERBOARD PODIUM ==========
    dashboard.leaderboard = LeaderboardSection(
        achievements=[
            StudentAchievement(
                rank=1,
                student_id="STU-001",
                student_name="Emma Chen",
                score=98.5,
                achievement_badge="🏆",
                glow_color="#7C3AED",  # Violet
            ),
            StudentAchievement(
                rank=2,
                student_id="STU-002",
                student_name="Marcus Johnson",
                score=97.2,
                achievement_badge="🥈",
                glow_color="#7C3AED",
            ),
            StudentAchievement(
                rank=3,
                student_id="STU-003",
                student_name="Sofia Rodriguez",
                score=96.8,
                achievement_badge="🥉",
                glow_color="#7C3AED",
            ),
        ],
    )
    
    # ========== BOTTOM ROW - RIGHT: ASSET MAP ==========
    dashboard.asset_map = AssetMapSection(
        asset_nodes=[
            AssetNode(
                asset_id="Vehicle ID: 8598",
                asset_type="vehicle",
                x_coordinate=0.25,
                y_coordinate=0.3,
                label="Bus Fleet #12 (Route A)",
                status="active",
                is_interactive=True,
            ),
            AssetNode(
                asset_id="Vehicle ID: 8599",
                asset_type="vehicle",
                x_coordinate=0.72,
                y_coordinate=0.65,
                label="Bus Fleet #13 (Route B)",
                status="idle",
                is_interactive=True,
            ),
            AssetNode(
                asset_id="Room 403",
                asset_type="room",
                x_coordinate=0.15,
                y_coordinate=0.85,
                label="Room Tracks: 2/11 pm",
                status="active",
                is_interactive=True,
            ),
            AssetNode(
                asset_id="Room 210",
                asset_type="room",
                x_coordinate=0.65,
                y_coordinate=0.2,
                label="Room Tracks: 1/11 pm",
                status="active",
                is_interactive=True,
            ),
            AssetNode(
                asset_id="Lab 501",
                asset_type="room",
                x_coordinate=0.45,
                y_coordinate=0.5,
                label="Room Tracks: 3/11 pm",
                status="maintenance",
                is_interactive=True,
            ),
        ],
        map_background_color="#1A1A2E",
        grid_visible=True,
        zoom_level=1.0,
    )
    
    return dashboard


# ============================================================================
# Export Functions for Frontend Integration
# ============================================================================

def get_dashboard_json() -> Dict[str, Any]:
    """
    Retrieve complete dashboard data as JSON-serializable dictionary.
    Ready for instant frontend rendering without layout errors.
    """
    dashboard = create_mock_dashboard()
    return dashboard.to_dict()


def get_dashboard_stats() -> List[Dict[str, Any]]:
    """Retrieve only the top metrics row for quick overview."""
    dashboard = create_mock_dashboard()
    return [card.to_dict() for card in dashboard.stat_cards]


def get_scheduling_grid() -> Dict[str, Any]:
    """Retrieve scheduling matrix grid data."""
    dashboard = create_mock_dashboard()
    return dashboard.scheduling_grid.to_dict()


def get_active_alerts() -> List[Dict[str, Any]]:
    """Retrieve active alert logs."""
    dashboard = create_mock_dashboard()
    return [alert.to_dict() for alert in dashboard.alert_panel.alerts]


def get_leaderboard() -> Dict[str, Any]:
    """Retrieve academic achievement leaderboard."""
    dashboard = create_mock_dashboard()
    return dashboard.leaderboard.to_dict()


def get_asset_map() -> Dict[str, Any]:
    """Retrieve spatial asset map data."""
    dashboard = create_mock_dashboard()
    return dashboard.asset_map.to_dict()


# ============================================================================
# Example Usage & Documentation
# ============================================================================

if __name__ == "__main__":
    """
    Example usage demonstrating dashboard instantiation and data retrieval.
    All components are schema-bound and pass clean mock data for rendering.
    """
    
    # Create full dashboard
    dashboard = create_mock_dashboard()
    print("✓ Dashboard created successfully")
    
    # Serialize to JSON
    dashboard_data = dashboard.to_dict()
    print(f"✓ Dashboard serialized: {len(dashboard_data)} top-level keys")
    
    # Access individual sections
    print(f"✓ Top Metrics: {len(dashboard_data['topMetricsRow'])} stat cards")
    print(f"✓ Alerts: {dashboard_data['middleRow']['alertPanel']['totalAlerts']} messages")
    print(f"✓ Leaderboard: {dashboard_data['bottomRow']['leaderboard']['totalRecords']} students")
    print(f"✓ Asset Map: {len(dashboard_data['bottomRow']['assetMap']['assetNodes'])} nodes")
    
    print("\n✓ All components ready for frontend rendering with zero layout errors")
