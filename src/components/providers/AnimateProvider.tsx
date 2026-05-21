'use client';

import React, { ReactNode } from 'react';
import {
  motion,
  AnimatePresence,
  Variants,
  TargetAndTransition,
  VariantLabels,
} from 'framer-motion';

/* ============================================================================
   Global Transition Presets
   ============================================================================ */

/**
 * Gemini Spring Physics
 * Premium spring animation with precise weight, stiffness, and dampening
 * Used for interactive elements, card expansions, and modal appearances
 */
export const geminiSpring = {
  type: 'spring' as const,
  stiffness: 280,
  damping: 30,
  mass: 0.8,
};

/**
 * Gemini Fade Transition
 * Smooth fade-in/out with premium easing curve
 * Applied to content changes, overlays, and state transitions
 */
export const geminiFade = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -8 },
  transition: {
    duration: 0.3,
    ease: [0.16, 1, 0.3, 1],
  },
};

/**
 * Gemini Scale Spring
 * Scale animation with spring physics for element emphasis
 */
export const geminiScaleSpring = {
  initial: { scale: 0.95, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  exit: { scale: 0.95, opacity: 0 },
  transition: geminiSpring,
};

/**
 * Gemini Slide Left
 * Horizontal slide animation for navigation and transitions
 */
export const geminiSlideLeft = {
  initial: { x: 20, opacity: 0 },
  animate: { x: 0, opacity: 1 },
  exit: { x: -20, opacity: 0 },
  transition: {
    duration: 0.3,
    ease: [0.16, 1, 0.3, 1],
  },
};

/**
 * Gemini Slide Up
 * Vertical slide animation for bottom sheets and modals
 */
export const geminiSlideUp = {
  initial: { y: 24, opacity: 0 },
  animate: { y: 0, opacity: 1 },
  exit: { y: 24, opacity: 0 },
  transition: {
    duration: 0.3,
    ease: [0.16, 1, 0.3, 1],
  },
};

/**
 * Gemini Blur Fade
 * Fade with scale for glassmorphic blur effects
 */
export const geminiBlurFade = {
  initial: { opacity: 0, scale: 0.98, backdropFilter: 'blur(0px)' },
  animate: { opacity: 1, scale: 1, backdropFilter: 'blur(8px)' },
  exit: { opacity: 0, scale: 0.98, backdropFilter: 'blur(0px)' },
  transition: {
    duration: 0.4,
    ease: [0.16, 1, 0.3, 1],
  },
};

/**
 * Gemini Stagger Container
 * Container for staggered child animations
 */
export const geminiStaggerContainer = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
  transition: {
    staggerChildren: 0.08,
    delayChildren: 0.1,
  },
};

/**
 * Gemini Stagger Item
 * Child item for staggered animations
 */
export const geminiStaggerItem = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -12 },
  transition: { duration: 0.3 },
};

/* ============================================================================
   FadeInContainer Component
   ============================================================================ */

interface FadeInContainerProps {
  /** Component children */
  children: ReactNode;
  /** Custom CSS class name */
  className?: string;
  /** Animation delay in seconds */
  delay?: number;
  /** Enable animation (default: true) */
  animated?: boolean;
  /** Custom initial state */
  initial?: TargetAndTransition | VariantLabels;
  /** Custom animate state */
  animate?: TargetAndTransition | VariantLabels;
  /** Custom exit state */
  exit?: TargetAndTransition | VariantLabels;
  /** Custom transition config */
  transition?: any;
  /** Optional key for AnimatePresence tracking */
  layoutId?: string;
}

/**
 * FadeInContainer - Premium fade animation wrapper
 * Applies smooth fade-in/out with vertical slide motion
 * Perfect for cards, panels, modals, and content sections
 */
export const FadeInContainer = React.forwardRef<
  HTMLDivElement,
  FadeInContainerProps
>(
  (
    {
      children,
      className = '',
      delay = 0,
      animated = true,
      initial,
      animate,
      exit,
      transition,
      layoutId,
    },
    ref
  ) => {
    if (!animated) {
      return (
        <div ref={ref} className={className}>
          {children}
        </div>
      );
    }

    return (
      <motion.div
        ref={ref}
        className={className}
        initial={initial ?? geminiFade.initial}
        animate={animate ?? geminiFade.animate}
        exit={exit ?? geminiFade.exit}
        transition={{
          ...geminiFade.transition,
          ...transition,
          delay,
        }}
        layoutId={layoutId}
      >
        {children}
      </motion.div>
    );
  }
);

FadeInContainer.displayName = 'FadeInContainer';

/* ============================================================================
   ScaleInContainer Component
   ============================================================================ */

