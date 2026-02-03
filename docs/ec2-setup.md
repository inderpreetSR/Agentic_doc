# EC2 Setup Guide

Complete guide for deploying DSAA Agents Diagram Viewer on AWS EC2.

## Prerequisites

- AWS Account
- EC2 instance (Ubuntu 22.04 LTS recommended)
- Security Group with port 8501 open (or 80/443 for production)

## Option 1: Quick Setup (Automated)

SSH into your EC2 instance and run:

```bash
curl -sSL https://raw.githubusercontent.com/inderpreetSR/Agentic_doc/main/scripts/setup-ec2.sh | bash
```

This will:
1. Install Python 3.11
2. Clone the repository
3. Set up virtual environment
4. Install dependencies
5. Create and start systemd service

## Option 2: Manual Setup

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Select **Ubuntu Server 22.04 LTS**
3. Choose instance type: `t2.micro` (free tier) or `t2.small` for better performance
4. Configure Security Group:
   - SSH (port 22) - Your IP
   - Custom TCP (port 8501) - Anywhere (or your IP)
5. Create/select key pair and launch

### Step 2: Connect to EC2

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python
sudo apt-get install -y python3.11 python3.11-venv python3-pip git
```

### Step 4: Clone and Setup

```bash
# Clone repository
git clone https://github.com/inderpreetSR/Agentic_doc.git
cd Agentic_doc

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r dsaa_agents_streamlit/requirements.txt
```

### Step 5: Test Run

```bash
streamlit run dsaa_agents_streamlit/app.py --server.port=8501 --server.address=0.0.0.0
```

Access at: `http://<EC2_PUBLIC_IP>:8501`

### Step 6: Create Systemd Service (Production)

```bash
sudo nano /etc/systemd/system/dsaa-agents.service
```

Add:
```ini
[Unit]
Description=DSAA Agents Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Agentic_doc
Environment="PATH=/home/ubuntu/Agentic_doc/venv/bin"
ExecStart=/home/ubuntu/Agentic_doc/venv/bin/streamlit run dsaa_agents_streamlit/app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable dsaa-agents
sudo systemctl start dsaa-agents
```

## Option 3: Docker Deployment

```bash
# Install Docker
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu
newgrp docker

# Clone and run
git clone https://github.com/inderpreetSR/Agentic_doc.git
cd Agentic_doc
docker-compose up -d
```

## Production Setup with Nginx

For production with custom domain and HTTPS:

### Install Nginx

```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

### Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/dsaa-agents
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/dsaa-agents /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Add SSL with Let's Encrypt

```bash
sudo certbot --nginx -d your-domain.com
```

## Useful Commands

```bash
# Service management
sudo systemctl status dsaa-agents
sudo systemctl restart dsaa-agents
sudo systemctl stop dsaa-agents

# View logs
sudo journalctl -u dsaa-agents -f

# Update application
cd /home/ubuntu/Agentic_doc
git pull
sudo systemctl restart dsaa-agents
```

## Troubleshooting

### Port 8501 not accessible
- Check Security Group allows inbound traffic on port 8501
- Check if service is running: `sudo systemctl status dsaa-agents`

### Service won't start
- Check logs: `sudo journalctl -u dsaa-agents -n 50`
- Verify Python path in service file

### Out of memory
- Upgrade to larger instance type
- Or add swap: `sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`
