# Strikem Platform - AWS Cloud Architecture

Welcome to the repository for **Strikem**, a real-time pool hall management and matchmaking platform. This README describes the updated AWS-based infrastructure, improved from the previous DigitalOcean deployment. It outlines how core services interact, and the enhancements made for scalability, automation, and performance.

---

## ✨ Tech Stack

### Backend
- **Framework**: Django Rest Framework (DRF)
- **Real-Time Communication**: Django Channels with Redis
- **Task Management**: Celery + Celery Beat (partially replaced by AWS Lambda)
- **Database**: MySQL (Amazon RDS)
- **Web Server**: Nginx (reverse proxy, if used)
- **Application Servers**: Gunicorn (WSGI) and Daphne (ASGI)
- **Authentication**: JWT for both WSGI and ASGI traffic

### Deployment & Hosting
- **Platform**: Amazon Web Services (AWS)
- **Containerization**: Docker + Docker Compose 
- **Hosting Services**: EC2, RDS, S3, Lambda, SQS, SNS, CodePipeline, EventBridge

---

## 🪧 AWS Cloud Architecture

### 1. **Request Routing and Load Balancing**
- **Amazon Route 53**: Handles DNS and routes user traffic.
- **Application Load Balancer (ALB)**: Distributes incoming HTTP(S) requests to EC2 instances running Django.

### 2. **Application Layer (EC2 Instances)**
- Hosted across multiple **Availability Zones (A, B, C)** in **Private Subnets**.
- Auto Scaling Group ensures high availability and elasticity.
- Each instance runs:
  - Gunicorn for WSGI traffic
  - Daphne for ASGI/WebSocket traffic
  - Background workers for Celery tasks

### 3. **Database and Cache Layer**
- **Amazon RDS (MySQL)**: Stores persistent data securely in a private subnet.
- **Redis** (likely via ElastiCache): Used for:
  - Django Channels (WebSocket Layer)
  - Celery Task Broker
  - Caching

### 4. **Media and Static Files**
- **Amazon S3** is used to store user-uploaded media and application static files.
- A dedicated bucket handles all media uploads (`Media Files For Strikem`).
- Amazon CloudFront is used as a CDN in front of S3 to serve media assets efficiently, reducing latency for global users.

### 5. **Asynchronous & Scheduled Tasks**
- **Celery With Celery Beat** is used to run background jobs like:
  - Sending notifications
  - Starting and finishing game sessions

> **Improvement:** Some recurring jobs were offloaded from Celery and replaced with **AWS Lambda + EventBridge**, reducing load and simplifying periodic scheduling.

### 6. **Lambda Functions**
Lambda functions are used for:
- `delete_old_notifications`: Runs daily, triggered by EventBridge
- `delete_denied_invite`, `done_invitation_cleanup`: Cleanup utilities

This allowed me to offload routine and scheduled operations from Celery, enhancing system performance and decoupling logic.

### 7. **SQS + SNS Fan-Out Pattern**
- We adopted an **SNS-to-SQS fan-out** model:
  - **SNS Topic** triggers two **SQS queues**.
  - Filtering policies ensure that each Lambda  only processes relevant messages.


### 8. **CI/CD with CodePipeline**
- Integrated with **GitHub** for source control.
- **CodePipeline** automates the deployment process:
  - Code changes are pulled from GitHub
  - Artifacts are stored in an **S3 bucket**
  - CodeBuild is inside VPC and runs tests and migrations
  - CodeDeploy uses AllAtOnce strategy for auto scaling groups.

---


## 🚫 Security & Access
- **Private Subnets**: All core infrastructure (DB, backend servers) is isolated
- **Bastion Host**: Secure access point for internal EC2 instances via SSH
- **IAM Roles & Policies**: Granular permission management for Lambda, S3, etc.

---

## ✅ Improvements Over DigitalOcean Setup
| Feature | DigitalOcean | AWS |
|--------|--------------|-----|
| Task Scheduling | Celery Beat | EventBridge + Lambda |
| Database | MySQL on Droplet | RDS MySQL (scalable, backed up) |
| CI/CD | Manual or GitHub Actions | Fully automated CodePipeline |
| Security | SSH to all servers | Bastion + Private Subnets + IAM |
| Autoscaling | Manual | Auto Scaling Group |
| Observability | Basic | CloudWatch Logs, Events, and Metrics |

---

## 🔧 Future Enhancements
- Improve CI/CD rollback mechanisms
- Auto-tagging and billing alerts

---

