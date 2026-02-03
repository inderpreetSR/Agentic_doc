"""
Additional diagram types: Sequence, ER, Class, Gantt, etc.
"""

# Sequence Diagram Templates
SEQUENCE_DIAGRAMS = {
    "api_request_flow": {
        "name": "API Request Flow",
        "description": "Shows the flow of an API request through the system",
        "code": """sequenceDiagram
    participant Client
    participant API Gateway
    participant Auth Service
    participant Orchestrator
    participant Agent
    participant RAG
    participant Database

    Client->>API Gateway: HTTP Request
    API Gateway->>Auth Service: Validate Token
    Auth Service-->>API Gateway: Token Valid
    API Gateway->>Orchestrator: Forward Request
    Orchestrator->>Agent: Route to Agent
    Agent->>RAG: Query Knowledge Base
    RAG->>Database: Vector Search
    Database-->>RAG: Relevant Chunks
    RAG-->>Agent: Augmented Context
    Agent-->>Orchestrator: Response
    Orchestrator-->>API Gateway: Formatted Response
    API Gateway-->>Client: HTTP Response
"""
    },
    "agent_reasoning": {
        "name": "Agent Reasoning Loop",
        "description": "Shows the internal reasoning process of an agent",
        "code": """sequenceDiagram
    participant User
    participant Planner
    participant Retriever
    participant Reasoner
    participant Validator
    participant Tools

    User->>Planner: Query
    Planner->>Planner: Decompose into steps

    loop For each step
        Planner->>Retriever: Get context
        Retriever-->>Planner: Relevant docs
        Planner->>Reasoner: Reason with context
        Reasoner->>Validator: Validate output

        alt Valid
            Validator-->>Reasoner: Approved
        else Invalid
            Validator->>Retriever: Request more context
        end

        opt Needs tool
            Reasoner->>Tools: Execute action
            Tools-->>Reasoner: Result
        end
    end

    Planner-->>User: Final Answer
"""
    },
    "data_pipeline": {
        "name": "Data Pipeline Flow",
        "description": "Shows data flowing through a processing pipeline",
        "code": """sequenceDiagram
    participant Source as Data Source
    participant Ingestion
    participant Transform
    participant Validate
    participant Store as Data Store
    participant Monitor

    Source->>Ingestion: Raw Data
    Ingestion->>Monitor: Log ingestion start
    Ingestion->>Transform: Cleaned Data
    Transform->>Validate: Transformed Data

    alt Validation Passed
        Validate->>Store: Valid Data
        Store->>Monitor: Log success
    else Validation Failed
        Validate->>Monitor: Log errors
        Validate->>Source: Request retry
    end
"""
    }
}

