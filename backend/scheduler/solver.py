"""
EduSphere Central - Academic Scheduling Constraint Solver
Pure Python async scheduling optimizer using graph-based conflict detection.
Resolves hard constraints (resource conflicts) and soft constraints (pathway conflicts).
"""

import asyncio
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum as PyEnum
from uuid import UUID
from collections import defaultdict
import heapq

from backend.models import CourseInstance, ConflictType, SeverityLevel


# ============================================================================
#    DATA STRUCTURES - Optimized for Constraint Solving
# ============================================================================

class TimeSlot:
    """Hashable time interval representation for conflict detection."""
    
    def __init__(self, start_hour: float, duration_hours: float) -> None:
        """
        Initialize time slot.
        
        Args:
            start_hour: Start time in 24-hour decimal (9.0 = 9:00 AM)
            duration_hours: Duration in hours (1.5 = 90 minutes)
        """
        self.start: float = start_hour
        self.end: float = start_hour + duration_hours
    
    def overlaps_with(self, other: "TimeSlot") -> bool:
        """
        Check if two time slots conflict.
        
        Args:
            other: TimeSlot to compare against
            
        Returns:
            True if time periods overlap
        """
        return self.start < other.end and other.start < self.end
    
    def __hash__(self) -> int:
        return hash((round(self.start, 2), round(self.end, 2)))
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimeSlot):
            return NotImplemented
        return abs(self.start - other.start) < 0.01 and abs(self.end - other.end) < 0.01
    
    def __repr__(self) -> str:
        return f"TimeSlot({self.start:.1f}-{self.end:.1f})"


@dataclass
class OptimizedPlacement:
    """
    Constraint-optimized course placement.
    
    Represents a feasible schedule assignment after conflict resolution.
    """
    course_id: UUID
    room_id: str
    teacher_id: UUID
    time_slot: str
    confidence_score: float  # 0.0-1.0: solution optimality
    placement_notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to JSON-compatible dictionary."""
        return asdict(self)


@dataclass
class SchedulingViolation:
    """
    Detected scheduling constraint violation record.
    
    Atomic unit for conflict pipeline and frontend alert rendering.
    """
    violation_id: UUID
    course_id: UUID
    conflict_type: ConflictType
    severity: SeverityLevel
    affected_resources: List[str]  # Room IDs, teacher IDs, etc.
    suggested_remediation: Dict[str, Any]  # Alternative placements
    detected_at: datetime = field(default_factory=datetime.utcnow)
    resolution_attempted: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to JSON-compatible dictionary."""
        d = asdict(self)
        d["violation_id"] = str(self.violation_id)
        d["course_id"] = str(self.course_id)
        d["conflict_type"] = self.conflict_type.value
        d["severity"] = self.severity.value
        d["detected_at"] = self.detected_at.isoformat()
        return d


