"""
Mermaid diagram blocks and builders for the DSAA Agents Streamlit application.
"""

# Architecture diagram blocks by tag
ARCH_BLOCKS = {
    "api": """
subgraph API["API / UI Layer (Request Surface)"]
  UI[Web UI / Chat UI]
  API1[FastAPI / Gateway]
  UI --> API1
end
""",
    "orchestrator": """
subgraph ORCH["Orchestrator (Control Plane)"]
  ROUTER[Router / Policy]
  STATE[State Store]
  ROUTER <--> STATE
end
""",
    "agents": """
subgraph AG["Agents (Intent + Reasoning)"]
  PLAN[Planner Agent]
  SPEC["Specialized Agents<br/>(Policy, DS, Ops, Risk)"]
  VALID[Validator / Critic]
  PLAN --> SPEC
  SPEC --> VALID
end
""",
    "retrieval": """
subgraph RAG["Retrieval (RAG Data Plane)"]
  EMB[Embed Query]
  VEC[Vector Search]
  CHUNK[Top-K Chunks]
  AUG[Prompt Augmentation]
  EMB --> VEC --> CHUNK --> AUG
end
""",
    "tools": """
subgraph TOOLS["Tools / Actions (Execution)"]
  DBT["DB Tool<br/>(SQL/NoSQL/Warehouse)"]
  FILE["Doc Tool<br/>(PDF/DOC/HTML)"]
  WEB[Web Search Tool]
  ACT["Action Tool<br/>(API calls / tickets / emails)"]
end
""",
    "data": """
subgraph DATA["Data Stores"]
  VDB[(Vector DB)]
  POL[(Policy Docs)]
  DWH[(Warehouse / Lake)]
  LOGS[(Logs / Traces)]
end
""",
    "governance": """
subgraph GOV["Governance (Safety Rails)"]
  AUTH[AuthN/AuthZ]
  PII[PII / Secrets Filter]
  INJ[Prompt Injection Guard]
  PROV[Provenance / Citation Policy]
end
""",
    "obs": """
subgraph OBS["Observability"]
  MET[Metrics]
  TRC[Traces]
  EVAL[Offline Eval / Regression Tests]
end
""",
    "ds": """
subgraph DSX["DS Project Workflows (as a workload)"]
  DSREQ[Project Brief / Hypothesis]
  DSPIP["EDA, Features, Model, Eval"]
  DSPKG["Packaging<br/>(Batch/Realtime)"]
end
"""
}

# Agent state diagram
AGENT_DIAGRAM = """stateDiagram-v2
  [*] --> Plan : goal
  Plan --> Retrieve : step / query
  Retrieve --> Ground : chunks
  Ground --> Reason : augmented prompt
  Reason --> Validate : draft answer
  Validate --> Decide : OK
  Validate --> Fallback : insufficient / conflict
  Fallback --> Retrieve : retry / tier-switch
  Decide --> Act : tool call / report
  Act --> Log : telemetry
  Log --> [*]
"""

# DS Project Depth diagram blocks
DS_BLOCKS = {
    "main": """flowchart TB
  subgraph DS["Data Science Project Depth (Agentized)"]
    BRIEF["Project Brief Agent<br/>(scope, KPI, constraints)"]
    DATAAUD["Data QA Agent<br/>(nulls, drift, leakage checks)"]
    EDA["EDA Agent<br/>profiles, segments, anomalies"]
    FEAT["Feature Agent<br/>transforms, selection, leakage guard"]
    TRAIN["Training Agent<br/>CV, tuning, baselines"]
    EVAL["Evaluation Agent<br/>metrics, stability, fairness"]
    PKG["Packaging Agent<br/>batch/realtime, schema contracts"]
    DEP["Deployment Agent<br/>CI/CD, infra, rollout"]
    MON["Monitoring Agent<br/>drift, quality, alarms"]
    BRIEF --> DATAAUD --> EDA --> FEAT --> TRAIN --> EVAL --> PKG --> DEP --> MON
  end

  subgraph RAGX["RAG Grounding (Reusable)"]
    RET[Retriever]
    KB[(Domain KB / Policy / Docs)]
    RET <--> KB
  end

  subgraph TOOLX["Tools (Reusable)"]
    SQL[SQL Tool]
    PY[Python Tool]
    FS[File Tool]
    VIZ[Viz Tool]
  end

  BRIEF --> RET
  DATAAUD --> SQL
  EDA --> PY
  FEAT --> PY
  TRAIN --> PY
  EVAL --> VIZ
  PKG --> FS
  DEP --> FS
  MON --> SQL
""",
    "governance_overlay": """
  subgraph GOV["Governance Overlay (applies to ALL agents)"]
    SCHEMA["Schema contracts<br/>(Pydantic / JSON schema)"]
    PII2[PII masking]
    AUDIT[Audit logs]
  end
  BRIEF -.-> GOV
  EVAL -.-> GOV
  PKG -.-> GOV
"""
}

