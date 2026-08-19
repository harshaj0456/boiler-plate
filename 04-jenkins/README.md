# Jenkins CI/CD

Automated CI/CD pipeline for building, testing, and deploying your application.

## Pipeline Flow

```
Developer
  │
  ▼
GitHub
  │
  ▼
Jenkins
  ├── Checkout
  ├── Install Dependencies
  ├── Lint
  ├── Unit Tests
  ├── Build Docker Image
  ├── Push to Registry
  ├── Deploy to AWS EC2
  └── Health Check
```

## Setup

### 1. Install Jenkins

```bash
# Ubuntu
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins
```

### 2. Required Jenkins Plugins

- Git Plugin
- Docker Plugin
- Pipeline Plugin
- AWS Credentials Plugin
- Credentials Binding Plugin

### 3. Configure Credentials

Add these credentials in Jenkins:

1. **docker-registry**: Docker Hub credentials
2. **ec2-host**: EC2 instance IP/hostname
3. **ec2-ssh-key**: SSH private key for EC2
4. **github-token**: GitHub personal access token (if private repo)

### 4. Create Pipeline

1. New Item → Pipeline
2. Pipeline from SCM
3. Select Git
4. Add repository URL
5. Specify branch (main)
6. Script Path: `04-jenkins/fastapi/Jenkinsfile` or `04-jenkins/flask/Jenkinsfile`

### 5. Configure Webhooks

In GitHub repository settings:
- Webhooks → Add webhook
- Payload URL: `http://your-jenkins-url/github-webhook/`
- Content type: `application/json`
- Events: Just the push event

## Environment Variables

Configure in Jenkins → Manage Jenkins → Configure System:

```
DOCKER_IMAGE=your-registry/your-app
AWS_REGION=us-east-1
```

## Jenkinsfile Customization

Update these values in Jenkinsfile:

```groovy
environment {
    DOCKER_IMAGE = "your-registry/fastapi-app"
    AWS_REGION = "us-east-1"
    EC2_HOST = credentials('ec2-host')
    SSH_KEY = credentials('ec2-ssh-key')
}
```

## Pipeline Stages

### 1. Checkout
Clones the repository from GitHub.

### 2. Install Dependencies
Installs Python dependencies in a virtual environment.

### 3. Lint
Runs flake8 to check code quality.

### 4. Unit Tests
Runs pytest with coverage reporting.

### 5. Build Docker Image
Builds Docker image with build number as tag.

### 6. Push Docker Image
Pushes image to Docker registry.

### 7. Deploy to AWS EC2
SSHs into EC2 instances and deploys new Docker container.

### 8. Health Check
Verifies the application is running correctly.

## Manual Deployment

```bash
# Trigger build manually
# Jenkins → Your Pipeline → Build with Parameters
```

## Rollback

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2

# View available images
docker images

# Stop current container
docker stop your-app

# Run previous version
docker run -d --name your-app \
  -p 8000:8000 \
  --env-file .env \
  your-registry/your-app:previous-tag
```

## Monitoring

View build logs:
- Jenkins → Your Pipeline → Build History → Console Output

## Notifications

Add Slack/Email notifications in Jenkinsfile:

```groovy
post {
    success {
        slackSend color: 'good', message: "Build Successful: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
    }
    failure {
        slackSend color: 'danger', message: "Build Failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
    }
}
```

## Best Practices

1. **Never commit credentials** - use Jenkins credentials
2. **Tag images with build number** for traceability
3. **Run tests before deployment**
4. **Implement health checks** to verify deployment
5. **Keep logs** for debugging
6. **Use staged deployments** (dev → staging → prod)
