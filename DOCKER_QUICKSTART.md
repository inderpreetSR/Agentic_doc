# Docker Quick Start Guide

Run the DSAA Agents app using Docker in 3 simple steps.

## Prerequisites

- Docker Desktop installed and running

## Steps

### 1. Clone the Repository

```bash
git clone https://github.com/inderpreetSR/Agentic_doc.git
cd Agentic_doc
```

### 2. Build the Docker Image

```bash
docker-compose build
```

This takes 2-3 minutes on first run.

### 3. Start the Container

```bash
docker-compose up -d
```

### 4. Open the App

Go to: **http://localhost:8501**

---

## Useful Commands

| Command | What it does |
|---------|--------------|
| `docker-compose up -d` | Start the app |
| `docker-compose down` | Stop the app |
| `docker-compose logs -f` | View logs |
| `docker-compose restart` | Restart the app |
| `docker ps` | Check running containers |

## Stop the App

```bash
docker-compose down
```

## Troubleshooting

**Port already in use?**
```bash
docker-compose down
docker-compose up -d
```

**Container not starting?**
```bash
docker-compose logs dsaa-agents-app
```

**Rebuild after code changes?**
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

That's it! The app runs in a secure Docker container with all dependencies included.