# Complete static diagram from v2
COMPLETE_DIAGRAM = """flowchart LR

%% =======================
%% API / UI LAYER
%% =======================
subgraph API["API / UI Layer (Request Surface)"]
  UI[Web UI / Chat UI]
  API1[FastAPI / Gateway]
  UI --> API1
end

%% =======================
%% ORCHESTRATOR
%% =======================
subgraph ORCH["Orchestrator (Control Plane)"]
  ROUTER[Router / Policy Engine]
  STATE[State Store]
  ROUTER <--> STATE
end

%% =======================
%% AGENTS
%% =======================
subgraph AG["Agents (Intent + Reasoning)"]
  PLAN[Planner Agent]
  SPEC["Specialized Agents<br/>(Policy, DS, Ops, Risk)"]
  VALID[Validator / Critic]
  PLAN --> SPEC --> VALID
end

%% =======================
%% RAG DATA PLANE
%% =======================
subgraph RAG["Retrieval (RAG Data Plane)"]
  EMB[Embed Query]
  VEC[Vector Search]
  CHUNK[Top-K Chunks]
  AUG[Prompt Augmentation]
  EMB --> VEC --> CHUNK --> AUG
end

%% =======================
%% TOOLS / ACTIONS
%% =======================
subgraph TOOLS["Tools / Actions (Execution)"]
  DBT["DB Tool<br/>(SQL / NoSQL / Warehouse)"]
  FILE["Doc Tool<br/>(PDF / DOC / HTML)"]
  WEB[Web Search Tool]
  ACT["Actions<br/>(APIs, Tickets, Emails)"]
end

%% =======================
%% DATA STORES
%% =======================
subgraph DATA["Data Stores"]
  VDB[(Vector DB)]
  POL[(Policy Docs)]
  DWH[(Warehouse / Lake)]
  LOGS[(Logs / Traces)]
end

%% =======================
%% GOVERNANCE
%% =======================
subgraph GOV["Governance (Safety Rails)"]
  AUTH[AuthN / AuthZ]
  PII[PII & Secrets Filter]
  INJ[Prompt Injection Guard]
  PROV[Provenance / Citation Policy]
end

%% =======================
%% OBSERVABILITY
%% =======================
subgraph OBS["Observability"]
  MET[Metrics]
  TRC[Traces]
  EVAL[Offline Eval / Regression Tests]
end

%% =======================
%% DS WORKLOAD
%% =======================
subgraph DSX["Data Science Project (Workload)"]
  DSREQ[Problem Statement / Hypothesis]
  DSPIP["EDA, Features, Model, Eval"]
  DSPKG["Packaging<br/>(Batch / Realtime)"]
end

%% =======================
%% CROSS-LINKS
%% =======================
API1 --> ROUTER
ROUTER --> PLAN
VALID --> ROUTER

SPEC --> EMB
AUG --> SPEC

VEC <--> VDB
CHUNK --> POL

SPEC --> DBT
SPEC --> FILE
SPEC --> WEB
VALID --> ACT

DBT <--> DWH
FILE <--> POL
ACT --> DWH

API1 --> MET
ROUTER --> TRC
VALID --> TRC
ACT --> TRC
TRC --> LOGS

API1 --> AUTH
SPEC --> PII
SPEC --> INJ
VALID --> PROV

PLAN --> DSREQ
DSREQ --> DSPIP
DSPIP --> DSPKG
DSPKG --> ACT
"""

