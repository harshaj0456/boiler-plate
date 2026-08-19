# AWS Deployment Guide

Deploy your Python backend to AWS EC2 with Application Load Balancer.

## Architecture

```
Internet
  ↓
Internet Gateway
  ↓
Application Load Balancer (ALB)
  ↓
Target Group
  ↓
┌──────────┴──────────┐
▼                     ▼
EC2 #1              EC2 #2
│                     │
Docker              Docker
│                     │
Backend             Backend
```

## Prerequisites

- AWS Account
- AWS CLI configured
- EC2 Key Pair
- Domain name (optional)

## Setup Steps

### 1. Launch EC2 Instances

```bash
# Launch 2 EC2 instances (t3.small or larger)
# Ubuntu 22.04 LTS
# Security Group: Allow 22 (SSH), 8000/5000 (App), 80, 443
```

### 2. Run Setup Script

```bash
# SSH into each EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Copy setup script
# For FastAPI:
bash setup.sh

# For Flask:
bash setup.sh
```

### 3. Configure Application Load Balancer

1. **Create Target Group**:
   - Type: Instances
   - Protocol: HTTP
   - Port: 8000 (FastAPI) or 5000 (Flask)
   - Health check: `/health`
   - Register EC2 instances

2. **Create Application Load Balancer**:
   - Scheme: Internet-facing
   - Listeners: HTTP (80), HTTPS (443)
   - Availability Zones: Select 2+
   - Security Group: Allow 80, 443

3. **Configure Listener Rules**:
   - Forward traffic to Target Group
   - Enable sticky sessions (if needed)

### 4. SSL Certificate

Using AWS Certificate Manager:

```bash
# Request certificate
aws acm request-certificate \
  --domain-name api.yourdomain.com \
  --validation-method DNS
```

Add certificate to ALB HTTPS listener.

### 5. Configure DNS

Point your domain to ALB:

```
Type: CNAME
Name: api
Value: your-alb-url.us-east-1.elb.amazonaws.com
```

### 6. Deploy Application

```bash
# On each EC2 instance
cd /home/ubuntu/app
git pull origin main
docker-compose down
docker-compose up -d --build
```

## Auto Scaling (Optional)

1. Create Launch Template from EC2 instance
2. Create Auto Scaling Group
3. Configure scaling policies:
   - Target CPU: 70%
   - Min instances: 2
   - Max instances: 10

## Monitoring

### CloudWatch Metrics

- EC2 CPU/Memory
- ALB request count
- Target health
- Error rates

### Logs

```bash
# Application logs
docker logs -f your-container

# System logs
sudo journalctl -u fastapi-app -f
```

## Cost Optimization

- Use Reserved Instances for predictable workloads
- Enable Auto Scaling to scale down during low traffic
- Use t3 instances with unlimited mode
- Consider AWS Fargate for containerized workloads

## Security Best Practices

1. Use IAM roles (no hardcoded credentials)
2. Enable VPC Flow Logs
3. Regular security updates: `sudo apt-get update && sudo apt-get upgrade`
4. Use AWS Secrets Manager for sensitive data
5. Enable CloudTrail for audit logs

## Disaster Recovery

1. Take AMI snapshots weekly
2. Backup database to S3
3. Multi-AZ deployment for high availability
4. Test restore procedures regularly

## Deployment Script

```bash
#!/bin/bash
# deploy.sh

ssh -i your-key.pem ubuntu@ec2-instance-1 << 'EOF'
cd /home/ubuntu/app
git pull
docker-compose down
docker-compose up -d --build
EOF

ssh -i your-key.pem ubuntu@ec2-instance-2 << 'EOF'
cd /home/ubuntu/app
git pull
docker-compose down
docker-compose up -d --build
EOF

echo "Deployment complete!"
```
