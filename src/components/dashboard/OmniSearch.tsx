'use client';

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import {
  Search,
  User,
  MapPin,
  Clock,
  Zap,
  ChevronRight,
  Loader,
  Users,
  Building2,
  Settings,
  LogOut,
} from 'lucide-react';

/* ============================================================================
   Type Definitions
   ============================================================================ */

interface CommandItem {
  id: string;
  label: string;
  category: 'students' | 'classrooms' | 'schedules' | 'actions';
  icon: React.ReactNode;
  description?: string;
  action?: () => void | Promise<void>;
  href?: string;
}

interface CommandGroup {
  category: 'students' | 'classrooms' | 'schedules' | 'actions';
  label: string;
  items: CommandItem[];
}

/* ============================================================================
   Mock Data
   ============================================================================ */

const generateCommandItems = (): CommandItem[] => [
  // Students
  {
    id: 'student-aria',
    label: 'Aria Patel',
    category: 'students',
    icon: <User className="w-4 h-4" />,
    description: 'Grade 11 • Top Performer',
    href: '/dashboard/student-pathways/aria-patel',
  },
  {
    id: 'student-marcus',
    label: 'Marcus Chen',
    category: 'students',
    icon: <User className="w-4 h-4" />,
    description: 'Grade 11 • Honor Student',
    href: '/dashboard/student-pathways/marcus-chen',
  },
  {
    id: 'student-sophie',
    label: 'Sophie Weber',
    category: 'students',
    icon: <User className="w-4 h-4" />,
    description: 'Grade 10 • Excellent Progress',
    href: '/dashboard/student-pathways/sophie-weber',
  },

  // Classrooms
  {
    id: 'room-a101',
    label: 'Room A101',
    category: 'classrooms',
    icon: <Building2 className="w-4 h-4" />,
    description: 'Main Physics Lab • 30 seats',
    href: '/dashboard/command-center?room=A101',
  },
  {
    id: 'room-b202',
    label: 'Room B202',
    category: 'classrooms',
    icon: <Building2 className="w-4 h-4" />,
    description: 'Math Department • 35 seats',
    href: '/dashboard/command-center?room=B202',
  },
  {
    id: 'room-c301',
    label: 'Room C301',
    category: 'classrooms',
    icon: <Building2 className="w-4 h-4" />,
    description: 'Chemistry Lab • 25 seats',
    href: '/dashboard/command-center?room=C301',
  },

  // Schedules
  {
    id: 'schedule-today',
    label: 'Today\'s Schedule',
    category: 'schedules',
    icon: <Clock className="w-4 h-4" />,
    description: 'View current day timetable',
    href: '/dashboard?view=today',
  },
  {
    id: 'schedule-week',
    label: 'Weekly View',
    category: 'schedules',
    icon: <Clock className="w-4 h-4" />,
    description: 'Full week scheduling matrix',
    href: '/dashboard?view=week',
  },

  // System Actions
  {
    id: 'action-optimize',
    label: '/optimize',
    category: 'actions',
    icon: <Zap className="w-4 h-4" />,
    description: 'Run Constraint Solver engine',
  },
  {
    id: 'action-resolve-conflicts',
    label: '/resolve-conflicts',
    category: 'actions',
    icon: <Zap className="w-4 h-4" />,
    description: 'Auto-resolve scheduling conflicts',
  },
  {
    id: 'action-generate-report',
    label: '/generate-report',
    category: 'actions',
    icon: <Zap className="w-4 h-4" />,
    description: 'Generate performance analytics',
  },
  {
    id: 'action-settings',
    label: 'Settings',
    category: 'actions',
    icon: <Settings className="w-4 h-4" />,
    description: 'System preferences',
    href: '/dashboard/settings',
  },
];

/* ============================================================================
   Command Item Component
   ============================================================================ */

interface CommandItemComponentProps {
  item: CommandItem;
  isHighlighted?: boolean;
  onSelect: (item: CommandItem) => void;
}

