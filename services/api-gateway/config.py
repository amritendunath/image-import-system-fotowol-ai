import os

class Config:
    # Database
    DB_HOST = os.getenv('DB_HOST', 'postgres')
    DB_NAME = os.getenv('DB_NAME', 'imagedb')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    # Redis / Celery
    REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    
    # Storage
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
