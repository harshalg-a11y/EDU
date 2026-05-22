"""
EduSphere Central - FastAPI Backend
====================================

High-performance async REST API for the EduSphere education management platform.
Handles dashboard metrics, scheduling conflicts, and data persistence.

To run:
    uvicorn app:app --reload --host 0.0.0.0 --port 8000

Production:
    uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uvicorn
from uuid import uuid4

# ============================================================================
#    FASTAPI APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="EduSphere Central API",
    description="Dashboard data layer for education management",
    version="1.0.0",
)

# Configure CORS middleware - Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# ============================================================================
#    DATA MODELS
# ============================================================================

class MetricObject(BaseModel):
    """Represents a single dashboard metric."""
    id: str = Field(..., description="Unique metric identifier")
    name: str = Field(..., description="Metric display name")
    value: int = Field(..., description="Current metric value")
    unit: str = Field(..., description="Unit label (e.g., 'Active', 'Total')")
    icon: str = Field(..., description="Emoji icon representation")


class SchedulingConflict(BaseModel):
    """Represents a scheduling conflict or warning."""
    id: str = Field(..., description="Unique conflict identifier")
    title: str = Field(..., description="Conflict title")
    description: str = Field(..., description="Detailed conflict description")
    severity: str = Field(..., description="Severity level: low, medium, high, critical")
    room_id: Optional[str] = Field(None, description="Associated room ID")
    timestamp: str = Field(..., description="When conflict was detected")


class ConflictResolutionRequest(BaseModel):
    """Request payload for resolving a conflict."""
    id: str = Field(..., description="ID of conflict to resolve")


# ============================================================================
#    IN-MEMORY DATA STORAGE
# ============================================================================

# Dashboard Metrics - 4 core objects
METRICS_DATA: List[MetricObject] = [
    MetricObject(
        id="metric_001",
        name="Schools",
        value=24,
        unit="Active",
        icon="🏫",
    ),
    MetricObject(
        id="metric_002",
        name="Teachers",
        value=287,
        unit="Total",
        icon="👨‍🏫",
    ),
    MetricObject(
        id="metric_003",
        name="Students",
        value=4156,
        unit="Enrolled",
        icon="👥",
    ),
    MetricObject(
        id="metric_004",
        name="Assets",
        value=1843,
        unit="Catalogued",
        icon="📦",
    ),
]

# Active Scheduling Conflicts/Warnings
CONFLICTS_DATA: List[SchedulingConflict] = [
    SchedulingConflict(
        id="conflict_001",
        title="Room 403 Double Booking",
        description="Room 403 scheduled for Physics (10:00-11:30) and Mathematics (10:45-12:15)",
        severity="critical",
        room_id="room_403",
        timestamp="2026-05-22T14:32:00Z",
    ),
    SchedulingConflict(
        id="conflict_002",
        title="Teacher Availability Conflict",
        description="Dr. Sarah Chen assigned to concurrent classes in different buildings",
        severity="high",
        room_id="room_405",
        timestamp="2026-05-22T13:45:00Z",
    ),
    SchedulingConflict(
        id="conflict_003",
        title="Resource Shortage - Lab Equipment",
        description="Biology Lab missing 3 microscopes for scheduled practicum session",
        severity="medium",
        room_id="room_512",
        timestamp="2026-05-22T13:15:00Z",
    ),
    SchedulingConflict(
        id="conflict_004",
        title="Overcapacity Warning - Auditorium",
        description="Assembly event (520 attendees) exceeds auditorium capacity (480 seats)",
        severity="high",
        room_id="room_001",
        timestamp="2026-05-22T12:50:00Z",
    ),
]


# ============================================================================
#    API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "online",
        "service": "EduSphere Central API",
        "version": "1.0.0",
        "endpoints": {
            "metrics": "/api/metrics",
            "conflicts": "/api/conflicts",
            "resolve_conflict": "/api/conflicts/resolve",
        },
    }


@app.get("/api/metrics", response_model=List[MetricObject])
async def get_metrics():
    """
    Retrieve all dashboard metrics.
    
    Returns:
        JSON array of 4 metric objects (Schools, Teachers, Students, Assets)
    
    Example:
        GET /api/metrics
        
        [
            {
                "id": "metric_001",
                "name": "Schools",
                "value": 24,
                "unit": "Active",
                "icon": "🏫"
            },
            ...
        ]
    """
    return METRICS_DATA


@app.get("/api/conflicts", response_model=List[SchedulingConflict])
async def get_conflicts():
    """
    Retrieve all active scheduling conflicts and warnings.
    
    Returns:
        JSON array of active conflict objects with severity levels
    
    Example:
        GET /api/conflicts
        
        [
            {
                "id": "conflict_001",
                "title": "Room 403 Double Booking",
                "description": "...",
                "severity": "critical",
                "room_id": "room_403",
                "timestamp": "2026-05-22T14:32:00Z"
            },
            ...
        ]
    """
    return CONFLICTS_DATA


@app.post("/api/conflicts/resolve", response_model=List[SchedulingConflict])
async def resolve_conflict(payload: ConflictResolutionRequest):
    """
    Resolve a conflict by ID - removes it from the active conflicts list.
    Updates server memory and returns the newly optimized conflicts array.
    
    Args:
        payload: JSON object with target conflict `id`
        
    Returns:
        Updated conflicts array after removal
        
    Raises:
        HTTPException 404: Conflict ID not found
    
    Example:
        POST /api/conflicts/resolve
        
        Request Body:
        {
            "id": "conflict_001"
        }
        
        Response:
        [
            {
                "id": "conflict_002",
                "title": "Teacher Availability Conflict",
                ...
            },
            ...
        ]
    """
    global CONFLICTS_DATA
    
    # Find conflict by ID
    conflict_exists = any(c.id == payload.id for c in CONFLICTS_DATA)
    
    if not conflict_exists:
        raise HTTPException(
            status_code=404,
            detail=f"Conflict with id '{payload.id}' not found",
        )
    
    # Filter out the resolved conflict
    CONFLICTS_DATA = [c for c in CONFLICTS_DATA if c.id != payload.id]
    
    return CONFLICTS_DATA


# ============================================================================
#    ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions gracefully."""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
    }


# ============================================================================
#    STARTUP & SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    print("✅ EduSphere Central API started")
    print(f"📊 Loaded {len(METRICS_DATA)} metrics")
    print(f"⚠️  Loaded {len(CONFLICTS_DATA)} active conflicts")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    print("🛑 EduSphere Central API shutting down")


# ============================================================================
#    ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Run with uvicorn on port 8000
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
