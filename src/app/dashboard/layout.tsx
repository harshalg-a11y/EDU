'use client';

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Zap,
  Users,
  BookOpen,
  Globe,
  FileText,
  LogOut,
  Settings,
  Bell,
} from 'lucide-react';

/* ============================================================================
   Navigation Menu Configuration
   ============================================================================ */

interface NavItem {
  id: string;
  label: string;
  href: string;
  icon: React.ReactNode;
  section: 'main' | 'secondary';
}

const NAV_ITEMS: NavItem[] = [
  {
    id: 'dashboard',
    label: 'Dashboard',
    href: '/dashboard',
    icon: <LayoutDashboard className="w-5 h-5" />,
    section: 'main',
  },
  {
    id: 'command-center',
    label: 'Command Center',
    href: '/dashboard/command-center',
    icon: <Zap className="w-5 h-5" />,
    section: 'main',
  },
  {
    id: 'student-pathways',
    label: 'Student Pathways',
    href: '/dashboard/student-pathways',
    icon: <Users className="w-5 h-5" />,
    section: 'main',
  },
  {
    id: 'curriculum-canvas',
    label: 'Curriculum Canvas',
    href: '/dashboard/curriculum-canvas',
    icon: <BookOpen className="w-5 h-5" />,
    section: 'main',
  },
  {
    id: 'global-operations',
    label: 'Global Operations',
    href: '/dashboard/global-operations',
    icon: <Globe className="w-5 h-5" />,
    section: 'main',
  },
  {
    id: 'asset-ledger',
    label: 'Asset Ledger',
    href: '/dashboard/asset-ledger',
    icon: <FileText className="w-5 h-5" />,
    section: 'main',
  },
];

/* ============================================================================
   Sidebar Navigation Component
   ============================================================================ */

interface SidebarNavigationProps {
  pathname: string;
  activeItem: string | null;
  onItemHover: (id: string | null) => void;
}

const SidebarNavigation: React.FC<SidebarNavigationProps> = ({
  pathname,
  activeItem,
  onItemHover,
}) => {
  const mainItems = NAV_ITEMS.filter((item) => item.section === 'main');

  const isActive = (href: string) => {
    if (href === '/dashboard') {
      return pathname === '/dashboard' || pathname === '/dashboard/';
    }
    return pathname.startsWith(href);
  };

  return (
    <nav className="flex-1 space-y-1 px-3 py-6">
      {mainItems.map((item) => {
        const active = isActive(item.href);
        return (
          <Link key={item.id} href={item.href}>
            <motion.div
              className="relative h-10 flex items-center rounded-lg transition-colors duration-200 px-3 cursor-pointer group"
              onMouseEnter={() => onItemHover(item.id)}
              onMouseLeave={() => onItemHover(null)}
              whileHover={{ x: 2 }}
            >
              {/* Background pill indicator - animated behind text */}
              {active && (
                <motion.div
                  layoutId="navbar-pill"
                  className="absolute inset-0 rounded-lg"
                  style={{
                    background:
                      'linear-gradient(135deg, rgba(101, 84, 192, 0.2) 0%, rgba(101, 84, 192, 0.1) 100%)',
                    borderLeft: '3px solid var(--primary)',
                  }}
                  transition={{
                    type: 'spring',
                    stiffness: 380,
                    damping: 30,
                  }}
                />
              )}

              {/* Hover background for inactive items */}
              {!active && activeItem === item.id && (
                <motion.div
                  className="absolute inset-0 rounded-lg"
                  style={{
                    background:
                      'linear-gradient(135deg, rgba(101, 84, 192, 0.08) 0%, rgba(101, 84, 192, 0.04) 100%)',
                  }}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.2 }}
                />
              )}

              {/* Icon */}
              <motion.div
                className={`relative z-10 mr-3 transition-colors duration-200 ${
                  active
                    ? 'text-primary'
                    : 'text-muted-foreground group-hover:text-primary'
                }`}
                animate={active ? { scale: 1.05 } : { scale: 1 }}
              >
                {item.icon}
              </motion.div>

              {/* Label */}
              <span
                className={`relative z-10 text-sm font-medium transition-colors duration-200 tracking-wide ${
                  active ? 'text-white' : 'text-muted-foreground'
                }`}
              >
                {item.label}
              </span>

              {/* Right accent for active items */}
              {active && (
                <motion.div
                  className="absolute right-2 z-10"
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 0.6 }}
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                >
                  <div className="w-1 h-1 rounded-full bg-primary" />
                </motion.div>
              )}
            </motion.div>
          </Link>
        );
      })}
    </nav>
  );
};

/* ============================================================================
   User Status Capsule Component
   ============================================================================ */

interface UserStatusCapsuleProps {
  userRole?: string;
  userName?: string;
}

