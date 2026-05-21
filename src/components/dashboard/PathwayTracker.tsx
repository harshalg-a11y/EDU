'use client';

import React, { useState, useMemo, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  CheckCircle2,
  AlertCircle,
  BookOpen,
  TrendingUp,
  Award,
  Clock,
  Zap,
} from 'lucide-react';

/* ============================================================================
   Type Definitions
   ============================================================================ */

interface Course {
  id: string;
  code: string;
  name: string;
  credits: number;
  status: 'completed' | 'in-progress' | 'missing-prerequisite' | 'failed';
  grade?: string;
  semester?: number;
}

interface AcademicPhase {
  year: number;
  phase: 'freshman' | 'sophomore' | 'junior' | 'senior';
  courses: Course[];
  completedCredits: number;
  totalCredits: number;
}

/* ============================================================================
   Mock Data
   ============================================================================ */

const generatePathwayData = (): AcademicPhase[] => [
  {
    year: 1,
    phase: 'freshman',
    courses: [
      {
        id: 'c1',
        code: 'ENG101',
        name: 'English Composition',
        credits: 3,
        status: 'completed',
        grade: 'A',
        semester: 1,
      },
      {
        id: 'c2',
        code: 'MATH101',
        name: 'Calculus I',
        credits: 4,
        status: 'completed',
        grade: 'A-',
        semester: 1,
      },
      {
        id: 'c3',
        code: 'CHEM101',
        name: 'Chemistry I',
        credits: 4,
        status: 'completed',
        grade: 'B+',
        semester: 1,
      },
      {
        id: 'c4',
        code: 'PHYS101',
        name: 'Physics I',
        credits: 4,
        status: 'in-progress',
        semester: 2,
      },
    ],
    completedCredits: 11,
    totalCredits: 15,
  },
  {
    year: 2,
    phase: 'sophomore',
    courses: [
      {
        id: 'c5',
        code: 'MATH201',
        name: 'Calculus II',
        credits: 4,
        status: 'completed',
        grade: 'B+',
        semester: 3,
      },
      {
        id: 'c6',
        code: 'CHEM201',
        name: 'Chemistry II',
        credits: 4,
        status: 'completed',
        grade: 'B',
        semester: 3,
      },
      {
        id: 'c7',
        code: 'BIO101',
        name: 'Biology I',
        credits: 3,
        status: 'missing-prerequisite',
        semester: 4,
      },
      {
        id: 'c8',
        code: 'PHYS201',
        name: 'Physics II',
        credits: 4,
        status: 'failed',
        grade: 'F',
        semester: 4,
      },
    ],
    completedCredits: 8,
    totalCredits: 15,
  },
  {
    year: 3,
    phase: 'junior',
    courses: [
      {
        id: 'c9',
        code: 'CS301',
        name: 'Data Structures',
        credits: 3,
        status: 'completed',
        grade: 'A',
        semester: 5,
      },
      {
        id: 'c10',
        code: 'MATH301',
        name: 'Linear Algebra',
        credits: 3,
        status: 'in-progress',
        semester: 5,
      },
      {
        id: 'c11',
        code: 'CS302',
        name: 'Algorithms',
        credits: 4,
        status: 'completed',
        grade: 'A-',
        semester: 6,
      },
    ],
    completedCredits: 6,
    totalCredits: 10,
  },
  {
    year: 4,
    phase: 'senior',
    courses: [
      {
        id: 'c12',
        code: 'CS401',
        name: 'Software Engineering',
        credits: 3,
        status: 'completed',
        grade: 'A',
        semester: 7,
      },
      {
        id: 'c13',
        code: 'CS499',
        name: 'Senior Capstone',
        credits: 4,
        status: 'in-progress',
        semester: 8,
      },
    ],
    completedCredits: 3,
    totalCredits: 7,
  },
];

/* ============================================================================
   Live Credits Gauge Component
   ============================================================================ */

interface CreditsGaugeProps {
  completedCredits: number;
  totalCredits: number;
}