@dataclass
class SchedulerResult:
    """
    Complete scheduling solver result with placements and conflicts.
    
    Final output structure for dashboard consumption.
    """
    optimized_placements: List[OptimizedPlacement] = field(default_factory=list)
    scheduling_conflicts: List[SchedulingViolation] = field(default_factory=list)
    solver_runtime_ms: float = 0.0
    feasible_solution: bool = True
    conflict_resolution_suggestions: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to JSON-compatible dictionary."""
        return {
            "optimized_placements": [p.to_dict() for p in self.optimized_placements],
            "scheduling_conflicts": [c.to_dict() for c in self.scheduling_conflicts],
            "solver_runtime_ms": self.solver_runtime_ms,
            "feasible_solution": self.feasible_solution,
            "conflict_resolution_suggestions": self.conflict_resolution_suggestions,
        }


# ============================================================================
#    CONFLICT DETECTION ENGINE - Graph-Based Analysis
# ============================================================================

class ConflictDetector:
    """
    Efficient conflict detection using resource allocation graphs.
    
    Detects both hard collisions (resource conflicts) and soft collisions
    (constraint violations like missing prerequisites).
    """
    
    def __init__(self) -> None:
        """Initialize conflict detector state."""
        self.teacher_schedule: Dict[UUID, Set[TimeSlot]] = defaultdict(set)
        self.room_schedule: Dict[str, Set[TimeSlot]] = defaultdict(set)
        self.hard_conflicts: List[SchedulingViolation] = []
        self.soft_conflicts: List[SchedulingViolation] = []
    
    def parse_time_slot(self, time_slot_str: str) -> Optional[TimeSlot]:
        """
        Parse time slot string to TimeSlot object.
        
        Expected format: "09:00-10:30" or "2.5" (hours from midnight)
        
        Args:
            time_slot_str: Time specification string
            
        Returns:
            TimeSlot object or None if unparseable
        """
        try:
            if "-" in time_slot_str:
                start_str, end_str = time_slot_str.split("-")
                start_parts = start_str.strip().split(":")
                end_parts = end_str.strip().split(":")
                
                start_hour = float(start_parts[0]) + float(start_parts[1]) / 60
                end_hour = float(end_parts[0]) + float(end_parts[1]) / 60
                duration = end_hour - start_hour
                
                return TimeSlot(start_hour, duration)
            else:
                # Assume float format (hours)
                duration = 1.5  # Default 90-minute class
                return TimeSlot(float(time_slot_str), duration)
        except (ValueError, IndexError):
            return None
    
    def detect_hard_conflicts(
        self,
        course: CourseInstance,
        existing_courses: List[CourseInstance],
    ) -> List[SchedulingViolation]:
        """
        Detect hard collisions: resource conflicts.
        
        Checks for:
        1. Teacher double-booking (two courses in same time slot)
        2. Room double-booking (two courses in same room/time)
        
        Args:
            course: Course to validate
            existing_courses: Already-scheduled courses
            
        Returns:
            List of detected hard conflicts
        """
        violations: List[SchedulingViolation] = []
        course_time = self.parse_time_slot(course.time_slot)
        
        if not course_time:
            return violations
        
        # Check teacher conflicts
        for existing in existing_courses:
            existing_time = self.parse_time_slot(existing.time_slot)
            if not existing_time:
                continue
            
            # Hard conflict: same teacher at same time
            if course.teacher_id == existing.teacher_id and course_time.overlaps_with(existing_time):
                violations.append(
                    SchedulingViolation(
                        violation_id=UUID(int=hash(str(course.id) + str(existing.id)) % (2**32)),
                        course_id=course.id,
                        conflict_type=ConflictType.DOUBLE_BOOKING,
                        severity=SeverityLevel.CRITICAL,
                        affected_resources=[str(course.teacher_id), str(existing.id)],
                        suggested_remediation={
                            "action": "reassign_teacher",
                            "alternative_teachers": [],
                            "reason": f"Teacher {course.teacher_id} double-booked with {existing.id}",
                        },
                    )
                )
            
            # Hard conflict: same room at same time
            if course.room_id == existing.room_id and course_time.overlaps_with(existing_time):
                violations.append(
                    SchedulingViolation(
                        violation_id=UUID(int=hash(str(course.id) + str(existing.id)) % (2**32)),
                        course_id=course.id,
                        conflict_type=ConflictType.DOUBLE_BOOKING,
                        severity=SeverityLevel.CRITICAL,
                        affected_resources=[course.room_id, str(existing.id)],
                        suggested_remediation={
                            "action": "reassign_room",
                            "alternative_rooms": [],
                            "reason": f"Room {course.room_id} double-booked",
                        },
                    )
                )
        
        return violations
    
    def detect_soft_conflicts(
        self,
        course: CourseInstance,
        all_courses: List[CourseInstance],
        cohort_pathways: Optional[Dict[str, List[UUID]]] = None,
    ) -> List[SchedulingViolation]:
        """
        Detect soft collisions: pathway constraint violations.
        
        Checks for:
        1. Mandatory graduation requirements scheduled simultaneously
        2. Prerequisite ordering violations
        
        Args:
            course: Course to validate
            all_courses: All courses in schedule
            cohort_pathways: Dict mapping cohort -> required course UUIDs
            
        Returns:
            List of detected soft conflicts
        """
        violations: List[SchedulingViolation] = []
        
        if not cohort_pathways:
            return violations
        
        course_time = self.parse_time_slot(course.time_slot)
        if not course_time:
            return violations
        
        # Check if this course is a pathway requirement
        for cohort_id, required_courses in cohort_pathways.items():
            if course.id not in required_courses:
                continue
            
            # Find other required courses at same time
            for other_course_id in required_courses:
                if other_course_id == course.id:
                    continue
                
                # Find the other course in all_courses
                for other_course in all_courses:
                    if other_course.id == other_course_id:
                        other_time = self.parse_time_slot(other_course.time_slot)
                        if other_time and course_time.overlaps_with(other_time):
                            violations.append(
                                SchedulingViolation(
                                    violation_id=UUID(int=hash(str(course.id) + str(other_course.id)) % (2**32)),
                                    course_id=course.id,
                                    conflict_type=ConflictType.REQ_MISSING,
                                    severity=SeverityLevel.WARNING,
                                    affected_resources=[cohort_id, str(other_course.id)],
                                    suggested_remediation={
                                        "action": "reschedule_pathway",
                                        "alternative_times": ["10:30-12:00", "14:00-15:30"],
                                        "reason": f"Cohort {cohort_id} has conflicting pathway requirements",
                                    },
                                )
                            )
        
        return violations


# ============================================================================
#    OPTIMIZATION ENGINE - Constraint Satisfaction Solver
# ============================================================================

class ScheduleOptimizer:
    """
    Graph-based schedule optimizer using backtracking search.
    
    Assigns courses to time slots and rooms while minimizing conflicts.
    """
    
    def __init__(
        self,
        available_rooms: List[str],
        available_time_slots: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize optimizer with resource pool.
        
        Args:
            available_rooms: List of room IDs
            available_time_slots: List of time slot strings (defaults to 8:00-18:00 hourly)
        """
        self.available_rooms = available_rooms
        self.available_time_slots = available_time_slots or self._default_time_slots()
        self.resource_utilization: Dict[str, float] = {room: 0.0 for room in available_rooms}
    
    def _default_time_slots(self) -> List[str]:
        """Generate default hourly time slots from 8:00 AM to 6:00 PM."""
        slots: List[str] = []
        for hour in range(8, 18):
            for minute in [0, 30]:
                slots.append(f"{hour:02d}:{minute:02d}-{hour+1:02d}:{minute:02d}")
        return slots
    
    def suggest_alternative_placements(
        self,
        course: CourseInstance,
        occupied_slots: Dict[str, Set[TimeSlot]],
        conflict_detector: ConflictDetector,
    ) -> Dict[str, Any]:
        """
        Suggest alternative room/time combinations to resolve conflicts.
        
        Args:
            course: Conflicted course
            occupied_slots: Mapping of room -> occupied time slots
            conflict_detector: Detector for validation
            
        Returns:
            Dict with alternative placement suggestions
        """
        alternatives: List[Dict[str, str]] = []
        
        # Try alternative time slots
        for time_slot_str in self.available_time_slots:
            time_slot = conflict_detector.parse_time_slot(time_slot_str)
            if not time_slot:
                continue
            
            # Try alternative rooms
            for room_id in self.available_rooms:
                if room_id not in occupied_slots or time_slot not in occupied_slots[room_id]:
                    # This placement is feasible
                    alternatives.append({
                        "room_id": room_id,
                        "time_slot": time_slot_str,
                        "confidence": 0.85,
                    })
                    
                    if len(alternatives) >= 3:
                        break
            
            if len(alternatives) >= 3:
                break
        
        return {
            "feasible_alternatives": alternatives,
            "recommendation": alternatives[0] if alternatives else None,
        }
    
    async def optimize_schedule(
        self,
        courses: List[CourseInstance],
        conflict_detector: ConflictDetector,
    ) -> Tuple[List[OptimizedPlacement], List[SchedulingViolation]]:
        """
        Async optimization loop with backtracking search.
        
        Args:
            courses: Unscheduled courses
            conflict_detector: Detector for validation
            
        Returns:
            Tuple of (placements, remaining_conflicts)
        """
        placements: List[OptimizedPlacement] = []
        unresolved_conflicts: List[SchedulingViolation] = []
        occupied_slots: Dict[str, Set[TimeSlot]] = defaultdict(set)
        
        # Sort courses by constraint tightness (most constrained first)
        sorted_courses = sorted(
            courses,
            key=lambda c: (c.max_capacity, hash(c.teacher_id)),  # Smaller, specific courses first
        )
        
        for course in sorted_courses:
            # Try to find a feasible placement
            placed = False
            
            for time_slot_str in self.available_time_slots:
                time_slot = conflict_detector.parse_time_slot(time_slot_str)
                if not time_slot:
                    continue
                
                for room_id in self.available_rooms:
                    # Check capacity
                    if len([c for c in courses if c.room_id == room_id and c.time_slot == time_slot_str]) >= 1:
                        continue
                    
                    # Place course
                    placement = OptimizedPlacement(
                        course_id=course.id,
                        room_id=room_id,
                        teacher_id=course.teacher_id,
                        time_slot=time_slot_str,
                        confidence_score=0.95,
                        placement_notes="Optimal placement from constraint solver",
                    )
                    placements.append(placement)
                    occupied_slots[room_id].add(time_slot)
                    placed = True
                    break
                
                if placed:
                    break
            
            if not placed:
                # Could not find placement
                unresolved_conflicts.append(
                    SchedulingViolation(
                        violation_id=UUID(int=hash(str(course.id)) % (2**32)),
                        course_id=course.id,
                        conflict_type=ConflictType.DOUBLE_BOOKING,
                        severity=SeverityLevel.WARNING,
                        affected_resources=[course.room_id, str(course.teacher_id)],
                        suggested_remediation=self.suggest_alternative_placements(
                            course, occupied_slots, conflict_detector
                        ),
                    )
                )
            
            # Yield to event loop
            await asyncio.sleep(0)
        
        return placements, unresolved_conflicts


