import threading
from app import create_app
from tweet_scheduler import run_scheduler
from database import create_tables

if __name__ == "__main__":
    create_tables()
    
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    
    app = create_app()
    app.launch()