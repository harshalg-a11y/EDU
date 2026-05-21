/**
 * EduSphere Global Type Definitions
 * 
 * This file serves as the absolute single source of truth for all data layer types
 * across the entire application. All components MUST import their types from this file
 * to maintain consistency, type safety, and prevent 'any' implicit errors.
 * 
 * Structure:
 * - Core Domain Models
 * - Dashboard Components
 * - Scheduling & Conflicts
 * - Student & Academic Data
 * - Asset & Infrastructure
 * - Utility & Helper Types
 */

/* ============================================================================
   METRIC CARD TYPES
   ============================================================================ */

/**
 * MetricCardData - Dashboard performance metric display unit
 * Used by MetricCards component for KPI visualization
 */
export interface MetricCardData {
  /** Unique identifier for the metric */
  id: string;
  /** Display title (e.g., "Total Students", "System Uptime") */
  title: string;
  /** Primary value display (e.g., "2,847", "99.98%") */
  value: string;
  /** Secondary increment/change indicator (e.g., "+12", "-5%") */
  increment: string;
  /** Visual color variant for the card */
  variant: 'coral' | 'violet' | 'amber' | 'emerald';
}

/* ============================================================================
   SCHEDULING & CONFLICT TYPES
   ============================================================================ */

/**
 * SchedulingConflict - Represents calendar/room booking conflicts
 * Used by MiddlePanel AI conflict resolver
 */
export interface SchedulingConflict {
  /** Unique identifier for the conflict */
  id: string;
  /** Type of scheduling issue */
  type: 'DOUBLE_BOOKING' | 'REQ_MISSING';
  /** Severity level determining urgency */
  severity: 'CRITICAL' | 'WARNING';
  /** Human-readable conflict description */
  message: string;
  /** Affected room identifier */
  room: string;
  /** Relative time since conflict occurred (e.g., "2 hours ago") */
  timeAgo: string;
  /** Resolution status flag */
  resolved: boolean;
}

/**
 * SchedulingGridCell - Individual cell in the scheduling matrix
 * Represents a room/timeslot combination
 */
export interface SchedulingGridCell {
  /** Unique identifier combining room and time */
  id: string;
  /** Room identifier */
  roomId: string;
  /** Time slot identifier */
  timeSlot: string;
  /** Utilization percentage (0-100) */
  utilization: number;
  /** Current cell status */
  status: 'optimal' | 'warning' | 'critical';
  /** Number of scheduled classes in this slot */
  classCount: number;
  /** Capacity information */
  capacity: {
    current: number;
    maximum: number;
  };
}

/**
 * CalendarEvent - Academic calendar events (holidays, exams, deadlines)
 */
export interface CalendarEvent {
  /** Unique identifier */
  id: string;
  /** Event title */
  title: string;
  /** Event start date/time ISO string */
  startDate: string;
  /** Event end date/time ISO string */
  endDate: string;
  /** Event classification */
  type: 'holiday' | 'exam' | 'event' | 'deadline';
  /** Optional detailed description */
  description?: string;
  /** Academic year */
  academicYear: number;
  /** Tenant identifier */
  tenantId: string;
}

/* ============================================================================
   STUDENT & ACADEMIC TYPES
   ============================================================================ */

/**
 * StudentRank - Student ranking and achievement data
 * Used by BottomPanel leaderboard component
 */
export interface StudentRank {
  /** Unique student identifier */
  id: string;
  /** Student full name */
  name: string;
  /** Profile avatar URL or initials */
  avatarUrl: string;
  /** Achievement percentage (0-100) */
  gradePercentage: number;
  /** Ranking position (1, 2, 3, etc.) */
  position: number;
  /** Visual indicator color variant */
  colorVariant: 'emerald' | 'violet' | 'amber';
}

/**
 * Course - Individual course enrollment record
 */
