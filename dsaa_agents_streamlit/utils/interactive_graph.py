"""
Interactive graph visualization using vis.js
Provides draggable, zoomable network graphs with physics-based layout.
"""

import json
from typing import Dict, List, Optional, Any


def create_vis_network_html(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    height: int = 600,
    physics: bool = True,
    hierarchical: bool = False,
    direction: str = "UD"  # UD, DU, LR, RL
) -> str:
    """
    Create an interactive vis.js network graph.

    Args:
        nodes: List of node dicts with id, label, group, title (tooltip), etc.
        edges: List of edge dicts with from, to, label, arrows, etc.
        height: Height of the graph container
        physics: Enable physics simulation for auto-layout
        hierarchical: Use hierarchical layout
        direction: Layout direction (UD=up-down, LR=left-right, etc.)

    Returns:
        HTML string with embedded vis.js graph
    """

    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    physics_options = """
        physics: {
            enabled: true,
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
                gravitationalConstant: -50,
                centralGravity: 0.01,
                springLength: 150,
                springConstant: 0.08,
                damping: 0.4
            },
            stabilization: {
                enabled: true,
                iterations: 200,
                updateInterval: 25
            }
        },
    """ if physics else "physics: { enabled: false },"

    hierarchical_options = f"""
        layout: {{
            hierarchical: {{
                enabled: true,
                direction: '{direction}',
                sortMethod: 'directed',
                levelSeparation: 150,
                nodeSpacing: 200,
                treeSpacing: 200,
                blockShifting: true,
                edgeMinimization: true
            }}
        }},
    """ if hierarchical else ""

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        #network {{
            width: 100%;
            height: {height}px;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            background: rgba(30, 30, 46, 0.95);
        }}
        .controls {{
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }}
        .control-btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .control-btn:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }}
        .control-btn.secondary {{
            background: rgba(255,255,255,0.1);
        }}
        .legend {{
            display: flex;
            gap: 16px;
            margin-top: 12px;
            flex-wrap: wrap;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: #9fb0d0;
        }}
        .legend-color {{
            width: 14px;
            height: 14px;
            border-radius: 4px;
        }}
        #tooltip {{
            position: absolute;
            background: rgba(30, 30, 46, 0.95);
            border: 1px solid rgba(102, 126, 234, 0.5);
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 13px;
            color: #e0e0e0;
            pointer-events: none;
            display: none;
            max-width: 300px;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
    </style>
