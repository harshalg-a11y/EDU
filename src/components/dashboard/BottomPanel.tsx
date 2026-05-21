'use client';

import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MapPin,
  Radio,
  Trophy,
  TrendingUp,
  Activity,
} from 'lucide-react';

/* ============================================================================
   Type Definitions
   ============================================================================ */

interface LeaderboardEntry {
  rank: 1 | 2 | 3;
  name: string;
  percentage: number;
  avatar: string;
  grade: string;
}

interface AssetNode {
  id: string;
  label: string;
  type: 'vehicle' | 'room' | 'equipment';
  x: number;
  y: number;
  status: 'active' | 'idle' | 'offline';
  connectivity: number;
  coordinates: { lat: string; lon: string };
}

/* ============================================================================
   Mock Data
   ============================================================================ */

const leaderboardData: LeaderboardEntry[] = [
  {
    rank: 1,
    name: 'Aria Patel',
    percentage: 99.88,
    avatar: 'AP',
    grade: 'Grade 11',
  },
  {
    rank: 2,
    name: 'Marcus Chen',
    percentage: 98.45,
    avatar: 'MC',
    grade: 'Grade 11',
  },
  {
    rank: 3,
    name: 'Sophie Weber',
    percentage: 97.12,
    avatar: 'SW',
    grade: 'Grade 10',
  },
];

const assetNodes: AssetNode[] = [
  {
    id: '1',
    label: 'Vehicle ID: 8598',
    type: 'vehicle',
    x: 35,
    y: 45,
    status: 'active',
    connectivity: 98,
    coordinates: { lat: '40.7128°N', lon: '74.0060°W' },
  },
  {
    id: '2',
    label: 'Room Tracking: 1/11 pm',
    type: 'room',
    x: 65,
    y: 25,
    status: 'active',
    connectivity: 95,
    coordinates: { lat: '40.7150°N', lon: '74.0090°W' },
  },
  {
    id: '3',
    label: 'Equipment: Lab-02',
    type: 'equipment',
    x: 55,
    y: 70,
    status: 'active',
    connectivity: 92,
    coordinates: { lat: '40.7100°N', lon: '74.0030°W' },
  },
  {
    id: '4',
    label: 'Vehicle ID: 7243',
    type: 'vehicle',
    x: 25,
    y: 60,
    status: 'idle',
    connectivity: 87,
    coordinates: { lat: '40.7110°N', lon: '74.0020°W' },
  },
  {
    id: '5',
    label: 'Room Tracking: 2/15 pm',
    type: 'room',
    x: 75,
    y: 55,
    status: 'active',
    connectivity: 94,
    coordinates: { lat: '40.7160°N', lon: '74.0100°W' },
  },
];

/* ============================================================================
   Leaderboard Card Component
   ============================================================================ */

interface LeaderboardCardProps {
  entry: LeaderboardEntry;
  isHighlight?: boolean;
}

