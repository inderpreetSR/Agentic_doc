# DSAA Agents Diagram Viewer

Interactive Streamlit application for visualizing **Agentic RAG + Data Science** project architectures using Mermaid diagrams.

## Features

- **Architecture View (SoC)**: Separation of concerns - UI/API, orchestrator, agents, retrieval/tools, governance, observability
- **Agent Graph**: State machine showing planner → specialized agents → validators → fallback loops
- **DS Project Depth**: Data science pipeline agents for EDA, feature engineering, modeling, evaluation, deployment
- **Interactive Filters**: Toggle visibility of system components
- **Presets**: Quick configurations for different focus areas

## Quick Start (Local Setup)

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/inderpreetSR/Agentic_doc.git
cd Agentic_doc

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r dsaa_agents_streamlit/requirements.txt

# Run the app
streamlit run dsaa_agents_streamlit/app.py
```

Open http://localhost:8501 in your browser.

---

## EC2 Linux Setup

See [docs/ec2-setup.md](docs/ec2-setup.md) for detailed instructions.

### Quick Setup Script

```bash
# SSH into your EC2 instance, then:
curl -sSL https://raw.githubusercontent.com/inderpreetSR/Agentic_doc/main/scripts/setup-ec2.sh | bash
```

---

## Docker Deployment

```bash
# Build image
docker build -t dsaa-agents .

# Run container
docker run -d -p 8501:8501 --name dsaa-agents dsaa-agents

# Access at http://localhost:8501
```

---

## CI/CD Deployment (GitHub Actions)

The repository includes GitHub Actions workflows for:
- **AWS EC2**: Auto-deploy on push to main
- **Docker Hub**: Build and push container images

See [docs/cicd-setup.md](docs/cicd-setup.md) for configuration.

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `EC2_HOST` | EC2 public IP or hostname |
| `EC2_USER` | SSH username (e.g., `ubuntu`) |
| `EC2_SSH_KEY` | Private SSH key for EC2 access |
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub access token |

---

## Project Structure

```
Agentic_doc/
├── .github/workflows/     # CI/CD pipelines
├── .claude/agents/        # Claude Code custom agents
├── docs/                  # Documentation
├── scripts/               # Setup scripts
├── dsaa_agents_streamlit/ # Main Streamlit app
│   ├── .streamlit/        # Streamlit config
│   ├── app.py             # Application entry point
│   ├── diagrams.py        # Mermaid diagram definitions
│   └── requirements.txt   # Python dependencies
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-container setup
└── README.md
```

---

## Architecture Pattern

```
Plan → Retrieve → Ground → Verify → Route → Act → Log
```

**Design Principles:**
- Separation of Concerns
- Fallback handling
- Audit trails

---

## License

MIT