interface ScaleInContainerProps {
  /** Component children */
  children: ReactNode;
  /** Custom CSS class name */
  className?: string;
  /** Animation delay in seconds */
  delay?: number;
  /** Enable animation (default: true) */
  animated?: boolean;
  /** Use spring physics (default: true) */
  useSpring?: boolean;
  /** Custom initial state */
  initial?: TargetAndTransition | VariantLabels;
  /** Custom animate state */
  animate?: TargetAndTransition | VariantLabels;
  /** Custom exit state */
  exit?: TargetAndTransition | VariantLabels;
  /** Custom transition config */
  transition?: any;
  /** Optional layout ID */
  layoutId?: string;
}

/**
 * ScaleInContainer - Premium scale animation wrapper
 * Applies spring-based scale animation with fade
 * Perfect for emphasis effects, card expansions, and modal pop-ins
 */
export const ScaleInContainer = React.forwardRef<
  HTMLDivElement,
  ScaleInContainerProps
>(
  (
    {
      children,
      className = '',
      delay = 0,
      animated = true,
      useSpring = true,
      initial,
      animate,
      exit,
      transition,
      layoutId,
    },
    ref
  ) => {
    if (!animated) {
      return (
        <div ref={ref} className={className}>
          {children}
        </div>
      );
    }

    return (
      <motion.div
        ref={ref}
        className={className}
        initial={initial ?? geminiScaleSpring.initial}
        animate={animate ?? geminiScaleSpring.animate}
        exit={exit ?? geminiScaleSpring.exit}
        transition={{
          ...(useSpring ? geminiSpring : geminiFade.transition),
          ...transition,
          delay,
        }}
        layoutId={layoutId}
      >
        {children}
      </motion.div>
    );
  }
);

ScaleInContainer.displayName = 'ScaleInContainer';

/* ============================================================================
   SlideInContainer Component
   ============================================================================ */

interface SlideInContainerProps {
  /** Component children */
  children: ReactNode;
  /** Custom CSS class name */
  className?: string;
  /** Animation delay in seconds */
  delay?: number;
  /** Enable animation (default: true) */
  animated?: boolean;
  /** Slide direction */
  direction?: 'left' | 'right' | 'up' | 'down';
  /** Distance to slide in pixels */
  distance?: number;
  /** Custom transition config */
  transition?: any;
  /** Optional layout ID */
  layoutId?: string;
}

/**
 * SlideInContainer - Premium slide animation wrapper
 * Applies directional slide animation
 * Perfect for navigation, sheet transitions, and panel reveals
 */
export const SlideInContainer = React.forwardRef<
  HTMLDivElement,
  SlideInContainerProps
>(
  (
    {
      children,
      className = '',
      delay = 0,
      animated = true,
      direction = 'left',
      distance = 20,
      transition,
      layoutId,
    },
    ref
  ) => {
    if (!animated) {
      return (
        <div ref={ref} className={className}>
          {children}
        </div>
      );
    }

    const getInitialState = () => {
      switch (direction) {
        case 'left':
          return { x: distance, opacity: 0 };
        case 'right':
          return { x: -distance, opacity: 0 };
        case 'up':
          return { y: distance, opacity: 0 };
        case 'down':
          return { y: -distance, opacity: 0 };
        default:
          return { x: distance, opacity: 0 };
      }
    };

    const getExitState = () => {
      switch (direction) {
        case 'left':
          return { x: -distance, opacity: 0 };
        case 'right':
          return { x: distance, opacity: 0 };
        case 'up':
          return { y: -distance, opacity: 0 };
        case 'down':
          return { y: distance, opacity: 0 };
        default:
          return { x: -distance, opacity: 0 };
      }
    };

    return (
      <motion.div
        ref={ref}
        className={className}
        initial={getInitialState()}
        animate={{ x: 0, y: 0, opacity: 1 }}
        exit={getExitState()}
        transition={{
          duration: 0.3,
          ease: [0.16, 1, 0.3, 1],
          ...transition,
          delay,
        }}
        layoutId={layoutId}
      >
        {children}
      </motion.div>
    );
  }
);

SlideInContainer.displayName = 'SlideInContainer';

/* ============================================================================
   StaggerContainer Component
   ============================================================================ */

interface StaggerContainerProps {
  /** Component children */
  children: ReactNode;
  /** Custom CSS class name */
  className?: string;
  /** Stagger delay between children in seconds */
  staggerDelay?: number;
  /** Initial delay before animation starts */
  initialDelay?: number;
  /** Enable animation (default: true) */
  animated?: boolean;
  /** Custom animation preset */
  preset?: 'fade' | 'scale' | 'slide';
}

/**
 * StaggerContainer - Staggered child animation wrapper
 * Automatically stagger animations for multiple children
 * Perfect for lists, grids, and sequential reveals
 */
export const StaggerContainer = React.forwardRef<
  HTMLDivElement,
  StaggerContainerProps
