"""
Streamlit DSAA Agents Diagram Viewer

Interactive viewer for Agentic RAG + Data Science Project Stack diagrams.
Uses HTML + Mermaid.js (CDN) for client-side rendering; no external image API.
"""

import json
import streamlit as st
import streamlit.components.v1 as components

from diagrams import (
    PRESETS,
    COMPLETE_DIAGRAM,
    build_architecture_diagram,
    build_agent_diagram,
    build_ds_diagram,
)

# Page configuration
st.set_page_config(
    page_title="DSAA Agents Diagram Viewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark theme enhancements
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 12px;
    }
    .info-card {
        background: rgba(122, 162, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .info-card h4 {
        margin: 0 0 8px 0;
        color: var(--primary-color, #7aa2ff);
    }
    .info-card p {
        margin: 0;
        color: var(--text-color, #9fb0d0);
        opacity: 0.85;
        font-size: 14px;
    }
    code {
        background: rgba(122, 162, 255, 0.15);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    .tab-description {
        background: rgba(122, 162, 255, 0.08);
        border-left: 3px solid var(--primary-color, #7aa2ff);
        padding: 12px 16px;
        margin-bottom: 16px;
        border-radius: 4px;
    }
    .tab-description strong {
        color: var(--primary-color, #7aa2ff);
    }
</style>
""", unsafe_allow_html=True)


def render_mermaid_html(mermaid_code: str, height_px: int = 500) -> str:
    """Build HTML that loads Mermaid.js from CDN and renders the diagram in the browser."""
    # Escape diagram for safe injection into JS string (handles newlines, quotes, backslashes)
    code_escaped = json.dumps(mermaid_code)
    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    body {{ margin: 0; padding: 12px; background: transparent; }}
    .mermaid {{ display: flex; justify-content: center; }}
    .mermaid svg {{ max-width: 100%; }}
  </style>
</head>
<body>
  <div class="mermaid" id="mermaid-root"></div>
  <script>
    mermaid.initialize({{ startOnLoad: false, theme: 'dark', securityLevel: 'loose' }});
    const code = {code_escaped};
    const container = document.getElementById('mermaid-root');
    mermaid.render('mermaid-svg', code).then(function({{ svg }}) {{
      container.innerHTML = svg;
    }}).catch(function(err) {{
      container.innerHTML = '<pre style="color:#e06c75;">' + err.message + '</pre>';
    }});
  </script>
</body>
</html>
"""


def init_session_state():
    """Initialize session state with default filter values."""
    if "filters" not in st.session_state:
        st.session_state.filters = PRESETS["all_on"].copy()


def apply_preset(preset_name: str):
    """Apply a preset filter configuration."""
    st.session_state.filters = PRESETS[preset_name].copy()


def main():
    """Main application entry point."""
    init_session_state()

    # Header
    st.title("Agentic RAG + Data Science Project Stack")
    st.markdown(
        "**Design and visualize** agent-based systems with clear separation of concerns. "
        "Use filters to explore how orchestrators, specialized agents, and data pipelines "
        "work together with governance and observability layers."
    )

    # Sidebar controls
    with st.sidebar:
        active_count = sum(1 for v in st.session_state.filters.values() if v)
        st.header(f"Diagram Filters ({active_count}/9)")
        st.markdown(
            "Use filters to emphasize specific system aspects (governance, DS lifecycle, or agent orchestration)."
        )

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
            st.session_state.filters[key] = st.checkbox(
                label,
                value=st.session_state.filters.get(key, True),
                key=f"filter_{key}",
            )

        # Preset buttons
        st.subheader("Quick Presets")

        st.markdown("**Full System:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("All Components", use_container_width=True, key="preset_all_on"):
                apply_preset("all_on")
                st.toast("All components enabled", icon="✅")
                st.rerun()
        with col2:
            if st.button("Clear All", use_container_width=True, key="preset_all_off"):
                apply_preset("all_off")
                st.toast("All components disabled", icon="🔄")
                st.rerun()

        st.markdown("**Focus Views:**")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("RAG + Agents", use_container_width=True, key="preset_rag"):
                apply_preset("rag_agents")
                st.toast("RAG+Agents focus applied", icon="🎯")
                st.rerun()
            if st.button("Governance", use_container_width=True, key="preset_gov"):
                apply_preset("governance")
                st.toast("Governance focus applied", icon="🛡️")
                st.rerun()
        with col4:
            if st.button("DS Pipeline", use_container_width=True, key="preset_ds"):
                apply_preset("ds_pipeline")
                st.toast("DS Pipeline focus applied", icon="📊")
                st.rerun()

        # Info cards - clearly separated
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

    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Architecture (SoC)",
        "Agent Graph",
        "DS Project Depth",
        "Complete View"
    ])

    with tab1:
        st.markdown("""
        <div class="tab-description">
            <strong>Architecture View:</strong> Emphasizes separation of concerns — UI/API (request surface),
            orchestrator (control plane), agents (intent & reasoning), retrieval/tools
            (data plane), plus governance + observability (safety rails).
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Rendering architecture diagram..."):
            arch_diagram = build_architecture_diagram(st.session_state.filters)
            components.html(render_mermaid_html(arch_diagram, 680), height=700, scrolling=True)

    with tab2:
        st.markdown("""
        <div class="tab-description">
            <strong>Agent Graph:</strong> State machine showing how planner routes to specialized agents;
            validators gate decisions; fallback loops prevent hallucination.
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Rendering agent graph..."):
            agent_diagram = build_agent_diagram(st.session_state.filters)
            components.html(render_mermaid_html(agent_diagram, 570), height=600, scrolling=True)

    with tab3:
        st.markdown("""
        <div class="tab-description">
            <strong>DS Project Depth:</strong> Specialized agents for EDA, feature engineering, modeling,
            evaluation, and deployment — each can be tool-using and RAG-grounded.
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Rendering DS pipeline diagram..."):
            ds_diagram = build_ds_diagram(st.session_state.filters)
            components.html(render_mermaid_html(ds_diagram, 770), height=800, scrolling=True)

    with tab4:
        st.markdown("""
        <div class="tab-description">
            <strong>Complete View:</strong> Static view showing all components and cross-links from the v2 design.
        </div>
        """, unsafe_allow_html=True)
        with st.spinner("Rendering complete diagram..."):
            components.html(render_mermaid_html(COMPLETE_DIAGRAM, 770), height=800, scrolling=True)

    # Footer
    st.divider()
    st.markdown(
        "**How to use this for designing agents:** Start by naming your 'verbs' "
        "(Plan, Retrieve, Verify, Decide, Act). Then create one agent per verb-class. "
        "If you notice a single agent doing too many verbs, split it (separation of concerns). "
        "Your system becomes resilient when verification + fallback are first-class citizens, "
        "not afterthoughts."
    )


if __name__ == "__main__":
    main()