const CreditsGauge: React.FC<CreditsGaugeProps> = ({
  completedCredits,
  totalCredits,
}) => {
  const [displayedCredits, setDisplayedCredits] = useState(0);
  const percentage = (completedCredits / totalCredits) * 100;
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  // Animate credit counter
  useEffect(() => {
    const timer = setTimeout(() => {
      setDisplayedCredits(completedCredits);
    }, 500);
    return () => clearTimeout(timer);
  }, [completedCredits]);

  const isAlmostComplete = percentage >= 90;
  const isComplete = percentage === 100;

  return (
    <motion.div
      className="flex flex-col items-center justify-center py-6"
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.2, duration: 0.4 }}
    >
      {/* Radial Progress Circle */}
      <div className="relative w-32 h-32 mb-4">
        {/* Background Circle */}
        <svg
          className="absolute inset-0 w-full h-full -rotate-90"
          viewBox="0 0 120 120"
        >
          <circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke="var(--border)"
            strokeWidth="3"
          />

          {/* Progress Circle */}
          <motion.circle
            cx="60"
            cy="60"
            r="45"
            fill="none"
            stroke={
              isComplete
                ? '#10b981'
                : isAlmostComplete
                  ? '#f59e0b'
                  : 'url(#creditGradient)'
            }
            strokeWidth="3"
            strokeDasharray={circumference}
            strokeDashoffset={circumference}
            strokeLinecap="round"
            animate={{
              strokeDashoffset,
            }}
            transition={{ duration: 1.2, ease: 'easeOut' }}
          />

          {/* Gradient Definition */}
          <defs>
            <linearGradient
              id="creditGradient"
              x1="0%"
              y1="0%"
              x2="100%"
              y2="100%"
            >
              <stop offset="0%" stopColor="var(--primary)" />
              <stop offset="100%" stopColor="var(--secondary)" />
            </linearGradient>
          </defs>
        </svg>

        {/* Center Content */}
        <motion.div
          className="absolute inset-0 flex flex-col items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          {/* Credit Count */}
          <p className="text-2xl font-black text-white">
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
            >
              {displayedCredits}
            </motion.span>
          </p>

          {/* Total */}
          <p className="text-xs text-muted-foreground">
            / {totalCredits} Credits
          </p>

          {/* Status Icon */}
          <motion.div
            className="mt-2"
            animate={isAlmostComplete ? { scale: [1, 1.1, 1] } : {}}
            transition={{ duration: 2, repeat: Infinity }}
          >
            {isComplete ? (
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            ) : isAlmostComplete ? (
              <AlertCircle className="w-5 h-5 text-amber-400" />
            ) : (
              <Zap className="w-5 h-5 text-primary" />
            )}
          </motion.div>
        </motion.div>
      </div>

      {/* Status Text */}
      <motion.div
        className="text-center text-xs text-muted-foreground"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        {isComplete ? (
          <p className="text-emerald-400 font-medium">
            Graduation Requirements Met ✓
          </p>
        ) : isAlmostComplete ? (
          <p className="text-amber-400 font-medium">
            {totalCredits - completedCredits} Credits Remaining
          </p>
        ) : (
          <p>
            {Math.round(percentage)}% Progress
            <br />
            {totalCredits - completedCredits} Credits Needed
          </p>
        )}
      </motion.div>
    </motion.div>
  );
};

/* ============================================================================
   Course Block Component
   ============================================================================ */

interface CourseBlockProps {
  course: Course;
  index: number;
}