# Filter preset configurations
PRESETS = {
    "all_on": {
        "api": True,
        "orchestrator": True,
        "agents": True,
        "retrieval": True,
        "tools": True,
        "data": True,
        "governance": True,
        "obs": True,
        "ds": True,
    },
    "all_off": {
        "api": False,
        "orchestrator": False,
        "agents": False,
        "retrieval": False,
        "tools": False,
        "data": False,
        "governance": False,
        "obs": False,
        "ds": False,
    },
    "rag_agents": {
        "api": True,
        "orchestrator": True,
        "agents": True,
        "retrieval": True,
        "tools": True,
        "data": True,
        "governance": True,
        "obs": True,
        "ds": False,
    },
    "ds_pipeline": {
        "api": False,
        "orchestrator": False,
        "agents": True,
        "retrieval": True,
        "tools": True,
        "data": True,
        "governance": True,
        "obs": True,
        "ds": True,
    },
    "governance": {
        "api": True,
        "orchestrator": True,
        "agents": True,
        "retrieval": True,
        "tools": True,
        "data": True,
        "governance": True,
        "obs": True,
        "ds": False,
    },
}


def build_architecture_diagram(filters: dict) -> str:
    """
    Constructs filtered architecture diagram with cross-links.

    Args:
        filters: Dictionary of tag -> bool for enabled/disabled blocks

    Returns:
        Mermaid diagram string
    """
    diagram = "flowchart LR\n%% === Agentic RAG Platform: Separation of Concerns ===\n"

    # Add blocks in consistent order
    block_order = ["api", "orchestrator", "agents", "retrieval", "tools", "data", "governance", "obs", "ds"]

    for tag in block_order:
        if filters.get(tag, False):
            diagram += ARCH_BLOCKS[tag]

    # Add cross-links (only if both endpoints are enabled)
    diagram += "\n%% Cross-links (only show if both ends enabled)\n"

    def has(tag):
        return filters.get(tag, False)

    # API <-> Orchestrator
    if has("api") and has("orchestrator"):
        diagram += "API1 --> ROUTER\n"

    # Orchestrator <-> Agents
    if has("orchestrator") and has("agents"):
        diagram += "ROUTER --> PLAN\nVALID --> ROUTER\n"

    # Agents <-> Retrieval
    if has("agents") and has("retrieval"):
        diagram += "SPEC --> EMB\nAUG --> SPEC\n"

    # Retrieval <-> Data
    if has("retrieval") and has("data"):
        diagram += "VEC <--> VDB\nCHUNK --> POL\n"

    # Tools <-> Agents
    if has("tools") and has("agents"):
        diagram += "SPEC --> DBT\nSPEC --> FILE\nSPEC --> WEB\nVALID --> ACT\n"

    # Tools <-> Data
    if has("tools") and has("data"):
        diagram += "DBT <--> DWH\nFILE <--> POL\nWEB --> POL\nACT --> DWH\n"

    # Observability links
    if has("obs"):
        obs_links = []
        if has("api"):
            obs_links.append("API1 --> MET")
        if has("orchestrator"):
            obs_links.append("ROUTER --> TRC")
        if has("agents"):
            obs_links.append("VALID --> TRC")
        if has("tools"):
            obs_links.append("ACT --> TRC")
        if has("data"):
            obs_links.append("TRC --> LOGS")
        diagram += "\n".join(obs_links) + "\n" if obs_links else ""

    # Governance links
    if has("governance"):
        gov_links = []
        if has("api"):
            gov_links.append("API1 --> AUTH")
        if has("agents"):
            gov_links.append("SPEC --> PII")
            gov_links.append("SPEC --> INJ")
            gov_links.append("VALID --> PROV")
        diagram += "\n".join(gov_links) + "\n" if gov_links else ""

    # DS <-> Agents
    if has("ds") and has("agents"):
        diagram += "PLAN --> DSREQ\nDSPIP --> SPEC\nDSPKG --> ACT\n"

    return diagram


def build_agent_diagram(filters: dict) -> str:
    """
    Returns agent state diagram if agents filter is enabled.

    Args:
        filters: Dictionary of tag -> bool for enabled/disabled blocks

    Returns:
        Mermaid diagram string
    """
    if filters.get("agents", False):
        return AGENT_DIAGRAM
    else:
        return "flowchart TB\nA[Enable 'Agents' to view the Agent Graph]"


def build_ds_diagram(filters: dict) -> str:
    """
    Returns DS pipeline diagram with optional governance overlay.

    Args:
        filters: Dictionary of tag -> bool for enabled/disabled blocks

    Returns:
        Mermaid diagram string
    """
    if filters.get("ds", False):
        diagram = DS_BLOCKS["main"]
        if filters.get("governance", False):
            diagram += "\n" + DS_BLOCKS["governance_overlay"]
        return diagram
    else:
        return "flowchart TB\nA[Enable 'DS Project Depth' to view the DS pipeline]"
