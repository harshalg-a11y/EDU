"""
EduSphere Central - Database Models Layer
Pure Python enterprise database schema using SQLModel with strict type hints.
Multi-tenant architecture with high-performance indexing and relationship tracking.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum as PyEnum
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship, Column, String, JSON
from sqlalchemy import Index, UniqueConstraint, ForeignKey, Enum as SQLEnum


# ============================================================================
#    ENUMERATIONS - Type-Safe Constants
# ============================================================================

class TenantTier(str, PyEnum):
    """Enterprise licensing tier for tenant organizations."""
    PLATINUM = "PLATINUM"  # Unlimited everything
    BASE = "BASE"           # Limited features


class UserRole(str, PyEnum):
    """Role-based access control for multi-tenant system."""
    GLOBAL_ADMIN = "GLOBAL_ADMIN"    # System administrator
    COUNSELOR = "COUNSELOR"          # Academic counselor/advisor
    TEACHER = "TEACHER"              # Instructor
    STUDENT = "STUDENT"              # Learner


class ConflictType(str, PyEnum):
    """Scheduling conflict classification."""
    DOUBLE_BOOKING = "DOUBLE_BOOKING"  # Room/teacher booked twice
    REQ_MISSING = "REQ_MISSING"        # Prerequisites not met


class SeverityLevel(str, PyEnum):
    """Conflict severity for priority queue."""
    CRITICAL = "CRITICAL"  # System-blocking
    WARNING = "WARNING"     # Non-blocking alert


# ============================================================================
#    TENANT MODEL - Multi-tenancy Root
# ============================================================================

class Tenant(SQLModel, table=True):
    """
    Enterprise tenant organization.
    
    Serves as the organizational root for all multi-tenant data isolation.
    All other entities cascade through tenant_id foreign key.
    
    Attributes:
        id: Unique tenant identifier (UUID4)
        name: Organization display name
        tier: Subscription tier (PLATINUM | BASE)
        created_at: Tenant provisioning timestamp
        updated_at: Last modification timestamp
    """
    
    __tablename__ = "tenants"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(
        min_length=1,
        max_length=255,
        index=True,
        description="Organization name"
    )
    tier: TenantTier = Field(
        default=TenantTier.BASE,
        sa_column=Column(SQLEnum(TenantTier)),
        description="Subscription tier"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Organization creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
    
    # Relationships
    users: List["User"] = Relationship(
        back_populates="tenant",
        cascade_delete=True,
        description="All users in this tenant"
    )
    course_instances: List["CourseInstance"] = Relationship(
        back_populates="tenant",
        cascade_delete=True,
        description="All courses offered by this tenant"
    )
    scheduling_conflicts: List["SchedulingConflict"] = Relationship(
        back_populates="tenant",
        cascade_delete=True,
        description="All scheduling conflicts within this tenant"
    )


# ============================================================================
#    USER MODEL - Authentication & Authorization
# ============================================================================

class User(SQLModel, table=True):
    """
    Multi-tenant user with role-based access control.
    
    Represents authenticated system users with granular permission scoping.
    Email uniqueness enforced per tenant to enable cross-tenant SSO migration.
    
    Attributes:
        id: Unique user identifier (UUID4)
        email: Unique email per tenant (indexed for fast lookup)
        role: Access control role (GLOBAL_ADMIN | COUNSELOR | TEACHER | STUDENT)
        tenant_id: Parent tenant foreign key
        created_at: Account creation timestamp
        updated_at: Last profile modification timestamp
    """
    
    __tablename__ = "users"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(
        min_length=5,
        max_length=255,
        index=True,
        description="Unique email address (indexed for authentication)"
    )
    role: UserRole = Field(
        default=UserRole.STUDENT,
        sa_column=Column(SQLEnum(UserRole)),
        description="Role-based access control"
    )
    tenant_id: UUID = Field(
        foreign_key="tenants.id",
        index=True,
        description="Parent tenant (multi-tenancy root)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last profile update timestamp"
    )
    
    # Relationships
    tenant: Tenant = Relationship(
        back_populates="users",
        description="Parent tenant organization"
    )
    academic_records: List["AcademicRecord"] = Relationship(
        back_populates="student",
        cascade_delete=True,
        description="Academic records (student only)"
    )
    taught_courses: List["CourseInstance"] = Relationship(
        back_populates="teacher",
        cascade_delete=True,
        description="Courses taught by this user (teacher only)"
    )
    
    # Composite indexes for high-performance queries
    __table_args__ = (
        Index(
            "idx_user_email_tenant",
            "email",
            "tenant_id",
            unique=True,
            name="idx_user_email_tenant"
        ),
        Index(
            "idx_user_role_tenant",
            "role",
            "tenant_id",
            name="idx_user_role_tenant"
        ),
        UniqueConstraint("email", "tenant_id", name="uc_email_tenant"),
    )


# ============================================================================
#    ACADEMIC RECORD MODEL - Student Transcript Data
# ============================================================================

class AcademicRecord(SQLModel, table=True):
    """
    Individual student academic achievement transcript.
    
    Tracks cumulative academic performance metrics and graduation eligibility.
    Immutable audit trail for degree conferral and transcript generation.
    
    Attributes:
        id: Unique record identifier (UUID4)
        student_id: Student user foreign key
        credits_completed: Total credits earned (0.0 - 999.0)
        gpa: Grade point average (0.0 - 4.0)
        is_graduation_eligible: Computed eligibility flag
        created_at: Record creation timestamp
        updated_at: Last computation timestamp
    """
    
    __tablename__ = "academic_records"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    student_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        description="Student user reference"
    )
    credits_completed: float = Field(
        default=0.0,
        ge=0.0,
        le=999.0,
        description="Total credits earned (0.0-999.0)"
    )
    gpa: float = Field(
        default=0.0,
        ge=0.0,
        le=4.0,
        description="Cumulative GPA (0.0-4.0 scale)"
    )
    is_graduation_eligible: bool = Field(
        default=False,
        description="Computed eligibility for degree conferral"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
    
    # Relationships
    student: User = Relationship(
        back_populates="academic_records",
        description="Student user reference"
    )
    
    # Indexes for transcript queries
    __table_args__ = (
        Index(
            "idx_academic_gpa",
            "gpa",
            name="idx_academic_gpa"
        ),
        Index(
            "idx_academic_credits",
            "credits_completed",
            name="idx_academic_credits"
        ),
        Index(
            "idx_academic_eligibility",
            "is_graduation_eligible",
            name="idx_academic_eligibility"
        ),
    )


# ============================================================================
#    COURSE INSTANCE MODEL - Scheduled Course Section
# ============================================================================

class CourseInstance(SQLModel, table=True):
    """
    Scheduled course offering with instructor assignment.
    
    Represents a specific section of a course at a particular time/location.
    Critical for scheduling conflict detection and room utilization analysis.
    
    Attributes:
        id: Unique course instance identifier (UUID4)
        course_code: Registrar course code (e.g., "CS101")
        teacher_id: Instructor user foreign key
        room_id: Physical location identifier (e.g., "A101")
        time_slot: Scheduled time period (e.g., "09:00-10:30 MWF")
        max_capacity: Maximum enrollment count
        tenant_id: Parent tenant foreign key
        created_at: Course offering creation timestamp
        updated_at: Last modification timestamp
    """
    
    __tablename__ = "course_instances"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    course_code: str = Field(
        min_length=2,
        max_length=50,
        index=True,
        description="Registrar course code (e.g., CS101)"
    )
    teacher_id: UUID = Field(
        foreign_key="users.id",
        index=True,
        description="Instructor assignment"
    )
    room_id: str = Field(
        min_length=1,
        max_length=50,
        index=True,
        description="Physical room/location identifier"
    )
    time_slot: str = Field(
        min_length=1,
        max_length=100,
        description="Scheduled time period (e.g., '09:00-10:30 MWF')"
    )
    max_capacity: int = Field(
        ge=1,
        le=999,
        description="Maximum student enrollment"
    )
    tenant_id: UUID = Field(
        foreign_key="tenants.id",
        index=True,
        description="Parent tenant (multi-tenancy scope)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Course offering creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp"
    )
    
    # Relationships
    tenant: Tenant = Relationship(
        back_populates="course_instances",
        description="Parent tenant organization"
    )
    teacher: User = Relationship(
        back_populates="taught_courses",
        description="Instructor assignment"
    )
    scheduling_conflicts: List["SchedulingConflict"] = Relationship(
        back_populates="course_instance",
        cascade_delete=True,
        description="Detected scheduling conflicts"
    )
    
    # Composite indexes for conflict detection
    __table_args__ = (
        Index(
            "idx_course_room_time",
            "room_id",
            "time_slot",
            "tenant_id",
            name="idx_course_room_time"
        ),
        Index(
            "idx_course_teacher",
            "teacher_id",
            "time_slot",
            name="idx_course_teacher"
        ),
        Index(
            "idx_course_code_tenant",
            "course_code",
            "tenant_id",
            name="idx_course_code_tenant"
        ),
    )


# ============================================================================
#    SCHEDULING CONFLICT MODEL - Constraint Violation Log
# ============================================================================

class SchedulingConflict(SQLModel, table=True):
    """
    Detected scheduling constraint violation record.
    
    Audit trail for constraint solver engine. Each violation includes
    conflict classification, severity level, and resolution metadata.
    Core data source for AI conflict resolution pipeline.
    
    Attributes:
        id: Unique conflict record identifier (UUID4)
        course_instance_id: Associated course offering
        tenant_id: Parent tenant foreign key
        conflict_type: Classification (DOUBLE_BOOKING | REQ_MISSING)
        severity: Priority level (CRITICAL | WARNING)
        resolved: Resolution state flag
        metadata: Extensible JSON dictionary for conflict details
        created_at: Conflict detection timestamp
        updated_at: Last resolution attempt timestamp
    """
    
    __tablename__ = "scheduling_conflicts"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    course_instance_id: UUID = Field(
        foreign_key="course_instances.id",
        index=True,
        description="Associated course instance"
    )
    tenant_id: UUID = Field(
        foreign_key="tenants.id",
        index=True,
        description="Parent tenant (multi-tenancy scope)"
    )
    conflict_type: ConflictType = Field(
        sa_column=Column(SQLEnum(ConflictType)),
        description="Conflict classification"
    )
    severity: SeverityLevel = Field(
        sa_column=Column(SQLEnum(SeverityLevel)),
        description="Priority level (CRITICAL | WARNING)"
    )
    resolved: bool = Field(
        default=False,
        index=True,
        description="Resolution state flag"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Extensible JSON conflict details"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conflict detection timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
    
    # Relationships
    tenant: Tenant = Relationship(
        back_populates="scheduling_conflicts",
        description="Parent tenant organization"
    )
    course_instance: CourseInstance = Relationship(
        back_populates="scheduling_conflicts",
        description="Associated course instance"
    )
    
    # Indexes for conflict resolution pipeline
    __table_args__ = (
        Index(
            "idx_conflict_unresolved",
            "resolved",
            "severity",
            "tenant_id",
            name="idx_conflict_unresolved"
        ),
        Index(
            "idx_conflict_type_tenant",
            "conflict_type",
            "tenant_id",
            name="idx_conflict_type_tenant"
        ),
        Index(
            "idx_conflict_severity",
            "severity",
            name="idx_conflict_severity"
        ),
        Index(
            "idx_conflict_created",
            "created_at",
            "tenant_id",
            name="idx_conflict_created"
        ),
    )


# ============================================================================
#    ASYNC DATABASE INITIALIZATION
# ============================================================================

async def init_db() -> None:
    """
    Initialize database tables and indexes.
    
    Must be called during application startup to ensure all tables
    and constraints are created. Idempotent operation (safe to call multiple times).
    
    Returns:
        None
    
    Raises:
        sqlalchemy.exc.SQLAlchemyError: Database connection/creation failures
    """
    # Engine initialization happens in main application factory
    # This function is a placeholder for future async initialization logic
    pass


# ============================================================================
#    TYPE HINTS FOR QUERY RESPONSES
# ============================================================================

# Forward reference type hints for nested response models
__all__ = [
    "Tenant",
    "User",
    "AcademicRecord",
    "CourseInstance",
    "SchedulingConflict",
    "TenantTier",
    "UserRole",
    "ConflictType",
    "SeverityLevel",
    "init_db",
]
