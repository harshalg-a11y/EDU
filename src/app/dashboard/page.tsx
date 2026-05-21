'use server';

import React, { Suspense } from 'react';
import { motion } from 'framer-motion';
import MetricCards from '@/components/dashboard/MetricCards';
import { MiddlePanel } from '@/components/dashboard/MiddlePanel';
import { BottomPanel } from '@/components/dashboard/BottomPanel';
import { OmniSearch } from '@/components/dashboard/OmniSearch';

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
   Server Data Fetchers
   ============================================================================ */

/**
 * Fetch high-fidelity tracking data from Prisma database
 * This would be replaced with actual Prisma queries
 */
async function fetchDashboardMetrics(tenantId: string) {
  // Simulate database fetch delay
  await new Promise((resolve) => setTimeout(resolve, 400));

  return {
    totalStudents: 2847,
    averageGPA: 3.72,
    completionRate: 94.2,
    schedulingEfficiency: 87.6,
    activeSchedules: 156,
    pendingResolutions: 8,
    systemUptime: 99.98,
    dataIntegrity: 100,
  };
}

/**
 * Fetch middle panel scheduling data
 */
async function fetchSchedulingData(tenantId: string) {
  await new Promise((resolve) => setTimeout(resolve, 500));

  return {
    gridCells: Array.from({ length: 36 }).map((_, i) => ({
      id: `cell-${i}`,
      utilization: Math.random() * 100,
      status: ['optimal', 'warning', 'critical'][
        Math.floor(Math.random() * 3)
      ],
    })),
    conflicts: Array.from({ length: 4 }).map((_, i) => ({
      id: `conflict-${i}`,
      type: i < 2 ? 'critical' : 'warning',
      resolved: false,
    })),
  };
}

/**
 * Fetch leaderboard and asset data
 */
async function fetchLeaderboardData(tenantId: string) {
  await new Promise((resolve) => setTimeout(resolve, 450));

  return {
    topStudents: [
      { rank: 1, name: 'Aria Patel', percentage: 99.88, avatar: 'AP' },
      { rank: 2, name: 'Marcus Chen', percentage: 98.45, avatar: 'MC' },
      { rank: 3, name: 'Sophie Weber', percentage: 97.12, avatar: 'SW' },
    ],
    assets: Array.from({ length: 5 }).map((_, i) => ({
      id: `asset-${i}`,
      type: ['vehicle', 'room', 'equipment'][Math.floor(Math.random() * 3)],
      status: ['active', 'idle', 'offline'][Math.floor(Math.random() * 3)],
    })),
  };
}

/* ============================================================================
   Master Dashboard Page Component
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
              <MetricCardsContainer tenantId={tenantId} />
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
                <MiddlePanel />
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
                <BottomPanel />
              </div>
            </Suspense>
          </motion.section>
        </div>
      </main>
    </>
  );
}

/* ============================================================================
   Async Container Components
   ============================================================================ */

/**
 * Metric Cards Container - Fetches and renders dashboard metrics
 */
async function MetricCardsContainer({ tenantId }: { tenantId: string }) {
  const metrics = await fetchDashboardMetrics(tenantId);

  return (
    <MetricCards
      totalStudents={metrics.totalStudents}
      averageGPA={metrics.averageGPA}
      completionRate={metrics.completionRate}
      schedulingEfficiency={metrics.schedulingEfficiency}
      activeSchedules={metrics.activeSchedules}
      pendingResolutions={metrics.pendingResolutions}
      systemUptime={metrics.systemUptime}
      dataIntegrity={metrics.dataIntegrity}
    />
  );
}

/**
 * Middle Panel Container - Fetches scheduling and conflict data
 */
async function MiddlePanelContainer({ tenantId }: { tenantId: string }) {
  const data = await fetchSchedulingData(tenantId);

  return <MiddlePanel />;
}

/**
 * Bottom Panel Container - Fetches leaderboard and asset data
 */
async function BottomPanelContainer({ tenantId }: { tenantId: string }) {
  const data = await fetchLeaderboardData(tenantId);

  return <BottomPanel />;
}

/* ============================================================================
   Metadata Export
   ============================================================================ */

export const metadata = {
  title: 'Dashboard - EduSphere',
  description:
    'Academic scheduling and student achievement tracking dashboard',
};