const UserStatusCapsule: React.FC<UserStatusCapsuleProps> = ({
  userRole = 'Academic Administrator',
  userName = 'Dr. Harrison',
}) => {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <div className="px-3 py-4 border-t border-border">
      {/* User Info Capsule */}
      <motion.div
        className="relative flex items-center gap-3 p-3 rounded-lg cursor-pointer group"
        whileHover={{ scale: 1.02 }}
        onClick={() => setShowMenu(!showMenu)}
      >
        {/* Background */}
        <motion.div
          className="absolute inset-0 rounded-lg"
          style={{
            background:
              'linear-gradient(135deg, rgba(101, 84, 192, 0.1) 0%, rgba(101, 84, 192, 0.05) 100%)',
            borderLeft: '2px solid rgba(101, 84, 192, 0.3)',
          }}
          initial={{ opacity: 0 }}
          whileHover={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
        />

        {/* Avatar */}
        <div className="relative z-10 w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center flex-shrink-0">
          <span className="text-xs font-bold text-white">
            {userName
              .split(' ')
              .map((n) => n[0])
              .join('')}
          </span>
        </div>

        {/* User Details */}
        <div className="relative z-10 flex-1 min-w-0">
          <p className="text-xs font-medium text-white truncate tracking-tight">
            {userName}
          </p>
          <p className="text-xs text-muted-foreground truncate tracking-tight">
            {userRole}
          </p>
        </div>

        {/* Status Indicator */}
        <motion.div
          className="relative z-10 w-2 h-2 rounded-full bg-success flex-shrink-0"
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </motion.div>

      {/* Dropdown Menu */}
      <AnimatePresence>
        {showMenu && (
          <motion.div
            className="mt-2 rounded-lg border border-border bg-card overflow-hidden"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
          >
            <button className="w-full flex items-center gap-2 px-3 py-2 text-xs font-medium text-muted-foreground hover:text-white hover:bg-primary/10 transition-colors">
              <Settings className="w-4 h-4" />
              Preferences
            </button>
            <button className="w-full flex items-center gap-2 px-3 py-2 text-xs font-medium text-muted-foreground hover:text-white hover:bg-primary/10 transition-colors border-t border-border">
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

/* ============================================================================
   Sidebar Component
   ============================================================================ */

interface SidebarProps {
  pathname: string;
}

const Sidebar: React.FC<SidebarProps> = ({ pathname }) => {
  const [activeItem, setActiveItem] = useState<string | null>(null);

  return (
    <motion.div
      className="fixed left-0 top-0 h-screen w-72 flex flex-col bg-background border-r border-border"
      initial={{ x: -288 }}
      animate={{ x: 0 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
    >
      {/* Logo/Brand Area */}
      <div className="px-6 py-6 border-b border-border">
        <motion.div
          className="flex items-center gap-2"
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
            <Zap className="w-4 h-4 text-white" />
          </div>
          <div className="flex flex-col">
            <p className="text-sm font-bold text-white tracking-wide">
              EduSphere
            </p>
            <p className="text-xs text-muted-foreground">Central</p>
          </div>
        </motion.div>
      </div>

      {/* Navigation */}
      <SidebarNavigation
        pathname={pathname}
        activeItem={activeItem}
        onItemHover={setActiveItem}
      />

      {/* User Status Capsule */}
      <UserStatusCapsule />
    </motion.div>
  );
};

/* ============================================================================
   Main Content Area Component
   ============================================================================ */

interface MainContentProps {
  children: React.ReactNode;
}

const MainContent: React.FC<MainContentProps> = ({ children }) => {
  return (
    <motion.div
      className="fixed left-72 top-0 right-0 bottom-0 h-screen overflow-hidden"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.1, duration: 0.3 }}
    >
      {/* Content Panel with Inward Curve */}
      <div className="h-full w-full bg-card rounded-l-[2.5rem] overflow-hidden flex flex-col border-l border-border">
        {/* Header Bar */}
        <motion.div
          className="flex items-center justify-between h-16 px-8 border-b border-border"
          initial={{ y: -64 }}
          animate={{ y: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        >
          <div className="flex-1">
            <p className="text-xs font-medium text-muted-foreground tracking-widest uppercase">
              Workspace
            </p>
          </div>

          {/* Header Actions */}
          <div className="flex items-center gap-3">
            <motion.button
              className="p-2 rounded-lg hover:bg-primary/10 transition-colors text-muted-foreground hover:text-primary"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Bell className="w-5 h-5" />
            </motion.button>
          </div>
        </motion.div>

        {/* Main Canvas Area */}
        <div className="flex-1 overflow-y-auto overflow-x-hidden">
          {/* Custom scrollbar styling inherited from globals.css */}
          <motion.div
            className="h-full w-full px-8 py-6"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.4 }}
          >
            {children}
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  );
};

/* ============================================================================
   Main Dashboard Layout Component (Server Component Wrapper)
   ============================================================================ */

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  return (
    <div className="h-screen w-screen bg-background overflow-hidden">
      {/* Sidebar Navigation */}
      <Sidebar pathname={pathname} />

      {/* Main Content Workspace */}
      <MainContent>{children}</MainContent>

      {/* Ambient Background Effects (Optional Enhancement) */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        {/* Subtle gradient accent in top-right corner */}
        <div
          className="absolute -top-48 -right-48 w-96 h-96 rounded-full opacity-5"
          style={{
            background:
              'radial-gradient(circle, var(--primary) 0%, transparent 70%)',
            filter: 'blur(40px)',
          }}
        />
      </div>
    </div>
  );
}
