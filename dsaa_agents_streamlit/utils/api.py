"""
REST API layer using FastAPI for diagram generation and management.
Run alongside Streamlit or as a separate service.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json

from .diagrams import (
    PRESETS,
    COMPLETE_DIAGRAM,
    build_architecture_diagram,
    build_agent_diagram,
    build_ds_diagram,
)
from .diagram_types import get_all_templates, get_template, ALL_DIAGRAM_TYPES
from .database import DiagramRepository, TemplateRepository
from .export import render_mermaid_with_export

# FastAPI app
app = FastAPI(
    title="DSAA Agents API",
    description="REST API for generating and managing Mermaid diagrams",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class DiagramFilters(BaseModel):
    api: bool = True
    orchestrator: bool = True
    agents: bool = True
    retrieval: bool = True
    tools: bool = True
    data: bool = True
    governance: bool = True
    obs: bool = True
    ds: bool = True


class DiagramRequest(BaseModel):
    diagram_type: str = Field(..., description="Type: architecture, agent, ds, complete")
    filters: Optional[DiagramFilters] = None
    preset: Optional[str] = Field(None, description="Preset name: all_on, all_off, rag_agents, ds_pipeline, governance")


class CustomDiagramCreate(BaseModel):
    name: str
    mermaid_code: str
    diagram_type: str = "flowchart"
    description: str = ""
    is_public: bool = False


class CustomDiagramUpdate(BaseModel):
    name: Optional[str] = None
    mermaid_code: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None


class MermaidRenderRequest(BaseModel):
    mermaid_code: str
    theme: str = "dark"


# API Routes

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "DSAA Agents API"}


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "endpoints": {
            "diagrams": "/api/v1/diagrams",
            "templates": "/api/v1/templates",
            "custom": "/api/v1/custom-diagrams",
            "render": "/api/v1/render",
        }
    }


# Diagram Generation Endpoints

@app.post("/api/v1/diagrams/generate", tags=["Diagrams"])
async def generate_diagram(request: DiagramRequest):
    """
    Generate a Mermaid diagram based on type and filters.

    - **diagram_type**: architecture, agent, ds, or complete
    - **filters**: Optional filter configuration
    - **preset**: Optional preset name (overrides filters)
    """
    # Get filters from preset or request
    if request.preset and request.preset in PRESETS:
        filters = PRESETS[request.preset]
    elif request.filters:
        filters = request.filters.model_dump()
    else:
        filters = PRESETS["all_on"]

    # Generate diagram based on type
    if request.diagram_type == "architecture":
        mermaid_code = build_architecture_diagram(filters)
    elif request.diagram_type == "agent":
        mermaid_code = build_agent_diagram(filters)
    elif request.diagram_type == "ds":
        mermaid_code = build_ds_diagram(filters)
    elif request.diagram_type == "complete":
        mermaid_code = COMPLETE_DIAGRAM
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid diagram_type: {request.diagram_type}. Use: architecture, agent, ds, complete"
        )

    return {
        "diagram_type": request.diagram_type,
        "filters": filters,
        "mermaid_code": mermaid_code,
    }


@app.get("/api/v1/diagrams/presets", tags=["Diagrams"])
async def list_presets():
    """List all available filter presets."""
    return {
        "presets": list(PRESETS.keys()),
        "details": PRESETS,
    }


@app.get("/api/v1/diagrams/types", tags=["Diagrams"])
async def list_diagram_types():
    """List all available diagram types."""
    return {
        "built_in": ["architecture", "agent", "ds", "complete"],
        "templates": {
            dtype: {
                "name": info["name"],
                "description": info["description"],
                "templates": list(info["templates"].keys())
            }
            for dtype, info in ALL_DIAGRAM_TYPES.items()
        }
    }


# Template Endpoints

@app.get("/api/v1/templates", tags=["Templates"])
async def list_templates(category: Optional[str] = None):
    """List all diagram templates, optionally filtered by category."""
    all_templates = get_all_templates()

    if category and category in all_templates:
        return {
            "category": category,
            "templates": all_templates[category]
        }

    return {"templates": all_templates}


@app.get("/api/v1/templates/{category}/{template_name}", tags=["Templates"])
async def get_template_detail(category: str, template_name: str):
    """Get a specific template by category and name."""
    template = get_template(category, template_name)

    if not template:
        raise HTTPException(
            status_code=404,
            detail=f"Template not found: {category}/{template_name}"
        )

    return {
        "category": category,
        "template_name": template_name,
        "template": template,
    }


# Custom Diagrams CRUD

@app.post("/api/v1/custom-diagrams", tags=["Custom Diagrams"])
async def create_custom_diagram(diagram: CustomDiagramCreate):
    """Create a new custom diagram."""
    diagram_id = DiagramRepository.create(
        name=diagram.name,
        mermaid_code=diagram.mermaid_code,
        diagram_type=diagram.diagram_type,
        description=diagram.description,
        is_public=diagram.is_public,
    )

    return {
        "id": diagram_id,
        "message": "Diagram created successfully",
    }


@app.get("/api/v1/custom-diagrams", tags=["Custom Diagrams"])
async def list_custom_diagrams(include_public: bool = True):
    """List all custom diagrams."""
    diagrams = DiagramRepository.get_all(include_public=include_public)
    return {"diagrams": diagrams}


@app.get("/api/v1/custom-diagrams/{diagram_id}", tags=["Custom Diagrams"])
async def get_custom_diagram(diagram_id: int):
    """Get a specific custom diagram by ID."""
    diagram = DiagramRepository.get_by_id(diagram_id)

    if not diagram:
        raise HTTPException(status_code=404, detail="Diagram not found")

    return {"diagram": diagram}


@app.put("/api/v1/custom-diagrams/{diagram_id}", tags=["Custom Diagrams"])
async def update_custom_diagram(diagram_id: int, update: CustomDiagramUpdate):
    """Update a custom diagram."""
    success = DiagramRepository.update(
        diagram_id,
        name=update.name,
        mermaid_code=update.mermaid_code,
        description=update.description,
        is_public=update.is_public,
    )

    if not success:
        raise HTTPException(status_code=404, detail="Diagram not found or no changes")

    return {"message": "Diagram updated successfully"}


@app.delete("/api/v1/custom-diagrams/{diagram_id}", tags=["Custom Diagrams"])
async def delete_custom_diagram(diagram_id: int):
    """Delete a custom diagram."""
    success = DiagramRepository.delete(diagram_id)

    if not success:
        raise HTTPException(status_code=404, detail="Diagram not found")

    return {"message": "Diagram deleted successfully"}


# Render Endpoints

@app.post("/api/v1/render/html", tags=["Render"], response_class=HTMLResponse)
async def render_diagram_html(request: MermaidRenderRequest):
    """Render Mermaid code as HTML with embedded SVG."""
    html = render_mermaid_with_export(request.mermaid_code)
    return HTMLResponse(content=html)


@app.post("/api/v1/render/preview", tags=["Render"])
async def render_preview(request: MermaidRenderRequest):
    """Get a preview URL for the diagram."""
    # Encode mermaid code for URL
    import base64
    encoded = base64.urlsafe_b64encode(request.mermaid_code.encode()).decode()

    return {
        "mermaid_code": request.mermaid_code,
        "preview_url": f"https://mermaid.ink/img/{encoded}",
        "edit_url": f"https://mermaid.live/edit#base64:{encoded}",
    }


# Utility function to run API server
def run_api_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_api_server()