export interface Course {
  /** Unique course identifier */
  id: string;
  /** Course code (e.g., "MATH101") */
  code: string;
  /** Course name */
  name: string;
  /** Credit hours */
  credits: number;
  /** Grade received (A, A-, B+, etc.) */
  grade: string;
  /** Semester number in academic year */
  semester: number;
  /** Current course status */
  status: 'completed' | 'in-progress' | 'failed' | 'dropped';
  /** Date course completed (ISO string) */
  completedDate?: string;
  /** Prerequisite courses required */
  prerequisites: string[];
}

/**
 * StudentAcademicRecord - Complete student academic profile
 */
export interface StudentAcademicRecord {
  /** Unique student identifier */
  id: string;
  /** Student full name */
  name: string;
  /** Current grade level */
  grade: string;
  /** Cumulative GPA */
  gpa: number;
  /** Total credits completed */
  completedCredits: number;
  /** Total credits required for graduation */
  totalCredits: number;
  /** Student rank in cohort */
  ranking: number;
  /** Enrollment date (ISO string) */
  enrollmentDate: string;
  /** All enrolled courses */
  courses: Course[];
  /** Academic year */
  academicYear: number;
  /** Tenant identifier */
  tenantId: string;
  /** Last updated timestamp */
  updatedAt: string;
}

/* ============================================================================
   ASSET & INFRASTRUCTURE TYPES
   ============================================================================ */

/**
 * AssetNode - Geographic asset tracking node
 * Used by BottomPanel spatial asset radar
 */
export interface AssetNode {
  /** Unique asset identifier */
  id: string;
  /** Human-readable asset label (e.g., "Vehicle ID: 8598") */
  label: string;
  /** Last update timestamp (ISO string) */
  timestamp: string;
  /** Geographic or grid coordinates */
  coordinates: {
    /** X position or latitude */
    x: number;
    /** Y position or longitude */
    y: number;
  };
  /** Additional asset metadata (JSON stringified) */
  metadata: string;
}

/**
 * AssetTrackerStatus - Real-time asset status information
 */
export interface AssetTrackerStatus {
  /** Asset node reference */
  asset: AssetNode;
  /** Current operational status */
  status: 'active' | 'idle' | 'offline';
  /** Signal connectivity percentage */
  connectivity: number;
  /** Detailed connectivity metrics */
  signal: {
    strength: number;
    quality: 'excellent' | 'good' | 'fair' | 'poor';
  };
  /** Last heartbeat timestamp */
  lastHeartbeat: string;
}

/**
 * Infrastructure - School infrastructure resource
 */
export interface Infrastructure {
  /** Unique infrastructure identifier */
  id: string;
  /** Resource name/identifier */
  name: string;
  /** Resource type */
  type: 'room' | 'vehicle' | 'equipment' | 'lab';
  /** Current capacity */
  capacity: number;
  /** Geographic location */
  location: {
    latitude: number;
    longitude: number;
    building?: string;
    floor?: number;
  };
  /** Resource availability status */
  availability: 'available' | 'occupied' | 'maintenance';
  /** Tenant identifier */
  tenantId: string;
}

/* ============================================================================
   DASHBOARD & LAYOUT TYPES
   ============================================================================ */

/**
 * DashboardLayoutState - Main dashboard grid state
 */
export interface DashboardLayoutState {
  /** Tenant identifier for data scoping */
  tenantId: string;
  /** Academic year context */
  academicYear: number;
  /** Metric cards data */
  metrics: MetricCardData[];
  /** Scheduling conflicts */
  conflicts: SchedulingConflict[];
  /** Grid utilization data */
  gridCells: SchedulingGridCell[];
  /** Calendar events */
  calendarEvents: CalendarEvent[];
  /** Student rankings */
  studentRankings: StudentRank[];
  /** Asset tracking nodes */
  assetNodes: AssetNode[];
}

/**
 * DashboardSuspenseState - Loading state for suspense boundaries
 */
export interface DashboardSuspenseState {
  /** Whether data is currently loading */
  isLoading: boolean;
  /** Optional error message if loading failed */
  error?: string;
  /** Timestamp of last successful data fetch */
  lastFetch?: string;
}

/* ============================================================================
   COMMAND PALETTE TYPES
   ============================================================================ */

/**
 * OmniSearchCommand - Individual searchable command
 */
