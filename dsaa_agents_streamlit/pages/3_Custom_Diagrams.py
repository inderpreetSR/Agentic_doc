"""
Custom Diagrams Page - Manage saved diagrams.
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Custom Diagrams | DSAA Agents",
    page_icon="💾",
    layout="wide",
)

from utils.database import DiagramRepository
from utils.export import render_mermaid_with_export
from utils.monitoring import log_page_view

log_page_view("Custom Diagrams")

# Custom CSS
st.markdown("""
<style>
    .diagram-card {
        background: rgba(122, 162, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .diagram-card h4 {
        color: #7aa2ff;
        margin: 0 0 8px 0;
    }
    .diagram-card p {
        color: #9fb0d0;
        font-size: 13px;
        margin: 0;
    }
    .diagram-meta {
        font-size: 11px;
        color: #666;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("💾 Custom Diagrams")
    st.markdown("Manage your saved diagrams.")

    # Get all diagrams
    diagrams = DiagramRepository.get_all(include_public=True)

    # Sidebar filters
    with st.sidebar:
        st.header("Filters")

        show_public = st.checkbox("Show Public", value=True)
        show_private = st.checkbox("Show Private", value=True)

        diagram_types = ["All"] + list(set(d.get("diagram_type", "flowchart") for d in diagrams))
        selected_type = st.selectbox("Diagram Type", diagram_types)

        st.divider()

        # Stats
        st.subheader("Statistics")
        st.metric("Total Diagrams", len(diagrams))
        public_count = sum(1 for d in diagrams if d.get("is_public"))
        st.metric("Public", public_count)
        st.metric("Private", len(diagrams) - public_count)

    # Filter diagrams
    filtered = diagrams
    if not show_public:
        filtered = [d for d in filtered if not d.get("is_public")]
    if not show_private:
        filtered = [d for d in filtered if d.get("is_public")]
    if selected_type != "All":
        filtered = [d for d in filtered if d.get("diagram_type") == selected_type]

    # Main content
    if not filtered:
        st.info("No diagrams found. Create one in the Diagram Editor!")

        if st.button("✏️ Go to Editor"):
            st.switch_page("pages/2_Diagram_Editor.py")
    else:
        # Display diagrams in grid
        cols = st.columns(2)

        for idx, diagram in enumerate(filtered):
            with cols[idx % 2]:
                with st.container():
                    # Header
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        visibility = "🌐" if diagram.get("is_public") else "🔒"
                        st.markdown(f"### {visibility} {diagram.get('name', 'Untitled')}")
                    with col2:
                        st.caption(diagram.get("diagram_type", "flowchart"))

                    # Description
                    if diagram.get("description"):
                        st.caption(diagram["description"])

                    # Preview
                    with st.expander("Preview", expanded=False):
                        code = diagram.get("mermaid_code", "")
                        if code:
                            components.html(
                                render_mermaid_with_export(code, 300),
                                height=380,
                                scrolling=True
                            )

                    # Actions
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("✏️ Edit", key=f"edit_{diagram['id']}", use_container_width=True):
                            st.session_state.editor_code = diagram.get("mermaid_code", "")
                            st.session_state.editor_diagram_type = diagram.get("diagram_type", "flowchart")
                            st.switch_page("pages/2_Diagram_Editor.py")

                    with col2:
                        if st.button("📋 Copy", key=f"copy_{diagram['id']}", use_container_width=True):
                            st.toast("Use the preview's copy functionality", icon="ℹ️")

                    with col3:
                        if st.button("🗑️ Delete", key=f"del_{diagram['id']}", use_container_width=True):
                            DiagramRepository.delete(diagram["id"])
                            st.toast(f"Deleted '{diagram.get('name')}'", icon="🗑️")
                            st.rerun()

                    # Metadata
                    created = diagram.get("created_at", "Unknown")
                    st.caption(f"Created: {created}")

                    st.divider()

    # Quick create section
    st.subheader("Quick Create")

    col1, col2 = st.columns(2)

    with col1:
        new_name = st.text_input("Diagram Name", key="quick_name")
        new_type = st.selectbox(
            "Type",
            ["flowchart", "sequence", "class", "state", "er", "gantt", "pie"],
            key="quick_type"
        )

    with col2:
        new_code = st.text_area(
            "Mermaid Code",
            height=120,
            placeholder="Enter Mermaid code...",
            key="quick_code"
        )

    col1, col2 = st.columns(2)
    with col1:
        is_public = st.checkbox("Make Public", key="quick_public")
    with col2:
        if st.button("💾 Save Diagram", type="primary", use_container_width=True):
            if new_name and new_code:
                DiagramRepository.create(
                    name=new_name,
                    mermaid_code=new_code,
                    diagram_type=new_type,
                    is_public=is_public,
                )
                st.toast(f"Created '{new_name}'", icon="✅")
                st.rerun()
            else:
                st.error("Please enter a name and code")


if __name__ == "__main__":
    main()
