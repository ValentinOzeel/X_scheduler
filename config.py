import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

DATABASE_NAME = "tweets.db"


USER_INFO_EXPANSIONS = 'pinned_tweet_id'
USER_INFO_TWEET_FIELDS = ['attachments', 'organic_metrics', 'public_metrics']
USER_INFO_USER_FIELDS = ['created_at', 
                     'description', 
                     'entities', 'id', 'location', 
                     'most_recent_tweet_id', 
                     'name', 'username',
                     'pinned_tweet_id', 
                     'profile_image_url', 
                     'protected', 
                     'public_metrics', 
                     'url', 
                     'verified', 'verified_type'] 


#if __name__ == "__main__":
#    print(API_KEY)
#    print(API_KEY_SECRET)
#    print(ACCESS_TOKEN)
#    print(ACCESS_TOKEN_SECRET)
#    print(BEARER_TOKEN)
#    print(DATABASE_NAME)