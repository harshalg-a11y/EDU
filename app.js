/**
 * ============================================================================
 * EDUSPHERE CENTRAL - Main Application Module
 * ============================================================================
 *
 * High-performance, modular JavaScript application that orchestrates:
 * - Authentication management
 * - Real-time API synchronization
 * - Reactive DOM updates
 * - Event handling & micro-interactions
 *
 * Production-ready with error handling, performance optimization, and
 * comprehensive logging for debugging.
 */

// ============================================================================
// APPLICATION STATE MANAGER
// ============================================================================

const AppState = {
  authenticated: false,
  user: null,
  metrics: [],
  conflicts: [],
  isLoading: false,
  apiBase: 'http://localhost:8000/api',

  /**
   * Update authentication state
   */
  setAuthenticated(value) {
    this.authenticated = value;
    if (value) {
      console.log('✅ User authenticated');
    } else {
      console.log('🔓 User logged out');
    }
  },

  /**
   * Set current user
   */
  setUser(email) {
    this.user = { email, timestamp: Date.now() };
    sessionStorage.setItem('userEmail', email);
  },

  /**
   * Update metrics data
   */
  updateMetrics(data) {
    this.metrics = data;
    console.log(`📊 Metrics updated: ${data.length} items`);
  },

  /**
   * Update conflicts data
   */
  updateConflicts(data) {
    this.conflicts = data;
    console.log(`⚠️ Conflicts updated: ${data.length} items`);
  },

  /**
   * Set loading state
   */
  setLoading(value) {
    this.isLoading = value;
  },
};

// ============================================================================
// LOGGER UTILITY
// ============================================================================

const Logger = {
  prefix: '[EduSphere]',

  log(message, data = null) {
    console.log(`${this.prefix} ${message}`, data || '');
  },

  error(message, error = null) {
    console.error(`${this.prefix} ❌ ${message}`, error || '');
  },

  warn(message, data = null) {
    console.warn(`${this.prefix} ⚠️ ${message}`, data || '');
  },

  success(message, data = null) {
    console.log(`${this.prefix} ✅ ${message}`, data || '');
  },

  info(message, data = null) {
    console.info(`${this.prefix} ℹ️ ${message}`, data || '');
  },
};

// ============================================================================
// AUTHENTICATION MODULE
// ============================================================================

