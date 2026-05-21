'use client';

import React, { useState, useMemo, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  Zap,
  X,
  Building2,
  User,
} from 'lucide-react';
import type { SchedulingConflict } from '@/types';

/* ============================================================================
   Type Definitions
   ============================================================================ */

interface GridCell {
  id: string;
  year: number;
  semester: number;
  room: string;
  teacher: string;
  status: 'optimal' | 'warning' | 'critical';
  utilization: number;
}

interface ConflictError {
  id: string;
  type: 'critical' | 'warning';
  room: string;
  timeSlot: string;
  conflict: string;
  resolved: boolean;
  resolving: boolean;
}

/* ============================================================================
   Mock Data Generation
   ============================================================================ */

const generateGridData = (): GridCell[] => {
  const cells: GridCell[] = [];
  const rooms = ['A101', 'A102', 'B201', 'B202', 'C301', 'C302'];
  const teachers = ['Dr. Smith', 'Prof. Johnson', 'Ms. Chen', 'Dr. Patel'];
  const statuses: Array<'optimal' | 'warning' | 'critical'> = [
    'optimal',
    'optimal',
    'optimal',
    'warning',
    'critical',
  ];

  for (let year = 2024; year <= 2025; year++) {
    for (let semester = 1; semester <= 2; semester++) {
      for (let i = 0; i < 12; i++) {
        cells.push({
          id: `${year}-${semester}-${i}`,
          year,
          semester,
          room: rooms[Math.floor(Math.random() * rooms.length)],
          teacher:
            teachers[Math.floor(Math.random() * teachers.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          utilization: Math.random() * 100,
        });
      }
    }
  }

  return cells;
};

/* ============================================================================
   Grid Cell Component
   ============================================================================ */

interface GridCellProps {
  cell: GridCell;
  onCellClick: (cell: GridCell) => void;
}

const GridCell: React.FC<GridCellProps> = ({ cell, onCellClick }) => {
  const getStatusColor = () => {
    switch (cell.status) {
      case 'optimal':
        return 'bg-emerald-500/10 hover:bg-emerald-500/20';
      case 'warning':
        return 'bg-amber-500/20 hover:bg-amber-500/30';
      case 'critical':
        return 'bg-rose-500/40 hover:bg-rose-500/50';
    }
  };

  const getBorderColor = () => {
    switch (cell.status) {
      case 'optimal':
        return 'border-emerald-500/20';
      case 'warning':
        return 'border-amber-500/30';
      case 'critical':
        return 'border-rose-500/50';
    }
  };

  return (
    <motion.button
      onClick={() => onCellClick(cell)}
      className={`relative w-12 h-12 rounded border transition-all duration-200 cursor-pointer group flex-shrink-0 ${getStatusColor()} ${getBorderColor()}`}
      whileHover={{ scale: 1.08 }}
      whileTap={{ scale: 0.95 }}
      type="button"
    >
      {/* Loading pulse indicator */}
      {cell.status === 'critical' && (
        <motion.div
          className="absolute inset-0 rounded bg-rose-500/20"
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      )}

      {/* Utilization bar */}
      <div className="absolute bottom-1 left-1 right-1 h-0.5 rounded-full bg-primary/20 overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-primary to-secondary"
          initial={{ width: 0 }}
          animate={{ width: `${cell.utilization}%` }}
          transition={{ duration: 0.8, delay: 0.1 }}
        />
      </div>

      {/* Hover tooltip preview */}
      <motion.div
        className="absolute -top-12 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 pointer-events-none z-50"
        initial={{ opacity: 0, y: 8 }}
        whileHover={{ opacity: 1, y: 0 }}
      >
        <div className="bg-background border border-border rounded px-2 py-1 whitespace-nowrap text-xs text-white font-mono">
          {cell.room}
        </div>
      </motion.div>
    </motion.button>
  );
};

/* ============================================================================
   Grid Popover Component
   ============================================================================ */

interface GridPopoverProps {
  cell: GridCell | null;
  onClose: () => void;
}

const GridPopover: React.FC<GridPopoverProps> = ({ cell, onClose }) => {
  if (!cell) return null;

  return (
    <AnimatePresence>
      {cell && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/50 z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Popover Card */}
          <motion.div
            className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 gemini-blur-card w-96 p-6 overflow-y-auto max-h-[90vh]"
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-6">
              <div>
                <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
                  Room Details
                </p>
                <h3 className="text-2xl font-bold text-white mt-1 tracking-tight font-mono">
                  {cell.room}
                </h3>
              </div>

              <motion.button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-primary/10 transition-colors text-muted-foreground hover:text-primary flex-shrink-0"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                type="button"
              >
                <X className="w-4 h-4" />
              </motion.button>
            </div>

            {/* Content Grid */}
            <div className="space-y-4">
              {/* Teacher Info */}
              <div className="flex items-center gap-3 p-3 rounded-lg bg-primary/5 border border-primary/20">
                <User className="w-4 h-4 text-primary flex-shrink-0" />
                <div className="min-w-0">
                  <p className="text-xs text-muted-foreground">Instructor</p>
                  <p className="text-sm font-medium text-white truncate">{cell.teacher}</p>
                </div>
              </div>

              {/* Year & Semester Info */}
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 rounded-lg border border-border">
                  <p className="text-xs text-muted-foreground">Academic Year</p>
                  <p className="text-sm font-bold text-white mt-1 font-mono">
                    {cell.year}
                  </p>
                </div>
                <div className="p-3 rounded-lg border border-border">
                  <p className="text-xs text-muted-foreground">Semester</p>
                  <p className="text-sm font-bold text-white mt-1 font-mono">
                    S{cell.semester}
                  </p>
                </div>
              </div>

              {/* Utilization Stat */}
              <div className="p-3 rounded-lg border border-border">
                <p className="text-xs text-muted-foreground">Utilization</p>
                <div className="flex items-center gap-2 mt-2">
                  <div className="flex-1 h-2 rounded-full bg-primary/20 overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-primary to-secondary"
                      initial={{ width: 0 }}
                      animate={{ width: `${cell.utilization}%` }}
                      transition={{ duration: 0.8 }}
                    />
                  </div>
                  <p className="text-sm font-bold text-primary font-mono flex-shrink-0">
                    {Math.round(cell.utilization)}%
                  </p>
                </div>
              </div>

              {/* Status Badge */}
              <div className="flex items-center gap-2">
                {cell.status === 'optimal' && (
                  <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                    <span className="text-xs font-medium text-emerald-400">
                      Optimal Availability
                    </span>
                  </div>
                )}
                {cell.status === 'warning' && (
                  <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-500/10 border border-amber-500/30">
                    <AlertTriangle className="w-4 h-4 text-amber-500 flex-shrink-0" />
                    <span className="text-xs font-medium text-amber-400">
                      Heavy Traffic
                    </span>
                  </div>
                )}
                {cell.status === 'critical' && (
                  <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-rose-500/10 border border-rose-500/30">
                    <AlertCircle className="w-4 h-4 text-rose-500 flex-shrink-0" />
                    <span className="text-xs font-medium text-rose-400">
                      Conflict Alert
                    </span>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

/* ============================================================================
   Conflict Error Banner Component
   ============================================================================ */

interface ConflictBannerProps {
  error: ConflictError;
  onResolve: (id: string) => void;
  onRemove: (id: string) => void;
}

const ConflictBanner: React.FC<ConflictBannerProps> = ({
  error,
  onResolve,
  onRemove,
}) => {
  const isResolved = error.resolved;
  const isResolving = error.resolving;

  const bgColor =
    error.type === 'critical'
      ? 'bg-rose-500/5 border-rose-500/30'
      : 'bg-amber-500/5 border-amber-500/30';

  const textColor =
    error.type === 'critical'
      ? 'text-rose-400'
      : 'text-amber-400';

  const badgeColor =
    error.type === 'critical'
      ? 'bg-rose-500/20 text-rose-300'
      : 'bg-amber-500/20 text-amber-300';

  return (
    <motion.div
      className={`rounded-lg border p-4 ${bgColor}`}
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 20 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-start justify-between gap-4">
        {/* Left Content */}
        <div className="flex-1 min-w-0">
          {/* Header with Badge */}
          <div className="flex items-center gap-2 mb-2">
            {isResolved ? (
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 300, damping: 25 }}
              >
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              </motion.div>
            ) : error.type === 'critical' ? (
              <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 text-amber-400 flex-shrink-0" />
            )}

            <span className={`text-xs font-bold tracking-widest uppercase ${textColor}`}>
              {isResolved
                ? 'RESOLVED'
                : error.type === 'critical'
                  ? 'CRITICAL ERROR'
                  : 'WARNING'}
            </span>
          </div>

          {/* Room & Time */}
          <div className="mb-2">
            <p className="text-sm font-semibold text-white flex items-center gap-2">
              <Building2 className="w-4 h-4 flex-shrink-0" />
              <span className="font-mono">Room {error.room}</span> • {error.timeSlot}
            </p>
          </div>

          {/* Conflict Description */}
          <p className="text-xs text-muted-foreground line-clamp-2">
            {error.conflict}
          </p>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-2 flex-shrink-0">
          {!isResolved && (
            <motion.button
              onClick={() => onResolve(error.id)}
              disabled={isResolving}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-primary/20 hover:bg-primary/30 disabled:opacity-50 text-xs font-medium text-primary transition-colors flex-shrink-0"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="button"
            >
              {isResolving ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, linear: true }}
                  >
                    <Zap className="w-3 h-3" />
                  </motion.div>
                  <span>Resolving...</span>
                </>
              ) : (
                <>
                  <Zap className="w-3 h-3" />
                  <span>Resolve with AI</span>
                </>
              )}
            </motion.button>
          )}

          <motion.button
            onClick={() => onRemove(error.id)}
            className="p-1.5 rounded-lg hover:bg-primary/10 text-muted-foreground hover:text-primary transition-colors flex-shrink-0"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            type="button"
          >
            <X className="w-4 h-4" />
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

/* ============================================================================
   Main MiddlePanel Component
   ============================================================================ */

interface MiddlePanelProps {
  conflicts?: SchedulingConflict[];
}

export const MiddlePanel: React.FC<MiddlePanelProps> = ({ conflicts = [] }) => {
  const [gridData] = useState<GridCell[]>(generateGridData());
  const [conflictErrors, setConflictErrors] = useState<ConflictError[]>(
    conflicts.map((c, i) => ({
      id: c.id,
      type: c.severity === 'CRITICAL' ? 'critical' : 'warning',
      room: c.room,
      timeSlot: c.timeAgo,
      conflict: c.message,
      resolved: c.resolved,
      resolving: false,
    }))
  );
  const [selectedCell, setSelectedCell] = useState<GridCell | null>(null);

  const groupedByYearSemester = useMemo(() => {
    const grouped: Record<string, GridCell[]> = {};
    gridData.forEach((cell) => {
      const key = `${cell.year}-S${cell.semester}`;
      if (!grouped[key]) grouped[key] = [];
      grouped[key].push(cell);
    });
    return Object.entries(grouped).sort();
  }, [gridData]);

  const handleResolve = useCallback((id: string) => {
    setConflictErrors((prev) =>
      prev.map((conflict) =>
        conflict.id === id
          ? { ...conflict, resolving: true }
          : conflict
      )
    );

    // Simulate AI resolution
    setTimeout(() => {
      setConflictErrors((prev) =>
        prev.map((conflict) =>
          conflict.id === id
            ? { ...conflict, resolving: false, resolved: true }
            : conflict
        )
      );
    }, 2000);
  }, []);

  const handleRemove = useCallback((id: string) => {
    setConflictErrors((prev) => prev.filter((conflict) => conflict.id !== id));
  }, []);

  return (
    <div className="h-full w-full flex gap-6 overflow-hidden">
      {/* Left Column - Contribution Matrix */}
      <div className="flex-1 min-w-0 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="mb-4 flex-shrink-0">
          <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
            Scheduling Matrix
          </p>
          <h2 className="text-2xl font-bold text-white mt-2 tracking-tight">
            Academic Calendar
          </h2>
          <p className="text-xs text-muted-foreground mt-1">
            Room availability and utilization tracking
          </p>
        </div>

        {/* Grid Container - Scrollable with Overflow Control */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden">
          <div className="space-y-6 pr-4">
            {groupedByYearSemester.map(([key, cells]) => (
              <motion.div
                key={key}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
              >
                {/* Period Header */}
                <div className="mb-3">
                  <p className="text-xs font-semibold text-primary tracking-wider uppercase font-mono">
                    {key}
                  </p>
                </div>

                {/* Grid */}
                <div className="flex flex-wrap gap-2">
                  {cells.map((cell) => (
                    <GridCell
                      key={cell.id}
                      cell={cell}
                      onCellClick={setSelectedCell}
                    />
                  ))}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Legend */}
        <motion.div
          className="mt-6 pt-4 border-t border-border grid grid-cols-3 gap-3 flex-shrink-0"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-emerald-500/20 border border-emerald-500/20 flex-shrink-0" />
            <span className="text-xs text-muted-foreground">Optimal</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-amber-500/20 border border-amber-500/30 flex-shrink-0" />
            <span className="text-xs text-muted-foreground">Warning</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded bg-rose-500/40 border border-rose-500/50 flex-shrink-0" />
            <span className="text-xs text-muted-foreground">Critical</span>
          </div>
        </motion.div>
      </div>

      {/* Divider */}
      <div className="w-px bg-border flex-shrink-0" />

      {/* Right Column - AI Compliance Stream */}
      <div className="w-96 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="mb-4 flex-shrink-0">
          <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
            AI Compliance
          </p>
          <h2 className="text-2xl font-bold text-white mt-2 tracking-tight">
            Conflict Resolution
          </h2>
          <p className="text-xs text-muted-foreground mt-1">
            {conflictErrors.filter((c) => !c.resolved).length} active issues
          </p>
        </div>

        {/* Errors List - Scrollable with Overflow Control */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden">
          <div className="space-y-3 pr-2">
            <AnimatePresence mode="popLayout">
              {conflictErrors.length === 0 ? (
                <motion.div
                  className="h-full flex items-center justify-center text-center py-12"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <div>
                    <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto mb-2" />
                    <p className="text-xs font-medium text-muted-foreground">
                      All conflicts resolved
                    </p>
                  </div>
                </motion.div>
              ) : (
                conflictErrors.map((error) => (
                  <ConflictBanner
                    key={error.id}
                    error={error}
                    onResolve={handleResolve}
                    onRemove={handleRemove}
                  />
                ))
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Grid Popover */}
      <GridPopover cell={selectedCell} onClose={() => setSelectedCell(null)} />
    </div>
  );
};

export default MiddlePanel;
