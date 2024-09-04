You are and expert at coding in python and using X (formally Twitter) API with tremendous experience. 
I have a X free API tier want to build a professional project that will help me automate my work on X (formally Twitter).
Necessary credentials such as API keys, access tokens, access tokens secrets and bearer tokens are provided in a .env file.

The project should be written in world class modular python code and the features should be accessible via a Gradio app.

Here are the ONLY X api endpoints that I have access to:
- POST /2/tweets (limit: 50 requests per 24 hours, 1500 requests per month).
- GET /2/users/me (limit: 25 requests per 2 hours).

App pages:
- Authentication page. The user can login using necessary credentials and API keys. Page should show the user information obtained from GET /2/users/me endpoint upon succesful login.
- User's tweets schedule page. In this page their are a few features: 
  - Schedule new tweets (User select the schedule time and provide the tweet + potential media.)
  - View scheduled tweets
  - Edit scheduled tweets
  - Delete scheduled tweets
  - Reschedule scheduled tweets
                                                    
Instructions for the whole project:
- API requests (POST /2/tweets and GET /2/users/me) should be made using the tweepy library.
- The app should manage API rate limits on its own and make sure limits are NEVER REACHED.

Instructions specific to the Authentication page:
- Authentication page with authentification (OAuth1) that shows the user information obtained from GET /2/users/me upon succesful login.

Instructions for the User's tweets schedule page:
- The app user should be able to schedule tweets for future dates and times and post them when the time is reached.
- Scheduled posts should handle both text and media tweets.
- Scheduled posts are stored in a sqlite database (terxt content, scheduled datetime and potentially the media object's path) and are to be retrieved when the scheduled time is reached. 
- The app user should be able to edit, delete or reschedule the tweets.
- The app user should be able to select the schedule time and provide the tweet + potential media.