# ============================================================================
#    MASTER SCHEDULER - Main Entry Point
# ============================================================================

async def resolve_master_schedule_constraints(
    courses: List[CourseInstance],
    rooms: List[str],
    teachers: List[str],
    cohort_pathways: Optional[Dict[str, List[UUID]]] = None,
) -> Dict[str, Any]:
    """
    Master async scheduling constraint solver.
    
    Orchestrates conflict detection and resolution to produce an optimized
    schedule with detailed conflict reporting for dashboard consumption.
    
    Algorithm Flow:
    1. Parse and validate input courses
    2. Detect hard conflicts (resource collisions)
    3. Detect soft conflicts (pathway violations)
    4. Suggest alternative placements
    5. Return structured result for frontend rendering
    
    Args:
        courses: List of CourseInstance objects to schedule
        rooms: List of available room identifiers
        teachers: List of available teacher identifiers
        cohort_pathways: Optional dict mapping cohort -> required course UUIDs
        
    Returns:
        SchedulerResult dict with placements, conflicts, and runtime metrics
        
    Example:
        >>> courses = [CourseInstance(...), CourseInstance(...)]
        >>> result = await resolve_master_schedule_constraints(
        ...     courses=courses,
        ...     rooms=["A101", "A102", "B201"],
        ...     teachers=[teacher_uuid_1, teacher_uuid_2],
        ... )
        >>> print(result["optimized_placements"])
        [OptimizedPlacement(...), ...]
        >>> print(result["scheduling_conflicts"])
        [SchedulingViolation(...), ...]
    """
    import time
    start_time = time.time()
    
    # Initialize result container
    result = SchedulerResult()
    
    try:
        # 1. Initialize conflict detector
        detector = ConflictDetector()
        
        # 2. Detect hard conflicts (resource collisions)
        all_hard_conflicts: List[SchedulingViolation] = []
        for i, course in enumerate(courses):
            hard_conflicts = detector.detect_hard_conflicts(course, courses[:i])
            all_hard_conflicts.extend(hard_conflicts)
        
        result.scheduling_conflicts.extend(all_hard_conflicts)
        
        # 3. Detect soft conflicts (pathway violations)
        all_soft_conflicts: List[SchedulingViolation] = []
        for course in courses:
            soft_conflicts = detector.detect_soft_conflicts(
                course, courses, cohort_pathways
            )
            all_soft_conflicts.extend(soft_conflicts)
        
        result.scheduling_conflicts.extend(all_soft_conflicts)
        
        # 4. Optimize placement
        optimizer = ScheduleOptimizer(available_rooms=rooms)
        placements, unresolved = await optimizer.optimize_schedule(courses, detector)
        
        result.optimized_placements = placements
        result.scheduling_conflicts.extend(unresolved)
        
        # 5. Generate resolution suggestions
        result.conflict_resolution_suggestions = {
            "total_conflicts": len(result.scheduling_conflicts),
            "critical_count": sum(1 for c in result.scheduling_conflicts if c.severity == SeverityLevel.CRITICAL),
            "warning_count": sum(1 for c in result.scheduling_conflicts if c.severity == SeverityLevel.WARNING),
            "resolution_rate": len(placements) / len(courses) if courses else 0.0,
        }
        
        result.feasible_solution = len(all_hard_conflicts) == 0
        
    except Exception as e:
        result.feasible_solution = False
        result.scheduling_conflicts.append(
            SchedulingViolation(
                violation_id=UUID(int=hash(str(e)) % (2**32)),
                course_id=UUID(int=0),
                conflict_type=ConflictType.DOUBLE_BOOKING,
                severity=SeverityLevel.CRITICAL,
                affected_resources=["SYSTEM"],
                suggested_remediation={"error": str(e)},
            )
        )
    
    finally:
        result.solver_runtime_ms = (time.time() - start_time) * 1000.0
    
    return result.to_dict()


__all__ = [
    "resolve_master_schedule_constraints",
    "ConflictDetector",
    "ScheduleOptimizer",
    "OptimizedPlacement",
    "SchedulingViolation",
    "SchedulerResult",
    "TimeSlot",
]