export interface OmniSearchCommand {
  /** Unique command identifier */
  id: string;
  /** Display label */
  label: string;
  /** Command category for grouping */
  category: 'students' | 'classrooms' | 'schedules' | 'actions';
  /** Icon component (React element or string reference) */
  icon: React.ReactNode;
  /** Optional description text */
  description?: string;
  /** Optional action to execute */
  action?: () => void | Promise<void>;
  /** Optional navigation href */
  href?: string;
  /** Search keywords for matching */
  keywords?: string[];
}

/**
 * OmniSearchState - Command palette state
 */
export interface OmniSearchState {
  /** Whether palette is open */
  isOpen: boolean;
  /** Current search query */
  query: string;
  /** Highlighted command index */
  highlightedIndex: number;
  /** Available commands */
  commands: OmniSearchCommand[];
}

/* ============================================================================
   PATHWAY TRACKER TYPES
   ============================================================================ */

/**
 * AcademicPhase - Four-year academic progression phase
 */
export interface AcademicPhase {
  /** Academic year (1-4) */
  year: number;
  /** Phase identifier */
  phase: 'freshman' | 'sophomore' | 'junior' | 'senior';
  /** Courses in this phase */
  courses: Course[];
  /** Credits completed in phase */
  completedCredits: number;
  /** Total credits required for phase */
  totalCredits: number;
  /** Prerequisite warnings */
  prerequisiteIssues: string[];
  /** Failed courses in this phase */
  failedCourses: Course[];
}

/**
 * GraduationPathway - Complete graduation audit trail
 */
export interface GraduationPathway {
  /** Student identifier */
  studentId: string;
  /** All academic phases */
  phases: AcademicPhase[];
  /** Overall graduation progress (0-100) */
  progressPercentage: number;
  /** Remaining requirements */
  remainingRequirements: string[];
  /** Estimated graduation date */
  estimatedGraduationDate: string;
  /** Last audit timestamp */
  lastAuditDate: string;
}

/* ============================================================================
   ARCHIVE & EXPORT TYPES
   ============================================================================ */

/**
 * ArchiveMetadata - Static archive file metadata
 */
export interface ArchiveMetadata {
  /** Tenant identifier */
  tenantId: string;
  /** Academic year archived */
  academicYear: number;
  /** Archive generation timestamp */
  generatedAt: string;
  /** Total students in archive */
  studentCount: number;
  /** Total records included */
  totalRecords: number;
  /** Compression ratio percentage */
  compressionRatio: string;
  /** Archive file version */
  version: string;
}

/**
 * ExportPackage - Complete export bundle
 */
export interface ExportPackage {
  /** Archive metadata */
  metadata: ArchiveMetadata;
  /** HTML content (self-contained) */
  htmlContent: string;
  /** Output filename */
  filename: string;
  /** File size in bytes */
  fileSize: number;
  /** MIME type */
  mimeType: 'application/octet-stream' | 'text/html';
}

/* ============================================================================
   API REQUEST/RESPONSE TYPES
   ============================================================================ */

/**
 * ApiResponse - Standard API response wrapper
 */
export interface ApiResponse<T> {
  /** Success status flag */
  success: boolean;
  /** Response data */
  data?: T;
  /** Error message if failed */
  error?: string;
  /** HTTP status code */
  status: number;
  /** Request timestamp */
  timestamp: string;
}

/**
 * PaginatedResponse - Paginated list response
 */
export interface PaginatedResponse<T> {
  /** List of items */
  items: T[];
  /** Current page number */
  page: number;
  /** Items per page */
  pageSize: number;
  /** Total item count */
  total: number;
  /** Total pages */
  totalPages: number;
  /** Whether more pages exist */
  hasNextPage: boolean;
}

/* ============================================================================
   ERROR TYPES
   ============================================================================ */

/**
 * AppError - Standardized application error
 */
export interface AppError extends Error {
  /** Error code for programmatic handling */
  code: string;
  /** HTTP status code */
  status: number;
  /** Additional error context */
  context?: Record<string, any>;
}

/* ============================================================================
   TENANT & AUTH TYPES
   ============================================================================ */

