# 🌌 𝕏 (Twitter) Posts Scheduler

A powerful and elegant Python-based application for scheduling and managing posts on 𝕏 (formerly Twitter). This project leverages the 𝕏 API to provide a seamless experience for users to schedule, format, edit, and delete tweets, all within a beautiful Gradio interface.

## 🌟 Features

- **User Authentication**: Securely log in using 𝕏 API credentials.
- **User Info Display**: View and update your 𝕏 profile information.
- **Text Formatting**: Enhance your tweets with unicode fonts and emojis.
- **Tweet Scheduling**: Schedule tweets for future posting, including media attachments.
- **Tweet Management**: View, edit, and delete scheduled tweets.
- **Rate Limiting**: Built-in rate limit management to ensure API compliance.
- **Persistent Storage**: SQLite database for reliable tweet storage and management.

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- 𝕏 Developer Account with API credentials

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/ValentinOzeel/X_scheduler.git
   cd X_scheduler
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   API_KEY=your_api_key
   API_KEY_SECRET=your_api_key_secret
   ACCESS_TOKEN=your_access_token
   ACCESS_TOKEN_SECRET=your_access_token_secret
   BEARER_TOKEN=your_bearer_token
   ```

### Running the Application

1. Start the application:
   ```
   python main.py
   ```

2. Open the provided Gradio interface URL in your web browser.

## 🛠 Usage

### User Info Tab
- Click "Get/Actualize my info" to fetch and display your 𝕏 profile information.

### Text Formatter Tab
- Use the "Post Builder" to craft your tweet.
- Apply unicode fonts and add emojis to enhance your text.

### Schedule Tweets Tab
- Enter your tweet text, optionally upload media, and set the date and time for posting.
- Click "Schedule Tweet" to add it to the queue.

### View Scheduled Tweets Tab
- Click "View Scheduled Tweets" to see all pending tweets.

### Edit/Delete Tweets Tab
- Enter a Tweet ID to edit or delete a scheduled tweet.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/ValentinOzeel/X_scheduler/issues).

## 📜 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## 🙏 Acknowledgements

- [Tweepy](https://www.tweepy.org/)
- [Gradio](https://www.gradio.app/)
- [SQLite](https://www.sqlite.org/)

---