const LeaderboardCard: React.FC<LeaderboardCardProps> = ({
  entry,
  isHighlight = false,
}) => {
  const heightClass =
    entry.rank === 1 ? 'h-48' : entry.rank === 2 ? 'h-40' : 'h-36';
  const rankColors = {
    1: 'from-primary to-secondary',
    2: 'from-primary/60 to-secondary/60',
    3: 'from-primary/40 to-secondary/40',
  };

  const rankBadgeColors = {
    1: 'bg-primary text-white shadow-lg shadow-primary/30',
    2: 'bg-primary/70 text-white',
    3: 'bg-primary/50 text-white',
  };

  return (
    <motion.div
      className={`relative ${heightClass} rounded-2xl overflow-hidden group transition-all duration-300 flex-shrink-0`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: entry.rank * 0.1 }}
      whileHover={isHighlight ? { scale: 1.02 } : {}}
    >
      {/* Background Gradient */}
      <div
        className={`absolute inset-0 bg-gradient-to-br ${rankColors[entry.rank]} opacity-20`}
      />

      {/* Gemini Blur Background */}
      <div className="absolute inset-0 gemini-blur-card border-2 border-transparent" />

      {/* Glow Ring for 1st Place */}
      {isHighlight && (
        <div className="absolute inset-0 rounded-2xl border-2 border-primary/50 shadow-[inset_0_0_24px_rgba(101,84,192,0.15)]" />
      )}

      {/* Content */}
      <div className="relative h-full flex flex-col items-center justify-between p-4">
        {/* Avatar */}
        <motion.div
          className={`w-12 h-12 rounded-full bg-gradient-to-br ${rankColors[entry.rank]} flex items-center justify-center text-sm font-bold text-white flex-shrink-0`}
          animate={isHighlight ? { scale: [1, 1.05, 1] } : {}}
          transition={{ duration: 3, repeat: Infinity }}
        >
          {entry.avatar}
        </motion.div>

        {/* Name */}
        <div className="text-center">
          <p className="text-xs font-medium text-muted-foreground tracking-tight">
            {entry.grade}
          </p>
          <p className="text-sm font-bold text-white mt-1 tracking-tight">
            {entry.name}
          </p>
        </div>

        {/* Performance Percentage - Razor Sharp */}
        <motion.div
          className="text-center"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2 + entry.rank * 0.1, duration: 0.4 }}
        >
          <p className="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary tracking-tighter font-mono">
            {entry.percentage.toFixed(2)}%
          </p>
        </motion.div>

        {/* Ranking Badge */}
        <motion.div
          className={`px-4 py-1.5 rounded-full text-xs font-bold tracking-widest uppercase ${rankBadgeColors[entry.rank]}`}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 + entry.rank * 0.1, duration: 0.3 }}
        >
          {entry.rank}
          {entry.rank === 1 ? 'st' : entry.rank === 2 ? 'nd' : 'rd'} Place
        </motion.div>
      </div>

      {/* Subtle Shine Effect */}
      <motion.div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            'linear-gradient(135deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%)',
          opacity: 0,
        }}
        animate={{ opacity: [0, 0.5, 0] }}
        transition={{ duration: 3, repeat: Infinity }}
      />
    </motion.div>
  );
};

/* ============================================================================
   Asset Tracker Node Component
   ============================================================================ */

interface AssetNodeComponentProps {
  node: AssetNode;
}

