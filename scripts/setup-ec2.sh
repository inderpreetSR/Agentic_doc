#!/bin/bash
# EC2 Setup Script for DSAA Agents Diagram Viewer
# Tested on Ubuntu 22.04 LTS

set -e  # Exit on error

echo "=========================================="
echo "DSAA Agents - EC2 Setup Script"
echo "=========================================="

# Update system
echo "[1/6] Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and pip
echo "[2/6] Installing Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip git curl

# Clone repository
echo "[3/6] Cloning repository..."
cd /home/ubuntu
if [ -d "Agentic_doc" ]; then
    cd Agentic_doc
    git pull
else
    git clone https://github.com/inderpreetSR/Agentic_doc.git
    cd Agentic_doc
fi

# Create virtual environment
echo "[4/6] Setting up Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
echo "[5/6] Installing Python dependencies..."
pip install --upgrade pip
pip install -r dsaa_agents_streamlit/requirements.txt

# Create systemd service
echo "[6/6] Creating systemd service..."
sudo tee /etc/systemd/system/dsaa-agents.service > /dev/null <<EOF
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
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable dsaa-agents
sudo systemctl start dsaa-agents

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "App running at: http://$(curl -s ifconfig.me):8501"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status dsaa-agents   # Check status"
echo "  sudo systemctl restart dsaa-agents  # Restart app"
echo "  sudo journalctl -u dsaa-agents -f   # View logs"
echo ""
echo "Don't forget to open port 8501 in your EC2 Security Group!"
