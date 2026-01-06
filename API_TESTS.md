# API Verification Instructions

You can use `curl` or Postman to test the API endpoints.

## Base URL
- **Local**: `http://localhost:5000` (Direct) or `http://localhost` (Nginx)
- **Production**: `https://api2.med44.site`

## 1. Health Check
Verify the service is running.
```bash
curl -X GET http://localhost/health
```
**Expected Output**: `{"status": "healthy"}`

## 2. Queue an Import Job (Google Drive)
```bash
curl -X POST http://localhost/import/google-drive \
  -H "Content-Type: application/json" \
  -d '{"folder_url": "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"}'
```
**Expected Output**:
```json
{
  "message": "Import job queued",
  "task_id": "<task_id>"
}
```

## 3. Check Task Status
Replace `<task_id>` with the ID received from the import request.
```bash
curl -X GET http://localhost/task/<task_id>
```
**Expected Output**:
```json
{
  "task_id": "<task_id>",
  "status": "SUCCESS" | "PENDING" | "FAILURE",
  "result": ...
}
```

## 4. List Imported Images
```bash
curl -X GET http://localhost/images
```
**Expected Output**: A list of image objects.
