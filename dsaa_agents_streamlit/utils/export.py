"""
Diagram export utilities for PNG/SVG download.
"""

import base64
import json
from typing import Optional


def get_mermaid_export_html(mermaid_code: str, format: str = "svg") -> str:
    """
    Generate HTML with JavaScript to export Mermaid diagram.

    Args:
        mermaid_code: Mermaid diagram code
        format: Export format ('svg' or 'png')

    Returns:
        HTML string with export functionality
    """
    code_escaped = json.dumps(mermaid_code)

    return f"""
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        async function exportDiagram(format) {{
            const code = {code_escaped};
            const {{ svg }} = await mermaid.render('export-diagram', code);

            if (format === 'svg') {{
                const blob = new Blob([svg], {{type: 'image/svg+xml'}});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'diagram.svg';
                a.click();
                URL.revokeObjectURL(url);
            }} else if (format === 'png') {{
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();

                img.onload = function() {{
                    canvas.width = img.width * 2;
                    canvas.height = img.height * 2;
                    ctx.fillStyle = '#1e1e1e';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

                    canvas.toBlob(function(blob) {{
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'diagram.png';
                        a.click();
                        URL.revokeObjectURL(url);
                    }}, 'image/png');
                }};

                img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svg)));
            }}
        }}
        mermaid.initialize({{ startOnLoad: false, theme: 'dark' }});
    </script>
    """


def create_download_button_html(button_id: str, format: str, label: str) -> str:
    """Create HTML for a download button."""
    return f"""
    <button id="{button_id}" onclick="exportDiagram('{format}')"
            style="background: #4CAF50; color: white; padding: 8px 16px;
                   border: none; border-radius: 4px; cursor: pointer; margin: 4px;">
        {label}
    </button>
    """


def render_mermaid_with_export(mermaid_code: str, height_px: int = 500) -> str:
    """
    Build HTML that renders Mermaid diagram with export buttons.

    Args:
        mermaid_code: Mermaid diagram code
        height_px: Height of the diagram container

    Returns:
        HTML string with diagram and export functionality
    """
    code_escaped = json.dumps(mermaid_code)

    return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    body {{ margin: 0; padding: 12px; background: transparent; font-family: sans-serif; }}
    .mermaid {{ display: flex; justify-content: center; }}
    .mermaid svg {{ max-width: 100%; height: auto; }}
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
    .export-btn.svg {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }}
    .export-btn.svg:hover {{ box-shadow: 0 4px 12px rgba(17, 153, 142, 0.4); }}
  </style>
</head>
<body>
  <div class="export-buttons">
    <button class="export-btn svg" onclick="exportDiagram('svg')">Download SVG</button>
    <button class="export-btn" onclick="exportDiagram('png')">Download PNG</button>
  </div>
  <div class="mermaid" id="mermaid-root"></div>

  <script>
    mermaid.initialize({{ startOnLoad: false, theme: 'dark', securityLevel: 'loose' }});
    const code = {code_escaped};
    const container = document.getElementById('mermaid-root');

    let renderedSvg = '';

    mermaid.render('mermaid-svg', code).then(function({{ svg }}) {{
      container.innerHTML = svg;
      renderedSvg = svg;
    }}).catch(function(err) {{
      container.innerHTML = '<pre style="color:#e06c75;">Error: ' + err.message + '</pre>';
    }});

    function exportDiagram(format) {{
      if (!renderedSvg) {{
        alert('Diagram not ready yet');
        return;
      }}

      if (format === 'svg') {{
        const blob = new Blob([renderedSvg], {{type: 'image/svg+xml'}});
        downloadBlob(blob, 'diagram.svg');
      }} else if (format === 'png') {{
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = function() {{
          canvas.width = img.width * 2;
          canvas.height = img.height * 2;
          ctx.fillStyle = '#1e1e1e';
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