const CommandItemComponent: React.FC<CommandItemComponentProps> = ({
  item,
  isHighlighted = false,
  onSelect,
}) => {
  return (
    <motion.button
      onClick={() => onSelect(item)}
      className={`w-full flex items-center justify-between gap-3 px-4 py-3 rounded-lg transition-all duration-200 text-left ${
        isHighlighted
          ? 'bg-primary/20 text-white'
          : 'text-muted-foreground hover:bg-primary/10'
      }`}
      whileHover={{ x: 4 }}
      whileTap={{ scale: 0.98 }}
      type="button"
    >
      {/* Left Content */}
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <div
          className={`${
            isHighlighted ? 'text-primary' : 'text-muted-foreground'
          } flex-shrink-0`}
        >
          {item.icon}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-white truncate">
            {item.label}
          </p>
          {item.description && (
            <p className="text-xs text-muted-foreground truncate mt-0.5">
              {item.description}
            </p>
          )}
        </div>
      </div>

      {/* Right Icon */}
      {isHighlighted && (
        <motion.div
          initial={{ opacity: 0, x: -4 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex-shrink-0"
        >
          <ChevronRight className="w-4 h-4 text-primary" />
        </motion.div>
      )}
    </motion.button>
  );
};

/* ============================================================================
   AI Action Loader Component
   ============================================================================ */

interface AIActionLoaderProps {
  action: string;
  onComplete: () => void;
}

const AIActionLoader: React.FC<AIActionLoaderProps> = ({
  action,
  onComplete,
}) => {
  const [state, setState] = useState<'loading' | 'success'>('loading');

  useEffect(() => {
    // Simulate backend processing
    const timer = setTimeout(() => {
      setState('success');
      setTimeout(onComplete, 1200);
    }, 2400);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <motion.div
      className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <motion.div
        className="gemini-blur-card px-8 py-6 max-w-md text-center overflow-y-auto max-h-[90vh]"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
      >
        {state === 'loading' ? (
          <>
            {/* Rotating Loader */}
            <motion.div
              className="w-12 h-12 mx-auto mb-4 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0"
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, linear: true }}
            >
              <Zap className="w-6 h-6 text-primary" />
            </motion.div>

            {/* Loading Text */}
            <p className="text-sm font-medium text-white mb-2">
              Processing: {action}
            </p>
            <p className="text-xs text-muted-foreground">
              Running Constraint Solver engine...
            </p>

            {/* Progress Bar */}
            <div className="mt-4 h-1 rounded-full bg-border overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary to-secondary"
                animate={{ width: ['0%', '85%', '100%'] }}
                transition={{ duration: 2.4, ease: 'easeInOut' }}
              />
            </div>
          </>
        ) : (
          <>
            {/* Success Checkmark */}
            <motion.div
              className="w-12 h-12 mx-auto mb-4 rounded-lg bg-emerald-500/20 flex items-center justify-center flex-shrink-0"
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            >
              <motion.svg
                className="w-6 h-6 text-emerald-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 0.6, ease: 'easeInOut' }}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={3}
                  d="M5 13l4 4L19 7"
                />
              </motion.svg>
            </motion.div>

            {/* Success Text */}
            <p className="text-sm font-medium text-emerald-400">
              Operation Complete
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              Optimization applied successfully
            </p>
          </>
        )}
      </motion.div>
    </motion.div>
  );
};

/* ============================================================================
   OmniSearch Component
   ============================================================================ */

export const OmniSearch: React.FC = () => {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [highlightedIndex, setHighlightedIndex] = useState(0);
  const [executingAction, setExecutingAction] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const allItems = useMemo(() => generateCommandItems(), []);

  // Filter and group items
  const filteredGroups = useMemo(() => {
    const query = searchQuery.toLowerCase().trim();

    const filtered = query
      ? allItems.filter(
          (item) =>
            item.label.toLowerCase().includes(query) ||
            item.description?.toLowerCase().includes(query)
        )
      : allItems;

    const grouped: Record<string, CommandGroup> = {
      students: { category: 'students', label: 'Students', items: [] },
      classrooms: {
        category: 'classrooms',
        label: 'Classrooms',
        items: [],
      },
      schedules: { category: 'schedules', label: 'Schedules', items: [] },
      actions: { category: 'actions', label: 'System Actions', items: [] },
    };

    filtered.forEach((item) => {
      grouped[item.category].items.push(item);
    });

    return Object.values(grouped).filter((g) => g.items.length > 0);
  }, [searchQuery, allItems]);

  const allFilteredItems = useMemo(
    () => filteredGroups.flatMap((g) => g.items),
    [filteredGroups]
  );

  // Keyboard handlers
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+K or Ctrl+K to open
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
        setSearchQuery('');
        setHighlightedIndex(0);
      }

      // Only handle if open
      if (!isOpen) return;

      switch (e.key) {
        case 'Escape':
          setIsOpen(false);
          break;
        case 'ArrowDown':
          e.preventDefault();
          setHighlightedIndex((prev) =>
            prev < allFilteredItems.length - 1 ? prev + 1 : prev
          );
          break;
        case 'ArrowUp':
          e.preventDefault();
          setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : prev));
          break;
        case 'Enter':
          e.preventDefault();
          if (allFilteredItems[highlightedIndex]) {
            handleSelectItem(allFilteredItems[highlightedIndex]);
          }
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, allFilteredItems, highlightedIndex]);

  const handleSelectItem = useCallback(
    async (item: CommandItem) => {
      // System actions
      if (item.category === 'actions') {
        if (item.id.startsWith('action-')) {
          setExecutingAction(item.label);
          setIsProcessing(true);
          setIsOpen(false);

          // Simulate async processing
          await new Promise((resolve) => setTimeout(resolve, 2400));

          setIsProcessing(false);
          setExecutingAction(null);
          return;
        }
      }

      // Navigation
      if (item.href) {
        setIsOpen(false);
        router.push(item.href);
        return;
      }

      // Custom actions
      if (item.action) {
        await item.action();
      }
    },
    [router]
  );

  return (
    <>
      {/* Keyboard Hint - Fixed Bottom Right */}
      <motion.button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-40 flex items-center gap-2 px-3 py-2 rounded-lg bg-background border border-border hover:border-primary/50 transition-colors"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        type="button"
      >
        <Search className="w-4 h-4 text-muted-foreground" />
        <span className="text-xs font-medium text-muted-foreground font-mono">
          ⌘K
        </span>
      </motion.button>

      {/* Command Modal */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              className="fixed inset-0 bg-black/50 z-40 backdrop-blur-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
            />

            {/* Command Palette */}
            <motion.div
              className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-2xl overflow-hidden"
              initial={{ opacity: 0, scale: 0.95, y: -20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -20 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            >
              <div className="gemini-blur-card overflow-hidden flex flex-col max-h-[90vh]">
                {/* Search Input */}
                <div className="px-6 py-4 border-b border-border/50 flex-shrink-0">
                  <div className="relative flex items-center">
                    <Search className="absolute left-0 w-5 h-5 text-muted-foreground pointer-events-none" />
                    <input
                      autoFocus
                      type="text"
                      value={searchQuery}
                      onChange={(e) => {
                        setSearchQuery(e.target.value);
                        setHighlightedIndex(0);
                      }}
                      placeholder="Search students, rooms, schedules, actions..."
                      className="w-full bg-transparent pl-8 pr-4 py-2 text-white placeholder-muted-foreground focus:outline-none text-sm"
                    />

                    {/* Pulsing Cursor Indicator */}
                    <motion.div
                      className="absolute right-0 w-0.5 h-5 bg-primary rounded-full"
                      animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                    />
                  </div>
                </div>

                {/* Results List */}
                <div className="overflow-y-auto flex-1">
                  {allFilteredItems.length === 0 ? (
                    <motion.div
                      className="px-6 py-12 text-center"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      <Search className="w-8 h-8 text-muted-foreground/30 mx-auto mb-3" />
                      <p className="text-sm text-muted-foreground">
                        No results found for "{searchQuery}"
                      </p>
                    </motion.div>
                  ) : (
                    <motion.div className="px-4 py-4 space-y-4">
                      <AnimatePresence mode="wait">
                        {filteredGroups.map((group, groupIndex) => (
                          <motion.div
                            key={group.category}
                            initial={{ opacity: 0, y: -8 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -8 }}
                            transition={{ delay: groupIndex * 0.05 }}
                          >
                            {/* Group Header */}
                            <div className="px-2 mb-2">
                              <p className="text-xs font-semibold text-primary tracking-widest uppercase font-mono">
                                {group.label}
                              </p>
                            </div>

                            {/* Group Items */}
                            <div className="space-y-1">
                              {group.items.map((item, itemIndex) => {
                                const globalIndex = allFilteredItems.indexOf(
                                  item
                                );
                                return (
                                  <CommandItemComponent
                                    key={item.id}
                                    item={item}
                                    isHighlighted={
                                      globalIndex === highlightedIndex
                                    }
                                    onSelect={handleSelectItem}
                                  />
                                );
                              })}
                            </div>
                          </motion.div>
                        ))}
                      </AnimatePresence>
                    </motion.div>
                  )}
                </div>

                {/* Footer Hints */}
                <motion.div
                  className="px-6 py-3 border-t border-border/50 flex items-center justify-between text-xs text-muted-foreground flex-shrink-0"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <div className="flex items-center gap-4">
                    <span>
                      <span className="inline-block px-1.5 py-0.5 rounded bg-border text-white font-mono text-xs mr-1">
                        ↑↓
                      </span>
                      Navigate
                    </span>
                    <span>
                      <span className="inline-block px-1.5 py-0.5 rounded bg-border text-white font-mono text-xs mr-1">
                        ⏎
                      </span>
                      Select
                    </span>
                  </div>
                  <span>
                    <span className="inline-block px-1.5 py-0.5 rounded bg-border text-white font-mono text-xs mr-1">
                      ESC
                    </span>
                    Close
                  </span>
                </motion.div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* AI Action Loader */}
      <AnimatePresence>
        {isProcessing && executingAction && (
          <AIActionLoader
            action={executingAction}
            onComplete={() => {
              setIsProcessing(false);
              setExecutingAction(null);
            }}
          />
        )}
      </AnimatePresence>
    </>
  );
};

export default OmniSearch;