const AuthModule = {
  /**
   * Initialize authentication UI
   */
  init() {
    Logger.log('Initializing authentication module');
    this.bindLoginForm();
    this.checkExistingSession();
  },

  /**
   * Bind login form submission
   */
  bindLoginForm() {
    const loginForm = document.getElementById('loginForm');

    if (loginForm) {
      loginForm.addEventListener('submit', (e) => {
        this.handleLoginSubmit(e);
      });
      Logger.success('Login form bound');
    } else {
      Logger.warn('Login form not found in DOM');
    }
  },

  /**
   * Handle login form submission
   */
  async handleLoginSubmit(event) {
    event.preventDefault();

    const emailInput = document.getElementById('emailInput');
    const passwordInput = document.getElementById('passwordInput');
    const rememberMe = document.getElementById('rememberMe');

    const email = emailInput?.value;
    const password = passwordInput?.value;

    if (!email || !password) {
      Logger.warn('Missing email or password');
      return;
    }

    if (password.length < 6) {
      Logger.warn('Password must be at least 6 characters');
      alert('❌ Password must be at least 6 characters');
      return;
    }

    Logger.log('Processing login for:', email);

    // Set authenticated state
    AppState.setAuthenticated(true);
    AppState.setUser(email);

    // Store auth token
    sessionStorage.setItem(
      'authToken',
      `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    );

    if (rememberMe?.checked) {
      localStorage.setItem('rememberEmail', email);
    }

    // Hide auth overlay and load dashboard
    this.hideAuthOverlay();

    // Load dashboard data
    await DashboardModule.initialize();
  },

  /**
   * Check if user has existing session
   */
  checkExistingSession() {
    const authToken = sessionStorage.getItem('authToken');
    const userEmail = sessionStorage.getItem('userEmail');

    if (authToken && userEmail) {
      Logger.success('Existing session found:', userEmail);
      AppState.setAuthenticated(true);
      AppState.setUser(userEmail);
      this.hideAuthOverlay();
      DashboardModule.initialize();
    } else {
      Logger.log('No existing session, showing auth overlay');
      this.showAuthOverlay();
    }
  },

  /**
   * Show authentication overlay
   */
  showAuthOverlay() {
    const overlay = document.getElementById('authOverlay');
    const mainViewport = document.getElementById('mainViewport');

    if (overlay && mainViewport) {
      overlay.classList.add('active');
      mainViewport.style.display = 'none';
      Logger.log('Auth overlay shown');
    }
  },

  /**
   * Hide authentication overlay with fade animation
   */
  hideAuthOverlay() {
    const overlay = document.getElementById('authOverlay');
    const mainViewport = document.getElementById('mainViewport');

    if (overlay && mainViewport) {
      // Add fade out class
      overlay.classList.add('fade-out');

      // Transition to dashboard after animation completes
      setTimeout(() => {
        overlay.classList.remove('active');
        overlay.style.display = 'none';
        mainViewport.style.display = 'flex';
        mainViewport.classList.add('animate-fade-in');

        Logger.success('Auth overlay hidden, dashboard revealed');
      }, 400);
    }
  },

  /**
   * Logout user
   */
  logout() {
    Logger.log('Logging out user');

    sessionStorage.removeItem('authToken');
    sessionStorage.removeItem('userEmail');
    localStorage.removeItem('rememberEmail');

    AppState.setAuthenticated(false);
    AppState.setUser(null);

    this.showAuthOverlay();
    document.getElementById('loginForm').reset();
  },
};

// ============================================================================
// METRICS MODULE - Dashboard Data Loading
// ============================================================================

const MetricsModule = {
  /**
   * Fetch metrics from API
   */
  async fetch() {
    AppState.setLoading(true);

    try {
      Logger.log('Fetching metrics from API...');

      const response = await fetch(`${AppState.apiBase}/metrics`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const metrics = await response.json();

      if (!Array.isArray(metrics)) {
        throw new Error('Metrics response is not an array');
      }

      AppState.updateMetrics(metrics);
      this.render(metrics);

      Logger.success('Metrics loaded and rendered:', metrics.length);
      return metrics;
    } catch (error) {
      Logger.error('Failed to fetch metrics', error);
      this.renderError();
      return [];
    } finally {
      AppState.setLoading(false);
    }
  },

  /**
   * Render metrics to DOM
   */
  render(metrics) {
    const container = document.getElementById('metricsGrid');

    if (!container) {
      Logger.warn('Metrics container not found');
      return;
    }

    // Clear existing metrics
    container.innerHTML = '';

    if (metrics.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--text-muted);">
          No metrics available
        </div>
      `;
      return;
    }

    // Render each metric card
    metrics.forEach((metric, index) => {
      const card = this.createMetricCard(metric, index);
      container.appendChild(card);
    });

    Logger.log('Metrics rendered to DOM');
  },

  /**
   * Create individual metric card element
   */
  createMetricCard(metric, index) {
    const card = document.createElement('div');
    card.className = 'metric-card animate-fade-in';
    card.style.animationDelay = `${index * 50}ms`;

    card.innerHTML = `
      <div class="metric-icon">${metric.icon || '📊'}</div>
      <div class="metric-value">${metric.value.toLocaleString()}</div>
      <div class="metric-label">${metric.name}</div>
      <div class="metric-unit">${metric.unit}</div>
    `;

    return card;
  },

  /**
   * Render error state
   */
  renderError() {
    const container = document.getElementById('metricsGrid');

    if (container) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 2rem; color: var(--status-critical);">
          ❌ Failed to load metrics. Check if API server is running on port 8000.
        </div>
      `;
    }
  },
};

// ============================================================================
// CONFLICTS MODULE - Alert Management
// ============================================================================

const ConflictsModule = {
  /**
   * Fetch conflicts from API
   */
  async fetch() {
    AppState.setLoading(true);

    try {
      Logger.log('Fetching conflicts from API...');

      const response = await fetch(`${AppState.apiBase}/conflicts`);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const conflicts = await response.json();

      if (!Array.isArray(conflicts)) {
        throw new Error('Conflicts response is not an array');
      }

      AppState.updateConflicts(conflicts);
      this.render(conflicts);

      Logger.success('Conflicts loaded and rendered:', conflicts.length);
      return conflicts;
    } catch (error) {
      Logger.error('Failed to fetch conflicts', error);
      this.renderError();
      return [];
    } finally {
      AppState.setLoading(false);
    }
  },

  /**
   * Render conflicts to DOM
   */
  render(conflicts) {
    const container = document.getElementById('conflictsContainer');

    if (!container) {
      Logger.warn('Conflicts container not found');
      return;
    }

    // Clear existing conflicts
    container.innerHTML = '';

    if (conflicts.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
          ✅ No active conflicts detected
        </div>
      `;
      return;
    }

    // Render each conflict card
    conflicts.forEach((conflict, index) => {
      const card = this.createConflictCard(conflict, index);
      container.appendChild(card);
    });

    // Bind resolve button events
    this.bindResolveButtons();

    Logger.log('Conflicts rendered to DOM');
  },

  /**
   * Create individual conflict card element
   */
  createConflictCard(conflict, index) {
    const card = document.createElement('div');
    card.className = `conflict-card severity-${conflict.severity} animate-slide-up`;
    card.dataset.conflictId = conflict.id;
    card.style.animationDelay = `${index * 75}ms`;

    const severityLabel = conflict.severity.charAt(0).toUpperCase() + conflict.severity.slice(1);

    card.innerHTML = `
      <div class="conflict-header">
        <h4 class="conflict-title">${this.escapeHtml(conflict.title)}</h4>
        <span class="severity-badge ${conflict.severity}">${severityLabel}</span>
      </div>
      <p class="conflict-description">${this.escapeHtml(conflict.description)}</p>
      <div class="conflict-meta">
        <span>${conflict.room_id || 'System'}</span>
        <button class="btn-resolve-conflict" data-conflict-id="${conflict.id}" title="Resolve this conflict">
          ✓ Resolve
        </button>
      </div>
    `;

    return card;
  },

  /**
   * Bind resolve button click events
   */
  bindResolveButtons() {
    document.querySelectorAll('.btn-resolve-conflict').forEach((btn) => {
      // Remove existing listeners by cloning
      const newBtn = btn.cloneNode(true);
      btn.replaceWith(newBtn);

      // Add new listener
      newBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const conflictId = newBtn.dataset.conflictId;
        this.resolveConflict(conflictId);
      });
    });

    Logger.log('Resolve buttons bound');
  },

  /**
   * Resolve conflict via API
   */
  async resolveConflict(conflictId) {
    Logger.log('Resolving conflict:', conflictId);

    try {
      // Find and animate the card
      const card = document.querySelector(`[data-conflict-id="${conflictId}"]`);

      if (!card) {
        Logger.warn('Conflict card not found for ID:', conflictId);
        return;
      }

      // Dispatch POST request to API
      const response = await fetch(`${AppState.apiBase}/conflicts/resolve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: conflictId }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const updatedConflicts = await response.json();

      // Add slide-out animation
      card.classList.add('slide-out-right');

      // Remove card after animation
      setTimeout(() => {
        AppState.updateConflicts(updatedConflicts);
        this.render(updatedConflicts);
        Logger.success('Conflict resolved and removed:', conflictId);
      }, 300);
    } catch (error) {
      Logger.error('Failed to resolve conflict', error);
      alert(`❌ Failed to resolve conflict: ${error.message}`);
    }
  },

  /**
   * Escape HTML to prevent XSS
   */
  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  /**
   * Render error state
   */
  renderError() {
    const container = document.getElementById('conflictsContainer');

    if (container) {
      container.innerHTML = `
        <div style="text-align: center; padding: 2rem; color: var(--status-critical);">
          ❌ Failed to load conflicts. Check API connection.
        </div>
      `;
    }
  },
};

// ============================================================================
// HEATMAP MODULE - Contribution Grid
// ============================================================================

const HeatmapModule = {
  /**
   * Generate and render heatmap
   */
  generate() {
    const grid = document.getElementById('heatmapGrid');

    if (!grid) {
      Logger.warn('Heatmap grid not found');
      return;
    }

    Logger.log('Generating heatmap grid (6×24)');

    const rows = 6;
    const cols = 24;
    const levels = ['level-0', 'level-1', 'level-2', 'level-3'];
    const levelWeights = [0.25, 0.45, 0.25, 0.05]; // Distribution: mostly low-medium, few critical

    grid.innerHTML = '';

    let levelIndex = 0;

    for (let i = 0; i < rows * cols; i++) {
      const cell = document.createElement('div');

      // Distribute levels with weighted randomness
      const rand = Math.random();
      let cumulativeWeight = 0;

      for (let j = 0; j < levelWeights.length; j++) {
        cumulativeWeight += levelWeights[j];
        if (rand < cumulativeWeight) {
          levelIndex = j;
          break;
        }
      }

      cell.className = `heatmap-cell ${levels[levelIndex]}`;
      cell.title = `Week ${Math.floor(i / cols) + 1}, Day ${(i % cols) + 1}`;

      grid.appendChild(cell);
    }

    Logger.success('Heatmap grid generated:', `${rows}×${cols} cells`);
  },
};

// ============================================================================
// PODIUMS MODULE - Top Performers Leaderboard
// ============================================================================

const PodiumsModule = {
  /**
   * Mock data for top performers
   */
  mockData: [
    {
      rank: 2,
      name: 'Sophia Martinez',
      grade: 'Grade 11',
      percentage: 98.45,
      initials: 'SM',
    },
    {
      rank: 1,
      name: 'Rayan Hassan',
      grade: 'Grade 11',
      percentage: 99.88,
      initials: 'RH',
    },
    {
      rank: 3,
      name: 'Emma Chen',
      grade: 'Grade 10',
      percentage: 97.92,
      initials: 'EC',
    },
  ],

  /**
   * Render podiums
   */
  render() {
    const grid = document.getElementById('podiumsGrid');

    if (!grid) {
      Logger.warn('Podiums grid not found');
      return;
    }

    Logger.log('Rendering podiums');

    grid.innerHTML = '';

    // Display order: 2nd, 1st (center), 3rd
    const displayOrder = [this.mockData[1], this.mockData[0], this.mockData[2]];

    displayOrder.forEach((student, index) => {
      const card = this.createPodiumCard(student, index);
      grid.appendChild(card);
    });

    Logger.success('Podiums rendered');
  },

  /**
   * Create podium card element
   */
  createPodiumCard(student, index) {
    const card = document.createElement('div');
    card.className = `podium-card rank-${student.rank} animate-slide-up`;
    card.style.animationDelay = `${index * 100}ms`;

    card.innerHTML = `
      <div class="rank-badge">#${student.rank}</div>
      <div class="avatar-ring">${student.initials}</div>
      <h4 class="student-name">${this.escapeHtml(student.name)}</h4>
      <p class="student-grade">${this.escapeHtml(student.grade)}</p>
      <div class="performance-percent">${student.percentage.toFixed(2)}%</div>
    `;

    return card;
  },

  /**
   * Escape HTML to prevent XSS
   */
  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },
};

// ============================================================================
// DASHBOARD MODULE - Main Orchestrator
// ============================================================================

const DashboardModule = {
  /**
   * Initialize dashboard and load all data
   */
  async initialize() {
    Logger.log('Initializing dashboard...');

    try {
      // Generate heatmap
      HeatmapModule.generate();

      // Render podiums
      PodiumsModule.render();

      // Fetch and render metrics
      await MetricsModule.fetch();

      // Fetch and render conflicts
      await ConflictsModule.fetch();

      Logger.success('Dashboard fully initialized');
    } catch (error) {
      Logger.error('Dashboard initialization error:', error);
    }
  },

  /**
   * Refresh dashboard data
   */
  async refresh() {
    Logger.log('Refreshing dashboard data...');

    try {
      await MetricsModule.fetch();
      await ConflictsModule.fetch();

      Logger.success('Dashboard refreshed');
    } catch (error) {
      Logger.error('Dashboard refresh error:', error);
    }
  },

  /**
   * Setup auto-refresh interval
   */
  setupAutoRefresh(intervalMs = 30000) {
    Logger.log(`Setting up auto-refresh every ${intervalMs}ms`);

    setInterval(() => {
      this.refresh();
    }, intervalMs);
  },
};

// ============================================================================
// NAVIGATION MODULE - Sidebar Interactions
// ============================================================================

const NavigationModule = {
  /**
   * Initialize navigation
   */
  init() {
    Logger.log('Initializing navigation');

    document.querySelectorAll('.nav-button').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        this.handleNavClick(e);
      });
    });

    Logger.success('Navigation initialized');
  },

  /**
   * Handle navigation button click
   */
  handleNavClick(event) {
    const btn = event.currentTarget;
    const section = btn.dataset.nav;

    // Update active state
    document.querySelectorAll('.nav-button').forEach((b) => {
      b.classList.remove('active');
    });
    btn.classList.add('active');

    Logger.log('Navigation:', section);

    // Handle specific section logic here
    switch (section) {
      case 'dashboard':
        DashboardModule.refresh();
        break;
      case 'command':
        Logger.log('Command palette would open here');
        break;
      case 'students':
        Logger.log('Student tracks view');
        break;
      case 'scheduler':
        Logger.log('Scheduler view');
        break;
    }
  },
};

// ============================================================================
// EVENT LISTENERS & DOM UTILITIES
// ============================================================================

const DOMUtils = {
  /**
   * Add fade-out animation to element
   */
  fadeOut(element, duration = 400) {
    element.classList.add('fade-out');

    return new Promise((resolve) => {
      setTimeout(() => {
        element.style.display = 'none';
        resolve();
      }, duration);
    });
  },

  /**
   * Add slide-out animation
   */
  slideOut(element, direction = 'right', duration = 300) {
    element.classList.add(`slide-out-${direction}`);

    return new Promise((resolve) => {
      setTimeout(() => {
        element.remove();
        resolve();
      }, duration);
    });
  },

  /**
   * Wait for DOM element to be available
   */
  waitForElement(selector, timeout = 5000) {
    return new Promise((resolve, reject) => {
      const element = document.querySelector(selector);

      if (element) {
        resolve(element);
        return;
      }

      const observer = new MutationObserver(() => {
        const el = document.querySelector(selector);
        if (el) {
          observer.disconnect();
          resolve(el);
        }
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true,
      });

      setTimeout(() => {
        observer.disconnect();
        reject(new Error(`Element ${selector} not found within ${timeout}ms`));
      }, timeout);
    });
  },
};

// ============================================================================
// APPLICATION BOOTSTRAP
// ============================================================================

/**
 * Initialize application when DOM is ready
 */
function bootstrap() {
  Logger.log('🚀 Bootstrapping EduSphere Central Application');

  // Initialize modules
  AuthModule.init();
  NavigationModule.init();

  Logger.success('Application bootstrapped and ready');
}

// Run bootstrap on DOM content loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrap);
} else {
  // DOM already loaded
  bootstrap();
}

// ============================================================================
// GLOBAL ERROR HANDLING
// ============================================================================

/**
 * Handle uncaught errors
 */
window.addEventListener('error', (event) => {
  Logger.error('Uncaught error:', event.error);
});

/**
 * Handle unhandled promise rejections
 */
window.addEventListener('unhandledrejection', (event) => {
  Logger.error('Unhandled promise rejection:', event.reason);
});

// ============================================================================
// PERFORMANCE MONITORING
// ============================================================================

/**
 * Log performance metrics
 */
if (window.performance && window.performance.timing) {
  window.addEventListener('load', () => {
    setTimeout(() => {
      const timing = window.performance.timing;
      const loadTime = timing.loadEventEnd - timing.navigationStart;

      Logger.log(`⚡ Page load time: ${loadTime}ms`);
      Logger.log(`⚡ DOM content loaded: ${timing.domContentLoadedEventEnd - timing.navigationStart}ms`);
    }, 0);
  });
}

// ============================================================================
// EXPORT FOR TESTING (Optional)
// ============================================================================

// Uncomment for testing/debugging
/*
window.AppState = AppState;
window.Logger = Logger;
window.AuthModule = AuthModule;
window.MetricsModule = MetricsModule;
window.ConflictsModule = ConflictsModule;
window.DashboardModule = DashboardModule;
window.NavigationModule = NavigationModule;
*/
