"""
Diagram Viewer Page - Interactive viewer for architecture diagrams.
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Diagram Viewer | DSAA Agents",
    page_icon="📊",
    layout="wide",
)

from utils.diagrams import (
    PRESETS,
    COMPLETE_DIAGRAM,
    build_architecture_diagram,
    build_agent_diagram,
    build_ds_diagram,
)
from utils.export import render_mermaid_with_export
from utils.monitoring import log_page_view, log_diagram_render

# Log page view
log_page_view("Diagram Viewer")

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 16px; border-radius: 8px; }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 12px; }
    .info-card {
        background: rgba(122, 162, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .info-card h4 { margin: 0 0 8px 0; color: var(--primary-color, #7aa2ff); }
    .info-card p { margin: 0; color: var(--text-color, #9fb0d0); opacity: 0.85; font-size: 14px; }
    .tab-description {
        background: rgba(122, 162, 255, 0.08);
        border-left: 3px solid var(--primary-color, #7aa2ff);
        padding: 12px 16px;
        margin-bottom: 16px;
        border-radius: 4px;
    }
    .tab-description strong { color: var(--primary-color, #7aa2ff); }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state."""
    if "viewer_filters" not in st.session_state:
        st.session_state.viewer_filters = PRESETS["all_on"].copy()


def apply_preset(preset_name: str):
    """Apply a preset filter configuration."""
    st.session_state.viewer_filters = PRESETS[preset_name].copy()


def main():
    init_session_state()

    # Header
    st.title("📊 Diagram Viewer")
    st.markdown(
        "**Explore** Agentic RAG + Data Science architecture diagrams with interactive filters."
    )

    # Sidebar controls
    with st.sidebar:
        active_count = sum(1 for v in st.session_state.viewer_filters.values() if v)
        st.header(f"Filters ({active_count}/9)")

        # Filter checkboxes
        st.subheader("Component Visibility")

        filter_labels = {
            "api": "API / UI",
            "orchestrator": "Orchestrator",
            "agents": "Agents",
            "retrieval": "Retrieval (RAG)",
            "tools": "Tools / Actions",
            "data": "Data Stores",
            "governance": "Governance",
            "obs": "Observability",
            "ds": "DS Project Depth",
        }

        for key, label in filter_labels.items():
            st.session_state.viewer_filters[key] = st.checkbox(
                label,
                value=st.session_state.viewer_filters.get(key, True),
                key=f"viewer_filter_{key}",
            )

        # Preset buttons
        st.subheader("Quick Presets")

        st.markdown("**Full System:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("All On", use_container_width=True, key="v_preset_all_on"):
                apply_preset("all_on")
                st.toast("All components enabled", icon="✅")
                st.rerun()
        with col2:
            if st.button("Clear All", use_container_width=True, key="v_preset_all_off"):
                apply_preset("all_off")
                st.toast("All components disabled", icon="🔄")
                st.rerun()

        st.markdown("**Focus Views:**")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("RAG + Agents", use_container_width=True, key="v_preset_rag"):
                apply_preset("rag_agents")
                st.toast("RAG+Agents focus applied", icon="🎯")
                st.rerun()
            if st.button("Governance", use_container_width=True, key="v_preset_gov"):
                apply_preset("governance")
                st.toast("Governance focus applied", icon="🛡️")
                st.rerun()
        with col4:
            if st.button("DS Pipeline", use_container_width=True, key="v_preset_ds"):
                apply_preset("ds_pipeline")
                st.toast("DS Pipeline focus applied", icon="📊")
                st.rerun()

        # Design principles
        st.divider()
        st.header("Design Principles")

        st.markdown("""
<div class="info-card">
    <h4>Design Intent</h4>
    <p>Keep "who does what" crisp: Separation of Concerns, Fallback handling, Audit trails</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="info-card">
    <h4>Key Pattern</h4>
    <p><code>Plan → Retrieve → Ground → Verify → Route → Act → Log</code></p>
</div>
""", unsafe_allow_html=True)

    # Main content - tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Architecture (SoC)",
        "Agent Graph",
        "DS Project Depth",
        "Complete View"
    ])

    with tab1:
        st.markdown("""
        <div class="tab-description">
            <strong>Architecture View:</strong> Separation of concerns — UI/API (request surface),
            orchestrator (control plane), agents (intent & reasoning), retrieval/tools
            (data plane), governance + observability (safety rails).
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Rendering architecture diagram..."):
            diagram = build_architecture_diagram(st.session_state.viewer_filters)
            log_diagram_render("architecture", st.session_state.viewer_filters)
            components.html(render_mermaid_with_export(diagram, 680), height=750, scrolling=True)

    with tab2:
        st.markdown("""
        <div class="tab-description">
            <strong>Agent Graph:</strong> State machine showing how planner routes to specialized agents;
            validators gate decisions; fallback loops prevent hallucination.
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Rendering agent graph..."):
            diagram = build_agent_diagram(st.session_state.viewer_filters)
            log_diagram_render("agent", st.session_state.viewer_filters)
            components.html(render_mermaid_with_export(diagram, 570), height=650, scrolling=True)

    with tab3:
        st.markdown("""
        <div class="tab-description">
            <strong>DS Project Depth:</strong> Specialized agents for EDA, feature engineering, modeling,
            evaluation, and deployment — each can be tool-using and RAG-grounded.
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Rendering DS pipeline diagram..."):
            diagram = build_ds_diagram(st.session_state.viewer_filters)
            log_diagram_render("ds", st.session_state.viewer_filters)
            components.html(render_mermaid_with_export(diagram, 770), height=850, scrolling=True)

    with tab4:
        st.markdown("""
        <div class="tab-description">
            <strong>Complete View:</strong> Static view showing all components and cross-links.
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Rendering complete diagram..."):
            log_diagram_render("complete", None)
            components.html(render_mermaid_with_export(COMPLETE_DIAGRAM, 770), height=850, scrolling=True)


if __name__ == "__main__":
    main()
