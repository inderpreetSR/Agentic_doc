# CI/CD Setup Guide

Automate deployment of DSAA Agents using GitHub Actions.

## Overview

The repository includes two CI/CD workflows:
1. **Deploy to EC2** - Auto-deploy on push to main
2. **Build Docker Image** - Build and push to Docker Hub

## Setup GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

### For EC2 Deployment

| Secret | How to Get |
|--------|------------|
| `EC2_HOST` | Your EC2 public IP or domain |
| `EC2_USER` | Usually `ubuntu` for Ubuntu AMIs |
| `EC2_SSH_KEY` | Your EC2 private key (contents of .pem file) |

### For Docker Hub

| Secret | How to Get |
|--------|------------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub Access Token (Account Settings → Security → New Access Token) |

## Workflow 1: Deploy to EC2

File: `.github/workflows/deploy-ec2.yml`

**Triggers:**
- Push to `main` branch
- Manual trigger (workflow_dispatch)

**What it does:**
1. SSH into EC2
2. Pull latest code
3. Install dependencies
4. Restart service

## Workflow 2: Build Docker Image

File: `.github/workflows/docker-build.yml`

**Triggers:**
- Push to `main` branch
- New release/tag

**What it does:**
1. Build Docker image
2. Push to Docker Hub
3. Tag with version and `latest`

## First-Time EC2 Setup

Before CI/CD works, run initial setup on EC2:

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2_HOST>

# Run setup script
curl -sSL https://raw.githubusercontent.com/inderpreetSR/Agentic_doc/main/scripts/setup-ec2.sh | bash
```

## Testing Locally

Test the GitHub Actions workflow locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow
act push
```

## Manual Deployment

If you need to deploy manually:

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2_HOST>

# Update code
cd /home/ubuntu/Agentic_doc
git pull origin main

# Restart service
sudo systemctl restart dsaa-agents
```

## Monitoring Deployments

### GitHub Actions
- Go to repository → Actions tab
- View workflow runs and logs

### EC2 Service
```bash
# Check status
sudo systemctl status dsaa-agents

# View logs
sudo journalctl -u dsaa-agents -f

# View recent deployments
git log --oneline -10
```

## Rollback

If a deployment breaks the app:

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<EC2_HOST>

# Find previous working commit
cd /home/ubuntu/Agentic_doc
git log --oneline -10

# Rollback to specific commit
git checkout <commit-hash>

# Restart service
sudo systemctl restart dsaa-agents
```

## Advanced: Blue-Green Deployment

For zero-downtime deployments, use Docker with two containers:

```bash
# Deploy new version to port 8502
docker run -d -p 8502:8501 --name dsaa-agents-new dsaa-agents:latest

# Test new version
curl http://localhost:8502/_stcore/health

# If healthy, switch traffic (update Nginx)
# Then stop old container
docker stop dsaa-agents-old
docker rm dsaa-agents-old
docker rename dsaa-agents-new dsaa-agents-old
```

## Notifications

Add Slack/Discord notifications to workflows:

```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```
