# 🚀 FastAPI CI/CD with Jenkins, Docker, and GitHub

This repository demonstrates a **complete, production-style CI/CD pipeline** for deploying a **FastAPI application** using **GitHub**, **Jenkins**, and **Docker**, all running on an **AWS EC2 instance**.

The guide walks you **from zero to deployment** — including EC2 setup, Jenkins installation, Docker configuration, credentials management, pipeline creation, and automated deployment.

---

## 📌 Table of Contents

1. Project Overview
2. Architecture
3. Project Structure
4. Prerequisites
5. EC2 Instance Setup
6. Installing Dependencies on EC2
7. Jenkins Installation & Configuration
8. Docker Installation & Configuration
9. GitHub Repository Setup
10. Jenkins Credentials Configuration
11. Jenkins Pipeline Setup
12. GitHub Webhook Configuration
13. CI/CD Pipeline Flow
14. Application Deployment
15. Verification
16. Common Issues & Fixes
17. Conclusion

---

## 1️⃣ Project Overview

This project automates the build, test, and deployment of a **FastAPI application** using:

- **GitHub** – Source code management
- **Jenkins** – CI/CD orchestration
- **Docker** – Containerization
- **AWS EC2** – Hosting Jenkins and the application

Every push to the `main` branch automatically:

- Pulls the latest code
- Builds a Docker image
- Tests the application
- Deploys the container

---

## 2️⃣ Architecture

```
Developer → GitHub → Jenkins (EC2) → Docker → FastAPI App
```

---

## 3️⃣ Project Structure

```
simple-fastapi/
│
├── app/
│   └── main.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
└── README.md
```

---

## 4️⃣ Prerequisites

Before you begin, ensure you have:

- AWS Account
- GitHub Account
- Basic Linux & Git knowledge
- SSH client

---

## 5️⃣ EC2 Instance Setup

### Launch EC2 Instance

- **AMI**: Ubuntu Server 22.04 LTS
- **Instance Type**: `t2.medium`
- **Storage**: ≥ 20 GB

### Security Group Rules

| Type    | Port | Source    |
| ------- | ---- | --------- |
| SSH     | 22   | Your IP   |
| HTTP    | 80   | 0.0.0.0/0 |
| Jenkins | 8080 | 0.0.0.0/0 |
| FastAPI | 8000 | 0.0.0.0/0 |

---

## 6️⃣ Installing Dependencies on EC2

### Connect to EC2

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Java (Required for Jenkins)

```bash
sudo apt install -y openjdk-17-jdk
java -version
```

### Install Git

```bash
sudo apt install -y git
git --version
```

---

## 7️⃣ Jenkins Installation & Configuration

### Add Jenkins Repository

```bash
curl -fsSL https://pkg.jenkins.io/debian/jenkins.io-2023.key | sudo tee \
/usr/share/keyrings/jenkins-keyring.asc > /dev/null
```

```bash
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian binary/ | sudo tee \
/etc/apt/sources.list.d/jenkins.list > /dev/null
```

### Install Jenkins

```bash
sudo apt update
sudo apt install -y jenkins
```

### Start & Enable Jenkins

```bash
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Access Jenkins UI

```
http://<EC2_PUBLIC_IP>:8080
```

Retrieve admin password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

## 8️⃣ Docker Installation & Configuration

### Install Docker

```bash
sudo apt install -y docker.io
```

### Enable Docker

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Allow Jenkins to Use Docker

```bash
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu
sudo systemctl restart jenkins
```

⚠️ Logout and SSH back into EC2.

Verify:

```bash
docker --version
docker run hello-world
```

---

## 9️⃣ GitHub Repository Setup

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<username>/simple-fastapi.git
git push -u origin main
```

---

## 🔐 10️⃣ Jenkins Credentials Configuration

Navigate:

```
Jenkins Dashboard → Manage Jenkins → Credentials → Global → Add Credentials
```

### GitHub Credentials

- Kind: Username with password
- Username: GitHub username
- Password: GitHub Personal Access Token
- ID: `github-creds`

### Docker Hub Credentials

- Kind: Username with password
- Username: Docker Hub username
- Password: Docker Hub password or token
- ID: `dockerhub-creds`

---

## 11️⃣ Jenkins Pipeline Setup

- New Item → Pipeline
- Definition: Pipeline script from SCM
- SCM: Git
- Repository URL: GitHub repo URL
- Branch: `main`
- Script Path: `Jenkinsfile`

Save and build.

---

## 12️⃣ GitHub Webhook Configuration

GitHub Repo → Settings → Webhooks → Add Webhook

- Payload URL:

```
http://<EC2_PUBLIC_IP>:8080/github-webhook/
```

- Content Type: `application/json`
- Trigger: Push events

---

## 13️⃣ CI/CD Pipeline Flow

1. Code pushed to GitHub
2. GitHub triggers Jenkins
3. Jenkins pulls code
4. Docker image built
5. Container tested
6. Application deployed

---

## 14️⃣ Application Deployment

Jenkins runs the container:

```bash
docker run -d --restart always -p 8000:8000 simple-fastapi
```

---

## 15️⃣ Verification

Open browser:

```
http://<EC2_PUBLIC_IP>:8000
```

Expected response:

```json
{ "message": "FastAPI CI/CD with Jenkins & Docker" }
```

---

## 16️⃣ Common Issues & Fixes

### Docker Permission Denied

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Jenkins Not Accessible

- Ensure port `8080` is open in EC2 security group

---

## 17️⃣ Conclusion

You now have a **fully automated CI/CD pipeline** for FastAPI using Jenkins, Docker, GitHub, and AWS EC2.

This setup is:

- Secure
- Scalable
- Production-aligned

---

### 🔜 Future Enhancements

- HTTPS (Nginx + SSL)
- Docker Hub / AWS ECR push
- Pytest integration
- Kubernetes (EKS)

---

✅ **Happy Building & Deploying!**
