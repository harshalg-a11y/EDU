'use server';

import React, { Suspense } from 'react';
import { motion } from 'framer-motion';
import MetricCards from '@/components/dashboard/MetricCards';
import { MiddlePanel } from '@/components/dashboard/MiddlePanel';
import { BottomPanel } from '@/components/dashboard/BottomPanel';
import { OmniSearch } from '@/components/dashboard/OmniSearch';
import type {
  MetricCardData,
  SchedulingConflict,
  StudentRank,
  AssetNode,
} from '@/types';

/* ============================================================================
   Hardcoded Mock Data Pools - Structured to Type Schema
   ============================================================================ */

/**
 * Metric Cards Data - Dashboard KPI metrics
 * Matches MetricCardData[] interface exactly
 */
const MOCK_METRIC_CARDS: MetricCardData[] = [
  {
    id: 'metric-schools',
    title: 'Schools',
    value: '145',
    increment: '+12',
    variant: 'coral',
  },
  {
    id: 'metric-teachers',
    title: 'Teachers',
    value: '220',
    increment: '+8',
    variant: 'violet',
  },
  {
    id: 'metric-students',
    title: 'Students',
    value: '3400',
    increment: '+89',
    variant: 'amber',
  },
  {
    id: 'metric-fleet',
    title: 'Fleet',
    value: '45',
    increment: '+2',
    variant: 'emerald',
  },
];

/**
 * Scheduling Conflicts Data - Active conflict feed
 * Matches SchedulingConflict[] interface exactly
 */
const MOCK_SCHEDULING_CONFLICTS: SchedulingConflict[] = [
  {
    id: 'conflict-001',
    type: 'DOUBLE_BOOKING',
    severity: 'WARNING',
    message: 'Warning: Room 403 double-booked',
    room: '403',
    timeAgo: '2 hours ago',
    resolved: false,
  },
  {
    id: 'conflict-002',
    type: 'DOUBLE_BOOKING',
    severity: 'WARNING',
    message: 'Warning: Room 403 double-booked',
    room: '401',
    timeAgo: '1 hour ago',
    resolved: false,
  },
  {
    id: 'conflict-003',
    type: 'DOUBLE_BOOKING',
    severity: 'WARNING',
    message: 'Warning: Room 403 double-booked',
    room: '403',
    timeAgo: '45 minutes ago',
    resolved: false,
  },
  {
    id: 'conflict-004',
    type: 'DOUBLE_BOOKING',
    severity: 'WARNING',
    message: 'Warning: Room 403 double-booked',
    room: '401',
    timeAgo: '30 minutes ago',
    resolved: false,
  },
];

/**
 * Student Rankings Data - Top student leaderboard
 * Matches StudentRank[] interface exactly
 */
const MOCK_STUDENT_RANKINGS: StudentRank[] = [
  {
    id: 'student-001',
    name: 'Rayan Hassan',
    avatarUrl: 'RH',
    gradePercentage: 99.88,
    position: 1,
    colorVariant: 'emerald',
  },
  {
    id: 'student-002',
    name: 'Reny Boyette',
    avatarUrl: 'RB',
    gradePercentage: 98.17,
    position: 2,
    colorVariant: 'violet',
  },
  {
    id: 'student-003',
    name: 'Aarav Sharma',
    avatarUrl: 'AS',
    gradePercentage: 96.12,
    position: 3,
    colorVariant: 'amber',
  },
];

/**
 * Asset Nodes Data - Vehicle and room tracking vectors
 * Matches AssetNode[] interface exactly
 */
const MOCK_ASSET_NODES: AssetNode[] = [
  {
    id: 'asset-001',
    label: 'Vehicle ID: 8598',
    timestamp: '2026-05-21T17:52:00Z',
    coordinates: {
      x: 45.2,
      y: 62.8,
    },
    metadata: JSON.stringify({
      type: 'vehicle',
      status: 'active',
      location: 'Room Tracks',
      time: '1/11 pm',
    }),
  },
  {
    id: 'asset-002',
    label: 'Vehicle 403',
    timestamp: '2026-05-21T17:51:45Z',
    coordinates: {
      x: 58.4,
      y: 48.1,
    },
    metadata: JSON.stringify({
      type: 'vehicle',
      status: 'active',
      location: 'Room Tracks',
      time: '3:31 pm',
    }),
  },
];

/* ============================================================================
   Skeletal Loading Components
   ============================================================================ */

