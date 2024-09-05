import gradio as gr
import json
import os
import requests

from auth import authenticate_v2
from x_actions import get_user_info
from database import add_scheduled_tweet, get_scheduled_tweets, update_scheduled_tweet, delete_scheduled_tweet, get_tweet_media

from constants import UNICODE_FONTS, EMOJI_CATEGORIES, USER_INFO_FILE, PROFILE_IMAGE_FILE


def load_user_info():
    if os.path.exists(USER_INFO_FILE):
        with open(USER_INFO_FILE, 'r') as f:
            return json.load(f)
    return None

def save_user_info(user_details, profile_image_url):
    # Download and save the profile image
    response = requests.get(profile_image_url)
    if response.status_code == 200:
        with open(PROFILE_IMAGE_FILE, 'wb') as f:
            f.write(response.content)
    
    with open(USER_INFO_FILE, 'w') as f:
        json.dump({"user_details": user_details, "profile_image_path": PROFILE_IMAGE_FILE}, f)
 
def user_info():
    api = authenticate_v2()
    user_info = get_user_info(api)
    if user_info is None:
        return "Rate limit exceeded. Please try again later.", None
    # Return both the login message and the profile image URL
    user_details = (
        f"Logged in as: {user_info.data['name']}/{user_info.data['username']}\n"
        f"User ID: {user_info.data['id']}\n"
        f"Followers Count: {user_info.data['public_metrics']['followers_count']}\n"
        f"Following Count: {user_info.data['public_metrics']['following_count']}\n\n"
        f"Description:\n{user_info.data['description']}\n\n"
        f"Pinned tweet:\n{user_info.includes}\n\n"
    )
    save_user_info(user_details, user_info.data['profile_image_url'])
    return user_details, PROFILE_IMAGE_FILE

def schedule_tweet(text, media_path, date, time):
    scheduled_time = f"{date} {time}:00"
    media_type = media_path.split('.')[-1] if media_path else None
    tweet_id = add_scheduled_tweet(text, media_path, media_type, scheduled_time)
    return f"Tweet scheduled with ID: {tweet_id}"

def view_scheduled_tweets():
    tweets = get_scheduled_tweets()
    return "\n".join([f"ID: {t[0]}, Text: {t[1]}, Media: {'Yes' if t[2] else 'No'}, Scheduled: {t[3]}" for t in tweets])

def edit_tweet(tweet_id, text, media_path, date, time):
    scheduled_time = f"{date} {time}:00"
    media_type = media_path.split('.')[-1] if media_path else None
    update_scheduled_tweet(tweet_id, text, media_path, media_type, scheduled_time)
    return f"Tweet {tweet_id} updated"

def delete_tweet(tweet_id):
    delete_scheduled_tweet(tweet_id)
    return f"Tweet {tweet_id} deleted"

def format_text(text, font_style):
    if font_style not in UNICODE_FONTS:
        return text
    
    mapping = UNICODE_FONTS[font_style]
    formatted_text = ''.join(chr(mapping[char]) if char in mapping else char for char in text)
    return formatted_text


