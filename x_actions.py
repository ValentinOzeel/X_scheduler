from config import USER_INFO_EXPANSIONS, USER_INFO_TWEET_FIELDS, USER_INFO_USER_FIELDS
import time
from request_counter import request_counter

class RateLimiter:
    def __init__(self, max_requests, endpoint, period):
        self.max_requests = max_requests
        self.endpoint = endpoint
        self.period = period

    def is_limit_reached(self):
        current_count = request_counter.get_count(self.endpoint, self.period)
        if current_count + 1 < self.max_requests:
            return True
        return False

def get_user_info(client_v2):
    endpoint, period = 'user_info', 'daily'
    # Rate limiting for user info
    user_info_daily_limiter = RateLimiter(25, endpoint, period)  # 25 requests per 24 hours
    # Assert that the rate limiter allows the request
    try:
        assert user_info_daily_limiter.is_limit_reached(), 'User info daily rate limit exceeded (25 requests per 24 hours)'
    except AssertionError as e:
        print(e)
        return None
    
    # Get user info
    user_info = client_v2.get_me(
        expansions=USER_INFO_EXPANSIONS,
        tweet_fields=USER_INFO_TWEET_FIELDS,
        user_fields=USER_INFO_USER_FIELDS
    )
    
    request_counter.increment_count(endpoint, period)

    return user_info

def post_tweet(client_v1, client_v2, text, media_path=None):
    endpoint, period = 'post_tweet', ['daily', 'monthly']
    daily_limiter = RateLimiter(50, endpoint, period[0])  # 50 requests per 24 hours
    monthly_limiter = RateLimiter(1500, endpoint, period[1])  # 1500 requests per month
    
    try:
        assert daily_limiter.is_limit_reached(), 'Post tweet daily rate limit exceeded (50 requests per 24 hours)'
        assert monthly_limiter.is_limit_reached(), 'Post tweet monthly rate limit exceeded (1500 requests per month)'
    except AssertionError as e:
        print(e)
        return e
    
    media_id = None

    if media_path:
        media = client_v1.media_upload(filename=media_path)
        media_id = media.media_id
        
    tweet = client_v2.create_tweet(text=text, media_ids=[media_id] if media_id else None)
    request_counter.increment_count(endpoint, period[0])
    request_counter.increment_count(endpoint, period[1])
    return True