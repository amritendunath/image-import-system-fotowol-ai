from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os
from celery import Celery
from dotenv import load_dotenv
from typing import Optional, List

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = FastAPI(title="Image Import API", description="API for importing images from Cloud Storage")

# CORS Configuration
origins = ["*"]  # In production, restrict this to your Vercel URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Celery Configuration
celery = Celery(
    'tasks',
    broker=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://redis:6379/0')
)

# Pydantic Models for Request Validation
class ImportRequest(BaseModel):
    folder_url: str

class TaskResponse(BaseModel):
    message: str
    task_id: str

class Image(BaseModel):
    id: int
    name: str
    google_drive_id: Optional[str]
    size: int
    mime_type: Optional[str]
    storage_path: str
    source: str
    created_at: Optional[str]

class ImagesResponse(BaseModel):
    images: List[Image]
    count: int

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('DB_NAME', 'imagedb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/import/google-drive", response_model=TaskResponse, status_code=202)
def import_google_drive(request: ImportRequest):
    if not request.folder_url:
        raise HTTPException(status_code=400, detail="folder_url is required")
    
    # Queue the import job
    task = celery.send_task(
        'worker.import_images',
        args=[request.folder_url, 'google_drive']
    )
    
    return {
        "message": "Import job queued",
        "task_id": task.id
    }

@app.post("/import/dropbox", response_model=TaskResponse, status_code=202)
def import_dropbox(request: ImportRequest):
    if not request.folder_url:
        raise HTTPException(status_code=400, detail="folder_url is required")
    
    task = celery.send_task(
        'worker.import_images',
        args=[request.folder_url, 'dropbox']
    )
    
    return {
        "message": "Import job queued",
        "task_id": task.id
    }

@app.get("/images", response_model=ImagesResponse)
def get_images(source: Optional[str] = Query(None)):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT id, name, google_drive_id, size, mime_type, 
                   storage_path, source, created_at
            FROM images 
        """
        
        if source:
            query += " WHERE source = %s"
            params = (source,)
        else:
            params = ()
            
        query += " ORDER BY created_at DESC"
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        images = []
        for row in rows:
            images.append({
                'id': row[0],
                'name': row[1],
                'google_drive_id': row[2],
                'size': row[3],
                'mime_type': row[4],
                'storage_path': row[5],
                'source': row[6],
                'created_at': row[7].isoformat() if row[7] else None
            })
        
        cur.close()
        conn.close()
        
        return {"images": images, "count": len(images)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/task/{task_id}")
def get_task_status(task_id: str):
    task = celery.AsyncResult(task_id)
    result = task.result if task.ready() else None
    
    # Handle serialization of result if needed
    if isinstance(result, Exception):
        result = str(result)
        
    return {
        "task_id": task_id,
        "status": task.state,
        "result": result
    }

# Ensure we run with Uvicorn when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