# ER Diagram Templates
ER_DIAGRAMS = {
    "agent_system": {
        "name": "Agent System Schema",
        "description": "Database schema for an agent-based system",
        "code": """erDiagram
    USERS ||--o{ SESSIONS : has
    USERS ||--o{ CUSTOM_DIAGRAMS : creates
    USERS ||--o{ PREFERENCES : has

    SESSIONS ||--o{ MESSAGES : contains
    SESSIONS ||--o{ AGENT_RUNS : triggers

    AGENT_RUNS ||--o{ TOOL_CALLS : makes
    AGENT_RUNS ||--o{ RETRIEVALS : performs

    MESSAGES {
        int id PK
        int session_id FK
        string role
        text content
        timestamp created_at
    }

    USERS {
        int id PK
        string email
        string name
        timestamp created_at
    }

    SESSIONS {
        int id PK
        int user_id FK
        string status
        timestamp created_at
    }

    AGENT_RUNS {
        int id PK
        int session_id FK
        string agent_type
        string status
        json metadata
        timestamp started_at
        timestamp completed_at
    }

    TOOL_CALLS {
        int id PK
        int agent_run_id FK
        string tool_name
        json input
        json output
        timestamp called_at
    }

    RETRIEVALS {
        int id PK
        int agent_run_id FK
        string query
        json results
        float score
        timestamp retrieved_at
    }

    CUSTOM_DIAGRAMS {
        int id PK
        int user_id FK
        string name
        text mermaid_code
        boolean is_public
        timestamp created_at
    }

    PREFERENCES {
        int id PK
        int user_id FK
        json settings
        timestamp updated_at
    }
"""
    },
    "ml_pipeline": {
        "name": "ML Pipeline Schema",
        "description": "Database schema for ML pipeline tracking",
        "code": """erDiagram
    PROJECTS ||--o{ EXPERIMENTS : contains
    EXPERIMENTS ||--o{ RUNS : has
    RUNS ||--o{ METRICS : records
    RUNS ||--o{ ARTIFACTS : produces
    RUNS ||--o{ PARAMETERS : uses

    PROJECTS {
        int id PK
        string name
        string description
        timestamp created_at
    }

    EXPERIMENTS {
        int id PK
        int project_id FK
        string name
        string hypothesis
        string status
    }

    RUNS {
        int id PK
        int experiment_id FK
        string run_name
        string status
        timestamp started_at
        timestamp completed_at
    }

    METRICS {
        int id PK
        int run_id FK
        string name
        float value
        int step
    }

    ARTIFACTS {
        int id PK
        int run_id FK
        string name
        string path
        string type
    }

    PARAMETERS {
        int id PK
        int run_id FK
        string name
        string value
    }
"""
    }
}

# Class Diagram Templates
CLASS_DIAGRAMS = {
    "agent_architecture": {
        "name": "Agent Architecture Classes",
        "description": "Class diagram for agent system architecture",
        "code": """classDiagram
    class Agent {
        <<abstract>>
        +String name
        +String description
        +List~Tool~ tools
        +run(query) Response
        +plan(goal) List~Step~
    }

    class PlannerAgent {
        +decompose(goal) List~Task~
        +prioritize(tasks) List~Task~
        +route(task) Agent
    }

    class SpecializedAgent {
        +String specialty
        +execute(task) Result
        +validate(result) bool
    }

    class RAGAgent {
        +Retriever retriever
        +retrieve(query) List~Document~
        +augment(query, docs) Prompt
    }

    class Tool {
        <<interface>>
        +String name
        +String description
        +execute(input) Output
    }

    class SQLTool {
        +Connection db
        +query(sql) Results
    }

    class APITool {
        +String endpoint
        +call(params) Response
    }

    class Orchestrator {
        +List~Agent~ agents
        +StateStore state
        +route(request) Agent
        +execute(request) Response
    }

    Agent <|-- PlannerAgent
    Agent <|-- SpecializedAgent
    Agent <|-- RAGAgent
    Tool <|.. SQLTool
    Tool <|.. APITool
    Agent "1" *-- "many" Tool
    Orchestrator "1" *-- "many" Agent
"""
    },
    "data_models": {
        "name": "Data Models",
        "description": "Class diagram for data models",
        "code": """classDiagram
    class BaseModel {
        <<abstract>>
        +int id
        +datetime created_at
        +datetime updated_at
        +save()
        +delete()
    }

    class User {
        +String email
        +String name
        +String password_hash
        +authenticate(password) bool
        +get_preferences() Preferences
    }

    class Diagram {
        +String name
        +String description
        +String mermaid_code
        +DiagramType type
        +bool is_public
        +render() SVG
        +export(format) File
    }

    class Session {
        +User user
        +String status
        +List~Message~ messages
        +add_message(content)
        +get_history() List
    }

    class Message {
        +Session session
        +String role
        +String content
    }

    BaseModel <|-- User
    BaseModel <|-- Diagram
    BaseModel <|-- Session
    BaseModel <|-- Message
    User "1" -- "many" Diagram
    User "1" -- "many" Session
    Session "1" -- "many" Message
"""
    }
}

