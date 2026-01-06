# Image Import System From Goolge Drive

> **Working Site URL:** [https://image-import-system-fotoowl-ai-f2oc.vercel.app/](https://image-import-system-fotoowl-ai-f2oc.vercel.app/)

A robust, scalable system for importing large volumes of images from Google Drive and Dropbox, processing them asynchronously, and serving them via a modern web interface.

## Table of Contents
- [Architecture](#architecture)
- [Services Breakdown](#services-breakdown)
- [Scalability & Performance](#scalability--performance)
- [Setup Instructions](#setup-instructions)
  - [Local Development](#local-development)
  - [Cloud Deployment](#cloud-deployment)
- [API Documentation](#api-documentation)

---

## Architecture

The system follows a microservices architecture designed for high throughput and reliability.

```
graph TD
    Client[Web Frontend (Vercel)] -->|HTTPS| Nginx[Nginx Reverse Proxy]
    Nginx -->|Proxy| API[API Gateway (FastAPI)]
    API -->|Async Task| Redis[Redis Message Broker]
    API -->|Read/Write| DB[(PostgreSQL)]
    Redis -->|Consume Task| Worker[Worker Service (Celery)]
    Worker -->|Update Status| Redis
    Worker -->|Save Metadata| DB
```

### Services Breakdown

1.  **Frontend (Interface)**
    *   **Tech Stack**: React (Next.js/Vite), Tailwind CSS.
    *   **Role**: Provides a user-friendly dashboard to initiate imports, view progress, and browse imported images. Hosted on Vercel for edge performance.

2.  **API Gateway**
    *   **Tech Stack**: Python, FastAPI.
    *   **Role**: Handles incoming HTTP requests, validates inputs, queues import tasks, and retrieves image data. It remains lightweight and stateless to handle high concurrency.

3.  **Worker Service**
    *   **Tech Stack**: Python, Celery.
    *   **Role**: Consumes tasks from the Redis queue. It handles the heavy lifting: fetching files from external providers (Google Drive, Dropbox), processing metadata, and updating the database.

4.  **Database (PostgreSQL)**
    *   **Role**: relational storage for image metadata (ID, URL, size, MIME type, source).

5.  **Message Broker (Redis)**
    *   **Role**: Decouples the API from the Worker. Ensures tasks are not lost and allows for asynchronous processing.

6.  **Nginx**
    *   **Role**: Reverse proxy, SSL termination, and static file serving (if needed). It routes traffic to the API Gateway.

---

## Scalability & How Large-Scale Imports are Handled

The system is engineered to handle large-scale imports without blocking the user interface or timing out requests.

*   **Asynchronous Processing**: All import requests are offloaded to a background task queue (Celery). The API responds immediately with a `task_id`, allowing the client to poll for status updates.
*   **Horizontal Scaling**:
    *   **Workers**: You can spin up multiple instances of the `worker-service` container to process the Redis queue in parallel.
    *   **API**: The FastAPI gateway is stateless and can be scaled behind a load balancer (Nginx).
*   **Resilience**: Redis guarantees message delivery. If a worker crashes, the task remains in the queue (or can be configured for retry).
*   **Database Optimization**: Bulk inserts and indexed queries ensure efficient metadata storage and retrieval.

---

## Setup Instructions

### Local Development

**Prerequisites**: Docker & Docker Compose.

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd image_import_system
    ```

2.  **Environment Variables**
    Create a `.env` file in the `services` directory:
    ```env
    POSTGRES_DB=imagedb
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=postgres
    REDIS_URL=redis://redis:6379/0
    ```

3.  **Start Services**
    Navigate to the `services` directory and run:
    ```bash
    cd services
    docker-compose up --build
    ```

4.  **Run Frontend**
    Navigate to the `interface` directory:
    ```bash
    cd interface
    npm install
    npm run dev
    ```

The API will be available at `http://localhost:5000` (via Nginx or direct depending on config) and the frontend at `http://localhost:5173`.

### Cloud Deployment (EC2 + Vercel)

1.  **Backend (EC2)**
    *   Provision an EC2 instance (Ubuntu recommended).
    *   Install Docker and Docker Compose.
    *   Copy the `services` directory to the instance.
    *   Configure `nginx/prod_default.conf` with your domain and SSL certificates (Certbot).
    *   Run `docker-compose -f docker-compose.prod.yml up -d --build`.

2.  **Frontend (Vercel)**
    *   Connect your repository to Vercel.
    *   Set the Build Command (`npm run build`) and Output Directory (`dist` or `.next`).
    *   Set the `VITE_API_URL` (or equivalent) environment variable to your EC2 domain (e.g., `https://api2.med44.site`).

---

## API Documentation

### Health Check
*   **Endpoint**: `GET /health`
*   **Description**: Checks if the API is running.
*   **Response**: `{"status": "healthy"}`

### Import from Google Drive
*   **Endpoint**: `POST /import/google-drive`
*   **Body**:
    ```json
    {
      "folder_url": "https://drive.google.com/drive/folders/..."
    }
    ```
*   **Response** (202 Accepted):
    ```json
    {
      "message": "Import job queued",
      "task_id": "c84b1a..."
    }
    ```

### Import from Dropbox
*   **Endpoint**: `POST /import/dropbox`
*   **Body**:
    ```json
    {
      "folder_url": "https://www.dropbox.com/sh/..."
    }
    ```
*   **Response** (202 Accepted):
    ```json
    {
      "message": "Import job queued",
      "task_id": "c84b1a..."
    }
    ```

### Check Task Status
*   **Endpoint**: `GET /task/{task_id}`
*   **Response**:
    ```json
    {
      "task_id": "c84b1a...",
      "status": "SUCCESS",
      "result": "..."
    }
    ```

### List Images
*   **Endpoint**: `GET /images`
*   **Query Params**: `source` (optional, e.g., 'google_drive', 'dropbox')
*   **Response**:
    ```json
    {
      "images": [
        {
          "id": 1,
          "name": "photo.jpg",
          "size": 102400,
          "mime_type": "image/jpeg",
          "source": "google_drive",
          "created_at": "2024-01-01T12:00:00"
        }
      ],
      "count": 1
    }
    ```
