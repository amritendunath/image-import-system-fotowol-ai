from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from celery import Celery
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = Flask(__name__)
CORS(app)

# Celery configuration
celery = Celery(
    'tasks',
    broker=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://redis:6379/0')
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('DB_NAME', 'imagedb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres')
    )

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/import/google-drive', methods=['POST'])
def import_google_drive():
    data = request.get_json()
    folder_url = data.get('folder_url')
    
    if not folder_url:
        return jsonify({'error': 'folder_url is required'}), 400
    
    # Queue the import job
    task = celery.send_task(
        'worker.import_images',
        args=[folder_url, 'google_drive']
    )
    
    return jsonify({
        'message': 'Import job queued',
        'task_id': task.id
    }), 202

@app.route('/import/dropbox', methods=['POST'])
def import_dropbox():
    data = request.get_json()
    folder_url = data.get('folder_url')
    
    if not folder_url:
        return jsonify({'error': 'folder_url is required'}), 400
    
    task = celery.send_task(
        'worker.import_images',
        args=[folder_url, 'dropbox']
    )
    
    return jsonify({
        'message': 'Import job queued',
        'task_id': task.id
    }), 202

@app.route('/images', methods=['GET'])
def get_images():
    source = request.args.get('source')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    if source:
        cur.execute("""
            SELECT id, name, google_drive_id, size, mime_type, 
                   storage_path, source, created_at
            FROM images WHERE source = %s
            ORDER BY created_at DESC
        """, (source,))
    else:
        cur.execute("""
            SELECT id, name, google_drive_id, size, mime_type, 
                   storage_path, source, created_at
            FROM images ORDER BY created_at DESC
        """)
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
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
    
    return jsonify({'images': images, 'count': len(images)}), 200

@app.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'task_id': task_id,
        'status': task.state,
        'result': task.result if task.ready() else None
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)