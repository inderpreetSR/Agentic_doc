"""
Improved Mermaid diagram styling with better colors, curved links, and spacing.
"""

import json


def render_styled_mermaid(mermaid_code: str, height_px: int = 600) -> str:
    """
    Render Mermaid diagram with improved styling.
    - Curved/smooth arrows
    - Better color scheme
    - Improved spacing
    - Cleaner fonts
    """
    code_escaped = json.dumps(mermaid_code)

    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    body {{
      margin: 0;
      padding: 12px;
      background: transparent;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .mermaid {{
      display: flex;
      justify-content: center;
    }}
    .mermaid svg {{
      max-width: 100%;
      height: auto;
    }}
    .export-buttons {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      justify-content: flex-end;
    }}
    .export-btn {{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 6px 14px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 13px;
      font-weight: 500;
      transition: transform 0.2s, box-shadow 0.2s;
    }}
    .export-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }}
    .export-btn.svg {{
      background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }}
  </style>
</head>
<body>
  <div class="export-buttons">
    <button class="export-btn svg" onclick="exportDiagram('svg')">Download SVG</button>
    <button class="export-btn" onclick="exportDiagram('png')">Download PNG</button>
  </div>
  <div class="mermaid" id="mermaid-root"></div>

  <script>
    // Enhanced Mermaid configuration for better visuals
    mermaid.initialize({{
      startOnLoad: false,
      theme: 'dark',
      securityLevel: 'loose',
      flowchart: {{
        curve: 'basis',           // Smooth curved lines
        padding: 20,              // More padding
        nodeSpacing: 50,          // Space between nodes
        rankSpacing: 80,          // Space between ranks
        htmlLabels: true,
        useMaxWidth: false
      }},
      themeVariables: {{
        // Background
        background: 'transparent',
        mainBkg: '#1e1e2e',

        // Primary colors
        primaryColor: '#667eea',
        primaryTextColor: '#ffffff',
        primaryBorderColor: '#764ba2',

        // Secondary colors
        secondaryColor: '#4facfe',
        secondaryTextColor: '#ffffff',
        secondaryBorderColor: '#00f2fe',

        // Tertiary colors
        tertiaryColor: '#43e97b',
        tertiaryTextColor: '#1e1e2e',
        tertiaryBorderColor: '#38ef7d',

        // Lines and arrows
        lineColor: '#9fb0d0',
        arrowheadColor: '#9fb0d0',

        // Text
        textColor: '#e0e0e0',

        // Nodes
        nodeBorder: '#667eea',
        clusterBkg: 'rgba(102, 126, 234, 0.1)',
        clusterBorder: 'rgba(102, 126, 234, 0.3)',

        // Special nodes
        edgeLabelBackground: 'rgba(30, 30, 46, 0.8)',

        // Font
        fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, sans-serif',
        fontSize: '14px'
      }}
    }});

    const code = {code_escaped};
    const container = document.getElementById('mermaid-root');
    let renderedSvg = '';

    mermaid.render('mermaid-svg', code).then(function({{ svg }}) {{
      container.innerHTML = svg;
      renderedSvg = svg;

      // Post-process SVG for additional styling
      const svgElement = container.querySelector('svg');
      if (svgElement) {{
        // Add drop shadow filter
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        defs.innerHTML = `
          <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="rgba(0,0,0,0.3)"/>
          </filter>
        `;
        svgElement.insertBefore(defs, svgElement.firstChild);

        // Apply shadow to nodes
        svgElement.querySelectorAll('.node rect, .node polygon, .node circle').forEach(node => {{
          node.style.filter = 'url(#dropShadow)';
        }});

        // Improve edge styling
        svgElement.querySelectorAll('.edge path').forEach(edge => {{
          edge.style.strokeWidth = '2px';
        }});
      }}
    }}).catch(function(err) {{
      container.innerHTML = '<pre style="color:#e06c75; padding: 20px;">Error: ' + err.message + '</pre>';
    }});

    function exportDiagram(format) {{
      if (!renderedSvg) {{
        alert('Diagram not ready');
        return;
      }}

      if (format === 'svg') {{
        const blob = new Blob([renderedSvg], {{type: 'image/svg+xml'}});
        downloadBlob(blob, 'diagram.svg');
      }} else {{
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = function() {{
          canvas.width = img.width * 2;
          canvas.height = img.height * 2;
          ctx.fillStyle = '#1e1e2e';
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

          canvas.toBlob(function(blob) {{
            downloadBlob(blob, 'diagram.png');
          }}, 'image/png');
        }};

        img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(renderedSvg)));
      }}
    }}

    function downloadBlob(blob, filename) {{
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}
  </script>
</body>
</html>
"""


# Improved diagram definitions with better styling hints
STYLED_ARCH_DIAGRAM = """%%{init: {'theme': 'dark', 'flowchart': {'curve': 'basis'}}}%%
flowchart LR
    subgraph API["🌐 API Layer"]
        direction TB
        UI["Web UI"]
        GW["API Gateway"]
        UI --> GW
    end

    subgraph ORCH["🎯 Orchestrator"]
        direction TB
        RT["Router"]
        ST[("State")]
        RT <--> ST
    end

    subgraph AGENTS["🤖 Agents"]
        direction TB
        PL["Planner"]
        SP["Specialists"]
        VL["Validator"]
        PL --> SP --> VL
    end

    subgraph RAG["📚 RAG"]
        direction TB
        EM["Embed"]
        VS["Search"]
        CH["Chunks"]
        AU["Augment"]
        EM --> VS --> CH --> AU
    end

    subgraph TOOLS["🔧 Tools"]
        direction TB
        SQL["SQL"]
        DOC["Docs"]
        WEB["Web"]
        ACT["Actions"]
    end

    subgraph DATA["💾 Data"]
        direction TB
        VDB[("Vectors")]
        POL[("Policies")]
        DWH[("Warehouse")]
    end

    subgraph GOV["🛡️ Governance"]
        direction TB
        AUTH["Auth"]
        PII["PII Filter"]
        INJ["Injection Guard"]
    end

    subgraph OBS["📊 Observability"]
        direction TB
        MET["Metrics"]
        TRC["Traces"]
    end

    %% Main flow
    GW --> RT
    RT --> PL
    VL --> RT

    %% RAG connections
    SP --> EM
    AU --> SP

    %% Data connections
    VS <--> VDB
    CH --> POL

    %% Tool connections
    SP -.-> SQL
    SP -.-> DOC
    SP -.-> WEB
    VL -.-> ACT

    %% Data store connections
    SQL <--> DWH
    DOC <--> POL

    %% Governance
    GW -.-> AUTH
    SP -.-> PII
    SP -.-> INJ

    %% Observability
    GW -.-> MET
    RT -.-> TRC

    %% Styling
    classDef api fill:#667eea,stroke:#5a6fd6,color:#fff
    classDef orch fill:#f093fb,stroke:#e080eb,color:#fff
    classDef agents fill:#4facfe,stroke:#3d9beb,color:#fff
    classDef rag fill:#43e97b,stroke:#38d46d,color:#1e1e2e
    classDef tools fill:#fa709a,stroke:#e8658c,color:#fff
    classDef data fill:#ffecd2,stroke:#f0dcc3,color:#333
    classDef gov fill:#a8edea,stroke:#96dbd8,color:#333
    classDef obs fill:#d299c2,stroke:#c28ab3,color:#fff

    class UI,GW api
    class RT,ST orch
    class PL,SP,VL agents
    class EM,VS,CH,AU rag
    class SQL,DOC,WEB,ACT tools
    class VDB,POL,DWH data
    class AUTH,PII,INJ gov
    class MET,TRC obs
"""


STYLED_AGENT_FLOW = """%%{init: {'theme': 'dark', 'flowchart': {'curve': 'basis'}}}%%
flowchart TD
    START(("🎯 Goal"))
    PLAN["📋 Plan"]
    RETRIEVE["🔍 Retrieve"]
    GROUND["📄 Ground"]
    REASON["🧠 Reason"]
    VALIDATE["✅ Validate"]
    DECIDE{"🤔 Decide"}
    FALLBACK["🔄 Fallback"]
    ACT["⚡ Act"]
    LOG["📊 Log"]
    END(("✨ Done"))

    START --> PLAN
    PLAN --> RETRIEVE
    RETRIEVE --> GROUND
    GROUND --> REASON
    REASON --> VALIDATE
    VALIDATE --> DECIDE

    DECIDE -->|"OK"| ACT
    DECIDE -->|"Retry"| FALLBACK
    FALLBACK --> RETRIEVE

    ACT --> LOG
    LOG --> END

    %% Styling
    classDef startEnd fill:#667eea,stroke:#5a6fd6,color:#fff
    classDef process fill:#4facfe,stroke:#3d9beb,color:#fff
    classDef decision fill:#f093fb,stroke:#e080eb,color:#fff
    classDef fallback fill:#fa709a,stroke:#e8658c,color:#fff
    classDef action fill:#43e97b,stroke:#38d46d,color:#1e1e2e

    class START,END startEnd
    class PLAN,RETRIEVE,GROUND,REASON,VALIDATE,LOG process
    class DECIDE decision
    class FALLBACK fallback
    class ACT action
"""