const AssetNodeComponent: React.FC<AssetNodeComponentProps> = ({ node }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  const statusColors = {
    active: 'bg-emerald-500',
    idle: 'bg-amber-500',
    offline: 'bg-rose-500',
  };

  const typeIcons = {
    vehicle: '🚗',
    room: '📍',
    equipment: '⚙️',
  };

  return (
    <div
      className="absolute cursor-pointer"
      style={{ left: `${node.x}%`, top: `${node.y}%` }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      {/* Node Badge */}
      <motion.div
        className={`relative flex items-center justify-center w-8 h-8 rounded-lg border border-border ${statusColors[node.status]} -translate-x-1/2 -translate-y-1/2 flex-shrink-0`}
        animate={{
          scale: [1, 1.15, 1],
          boxShadow: [
            `0 0 0 0 rgba(${node.status === 'active' ? '34,197,94' : node.status === 'idle' ? '217,119,6' : '244,63,94'}, 0.3)`,
            `0 0 0 8px rgba(${node.status === 'active' ? '34,197,94' : node.status === 'idle' ? '217,119,6' : '244,63,94'}, 0)`,
          ],
        }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <span className="text-xs font-bold text-white">{typeIcons[node.type]}</span>
      </motion.div>

      {/* Tooltip */}
      <AnimatePresence>
        {showTooltip && (
          <motion.div
            className="absolute left-full ml-3 -translate-y-1/2 top-1/2 z-50 pointer-events-none"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -8 }}
            transition={{ duration: 0.2 }}
          >
            <div className="gemini-blur-card p-3 min-w-max max-w-xs">
              {/* Label */}
              <p className="text-xs font-semibold text-white mb-2 truncate">
                {node.label}
              </p>

              {/* Coordinates */}
              <div className="flex items-center gap-2 mb-2 text-xs text-muted-foreground min-w-0">
                <MapPin className="w-3 h-3 flex-shrink-0" />
                <span className="truncate font-mono">
                  {node.coordinates.lat}, {node.coordinates.lon}
                </span>
              </div>

              {/* Connectivity */}
              <div className="flex items-center gap-2">
                <Radio className="w-3 h-3 text-primary flex-shrink-0" />
                <div className="flex-1">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="text-xs text-muted-foreground">Signal</span>
                    <span className="text-xs font-bold text-primary font-mono flex-shrink-0">
                      {node.connectivity}%
                    </span>
                  </div>
                  <div className="w-24 h-1 rounded-full bg-border overflow-hidden">
                    <motion.div
                      className="h-full bg-gradient-to-r from-primary to-secondary"
                      initial={{ width: 0 }}
                      animate={{ width: `${node.connectivity}%` }}
                      transition={{ duration: 0.6 }}
                    />
                  </div>
                </div>
              </div>

              {/* Status Badge */}
              <div className="mt-3 pt-3 border-t border-border/50 flex items-center gap-2">
                <div
                  className={`w-2 h-2 rounded-full ${statusColors[node.status]} flex-shrink-0`}
                />
                <span className="text-xs font-medium text-muted-foreground capitalize">
                  {node.status}
                </span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

/* ============================================================================
   Spatial Asset Fleet Radar Component
   ============================================================================ */

const SpatialAssetRadar: React.FC = () => {
  const activeCount = useMemo(
    () => assetNodes.filter((n) => n.status === 'active').length,
    []
  );

  return (
    <div className="relative h-full w-full rounded-2xl overflow-hidden bg-background border border-border">
      {/* Grid Lines Background */}
      <svg
        className="absolute inset-0 w-full h-full pointer-events-none"
        style={{ opacity: 0.15 }}
      >
        {/* Vertical grid lines */}
        {Array.from({ length: 11 }).map((_, i) => (
          <line
            key={`v-${i}`}
            x1={`${i * 10}%`}
            y1="0%"
            x2={`${i * 10}%`}
            y2="100%"
            stroke="var(--primary)"
            strokeWidth="1"
            vectorEffect="non-scaling-stroke"
          />
        ))}

        {/* Horizontal grid lines */}
        {Array.from({ length: 11 }).map((_, i) => (
          <line
            key={`h-${i}`}
            x1="0%"
            y1={`${i * 10}%`}
            x2="100%"
            y2={`${i * 10}%`}
            stroke="var(--primary)"
            strokeWidth="1"
            vectorEffect="non-scaling-stroke"
          />
        ))}

        {/* Concentric circles for radar effect */}
        {Array.from({ length: 5 }).map((_, i) => (
          <circle
            key={`circle-${i}`}
            cx="50%"
            cy="50%"
            r={`${(i + 1) * 10}%`}
            fill="none"
            stroke="var(--primary)"
            strokeWidth="1"
            vectorEffect="non-scaling-stroke"
            opacity="0.1"
          />
        ))}
      </svg>

      {/* Asset Nodes */}
      <div className="absolute inset-0">
        {assetNodes.map((node) => (
          <motion.div
            key={node.id}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.1 * parseInt(node.id) }}
          >
            <AssetNodeComponent node={node} />
          </motion.div>
        ))}
      </div>

      {/* Header Stats */}
      <div className="absolute top-4 left-4 right-4 z-10 flex items-center justify-between flex-shrink-0">
        {/* Title */}
        <div>
          <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
            Live Fleet
          </p>
          <p className="text-lg font-bold text-white mt-1">Asset Tracker</p>
        </div>

        {/* Active Count Badge */}
        <motion.div
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex-shrink-0"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <Activity className="w-4 h-4 text-emerald-400 flex-shrink-0" />
          <span className="text-xs font-bold text-emerald-400 font-mono">
            {activeCount}/{assetNodes.length} Active
          </span>
        </motion.div>
      </div>

      {/* Corner Labels for Coordinates */}
      <div className="absolute bottom-4 left-4 text-xs text-muted-foreground/50 font-mono flex-shrink-0">
        (40.71°N, 74.00°W)
      </div>
      <div className="absolute bottom-4 right-4 text-xs text-muted-foreground/50 font-mono flex-shrink-0">
        (40.72°N, 74.01°W)
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-4 z-10 flex-shrink-0 flex-wrap justify-center">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <div className="w-2 h-2 rounded-full bg-emerald-500 flex-shrink-0" />
          <span>Active</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <div className="w-2 h-2 rounded-full bg-amber-500 flex-shrink-0" />
          <span>Idle</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <div className="w-2 h-2 rounded-full bg-rose-500 flex-shrink-0" />
          <span>Offline</span>
        </div>
      </div>
    </div>
  );
};

/* ============================================================================
   Main BottomPanel Component
   ============================================================================ */

export const BottomPanel: React.FC = () => {
  const firstPlace = leaderboardData.find((e) => e.rank === 1)!;
  const secondPlace = leaderboardData.find((e) => e.rank === 2)!;
  const thirdPlace = leaderboardData.find((e) => e.rank === 3)!;

  return (
    <div className="h-full w-full flex gap-6 overflow-hidden">
      {/* Left Split-Pane: Academic Achievement Leaderboard */}
      <div className="flex-1 min-w-0 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="mb-4 flex-shrink-0">
          <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
            Performance
          </p>
          <h2 className="text-2xl font-bold text-white mt-2 tracking-tight">
            Academic Leaderboard
          </h2>
          <p className="text-xs text-muted-foreground mt-1">
            Top performing students by achievement score
          </p>
        </div>

        {/* Podium Layout */}
        <div className="flex-1 flex items-end justify-center gap-4 min-h-0 overflow-hidden">
          {/* 2nd Place (Left) */}
          <div className="flex-1 flex items-end justify-end min-h-0 overflow-hidden">
            <motion.div
              className="w-full max-w-xs"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1, duration: 0.4 }}
            >
              <LeaderboardCard entry={secondPlace} />
            </motion.div>
          </div>

          {/* 1st Place (Center) - Elevated */}
          <div className="flex-1 flex items-end justify-center mb-4 min-h-0 overflow-hidden">
            <motion.div
              className="w-full max-w-xs"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0, duration: 0.4 }}
            >
              <LeaderboardCard entry={firstPlace} isHighlight={true} />
            </motion.div>
          </div>

          {/* 3rd Place (Right) */}
          <div className="flex-1 flex items-end justify-start min-h-0 overflow-hidden">
            <motion.div
              className="w-full max-w-xs"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2, duration: 0.4 }}
            >
              <LeaderboardCard entry={thirdPlace} />
            </motion.div>
          </div>
        </div>

        {/* Footer Stats */}
        <motion.div
          className="mt-6 pt-4 border-t border-border flex items-center gap-4 flex-shrink-0"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center gap-2">
            <Trophy className="w-4 h-4 text-primary flex-shrink-0" />
            <span className="text-xs font-medium text-muted-foreground">
              Top tier average:
            </span>
            <span className="text-sm font-bold text-white font-mono">98.48%</span>
          </div>
        </motion.div>
      </div>

      {/* Divider */}
      <div className="w-px bg-border flex-shrink-0" />

      {/* Right Split-Pane: Spatial Asset Fleet Radar */}
      <div className="flex-1 min-w-0 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="mb-4 flex-shrink-0">
          <p className="text-xs font-bold text-muted-foreground tracking-widest uppercase">
            Infrastructure
          </p>
          <h2 className="text-2xl font-bold text-white mt-2 tracking-tight">
            Asset Fleet Radar
          </h2>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time geographic coordinate tracking
          </p>
        </div>

        {/* Radar Canvas */}
        <div className="flex-1 min-h-0 overflow-hidden">
          <SpatialAssetRadar />
        </div>
      </div>
    </div>
  );
};

export default BottomPanel;