/**
 * TenantContext - Multi-tenant application context
 */
export interface TenantContext {
  /** Current tenant identifier */
  tenantId: string;
  /** Tenant name */
  name: string;
  /** Academic years available */
  academicYears: number[];
  /** Current active academic year */
  activeAcademicYear: number;
  /** Tenant subscription tier */
  tier: 'starter' | 'professional' | 'enterprise';
  /** Feature flags */
  features: Record<string, boolean>;
}

/* ============================================================================
   UTILITY TYPES
   ============================================================================ */

/**
 * Dimensions - Width and height measurements
 */
export interface Dimensions {
  /** Width in pixels */
  width: number;
  /** Height in pixels */
  height: number;
}

/**
 * Position - X,Y coordinate point
 */
export interface Position {
  /** X coordinate */
  x: number;
  /** Y coordinate */
  y: number;
}

/**
 * Bounds - Rectangle boundaries
 */
export interface Bounds {
  /** Left boundary */
  left: number;
  /** Top boundary */
  top: number;
  /** Right boundary */
  right: number;
  /** Bottom boundary */
  bottom: number;
}

/**
 * TimeRange - Start and end time interval
 */
export interface TimeRange {
  /** Start time (ISO string) */
  startTime: string;
  /** End time (ISO string) */
  endTime: string;
}

/**
 * ColorVariant - Design system color options
 */
export type ColorVariant = 'coral' | 'violet' | 'amber' | 'emerald';

/**
 * SeverityLevel - Severity classification
 */
export type SeverityLevel = 'critical' | 'warning' | 'info' | 'success';

/**
 * StatusType - General status values
 */
export type StatusType = 'active' | 'idle' | 'offline' | 'pending' | 'completed' | 'failed';

/**
 * ContentAlignment - Text/content alignment options
 */
export type ContentAlignment = 'left' | 'center' | 'right';

/* ============================================================================
   REACT COMPONENT PROP TYPES
   ============================================================================ */

/**
 * CommonComponentProps - Base props for all components
 */
export interface CommonComponentProps {
  /** CSS class name */
  className?: string;
  /** Component children */
  children?: React.ReactNode;
  /** Accessible label */
  ariaLabel?: string;
}

/**
 * AnimatedComponentProps - Props for animated components
 */
export interface AnimatedComponentProps extends CommonComponentProps {
  /** Animation variant key */
  variant?: string;
  /** Enable animations */
  animated?: boolean;
  /** Animation delay in seconds */
  delay?: number;
}

/* ============================================================================
   DATABASE MODEL TYPES
   ============================================================================ */

/**
 * BaseEntity - Common database entity fields
 */
export interface BaseEntity {
  /** Unique identifier */
  id: string;
  /** Creation timestamp */
  createdAt: string;
  /** Last update timestamp */
  updatedAt: string;
  /** Tenant identifier for multi-tenancy */
  tenantId: string;
}

/**
 * StudentEntity - Database student record
 */
export interface StudentEntity extends BaseEntity {
  /** Student name */
  name: string;
  /** Current grade level */
  grade: string;
  /** Cumulative GPA */
  gpa: number;
  /** Completed credits */
  completedCredits: number;
  /** Total required credits */
  totalCredits: number;
  /** Class rank */
  ranking: number;
  /** Enrollment date */
  enrollmentDate: string;
  /** Academic year */
  academicYear: number;
}

/**
 * CourseEntity - Database course record
 */
export interface CourseEntity extends BaseEntity {
  /** Course code */
  code: string;
  /** Course name */
  name: string;
  /** Credit hours */
  credits: number;
  /** Academic year */
  academicYear: number;
}

/**
 * EnrollmentEntity - Database enrollment record
 */
export interface EnrollmentEntity extends BaseEntity {
  /** Student ID reference */
  studentId: string;
  /** Course ID reference */
  courseId: string;
  /** Received grade */
  grade: string;
  /** Enrollment semester */
  semester: number;
  /** Course status */
  status: 'completed' | 'in-progress' | 'failed' | 'dropped';
}

export default {};
