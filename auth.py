import tweepy
from config import (
    API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN,
)

def authenticate_v2():
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        bearer_token=BEARER_TOKEN
    )
    return client

def authenticate_v1():
    auth = tweepy.OAuth1UserHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET,
    )
    return tweepy.API(auth)