def create_app():
    theme = gr.themes.Base(
        primary_hue="indigo",
        secondary_hue="purple",
        neutral_hue="slate",
        font=("Space Grotesk", "sans-serif"),
    ).set(
        body_background_fill="linear-gradient(to bottom, #0a0a2a, #1a1a4a)",
        body_background_fill_dark="linear-gradient(to bottom, #0a0a2a, #1a1a4a)",
        button_primary_background_fill="linear-gradient(90deg, #4b0082, #8a2be2)",
        button_primary_background_fill_dark="linear-gradient(90deg, #4b0082, #8a2be2)",
        button_primary_background_fill_hover="linear-gradient(90deg, #5c1199, #9d3cf3)",
        button_primary_border_color="rgba(138, 43, 226, 0.5)",
        button_primary_text_color="white",
        background_fill_primary="#1a1a4a",
        background_fill_primary_dark="#1a1a4a",
        block_title_text_color="#e0e0ff",
        block_title_background_fill="rgba(138, 43, 226, 0.2)",
        input_background_fill="rgba(255, 255, 255, 0.05)",
        input_background_fill_dark="rgba(255, 255, 255, 0.05)",
        input_border_color="rgba(138, 43, 226, 0.5)",
        input_border_color_dark="rgba(138, 43, 226, 0.5)",
    )

    with gr.Blocks(theme=theme, css="#galaxy-bg{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;pointer-events:none;}") as app:
        gr.Markdown(
            """
            # 🌌 𝕏 -- Posts Scheduler 🌌
            """
        )
        
        with gr.Tab("User info"):
            # Load saved user info on app start
            saved_info = load_user_info()

                
            user_info_button = gr.Button("Get/Actualize my info")
            with gr.Row():
                user_info_output = gr.Textbox(label="User info", value=saved_info["user_details"] if saved_info else None)
                profile_image = gr.Image(label="Profile Image", value=PROFILE_IMAGE_FILE)
            


            user_info_button.click(user_info, outputs=[user_info_output, profile_image])
            
        with gr.Tab("Text Formatter"):

            input_text = gr.Textbox(label="Post Builder", lines=5, show_copy_button=True)
            
            with gr.Row():
                to_format_text = gr.Textbox(label="To Format Text", lines=3)

            with gr.Row(variant="compact"):
                font_style = gr.Dropdown(choices=list(UNICODE_FONTS.keys()), label="Font Style")
                emoji_category = gr.Dropdown(choices=list(EMOJI_CATEGORIES.keys()), label="Emoji Category")
                emoji_selector = gr.Dropdown(label="Select Emoji", interactive=True)
                
            formatted_output = gr.Textbox(label="Formatted Text", lines=3, interactive=False, show_copy_button=True)
            
            def update_emoji_choices(category):
                return gr.Dropdown(choices=EMOJI_CATEGORIES[category])

            def add_emoji_to_text(text, emoji):
                return text + emoji

            emoji_category.change(update_emoji_choices, inputs=[emoji_category], outputs=[emoji_selector])
            emoji_selector.change(add_emoji_to_text, inputs=[to_format_text, emoji_selector], outputs=[to_format_text])
            font_style.change(format_text, inputs=[to_format_text, font_style], outputs=[formatted_output])
            
        with gr.Tab("Schedule Tweets"):
            text_input = gr.Textbox(label="Tweet Text", lines=5)
            with gr.Accordion("Click there to add a media file", open=False):
                media_input = gr.File(label="Media (optional)")
            with gr.Row():  
                date_input = gr.Textbox(label="Date (YYYY-MM-DD)")
                time_input = gr.Textbox(label="Time (HH:MM)")
            schedule_button = gr.Button("Schedule Tweet")
            schedule_output = gr.Textbox(label="Schedule Status")
            schedule_button.click(schedule_tweet, inputs=[text_input, media_input, date_input, time_input], outputs=schedule_output)
        
        with gr.Tab("View Scheduled Tweets"):
            view_button = gr.Button("View Scheduled Tweets")
            view_output = gr.Textbox(label="Scheduled Tweets")
            view_button.click(view_scheduled_tweets, outputs=view_output)
        
        with gr.Tab("Edit/Delete Tweets"):
            tweet_id_input = gr.Number(label="Tweet ID")
            edit_text_input = gr.Textbox(label="New Tweet Text", lines=5)
            with gr.Accordion("Click there to add a media file", open=False):
                edit_media_input = gr.File(label="New Media (optional)")
            with gr.Row():  
                edit_date_input = gr.Textbox(label="New Date (YYYY-MM-DD)")
                edit_time_input = gr.Textbox(label="New Time (HH:MM)")
            edit_button = gr.Button("Edit Tweet")
            delete_button = gr.Button("Delete Tweet")
            edit_output = gr.Textbox(label="Edit/Delete Status")
            edit_button.click(edit_tweet, inputs=[tweet_id_input, edit_text_input, edit_media_input, edit_date_input, edit_time_input], outputs=edit_output)
            delete_button.click(delete_tweet, inputs=[tweet_id_input], outputs=edit_output)

    return app