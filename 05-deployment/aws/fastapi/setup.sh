#!/bin/bash

# FastAPI AWS EC2 Setup Script
# Run this on a fresh EC2 instance (Ubuntu 22.04 LTS recommended)

set -e

echo "Starting FastAPI server setup..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add current user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
echo "Installing Git..."
sudo apt-get install -y git

# Clone repository (update with your repo URL)
# git clone https://github.com/your-username/your-repo.git /home/ubuntu/app

# Create .env file
echo "Creating environment file..."
cat > /home/ubuntu/.env << EOF
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/app_db

# JWT
JWT_SECRET_KEY=$(openssl rand -hex 32)

# CORS
CORS_ORIGINS=https://your-frontend-domain.com

# Environment
ENVIRONMENT=production
EOF

# Set proper permissions
chmod 600 /home/ubuntu/.env

# Install CloudWatch agent (for monitoring)
echo "Installing CloudWatch agent..."
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
rm amazon-cloudwatch-agent.deb

# Configure firewall
echo "Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Setup systemd service for auto-restart
echo "Setting up systemd service..."
sudo tee /etc/systemd/system/fastapi-app.service > /dev/null << EOF
[Unit]
Description=FastAPI Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/app
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable fastapi-app.service

echo "Setup complete!"
echo "Next steps:"
echo "1. Update /home/ubuntu/.env with your actual values"
echo "2. Clone your repository to /home/ubuntu/app"
echo "3. Run: sudo systemctl start fastapi-app"
echo "4. Configure ALB to point to this instance on port 8000"