const MetricCardsSkeleton = () => (
  <motion.div
    className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.3 }}
  >
    {Array.from({ length: 4 }).map((_, i) => (
      <motion.div
        key={i}
        className="h-32 rounded-xl bg-gradient-to-br from-border/50 to-border/30 animate-pulse"
        initial={{ opacity: 0.5 }}
        animate={{ opacity: [0.5, 0.8, 0.5] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
    ))}
  </motion.div>
);

const MiddlePanelSkeleton = () => (
  <motion.div
    className="flex gap-6 h-full"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.3 }}
  >
    {/* Left Column Skeleton */}
    <div className="flex-1">
      <div className="h-8 w-48 bg-gradient-to-r from-border/50 to-border/30 rounded animate-pulse mb-4" />
      <div className="space-y-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="flex gap-2">
            {Array.from({ length: 6 }).map((_, j) => (
              <div
                key={j}
                className="w-12 h-12 bg-gradient-to-br from-border/50 to-border/30 rounded animate-pulse"
              />
            ))}
          </div>
        ))}
      </div>
    </div>

    {/* Divider */}
    <div className="w-px bg-border" />

    {/* Right Column Skeleton */}
    <div className="w-96">
      <div className="h-8 w-48 bg-gradient-to-r from-border/50 to-border/30 rounded animate-pulse mb-4" />
      <div className="space-y-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="h-20 bg-gradient-to-r from-border/50 to-border/30 rounded animate-pulse"
          />
        ))}
      </div>
    </div>
  </motion.div>
);

const BottomPanelSkeleton = () => (
  <motion.div
    className="flex gap-6 h-full"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.3 }}
  >
    {/* Left Column Skeleton */}
    <div className="flex-1 space-y-4">
      <div className="h-8 w-40 bg-gradient-to-r from-border/50 to-border/30 rounded animate-pulse" />
      <div className="flex justify-center gap-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <div
            key={i}
            className="w-24 h-40 bg-gradient-to-br from-border/50 to-border/30 rounded animate-pulse"
          />
        ))}
      </div>
    </div>

    {/* Divider */}
    <div className="w-px bg-border" />

    {/* Right Column Skeleton */}
    <div className="flex-1">
      <div className="h-8 w-40 bg-gradient-to-r from-border/50 to-border/30 rounded animate-pulse mb-4" />
      <div className="w-full h-full bg-gradient-to-br from-border/50 to-border/30 rounded animate-pulse" />
    </div>
  </motion.div>
);

/* ============================================================================
   Metric Cards Container - Type Safe
   ============================================================================ */

interface MetricCardsContainerProps {
  metrics: MetricCardData[];
}

async function MetricCardsContainer({
  metrics,
}: MetricCardsContainerProps) {
  return <MetricCards data={metrics} />;
}

/* ============================================================================
   Middle Panel Container - Type Safe
   ============================================================================ */

interface MiddlePanelContainerProps {
  conflicts: SchedulingConflict[];
}

async function MiddlePanelContainer({
  conflicts,
}: MiddlePanelContainerProps) {
  return <MiddlePanel conflicts={conflicts} />;
}

/* ============================================================================
   Bottom Panel Container - Type Safe
   ============================================================================ */

interface BottomPanelContainerProps {
  rankings: StudentRank[];
  assetNodes: AssetNode[];
}

async function BottomPanelContainer({
  rankings,
  assetNodes,
}: BottomPanelContainerProps) {
  return <BottomPanel rankings={rankings} assetNodes={assetNodes} />;
}

/* ============================================================================
   Main Dashboard Page Component
   ============================================================================ */

interface DashboardPageProps {
  searchParams: {
    tenantId?: string;
  };
}

export default async function DashboardPage({
  searchParams,
}: DashboardPageProps) {
  const tenantId = searchParams.tenantId || 'default-tenant';

  return (
    <>
      {/* Global Command Palette */}
      <OmniSearch />

      {/* Main Dashboard Grid */}
      <main className="min-h-screen w-full bg-background">
        {/* Container with padding */}
        <div className="h-screen flex flex-col gap-6 p-6 overflow-hidden">
          {/* ========== TOP ROW: Metric Cards ========== */}
          <motion.section
            className="w-full flex-shrink-0"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0 }}
          >
            <Suspense fallback={<MetricCardsSkeleton />}>
              <MetricCardsContainer metrics={MOCK_METRIC_CARDS} />
            </Suspense>
          </motion.section>

          {/* ========== MIDDLE ROW: Scheduling Matrix & AI Conflicts ========== */}
          <motion.section
            className="flex-1 min-h-0 w-full"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
          >
            <Suspense fallback={<MiddlePanelSkeleton />}>
              <div className="h-full rounded-xl border border-border overflow-hidden bg-card/50">
                <MiddlePanelContainer conflicts={MOCK_SCHEDULING_CONFLICTS} />
              </div>
            </Suspense>
          </motion.section>

          {/* ========== BOTTOM ROW: Leaderboard & Asset Radar ========== */}
          <motion.section
            className="flex-1 min-h-0 w-full"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
          >
            <Suspense fallback={<BottomPanelSkeleton />}>
              <div className="h-full rounded-xl border border-border overflow-hidden bg-card/50">
                <BottomPanelContainer
                  rankings={MOCK_STUDENT_RANKINGS}
                  assetNodes={MOCK_ASSET_NODES}
                />
              </div>
            </Suspense>
          </motion.section>
        </div>
      </main>
    </>
  );
}

/* ============================================================================
   Metadata Export
   ============================================================================ */

export const metadata = {
  title: 'Dashboard - EduSphere',
  description:
    'Academic scheduling and student achievement tracking dashboard',
};
