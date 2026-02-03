"""
DSAA Agents - Multi-Page Streamlit Application

Main entry point and home page for the diagram viewer application.
"""

import streamlit as st

# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="DSAA Agents",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import monitoring after page config
from utils.monitoring import log_page_view, metrics

# Log page view
log_page_view("Home")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #9fb0d0;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: rgba(122, 162, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
    }
    .feature-card h3 {
        color: #7aa2ff;
        margin-bottom: 8px;
    }
    .feature-card p {
        color: #9fb0d0;
        font-size: 14px;
    }
    .stats-container {
        display: flex;
        gap: 24px;
        margin: 24px 0;
    }
    .stat-card {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        padding: 16px 24px;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #9fb0d0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main home page."""

    # Header
    st.markdown('<h1 class="main-header">DSAA Agents</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Interactive diagram viewer for Agentic RAG + Data Science architectures</p>',
        unsafe_allow_html=True
    )

    # Quick stats
    stats = metrics.get_metrics_summary()
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Diagram Types", "5+", help="Flowchart, Sequence, ER, Class, Gantt")
    with col2:
        st.metric("Templates", "15+", help="Pre-built diagram templates")
    with col3:
        st.metric("Export Formats", "2", help="PNG and SVG")
    with col4:
        st.metric("Total Views", stats.get("total_events", 0))

    st.divider()

    # Feature cards
    st.subheader("Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Diagram Viewer</h3>
            <p>Interactive viewer for Agentic RAG architecture diagrams with customizable filters and presets.
            Visualize separation of concerns, agent graphs, and data science pipelines.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>✏️ Diagram Editor</h3>
            <p>Live Mermaid code editor with instant preview. Create custom diagrams with syntax highlighting
            and real-time rendering.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>💾 Custom Diagrams</h3>
            <p>Save, manage, and share your custom diagrams. Built-in database for persistence with
            public/private visibility options.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📥 Export Options</h3>
            <p>Download diagrams as PNG or SVG for use in documentation, presentations, or other applications.
            High-quality exports with dark theme support.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>📚 Template Library</h3>
            <p>Browse pre-built templates for sequence diagrams, ER diagrams, class diagrams, Gantt charts,
            and more. One-click to use any template.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <h3>🔌 REST API</h3>
            <p>Programmatic access to diagram generation via REST API. Integrate with CI/CD pipelines,
            documentation generators, or custom tools.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Quick Start
    st.subheader("Quick Start")

    st.markdown("""
    1. **Diagram Viewer** → Explore pre-built architecture diagrams with interactive filters
    2. **Diagram Editor** → Create custom diagrams with live preview
    3. **Custom Diagrams** → Save and manage your diagram collection
    4. **API Docs** → Integrate diagram generation into your workflow
    """)

    # Navigation buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📊 Open Viewer", use_container_width=True):
            st.switch_page("pages/1_Diagram_Viewer.py")

    with col2:
        if st.button("✏️ Open Editor", use_container_width=True):
            st.switch_page("pages/2_Diagram_Editor.py")

    with col3:
        if st.button("💾 My Diagrams", use_container_width=True):
            st.switch_page("pages/3_Custom_Diagrams.py")

    with col4:
        if st.button("🔌 API Docs", use_container_width=True):
            st.switch_page("pages/4_API_Docs.py")

    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Built with Streamlit | <a href="https://github.com/inderpreetSR/Agentic_doc" target="_blank">GitHub</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
