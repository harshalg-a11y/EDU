"""
EduSphere Central - Main Application Entry Point
================================================

This is the primary entry point for the EduSphere Reflex application.
Initializes and configures the entire web application with all pages and routes.

To run the application:
    reflex run

This will start the development server on http://localhost:3000
"""

import reflex as rx
from frontend.index import index_layout, MainDashboardState
from frontend.edusphere import OmniSearchState


# ============================================================================
#    APP CONFIGURATION
# ============================================================================

config = rx.Config(
    app_name="edu_sphere",
    env=rx.Env.DEV,
)


# ============================================================================
#    STATE MANAGEMENT
# ============================================================================

class AppState(rx.State):
    """Global application state."""
    pass


# ============================================================================
#    PAGES
# ============================================================================

def dashboard_page() -> rx.Component:
    """Main dashboard page."""
    return index_layout()


# ============================================================================
#    APP INITIALIZATION
# ============================================================================

# Create Reflex app
app = rx.App()

# Add pages
app.add_page(
    dashboard_page,
    path="/",
    title="EduSphere Central - Dashboard"
)

# Compile the app
if __name__ == "__main__":
    app.compile()