</head>
<body>
    <div class="controls">
        <button class="control-btn" onclick="fit()">🔍 Fit View</button>
        <button class="control-btn secondary" onclick="togglePhysics()">⚡ Toggle Physics</button>
        <button class="control-btn secondary" onclick="resetLayout()">🔄 Reset Layout</button>
        <button class="control-btn secondary" onclick="exportPNG()">📥 Export PNG</button>
    </div>

    <div id="network"></div>
    <div id="tooltip"></div>

    <div class="legend">
        <div class="legend-item"><div class="legend-color" style="background: #667eea;"></div> API / UI</div>
        <div class="legend-item"><div class="legend-color" style="background: #f093fb;"></div> Orchestrator</div>
        <div class="legend-item"><div class="legend-color" style="background: #4facfe;"></div> Agents</div>
        <div class="legend-item"><div class="legend-color" style="background: #43e97b;"></div> RAG / Retrieval</div>
        <div class="legend-item"><div class="legend-color" style="background: #fa709a;"></div> Tools</div>
        <div class="legend-item"><div class="legend-color" style="background: #ffecd2;"></div> Data Stores</div>
        <div class="legend-item"><div class="legend-color" style="background: #a8edea;"></div> Governance</div>
        <div class="legend-item"><div class="legend-color" style="background: #d299c2;"></div> Observability</div>
    </div>

    <script>
        const nodes = new vis.DataSet({nodes_json});
        const edges = new vis.DataSet({edges_json});

        const container = document.getElementById('network');
        const tooltip = document.getElementById('tooltip');

        const data = {{ nodes: nodes, edges: edges }};

        const options = {{
            {hierarchical_options}
            {physics_options}
            nodes: {{
                shape: 'box',
                borderWidth: 2,
                borderWidthSelected: 3,
                font: {{
                    size: 14,
                    color: '#ffffff',
                    face: 'Inter, -apple-system, sans-serif',
                    bold: {{ color: '#ffffff' }}
                }},
                shadow: {{
                    enabled: true,
                    color: 'rgba(0,0,0,0.3)',
                    size: 10,
                    x: 3,
                    y: 3
                }},
                margin: {{ top: 10, bottom: 10, left: 15, right: 15 }},
                widthConstraint: {{ minimum: 120, maximum: 200 }}
            }},
            edges: {{
                width: 2,
                color: {{
                    color: 'rgba(150, 150, 200, 0.6)',
                    highlight: '#667eea',
                    hover: '#667eea'
                }},
                arrows: {{
                    to: {{
                        enabled: true,
                        scaleFactor: 0.8,
                        type: 'arrow'
                    }}
                }},
                smooth: {{
                    enabled: true,
                    type: 'curvedCW',
                    roundness: 0.2
                }},
                font: {{
                    size: 11,
                    color: '#9fb0d0',
                    strokeWidth: 3,
                    strokeColor: '#1e1e2e'
                }},
                shadow: {{
                    enabled: true,
                    color: 'rgba(0,0,0,0.2)',
                    size: 5
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200,
                hideEdgesOnDrag: true,
                navigationButtons: true,
                keyboard: {{
                    enabled: true,
                    bindToWindow: false
                }}
            }},
            groups: {{
                api: {{ color: {{ background: '#667eea', border: '#5a6fd6' }} }},
                orchestrator: {{ color: {{ background: '#f093fb', border: '#e080eb' }} }},
                agents: {{ color: {{ background: '#4facfe', border: '#3d9beb' }} }},
                rag: {{ color: {{ background: '#43e97b', border: '#38d46d' }} }},
                tools: {{ color: {{ background: '#fa709a', border: '#e8658c' }} }},
                data: {{ color: {{ background: '#ffecd2', border: '#f0dcc3' }}, font: {{ color: '#333' }} }},
                governance: {{ color: {{ background: '#a8edea', border: '#96dbd8' }}, font: {{ color: '#333' }} }},
                observability: {{ color: {{ background: '#d299c2', border: '#c28ab3' }} }},
                ds: {{ color: {{ background: '#89f7fe', border: '#78e6ed' }}, font: {{ color: '#333' }} }}
            }}
        }};

        const network = new vis.Network(container, data, options);

        let physicsEnabled = {'true' if physics else 'false'};

        // Tooltip on hover
        network.on('hoverNode', function(params) {{
            const node = nodes.get(params.node);
            if (node && node.title) {{
                tooltip.innerHTML = '<strong>' + node.label + '</strong><br>' + node.title;
                tooltip.style.display = 'block';
            }}
        }});

        network.on('blurNode', function() {{
            tooltip.style.display = 'none';
        }});

        container.addEventListener('mousemove', function(e) {{
            tooltip.style.left = (e.offsetX + 15) + 'px';
            tooltip.style.top = (e.offsetY + 15) + 'px';
        }});

        function fit() {{
            network.fit({{ animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }} }});
        }}

        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
        }}

        function resetLayout() {{
            network.setOptions({{ physics: {{ enabled: true }} }});
            setTimeout(() => {{
                network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
                fit();
            }}, 2000);
        }}

        function exportPNG() {{
            const canvas = container.getElementsByTagName('canvas')[0];
            const link = document.createElement('a');
            link.download = 'network-diagram.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        }}

        // Initial fit
        network.once('stabilizationIterationsDone', function() {{
            fit();
        }});
    </script>
</body>
</html>
"""


def build_architecture_network(filters: Dict[str, bool]) -> tuple:
    """
    Build nodes and edges for the architecture network graph.

    Returns:
        Tuple of (nodes, edges)
    """
    nodes = []
    edges = []

    # API / UI Layer
    if filters.get("api", False):
        nodes.extend([
            {"id": "ui", "label": "Web UI / Chat", "group": "api",
             "title": "User interface layer - handles user interactions and displays responses"},
            {"id": "api", "label": "API Gateway", "group": "api",
             "title": "FastAPI gateway - authentication, rate limiting, request routing"},
        ])
        edges.append({"from": "ui", "to": "api", "label": "requests"})

    # Orchestrator
    if filters.get("orchestrator", False):
        nodes.extend([
            {"id": "router", "label": "Router / Policy", "group": "orchestrator",
             "title": "Routes requests to appropriate agents based on intent classification"},
            {"id": "state", "label": "State Store", "group": "orchestrator",
             "title": "Maintains conversation state, context, and session history"},
        ])
        edges.append({"from": "router", "to": "state", "label": "read/write"})

        if filters.get("api", False):
            edges.append({"from": "api", "to": "router", "label": "route"})

    # Agents
    if filters.get("agents", False):
        nodes.extend([
            {"id": "planner", "label": "Planner Agent", "group": "agents",
             "title": "Decomposes complex goals into executable steps"},
            {"id": "specialist", "label": "Specialist Agents", "group": "agents",
             "title": "Domain-specific agents (Policy, DS, Ops, Risk)"},
            {"id": "validator", "label": "Validator / Critic", "group": "agents",
             "title": "Validates outputs, checks for hallucinations, ensures quality"},
        ])
        edges.append({"from": "planner", "to": "specialist", "label": "delegate"})
        edges.append({"from": "specialist", "to": "validator", "label": "verify"})

        if filters.get("orchestrator", False):
            edges.append({"from": "router", "to": "planner", "label": "plan"})
            edges.append({"from": "validator", "to": "router", "label": "result"})

    # RAG / Retrieval
    if filters.get("retrieval", False):
        nodes.extend([
            {"id": "embed", "label": "Embed Query", "group": "rag",
             "title": "Converts query to vector embedding for similarity search"},
            {"id": "search", "label": "Vector Search", "group": "rag",
             "title": "Searches vector database for relevant documents"},
            {"id": "chunks", "label": "Top-K Chunks", "group": "rag",
             "title": "Retrieves most relevant document chunks"},
            {"id": "augment", "label": "Prompt Augment", "group": "rag",
             "title": "Augments prompt with retrieved context"},
        ])
        edges.append({"from": "embed", "to": "search"})
        edges.append({"from": "search", "to": "chunks"})
        edges.append({"from": "chunks", "to": "augment"})

        if filters.get("agents", False):
            edges.append({"from": "specialist", "to": "embed", "label": "query"})
            edges.append({"from": "augment", "to": "specialist", "label": "context"})

    # Tools
    if filters.get("tools", False):
        nodes.extend([
            {"id": "sql_tool", "label": "SQL Tool", "group": "tools",
             "title": "Execute SQL queries against databases"},
            {"id": "doc_tool", "label": "Doc Tool", "group": "tools",
             "title": "Read/parse documents (PDF, DOC, HTML)"},
            {"id": "web_tool", "label": "Web Search", "group": "tools",
             "title": "Search the web for information"},
            {"id": "action_tool", "label": "Action Tool", "group": "tools",
             "title": "Execute actions (API calls, tickets, emails)"},
        ])

        if filters.get("agents", False):
            edges.append({"from": "specialist", "to": "sql_tool", "label": "query", "dashes": True})
            edges.append({"from": "specialist", "to": "doc_tool", "label": "read", "dashes": True})
            edges.append({"from": "specialist", "to": "web_tool", "label": "search", "dashes": True})
            edges.append({"from": "validator", "to": "action_tool", "label": "execute", "dashes": True})

    # Data Stores
    if filters.get("data", False):
        nodes.extend([
            {"id": "vectordb", "label": "Vector DB", "group": "data", "shape": "database",
             "title": "Stores document embeddings for semantic search"},
            {"id": "policydb", "label": "Policy Docs", "group": "data", "shape": "database",
             "title": "Stores policy documents and compliance rules"},
            {"id": "warehouse", "label": "Data Warehouse", "group": "data", "shape": "database",
             "title": "Central data warehouse for analytics"},
            {"id": "logs", "label": "Logs / Traces", "group": "data", "shape": "database",
             "title": "Stores application logs and distributed traces"},
        ])

        if filters.get("retrieval", False):
            edges.append({"from": "search", "to": "vectordb"})
            edges.append({"from": "chunks", "to": "policydb"})

        if filters.get("tools", False):
            edges.append({"from": "sql_tool", "to": "warehouse"})
            edges.append({"from": "doc_tool", "to": "policydb"})

    # Governance
    if filters.get("governance", False):
        nodes.extend([
            {"id": "auth", "label": "AuthN / AuthZ", "group": "governance",
             "title": "Authentication and authorization checks"},
            {"id": "pii", "label": "PII Filter", "group": "governance",
             "title": "Detects and masks personally identifiable information"},
            {"id": "injection", "label": "Injection Guard", "group": "governance",
             "title": "Protects against prompt injection attacks"},
            {"id": "provenance", "label": "Provenance", "group": "governance",
             "title": "Tracks data lineage and citation sources"},
        ])

        if filters.get("api", False):
            edges.append({"from": "api", "to": "auth", "dashes": True})
        if filters.get("agents", False):
            edges.append({"from": "specialist", "to": "pii", "dashes": True})
            edges.append({"from": "specialist", "to": "injection", "dashes": True})
            edges.append({"from": "validator", "to": "provenance", "dashes": True})

    # Observability
    if filters.get("obs", False):
        nodes.extend([
            {"id": "metrics", "label": "Metrics", "group": "observability",
             "title": "Application metrics (latency, throughput, errors)"},
            {"id": "traces", "label": "Traces", "group": "observability",
             "title": "Distributed tracing for request flows"},
            {"id": "eval", "label": "Eval / Tests", "group": "observability",
             "title": "Offline evaluation and regression tests"},
        ])

        if filters.get("api", False):
            edges.append({"from": "api", "to": "metrics", "dashes": True})
        if filters.get("orchestrator", False):
            edges.append({"from": "router", "to": "traces", "dashes": True})
        if filters.get("agents", False):
            edges.append({"from": "validator", "to": "traces", "dashes": True})
        if filters.get("data", False):
            edges.append({"from": "traces", "to": "logs", "dashes": True})

    # DS Workflows
    if filters.get("ds", False):
        nodes.extend([
            {"id": "ds_brief", "label": "Project Brief", "group": "ds",
             "title": "Define problem statement, KPIs, constraints"},
            {"id": "ds_pipeline", "label": "EDA → Model → Eval", "group": "ds",
             "title": "Data science pipeline: exploration, modeling, evaluation"},
            {"id": "ds_deploy", "label": "Packaging", "group": "ds",
             "title": "Package model for batch or realtime deployment"},
        ])
        edges.append({"from": "ds_brief", "to": "ds_pipeline"})
        edges.append({"from": "ds_pipeline", "to": "ds_deploy"})

        if filters.get("agents", False):
            edges.append({"from": "planner", "to": "ds_brief", "label": "initiate"})
            edges.append({"from": "ds_pipeline", "to": "specialist", "label": "assist"})
        if filters.get("tools", False):
            edges.append({"from": "ds_deploy", "to": "action_tool", "label": "deploy"})

    return nodes, edges


def build_agent_flow_network() -> tuple:
    """Build nodes and edges for agent reasoning flow."""

    nodes = [
        {"id": "start", "label": "Goal", "group": "api", "shape": "circle",
         "title": "User provides a goal or query"},
        {"id": "plan", "label": "Plan", "group": "orchestrator",
         "title": "Decompose goal into steps"},
        {"id": "retrieve", "label": "Retrieve", "group": "rag",
         "title": "Fetch relevant context from knowledge base"},
        {"id": "ground", "label": "Ground", "group": "rag",
         "title": "Augment prompt with retrieved context"},
        {"id": "reason", "label": "Reason", "group": "agents",
         "title": "Generate response using LLM"},
        {"id": "validate", "label": "Validate", "group": "governance",
         "title": "Check for hallucinations, verify facts"},
        {"id": "decide", "label": "Decide", "group": "orchestrator",
         "title": "Determine if response is acceptable"},
        {"id": "fallback", "label": "Fallback", "group": "tools",
         "title": "Retry with different approach or escalate"},
        {"id": "act", "label": "Act", "group": "tools",
         "title": "Execute tool calls or return response"},
        {"id": "log", "label": "Log", "group": "observability",
         "title": "Record telemetry and traces"},
        {"id": "end", "label": "Done", "group": "api", "shape": "circle",
         "title": "Return final response to user"},
    ]

    edges = [
        {"from": "start", "to": "plan", "label": "goal"},
        {"from": "plan", "to": "retrieve", "label": "query"},
        {"from": "retrieve", "to": "ground", "label": "chunks"},
        {"from": "ground", "to": "reason", "label": "prompt"},
        {"from": "reason", "to": "validate", "label": "draft"},
        {"from": "validate", "to": "decide", "label": "check"},
        {"from": "decide", "to": "act", "label": "OK"},
        {"from": "decide", "to": "fallback", "label": "retry"},
        {"from": "fallback", "to": "retrieve", "label": "new query"},
        {"from": "act", "to": "log", "label": "telemetry"},
        {"from": "log", "to": "end"},
    ]

    return nodes, edges
