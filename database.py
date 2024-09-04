import sqlite3
from datetime import datetime
from config import DATABASE_NAME

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scheduled_tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            media_path TEXT,
            media_type TEXT,
            scheduled_time DATETIME NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

def add_scheduled_tweet(text, media_path, media_type, scheduled_time):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scheduled_tweets (text, media_path, media_type, scheduled_time)
        VALUES (?, ?, ?, ?)
    ''', (text, media_path, media_type, scheduled_time))
    tweet_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return tweet_id

def get_scheduled_tweets():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, text, media_type, scheduled_time, status FROM scheduled_tweets WHERE status = "pending" ORDER BY scheduled_time')
    tweets = cursor.fetchall()
    conn.close()
    return tweets

def get_tweet_media(tweet_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT media_path, media_type FROM scheduled_tweets WHERE id = ?', (tweet_id,))
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, None)

def update_scheduled_tweet(tweet_id, text, media_path, media_type, scheduled_time):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE scheduled_tweets
        SET text = ?, media_path = ?, media_type = ?, scheduled_time = ?
        WHERE id = ?
    ''', (text, media_path, media_type, scheduled_time, tweet_id))
    conn.commit()
    conn.close()

def delete_scheduled_tweet(tweet_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM scheduled_tweets WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()

def mark_tweet_as_posted(tweet_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE scheduled_tweets SET status = "posted" WHERE id = ?', (tweet_id,))
    conn.commit()
    conn.close()