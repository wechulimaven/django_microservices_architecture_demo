# Detailed System Design Document

## Table of Contents

1. **Introduction**
2. **Architecture Overview**
3. **Microservices Description**
4. **Communication Protocols**
5. **Data Storage Strategies**
6. **Deployment Strategies**
7. **Security Considerations**
8. **Scalability and Fault Tolerance**
9. **Monitoring and Logging**
10. **Appendix**

## 1. Introduction

This document provides a detailed design for a microservices-based architecture for a social media platform. The system comprises four main services: User, Notification, Feeds, and Gateway. Each service uses an independent Sql database connected by IDs. The Gateway service integrates with all the other services and has its own PostgreSQL database.The Notification service is triggered by the Feeds service upon post creation and sends notifications only to active users.

## 2. Architecture Overview

The architecture follows a microservices approach where each service is independently developed, deployed, and scaled. The services communicate via REST APIs, and the Notification service uses Django Channels for real-time notifications. The Feeds service utilizes Celery for asynchronous background tasks and Redis for caching requests. Monitoring is handled using Prometheus and Grafana, with error logging provided by Sentry.

### Components

- **User Service**: Manages user data and authentication.
- **Notification Service**: Sends notifications to active users using Django Channels for real-time notifications, African's Talking for SMS, and Django Mailing system for emails.
- **Feeds Service**: Manages user posts and feeds, uses SQLite, Celery for async tasks, and Redis for caching.
- **Gateway Service**: Acts as an API gateway, routing requests to the appropriate microservice and handling its own PostgreSQL database.
- **PostgreSQL Databases**: Independent databases for gateway service.
- **Sqlite Databases**: Databases for each service.

### Architecture Diagram

![Microservices Architecture Diagram](architecture-diagram.png)

## 3. Microservices Description

### 3.1 User Service

- **Responsibilities**: Manages user registration, authentication, and profile management.
- **Endpoints**:
  - `POST /register/`: Register a new user.
  - `POST /login/`: Authenticate a user.
  - `POST /logout/`: Logout a user.
  - `PUT /update-account/`: Update user account information.
  - `GET /detail/<str:id>/`: Retrieve user profile information.
  - `GET /all/`: Retrieve all users.

### 3.2 Notification Service

- **Responsibilities**: Sends notifications to active users using Django Channels for real-time notifications, African's Talking for SMS, and Django Mailing system for emails.
- **Endpoints**:
  - `POST /send-notification/`: Send a notification to a user.

### 3.3 Feeds Service

- **Responsibilities**: Manages user posts and feeds.
- It utiizes celery and redis for async and request caching
- **Endpoints**:
  - `GET /all/`: Retrieve all posts.
  - `GET /detail/<str:id>/`: Retrieve a specific post.
  - `POST /create/`: Create a new post.

### 3.4 Gateway Service

- **Responsibilities**: Routes requests to the appropriate microservice, handles authentication, and provides a unified API endpoint.
- **Endpoints**:
  - `GET /all-posts/`: Retrieve all posts (from Feeds Service).
  - `GET /post-detail/<str:id>/`: Retrieve a specific post (from Feeds Service).
  - `POST /create-post/`: Create a new post (to Feeds Service).
  - `POST /login/`: Authenticate a user (to User Service).
  - `POST /register/`: Register a new user (to User Service).

## 4. Communication Protocols

### 4.1 REST API

All services communicate via REST APIs using HTTP/HTTPS protocols. JSON is used as the standard format for data exchange.

### 4.2 Internal Service Communication

Internal communication between services (e.g., from Gateway Service to User Service) is handled via service URLs defined in environment variables. These URLs are resolved within the Kubernetes cluster.

Example:
- `USER_SERVICE_URL=http://user-service:8000`

### 4.3 Real-time Communication

The Notification Service uses Django Channels for real-time notifications.

## 5. Data Storage Strategies

### 5.1 Independent Databases

Each microservice uses its own database. The databases are related by IDs to ensure data consistency across services
1. User Service: Uses PostgreSQL for reliable and scalable user data management.
2. Notification Service: Uses SQLite for lightweight and simple data storage.
3. Feeds Service: Uses SQLite for lightweight and simple data storage.
4. Gateway Service: Uses its own PostgreSQL database for managing aggregated data and routing information.

#### Example Configuration for gateway Service
- **Database**: `user_db`
- **User**: `user_user`
- **Password**: `user_password`
- **Host**: `user-postgres-service`
- **Port**: `5432`

Environment variables for User Service:
```yaml
env:
  - name: POSTGRES_DB
    value: user_db
  - name: POSTGRES_USER
    value: user_user
  - name: POSTGRES_PASSWORD
    value: user_password
  - name: POSTGRES_HOST
    value: user-postgres-service
  - name: POSTGRES_PORT
    value: "5432"
```

### 5.2 Gateway Database

The Gateway Service has its own PostgreSQL database for managing aggregated data and routing information.

## 6. Deployment Strategies

### 6.1 Docker

Each microservice is containerized using Docker. Dockerfiles are created for each service to define their respective environments and dependencies.

Example Dockerfile for User Service:
```Dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

### 6.2 Kubernetes

Kubernetes is used to deploy and manage the containers. Deployment files define the desired state for each microservice, including the number of replicas, container images, and environment variables.

Example `user-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: user
  template:
    metadata:
      labels:
        app: user
    spec:
      containers:
      - name: user
        image: user_service_image:latest
        ports:
        - containerPort: 8000
        env:
        - name: DJANGO_SETTINGS_MODULE
          value: user_service.settings
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: ClusterIP
```

## 7. Security Considerations

- **Authentication**: Auth token are used for both user authentication and service to service communication.
- **HTTPS**: Secure communication between clients and the gateway service.
- **Secrets Management**: Kubernetes secrets are used to store sensitive data such as database credentials.
- **Request Throttling**: The Gateway Service implements request throttling to prevent abuse and ensure fair usage.
  
Example implementation of request throttling in Django REST Framework (for Gateway Service):
```
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## 8. Scalability and Fault Tolerance

- **Horizontal Scaling**: Each microservice can be scaled independently by increasing the number of replicas.
- **Load Balancing**: Kubernetes services provide load balancing across multiple pod instances.
- **Health Checks**: Kubernetes liveness and readiness probes ensure that only healthy pods receive traffic.

## 9. Monitoring and Logging

- **Monitoring**: Prometheus is used for monitoring system metrics, and Grafana is used for visualization.
- **Logging**: Sentry is used for error logging and tracking.

## 10. Appendix

### Kubernetes Commands

- **Apply a Deployment**:
  ```bash
  kubectl apply -f <deployment-file.yaml>
  ```

- **Get Pods**:
  ```bash
  kubectl get pods
  ```

- **Get Services**:
  ```bash
  kubectl get services
  ```

- **View Logs**:
  ```bash
  kubectl logs <pod-name>
  ```

---

This document provides a detailed overview of the microservices architecture, communication protocols, and data storage strategies for the given system. It serves as a guide for the development, deployment, and maintenance of the system.