>(
  (
    {
      children,
      className = '',
      staggerDelay = 0.08,
      initialDelay = 0.1,
      animated = true,
      preset = 'fade',
    },
    ref
  ) => {
    if (!animated) {
      return (
        <div ref={ref} className={className}>
          {children}
        </div>
      );
    }

    const getItemVariants = () => {
      switch (preset) {
        case 'scale':
          return {
            initial: { scale: 0.95, opacity: 0 },
            animate: { scale: 1, opacity: 1 },
            exit: { scale: 0.95, opacity: 0 },
          };
        case 'slide':
          return {
            initial: { x: 20, opacity: 0 },
            animate: { x: 0, opacity: 1 },
            exit: { x: -20, opacity: 0 },
          };
        default:
          return {
            initial: { opacity: 0, y: 12 },
            animate: { opacity: 1, y: 0 },
            exit: { opacity: 0, y: -12 },
          };
      }
    };

    const itemVariants = getItemVariants();

    return (
      <motion.div
        ref={ref}
        className={className}
        initial="initial"
        animate="animate"
        exit="exit"
        variants={{
          initial: { opacity: 0 },
          animate: { opacity: 1 },
          exit: { opacity: 0 },
          transition: {
            staggerChildren: staggerDelay,
            delayChildren: initialDelay,
          },
        }}
      >
        {React.Children.map(children, (child, index) => (
          <motion.div
            key={index}
            variants={itemVariants}
            transition={{
              duration: 0.3,
              ease: [0.16, 1, 0.3, 1],
            }}
          >
            {child}
          </motion.div>
        ))}
      </motion.div>
    );
  }
);

StaggerContainer.displayName = 'StaggerContainer';

/* ============================================================================
   LayoutGroupWrapper Component
   ============================================================================ */

interface LayoutGroupWrapperProps {
  /** Component children */
  children: ReactNode;
  /** Custom CSS class name */
  className?: string;
  /** Unique layout group ID */
  id?: string;
}

/**
 * LayoutGroupWrapper - Framer Motion layout animation group
 * Enables shared layout animations across sibling components
 * Perfect for dashboard grid reorganization and dynamic layouts
 */
export const LayoutGroupWrapper = React.forwardRef<
  HTMLDivElement,
  LayoutGroupWrapperProps
>(({ children, className = '', id = 'layout-group' }, ref) => {
  return (
    <motion.div ref={ref} className={className}>
      {children}
    </motion.div>
  );
});

LayoutGroupWrapper.displayName = 'LayoutGroupWrapper';

/* ============================================================================
   AnimatePresenceWrapper Component
   ============================================================================ */

interface AnimatePresenceWrapperProps {
  /** Component children */
  children: ReactNode;
  /** Mode for presence animation */
  mode?: 'sync' | 'wait' | 'popLayout';
  /** Initial value for children */
  initial?: boolean;
}

/**
 * AnimatePresenceWrapper - Wrapper for AnimatePresence functionality
 * Handles enter/exit animations for conditional rendering
 * Perfect for modals, tooltips, and conditional content
 */
export const AnimatePresenceWrapper: React.FC<
  AnimatePresenceWrapperProps
> = ({ children, mode = 'wait', initial = true }) => {
  return (
    <AnimatePresence mode={mode} initial={initial}>
      {children}
    </AnimatePresence>
  );
};

AnimatePresenceWrapper.displayName = 'AnimatePresenceWrapper';

/* ============================================================================
   useGeminiAnimation Hook
   ============================================================================ */

/**
 * Hook to access global animation presets in components
 * Ensures consistent animation patterns across the app
 */
export const useGeminiAnimation = () => ({
  spring: geminiSpring,
  fade: geminiFade,
  scaleSpring: geminiScaleSpring,
  slideLeft: geminiSlideLeft,
  slideUp: geminiSlideUp,
  blurFade: geminiBlurFade,
  staggerContainer: geminiStaggerContainer,
  staggerItem: geminiStaggerItem,
});

/* ============================================================================
   AnimateProvider Context Component (Optional)
   ============================================================================ */

interface AnimateProviderProps {
  /** Application components */
  children: ReactNode;
  /** Global animation enabled flag */
  enabled?: boolean;
}

/**
 * AnimateProvider - Optional context provider for global animation settings
 * Can be used to toggle animations globally or pass animation config
 */
export const AnimateProvider: React.FC<AnimateProviderProps> = ({
  children,
  enabled = true,
}) => {
  return <>{children}</>;
};

AnimateProvider.displayName = 'AnimateProvider';

/* ============================================================================
   Export all animation presets and components
   ============================================================================ */

export default {
  // Presets
  geminiSpring,
  geminiFade,
  geminiScaleSpring,
  geminiSlideLeft,
  geminiSlideUp,
  geminiBlurFade,
  geminiStaggerContainer,
  geminiStaggerItem,

  // Components
  FadeInContainer,
  ScaleInContainer,
  SlideInContainer,
  StaggerContainer,
  LayoutGroupWrapper,
  AnimatePresenceWrapper,
  AnimateProvider,

  // Hook
  useGeminiAnimation,
};
