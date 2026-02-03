"""
Diagram Editor Page - Live Mermaid code editor with preview.
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="Diagram Editor | DSAA Agents",
    page_icon="✏️",
    layout="wide",
)

from utils.export import render_mermaid_with_export
from utils.diagram_types import get_all_templates, ALL_DIAGRAM_TYPES
from utils.database import DiagramRepository
from utils.monitoring import log_page_view

log_page_view("Diagram Editor")

# Default diagram
DEFAULT_DIAGRAM = """flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
"""


def init_session_state():
    if "editor_code" not in st.session_state:
        st.session_state.editor_code = DEFAULT_DIAGRAM
    if "editor_diagram_type" not in st.session_state:
        st.session_state.editor_diagram_type = "flowchart"


def main():
    init_session_state()

    st.title("✏️ Diagram Editor")
    st.markdown("Create and edit Mermaid diagrams with live preview.")

    # Sidebar - Templates
    with st.sidebar:
        st.header("Templates")

        # Template category selector
        categories = list(ALL_DIAGRAM_TYPES.keys())
        selected_category = st.selectbox(
            "Category",
            categories,
            format_func=lambda x: ALL_DIAGRAM_TYPES[x]["name"]
        )

        # Template selector
        if selected_category:
            templates = ALL_DIAGRAM_TYPES[selected_category]["templates"]
            template_names = list(templates.keys())

            selected_template = st.selectbox(
                "Template",
                template_names,
                format_func=lambda x: templates[x]["name"]
            )

            if selected_template:
                st.markdown(f"*{templates[selected_template]['description']}*")

                if st.button("Load Template", use_container_width=True):
                    st.session_state.editor_code = templates[selected_template]["code"]
                    st.session_state.editor_diagram_type = selected_category
                    st.toast(f"Loaded: {templates[selected_template]['name']}", icon="📋")
                    st.rerun()

        st.divider()

        # Quick snippets
        st.subheader("Quick Snippets")

        snippets = {
            "Flowchart": "flowchart TD\n    A[Start] --> B[End]",
            "Sequence": "sequenceDiagram\n    A->>B: Message",
            "Class": "classDiagram\n    class MyClass {\n        +method()\n    }",
            "State": "stateDiagram-v2\n    [*] --> State1\n    State1 --> [*]",
            "ER": "erDiagram\n    USER ||--o{ ORDER : places",
            "Gantt": "gantt\n    title Project\n    Task1 :a1, 2024-01-01, 7d",
            "Pie": "pie\n    title Usage\n    \"A\" : 40\n    \"B\" : 60",
        }

        for name, code in snippets.items():
            if st.button(name, key=f"snippet_{name}", use_container_width=True):
                st.session_state.editor_code = code
                st.toast(f"Loaded {name} snippet", icon="📝")
                st.rerun()

        st.divider()

        # Save diagram
        st.subheader("Save Diagram")

        save_name = st.text_input("Diagram Name", placeholder="My Diagram")
        save_desc = st.text_area("Description", placeholder="Optional description...", height=80)
        is_public = st.checkbox("Make Public", value=False)

        if st.button("💾 Save to Library", use_container_width=True, type="primary"):
            if save_name:
                diagram_id = DiagramRepository.create(
                    name=save_name,
                    mermaid_code=st.session_state.editor_code,
                    diagram_type=st.session_state.editor_diagram_type,
                    description=save_desc,
                    is_public=is_public,
                )
                st.toast(f"Saved as '{save_name}'", icon="✅")
            else:
                st.error("Please enter a diagram name")

    # Main content - Editor and Preview
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Mermaid Code")

        # Code editor
        new_code = st.text_area(
            "Edit your diagram code:",
            value=st.session_state.editor_code,
            height=500,
            key="code_editor",
            label_visibility="collapsed",
        )

        if new_code != st.session_state.editor_code:
            st.session_state.editor_code = new_code

        # Editor controls
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.editor_code = DEFAULT_DIAGRAM
                st.rerun()
        with col_b:
            if st.button("📋 Copy Code", use_container_width=True):
                st.toast("Code copied! (Use Ctrl+C in text area)", icon="📋")
        with col_c:
            if st.button("🔍 Format", use_container_width=True):
                # Basic formatting - add consistent indentation
                lines = st.session_state.editor_code.split('\n')
                formatted = '\n'.join(line.strip() for line in lines if line.strip())
                st.session_state.editor_code = formatted
                st.rerun()

    with col2:
        st.subheader("Preview")

        # Render preview
        with st.spinner("Rendering..."):
            components.html(
                render_mermaid_with_export(st.session_state.editor_code, 500),
                height=580,
                scrolling=True
            )

    # Mermaid syntax help
    with st.expander("📖 Mermaid Syntax Help"):
        st.markdown("""
        ### Common Diagram Types

        **Flowchart:**
        ```
        flowchart TD
            A[Rectangle] --> B(Rounded)
            B --> C{Diamond}
            C -->|Yes| D[Result 1]
            C -->|No| E[Result 2]
        ```

        **Sequence Diagram:**
        ```
        sequenceDiagram
            participant A as Alice
            participant B as Bob
            A->>B: Hello
            B-->>A: Hi there!
        ```

        **Class Diagram:**
        ```
        classDiagram
            class Animal {
                +String name
                +eat()
            }
            Animal <|-- Dog
        ```

        **State Diagram:**
        ```
        stateDiagram-v2
            [*] --> Active
            Active --> Inactive : timeout
            Inactive --> Active : wake
            Active --> [*]
        ```

        ### Arrow Types
        - `-->` Solid arrow
        - `-.->` Dotted arrow
        - `==>` Thick arrow
        - `-->>` Open arrow

        ### Shapes
        - `[text]` Rectangle
        - `(text)` Rounded rectangle
        - `{text}` Diamond
        - `([text])` Stadium
        - `[(text)]` Cylinder
        - `((text))` Circle
        """)


if __name__ == "__main__":
    main()
