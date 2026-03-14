# Event Management Microservice

A clean-architecture microservice built with FastAPI, PostgreSQL, and Docker for managing events.

## Requirements
- Python 3.10+
- PostgreSQL
- Docker (optional for containerization)

## Run Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL**:
   Make sure a PostgreSQL server is running and the `DATABASE_URL` is correct.
   *Example*: `export DATABASE_URL=postgresql://event_user:event_pass@localhost:5432/event_db`
   
   *Note: On startup, SQLAlchemy will automatically create the database tables if they do not exist.*

3. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   
   The API will be accessible at `http://localhost:8000`. Test the health check at `/health`.

## Example API Requests

### 1. Register a User
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "secretpassword"
}'
```

### 2. Login to get JWT Token
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=johndoe&password=secretpassword'
```

*Extract the `access_token` from the response JSON.*

### 3. Create an Event
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/events/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Annual Tech Conference",
  "description": "Tech conference in 2026",
  "location": "Convention Center",
  "start_time": "2026-04-01T09:00:00",
  "end_time": "2026-04-03T18:00:00"
}'
```

### 4. Fetch Events
```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/events/' \
  -H 'accept: application/json'
```

## Inter-Service Communication

To communicate with this service from another microservice asynchronously or synchronously, make standard HTTP requests to the REST API via the internal Kubernetes Service hostname:
* Example Hostname: `http://event-service.default.svc.cluster.local`
* Example Create Event Request from Service B to Event Service:
```python
import requests
headers = {"Authorization": "Bearer SERVICE_JWT_TOKEN"}
payload = {"title": "Service B Event", "location": "Remote", "start_time": "...", "end_time": "..."}
response = requests.post("http://event-service.default.svc.cluster.local/api/v1/events/", json=payload, headers=headers)
```

## Kubernetes Deployment
Deploy using the provided manifests:
```bash
# Don't forget to create a Secret with the correct DATABASE_URL first!
# kubectl create secret generic db-secret --from-literal=database-url=postgresql://user:pass@host:5432/db
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```