const CourseBlock: React.FC<CourseBlockProps> = ({ course, index }) => {
  const [isHovered, setIsHovered] = useState(false);

  const getStatusColor = () => {
    switch (course.status) {
      case 'completed':
        return 'bg-emerald-500/10 border-emerald-500/30 hover:border-emerald-500/50';
      case 'in-progress':
        return 'bg-primary/10 border-primary/30 hover:border-primary/50';
      case 'missing-prerequisite':
        return 'bg-amber-500/10 border-amber-500/30 hover:border-amber-500/50';
      case 'failed':
        return 'bg-rose-500/10 border-rose-500/30 hover:border-rose-500/50';
    }
  };

  const getIcon = () => {
    switch (course.status) {
      case 'completed':
        return (
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ delay: index * 0.1 + 0.2, type: 'spring' }}
          >
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </motion.div>
        );
      case 'missing-prerequisite':
        return (
          <motion.div
            animate={{ scale: [1, 1.15, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <AlertCircle className="w-4 h-4 text-amber-400" />
          </motion.div>
        );
      case 'failed':
        return (
          <motion.div
            animate={{ scale: [1, 1.15, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            <AlertCircle className="w-4 h-4 text-rose-400" />
          </motion.div>
        );
      default:
        return <Clock className="w-4 h-4 text-primary" />;
    }
  };

  return (
    <motion.div
      className={`px-3 py-2 rounded-lg border transition-all duration-200 cursor-pointer ${getStatusColor()}`}
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.08 }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={{ scale: 1.05, x: 4 }}
    >
      {/* Status Icon & Course Code */}
      <div className="flex items-center gap-2 mb-1">
        {getIcon()}
        <p className="text-xs font-bold text-white">{course.code}</p>
      </div>

      {/* Course Name */}
      <p className="text-xs text-muted-foreground truncate">
        {course.name}
      </p>

      {/* Grade & Credits */}
      <div className="flex items-center justify-between mt-1.5 text-xs">
        {course.grade && (
          <span className="font-medium text-white">{course.grade}</span>
        )}
        <span className="text-muted-foreground">{course.credits} cr</span>
      </div>

      {/* Hover Tooltip */}
      <AnimatePresence>
        {isHovered && (
          <motion.div
            className="absolute left-full ml-2 top-0 z-50 pointer-events-none"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -8 }}
          >
            <div className="gemini-blur-card px-3 py-2 min-w-max text-xs">
              <p className="font-semibold text-white mb-1">{course.name}</p>
              <div className="space-y-1 text-muted-foreground">
                <p>Code: {course.code}</p>
                <p>Credits: {course.credits}</p>
                {course.status === 'completed' && course.grade && (
                  <p>Grade: {course.grade}</p>
                )}
                <p className="capitalize">
                  Status:{' '}
                  <span
                    className={
                      course.status === 'completed'
                        ? 'text-emerald-400'
                        : course.status === 'in-progress'
                          ? 'text-primary'
                          : 'text-amber-400'
                    }
                  >
                    {course.status.replace('-', ' ')}
                  </span>
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

/* ============================================================================
   Timeline Phase Component
   ============================================================================ */

interface TimelinePhaseProps {
  phase: AcademicPhase;
  phaseIndex: number;
  totalPhases: number;
}

const TimelinePhase: React.FC<TimelinePhaseProps> = ({
  phase,
  phaseIndex,
  totalPhases,
}) => {
  const completedCourses = phase.courses.filter(
    (c) => c.status === 'completed'
  ).length;
  const hasWarnings = phase.courses.some(
    (c) =>
      c.status === 'missing-prerequisite' ||
      c.status === 'failed'
  );
  const isLastPhase = phaseIndex === totalPhases - 1;

  const phaseLabels = {
    freshman: 'Freshman',
    sophomore: 'Sophomore',
    junior: 'Junior',
    senior: 'Senior',
  };

  return (
    <motion.div
      className="relative flex-1 flex flex-col"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: phaseIndex * 0.15 }}
    >
      {/* Connector Line */}
      {!isLastPhase && (
        <motion.div
          className="absolute top-8 left-[calc(50%+24px)] right-0 h-0.5 bg-gradient-to-r from-primary to-transparent"
          initial={{ scaleX: 0, opacity: 0 }}
          animate={{ scaleX: 1, opacity: 0.3 }}
          transition={{ delay: phaseIndex * 0.15 + 0.3, duration: 0.6 }}
          style={{ originX: 0 }}
        />
      )}

      {/* Phase Node */}
      <div className="flex items-start gap-4">
        {/* Node Circle */}
        <motion.div
          className="relative flex-shrink-0 w-12 h-12 rounded-full border-2 border-border bg-background flex items-center justify-center"
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{
            delay: phaseIndex * 0.15 + 0.1,
            type: 'spring',
            stiffness: 300,
          }}
        >
          <motion.div
            className="text-xs font-bold text-primary"
            animate={hasWarnings ? { scale: [1, 1.1, 1] } : {}}
            transition={{ duration: 2, repeat: Infinity }}
          >
            {completedCourses}/{phase.courses.length}
          </motion.div>

          {/* Glow Effect for Completion */}
          {completedCourses === phase.courses.length && (
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-emerald-400"
              animate={{ scale: [1, 1.2, 1], opacity: [1, 0, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          )}

          {/* Warning Pulse */}
          {hasWarnings && (
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-amber-400"
              animate={{ scale: [1, 1.1, 1], opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
          )}
        </motion.div>

        {/* Phase Content */}
        <motion.div
          className="flex-1"
          initial={{ opacity: 0, x: -12 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: phaseIndex * 0.15 + 0.2 }}
        >
          {/* Phase Header */}
          <div className="flex items-center gap-2 mb-3">
            <h3 className="text-sm font-bold text-white">
              {phaseLabels[phase.phase]} Year
            </h3>
            {hasWarnings && (
              <motion.div
                className="px-2 py-0.5 rounded bg-amber-500/20 border border-amber-500/30"
                animate={{ scale: [1, 1.05, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <span className="text-xs font-medium text-amber-400">
                  ⚠ Issues
                </span>
              </motion.div>
            )}
            {completedCourses === phase.courses.length && (
              <motion.div
                className="px-2 py-0.5 rounded bg-emerald-500/20 border border-emerald-500/30"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{
                  delay: phaseIndex * 0.15 + 0.5,
                  type: 'spring',
                }}
              >
                <span className="text-xs font-medium text-emerald-400">
                  ✓ Complete
                </span>
              </motion.div>
            )}
          </div>

          {/* Courses Grid */}
          <motion.div
            className="grid grid-cols-2 gap-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: phaseIndex * 0.15 + 0.3 }}
          >
            {phase.courses.map((course, courseIndex) => (
              <div key={course.id} className="relative">
                <CourseBlock
                  course={course}
                  index={phaseIndex * 4 + courseIndex}
                />
              </div>
            ))}
          </motion.div>

          {/* Phase Stats */}
          <motion.div
            className="mt-3 flex items-center gap-2 text-xs text-muted-foreground"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: phaseIndex * 0.15 + 0.4 }}
          >
            <div className="flex-1 h-1 rounded-full bg-border overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary to-secondary"
                initial={{ width: 0 }}
                animate={{
                  width: `${(phase.completedCredits / phase.totalCredits) * 100}%`,
                }}
                transition={{ delay: phaseIndex * 0.15 + 0.5, duration: 0.8 }}
              />
            </div>
            <span className="font-medium">
              {phase.completedCredits}/{phase.totalCredits}
            </span>
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
};

/* ============================================================================
   Main PathwayTracker Component
   ============================================================================ */

export const PathwayTracker: React.FC = () => {
  const pathwayData = useMemo(() => generatePathwayData(), []);

  const totalCompletedCredits = useMemo(
    () => pathwayData.reduce((sum, phase) => sum + phase.completedCredits, 0),
    [pathwayData]
  );

  const totalCredits = useMemo(
    () => pathwayData.reduce((sum, phase) => sum + phase.totalCredits, 0),
    [pathwayData]
  );

  const totalCompletedCourses = useMemo(
    () =>
      pathwayData.reduce(
        (sum, phase) =>
          sum +
          phase.courses.filter((c) => c.status === 'completed').length,
        0
      ),
    [pathwayData]
  );

  const totalCourses = useMemo(
    () =>
      pathwayData.reduce((sum, phase) => sum + phase.courses.length, 0),
    [pathwayData]
  );

  return (
    <div className="h-full w-full flex gap-6">
      {/* Left Sidebar - Credits Gauge */}
      <motion.div
        className="w-40 flex flex-col items-center justify-start pt-4"
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.4 }}
      >
        {/* Header */}
        <div className="text-center mb-4">
          <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
            Progress
          </p>
          <h2 className="text-lg font-bold text-white mt-1 tracking-tight">
            Graduation Path
          </h2>
        </div>

        {/* Gauge */}
        <CreditsGauge
          completedCredits={totalCompletedCredits}
          totalCredits={totalCredits}
        />

        {/* Stats */}
        <motion.div
          className="w-full mt-6 space-y-3 text-xs"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <div className="p-3 rounded-lg bg-primary/5 border border-primary/20 text-center">
            <p className="text-muted-foreground">Courses</p>
            <p className="text-lg font-bold text-white mt-1">
              {totalCompletedCourses}/{totalCourses}
            </p>
          </div>
          <div className="p-3 rounded-lg bg-border/50 text-center">
            <p className="text-muted-foreground">GPA</p>
            <p className="text-lg font-bold text-white mt-1">3.72</p>
          </div>
        </motion.div>
      </motion.div>

      {/* Divider */}
      <div className="w-px bg-border" />

      {/* Right Main - Timeline Rail */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="mb-6">
          <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
            Academic Timeline
          </p>
          <h2 className="text-2xl font-bold text-white mt-2 tracking-tight">
            Graduation Pathway Audit
          </h2>
          <p className="text-xs text-muted-foreground mt-1">
            Track completion status across all academic phases
          </p>
        </div>

        {/* Timeline Phases */}
        <motion.div
          className="flex-1 flex flex-col gap-6 overflow-y-auto pr-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          {pathwayData.map((phase, index) => (
            <TimelinePhase
              key={phase.phase}
              phase={phase}
              phaseIndex={index}
              totalPhases={pathwayData.length}
            />
          ))}
        </motion.div>

        {/* Legend */}
        <motion.div
          className="mt-6 pt-4 border-t border-border grid grid-cols-4 gap-3"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <div className="flex items-center gap-2 text-xs">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span className="text-muted-foreground">Completed</span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <Clock className="w-4 h-4 text-primary flex-shrink-0" />
            <span className="text-muted-foreground">In Progress</span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
            <span className="text-muted-foreground">Missing Prereq</span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <span className="text-muted-foreground">Failed</span>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PathwayTracker;
