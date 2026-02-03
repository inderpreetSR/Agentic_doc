"""
Interactive Graph Page - vis.js network visualization with draggable nodes.
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Interactive Graph | DSAA Agents",
    page_icon="🕸️",
    layout="wide",
)

from utils.interactive_graph import (
    create_vis_network_html,
    build_architecture_network,
    build_agent_flow_network,
)
from utils.diagrams import PRESETS
from utils.monitoring import log_page_view

log_page_view("Interactive Graph")

# Custom CSS
st.markdown("""
<style>
    .view-toggle {
        display: flex;
        gap: 8px;
        margin-bottom: 16px;
    }
    .info-box {
        background: rgba(102, 126, 234, 0.1);
        border-left: 3px solid #667eea;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    if "graph_filters" not in st.session_state:
        st.session_state.graph_filters = PRESETS["all_on"].copy()
    if "graph_view" not in st.session_state:
        st.session_state.graph_view = "architecture"
    if "graph_layout" not in st.session_state:
        st.session_state.graph_layout = "physics"


def main():
    init_session_state()

    st.title("🕸️ Interactive Graph")
    st.markdown("**Drag, zoom, and explore** the architecture with physics-based layout.")

    # Sidebar
    with st.sidebar:
        st.header("Graph Settings")

        # View selector
        st.subheader("View")
        view = st.radio(
            "Select view:",
            ["architecture", "agent_flow"],
            format_func=lambda x: "🏗️ Architecture" if x == "architecture" else "🔄 Agent Flow",
            key="view_selector",
            label_visibility="collapsed"
        )
        st.session_state.graph_view = view

        # Layout options
        st.subheader("Layout")
        layout = st.radio(
            "Layout mode:",
            ["physics", "hierarchical"],
            format_func=lambda x: "⚡ Physics (Auto)" if x == "physics" else "📊 Hierarchical",
            key="layout_selector",
            label_visibility="collapsed"
        )
        st.session_state.graph_layout = layout

        if layout == "hierarchical":
            direction = st.selectbox(
                "Direction",
                ["UD", "DU", "LR", "RL"],
                format_func=lambda x: {
                    "UD": "↓ Top to Bottom",
                    "DU": "↑ Bottom to Top",
                    "LR": "→ Left to Right",
                    "RL": "← Right to Left"
                }[x]
            )
        else:
            direction = "UD"

        # Filters (only for architecture view)
        if view == "architecture":
            st.divider()
            st.subheader("Filters")

            filter_labels = {
                "api": "🌐 API / UI",
                "orchestrator": "🎯 Orchestrator",
                "agents": "🤖 Agents",
                "retrieval": "📚 RAG",
                "tools": "🔧 Tools",
                "data": "💾 Data Stores",
                "governance": "🛡️ Governance",
                "obs": "📊 Observability",
                "ds": "📈 DS Workflows",
            }

            for key, label in filter_labels.items():
                st.session_state.graph_filters[key] = st.checkbox(
                    label,
                    value=st.session_state.graph_filters.get(key, True),
                    key=f"graph_filter_{key}",
                )

            # Quick presets
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                if st.button("All On", use_container_width=True):
                    st.session_state.graph_filters = PRESETS["all_on"].copy()
                    st.rerun()
            with col2:
                if st.button("All Off", use_container_width=True):
                    st.session_state.graph_filters = PRESETS["all_off"].copy()
                    st.rerun()

        # Help
        st.divider()
        st.subheader("Controls")
        st.markdown("""
        - **Drag** nodes to reposition
        - **Scroll** to zoom in/out
        - **Click + drag** background to pan
        - **Hover** nodes for details
        - Use buttons above graph for more options
        """)

    # Main content
    st.markdown("""
    <div class="info-box">
        <strong>Interactive Features:</strong> Drag nodes to reposition • Scroll to zoom •
        Hover for tooltips • Click buttons above for fit/reset/export
    </div>
    """, unsafe_allow_html=True)

    # Build graph based on view
    if st.session_state.graph_view == "architecture":
        nodes, edges = build_architecture_network(st.session_state.graph_filters)

        if not nodes:
            st.warning("No components selected. Enable some filters in the sidebar.")
        else:
            html = create_vis_network_html(
                nodes=nodes,
                edges=edges,
                height=650,
                physics=(st.session_state.graph_layout == "physics"),
                hierarchical=(st.session_state.graph_layout == "hierarchical"),
                direction=direction if st.session_state.graph_layout == "hierarchical" else "UD"
            )
            components.html(html, height=780, scrolling=False)

    else:  # agent_flow
        nodes, edges = build_agent_flow_network()

        html = create_vis_network_html(
            nodes=nodes,
            edges=edges,
            height=600,
            physics=(st.session_state.graph_layout == "physics"),
            hierarchical=(st.session_state.graph_layout == "hierarchical"),
            direction=direction if st.session_state.graph_layout == "hierarchical" else "UD"
        )
        components.html(html, height=730, scrolling=False)

    # Comparison with Mermaid
    with st.expander("📊 Compare with Mermaid View"):
        st.markdown("""
        **vis.js Network (this page):**
        - ✅ Draggable nodes
        - ✅ Physics-based auto-layout
        - ✅ Smooth zoom/pan
        - ✅ Hover tooltips
        - ✅ Better for exploration

        **Mermaid (Diagram Viewer):**
        - ✅ Structured layouts
        - ✅ Better for documentation
        - ✅ Subgraph grouping
        - ✅ More diagram types

        Use **Interactive Graph** for exploration, **Diagram Viewer** for documentation.
        """)

        if st.button("Go to Diagram Viewer"):
            st.switch_page("pages/1_Diagram_Viewer.py")


if __name__ == "__main__":
    main()