# Gantt Chart Templates
GANTT_DIAGRAMS = {
    "ml_project": {
        "name": "ML Project Timeline",
        "description": "Gantt chart for ML project phases",
        "code": """gantt
    title ML Project Timeline
    dateFormat  YYYY-MM-DD

    section Discovery
    Problem Definition     :done, d1, 2024-01-01, 7d
    Data Assessment        :done, d2, after d1, 5d
    Feasibility Study      :done, d3, after d2, 3d

    section Data Preparation
    Data Collection        :active, dp1, after d3, 10d
    Data Cleaning          :dp2, after dp1, 7d
    Feature Engineering    :dp3, after dp2, 10d

    section Modeling
    Baseline Models        :m1, after dp3, 5d
    Model Selection        :m2, after m1, 7d
    Hyperparameter Tuning  :m3, after m2, 7d

    section Evaluation
    Model Validation       :e1, after m3, 5d
    A/B Testing           :e2, after e1, 14d

    section Deployment
    Packaging             :dep1, after e2, 5d
    CI/CD Setup           :dep2, after dep1, 3d
    Production Deploy     :milestone, dep3, after dep2, 0d

    section Monitoring
    Setup Monitoring      :mon1, after dep3, 5d
    Drift Detection       :mon2, after mon1, 30d
"""
    },
    "sprint_plan": {
        "name": "Sprint Planning",
        "description": "Two-week sprint plan",
        "code": """gantt
    title Sprint 23 - Agent Features
    dateFormat  YYYY-MM-DD

    section Backend
    API endpoints          :b1, 2024-02-01, 3d
    Database models        :b2, 2024-02-01, 2d
    Agent integration      :b3, after b1, 4d

    section Frontend
    UI components          :f1, 2024-02-01, 4d
    State management       :f2, after f1, 2d
    API integration        :f3, after f2, 2d

    section Testing
    Unit tests             :t1, after b3, 2d
    Integration tests      :t2, after f3, 2d
    E2E tests              :t3, after t2, 2d

    section Release
    Code review            :r1, after t3, 1d
    Deploy to staging      :r2, after r1, 1d
    Production release     :milestone, r3, after r2, 0d
"""
    }
}

# Pie Chart Templates
PIE_DIAGRAMS = {
    "system_usage": {
        "name": "System Usage Distribution",
        "description": "Pie chart showing system component usage",
        "code": """pie showData
    title System Resource Usage
    "RAG Retrieval" : 35
    "Agent Reasoning" : 25
    "Tool Execution" : 20
    "API Processing" : 12
    "Other" : 8
"""
    },
    "error_distribution": {
        "name": "Error Distribution",
        "description": "Distribution of error types",
        "code": """pie showData
    title Error Types Distribution
    "Validation Errors" : 40
    "Timeout Errors" : 25
    "Auth Errors" : 15
    "Rate Limit" : 12
    "Unknown" : 8
"""
    }
}

# Combine all diagram types
ALL_DIAGRAM_TYPES = {
    "sequence": {
        "name": "Sequence Diagrams",
        "description": "Show interactions between components over time",
        "templates": SEQUENCE_DIAGRAMS
    },
    "er": {
        "name": "ER Diagrams",
        "description": "Entity-Relationship diagrams for database design",
        "templates": ER_DIAGRAMS
    },
    "class": {
        "name": "Class Diagrams",
        "description": "Object-oriented class structures",
        "templates": CLASS_DIAGRAMS
    },
    "gantt": {
        "name": "Gantt Charts",
        "description": "Project timelines and scheduling",
        "templates": GANTT_DIAGRAMS
    },
    "pie": {
        "name": "Pie Charts",
        "description": "Distribution and proportion visualization",
        "templates": PIE_DIAGRAMS
    }
}


def get_all_templates() -> dict:
    """Get all diagram templates organized by type."""
    return ALL_DIAGRAM_TYPES


def get_template(diagram_type: str, template_name: str) -> dict:
    """Get a specific template by type and name."""
    if diagram_type in ALL_DIAGRAM_TYPES:
        templates = ALL_DIAGRAM_TYPES[diagram_type]["templates"]
        if template_name in templates:
            return templates[template_name]
    return None
