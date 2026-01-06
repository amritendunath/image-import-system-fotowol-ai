import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def init_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'imagedb'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
        )
        cur = conn.cursor()
        
        # Read init.sql
        with open('../init.sql', 'r') as f:
            sql_commands = f.read()
            
        print("Executing SQL schema...")
        cur.execute(sql_commands)
        conn.commit()
        
        cur.close()
        conn.close()
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == '__main__':
    init_db()
