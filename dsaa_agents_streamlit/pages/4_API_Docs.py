"""
API Documentation Page - REST API reference and testing.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="API Docs | DSAA Agents",
    page_icon="🔌",
    layout="wide",
)

from utils.monitoring import log_page_view

log_page_view("API Docs")

# Custom CSS
st.markdown("""
<style>
    .endpoint-card {
        background: rgba(122, 162, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
    }
    .method-get { color: #61affe; font-weight: bold; }
    .method-post { color: #49cc90; font-weight: bold; }
    .method-put { color: #fca130; font-weight: bold; }
    .method-delete { color: #f93e3e; font-weight: bold; }
    code {
        background: rgba(0,0,0,0.3);
        padding: 2px 6px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    st.title("🔌 REST API Documentation")
    st.markdown("Programmatic access to diagram generation and management.")

    # API Overview
    st.header("Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Base URL:** `http://localhost:8000/api/v1`

        **Authentication:** None required (add your own auth layer for production)

        **Response Format:** JSON

        **Content-Type:** `application/json`
        """)

    with col2:
        st.markdown("""
        **Quick Start:**
        ```bash
        # Start API server
        cd dsaa_agents_streamlit
        uvicorn utils.api:app --reload --port 8000

        # Test endpoint
        curl http://localhost:8000/api/v1/health
        ```
        """)

    st.divider()

    # Endpoints
    st.header("Endpoints")

    # Health
    with st.expander("🏥 Health Check", expanded=True):
        st.markdown('<span class="method-get">GET</span> `/api/v1/health`', unsafe_allow_html=True)
        st.markdown("Check API health status.")

        st.markdown("**Response:**")
        st.code('''{
    "status": "healthy",
    "version": "1.0.0",
    "endpoints": {...}
}''', language="json")

    # Generate Diagram
    with st.expander("📊 Generate Diagram", expanded=True):
        st.markdown('<span class="method-post">POST</span> `/api/v1/diagrams/generate`', unsafe_allow_html=True)
        st.markdown("Generate a Mermaid diagram based on type and filters.")

        st.markdown("**Request Body:**")
        st.code('''{
    "diagram_type": "architecture",  // architecture, agent, ds, complete
    "preset": "all_on",              // Optional: all_on, all_off, rag_agents, ds_pipeline, governance
    "filters": {                     // Optional: custom filters (overridden by preset)
        "api": true,
        "orchestrator": true,
        "agents": true,
        "retrieval": true,
        "tools": true,
        "data": true,
        "governance": true,
        "obs": true,
        "ds": true
    }
}''', language="json")

        st.markdown("**Response:**")
        st.code('''{
    "diagram_type": "architecture",
    "filters": {...},
    "mermaid_code": "flowchart LR\\n..."
}''', language="json")

        st.markdown("**Example:**")
        st.code('''curl -X POST http://localhost:8000/api/v1/diagrams/generate \\
    -H "Content-Type: application/json" \\
    -d '{"diagram_type": "architecture", "preset": "rag_agents"}'
''', language="bash")

    # List Presets
    with st.expander("📋 List Presets"):
        st.markdown('<span class="method-get">GET</span> `/api/v1/diagrams/presets`', unsafe_allow_html=True)
        st.markdown("Get all available filter presets.")

        st.markdown("**Response:**")
        st.code('''{
    "presets": ["all_on", "all_off", "rag_agents", "ds_pipeline", "governance"],
    "details": {
        "all_on": {"api": true, "orchestrator": true, ...},
        ...
    }
}''', language="json")

    # List Diagram Types
    with st.expander("📑 List Diagram Types"):
        st.markdown('<span class="method-get">GET</span> `/api/v1/diagrams/types`', unsafe_allow_html=True)
        st.markdown("Get all available diagram types and templates.")

    # Templates
    with st.expander("📚 Templates"):
        st.markdown('<span class="method-get">GET</span> `/api/v1/templates`', unsafe_allow_html=True)
        st.markdown("List all diagram templates.")

        st.markdown('<span class="method-get">GET</span> `/api/v1/templates/{category}/{template_name}`', unsafe_allow_html=True)
        st.markdown("Get a specific template.")

        st.markdown("**Example:**")
        st.code('''curl http://localhost:8000/api/v1/templates/sequence/api_request_flow''', language="bash")

    # Custom Diagrams CRUD
    with st.expander("💾 Custom Diagrams CRUD"):
        st.markdown("**Create:**")
        st.markdown('<span class="method-post">POST</span> `/api/v1/custom-diagrams`', unsafe_allow_html=True)
        st.code('''{
    "name": "My Diagram",
    "mermaid_code": "flowchart TD\\n    A --> B",
    "diagram_type": "flowchart",
    "description": "Optional description",
    "is_public": false
}''', language="json")

        st.markdown("**List:**")
        st.markdown('<span class="method-get">GET</span> `/api/v1/custom-diagrams`', unsafe_allow_html=True)

        st.markdown("**Get by ID:**")
        st.markdown('<span class="method-get">GET</span> `/api/v1/custom-diagrams/{id}`', unsafe_allow_html=True)

        st.markdown("**Update:**")
        st.markdown('<span class="method-put">PUT</span> `/api/v1/custom-diagrams/{id}`', unsafe_allow_html=True)

        st.markdown("**Delete:**")
        st.markdown('<span class="method-delete">DELETE</span> `/api/v1/custom-diagrams/{id}`', unsafe_allow_html=True)

    # Render
    with st.expander("🖼️ Render Endpoints"):
        st.markdown('<span class="method-post">POST</span> `/api/v1/render/html`', unsafe_allow_html=True)
        st.markdown("Render Mermaid code as HTML with embedded SVG.")

        st.markdown('<span class="method-post">POST</span> `/api/v1/render/preview`', unsafe_allow_html=True)
        st.markdown("Get preview URLs for the diagram (mermaid.ink and mermaid.live).")

        st.markdown("**Request:**")
        st.code('''{
    "mermaid_code": "flowchart TD\\n    A --> B",
    "theme": "dark"
}''', language="json")

    st.divider()

    # Interactive Tester
    st.header("API Tester")

    col1, col2 = st.columns(2)

    with col1:
        endpoint = st.selectbox(
            "Endpoint",
            [
                "GET /api/v1/health",
                "GET /api/v1/diagrams/presets",
                "GET /api/v1/diagrams/types",
                "GET /api/v1/templates",
                "POST /api/v1/diagrams/generate",
            ]
        )

        if "POST" in endpoint:
            body = st.text_area(
                "Request Body (JSON)",
                value='{\n    "diagram_type": "architecture",\n    "preset": "all_on"\n}',
                height=150
            )

        base_url = st.text_input("Base URL", value="http://localhost:8000")

    with col2:
        st.markdown("**Generated cURL command:**")

        method, path = endpoint.split(" ", 1)
        curl_cmd = f"curl -X {method} {base_url}{path}"

        if "POST" in endpoint:
            curl_cmd += f" \\\n    -H 'Content-Type: application/json' \\\n    -d '{body}'"

        st.code(curl_cmd, language="bash")

    st.divider()

    # Running the API
    st.header("Running the API Server")

    st.markdown("""
    The API runs separately from the Streamlit app using FastAPI + Uvicorn.

    **Option 1: Development mode**
    ```bash
    cd dsaa_agents_streamlit
    uvicorn utils.api:app --reload --port 8000
    ```

    **Option 2: Production mode**
    ```bash
    uvicorn utils.api:app --host 0.0.0.0 --port 8000 --workers 4
    ```

    **Option 3: Run both Streamlit and API**
    ```bash
    # Terminal 1 - Streamlit
    streamlit run app.py --server.port 8501

    # Terminal 2 - API
    uvicorn utils.api:app --port 8000
    ```

    **Interactive Docs:**
    - Swagger UI: `http://localhost:8000/api/docs`
    - ReDoc: `http://localhost:8000/api/redoc`
    """)


if __name__ == "__main__":
    main()
