import schedule
import time
from datetime import datetime

from database import get_scheduled_tweets, mark_tweet_as_posted, get_tweet_media
from auth import authenticate_v2, authenticate_v1
from x_actions import post_tweet, RateLimiter
import tempfile
import os



def post_scheduled_tweets():
    api_v2 = authenticate_v2()
    api_v1 = authenticate_v1()
    tweets = get_scheduled_tweets()
    now = datetime.now()

    for tweet in tweets:
        tweet_id, text, media_type, scheduled_time, _ = tweet
        scheduled_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")

        if scheduled_time <= now:
            try:
                # Get media path from sqlite
                media_path, _ = get_tweet_media(tweet_id)
                # Post tweet with media
                status = post_tweet(api_v1, api_v2, text, media_path)
                # Check if tweet has been posted otherwise raise an error
                assert status is True, status
                # Mark tweet as posted
                mark_tweet_as_posted(tweet_id)
                print(f"Posted tweet: {text}")
                
                # Delete the media file after posting
                if media_path and os.path.exists(media_path):
                    os.remove(media_path)
                    print(f"Deleted media file: {media_path}")
            except Exception as e:
                print(f"Error posting tweet: {e}")


def run_scheduler():
    schedule.every(1).minutes.do(post_scheduled_tweets)
    while True:
        schedule.run_pending()
        time.sleep(1)