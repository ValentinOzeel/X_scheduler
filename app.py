import gradio as gr
import threading
import os
import shutil
from auth import authenticate_v2
from x_actions import get_user_info
from database import add_scheduled_tweet, get_scheduled_tweets, update_scheduled_tweet, delete_scheduled_tweet, get_tweet_media
from tweet_scheduler import run_scheduler
import unicodedata
import emoji
from emoji import unicode_codes

def user_info():
    api = authenticate_v2()
    user_info = get_user_info(api)
    if user_info is None:
        return "Rate limit exceeded. Please try again later."
    # Return both the login message and the profile image URL
    user_details = (
        f"Logged in as: {user_info.data['name']}/{user_info.data['username']}\n"
        f"User ID: {user_info.data['id']}\n"
        f"Followers Count: {user_info.data['public_metrics']['followers_count']}\n"
        f"Following Count: {user_info.data['public_metrics']['following_count']}\n\n"
        f"Description:\n{user_info.data['description']}\n\n"
        f"Pinned tweet:\n{user_info.includes}\n\n"
    )
    return user_details, user_info.data['profile_image_url']

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
    font_styles = {
        "𝐁𝐨𝐥𝐝 𝐒𝐞𝐫𝐢𝐟": range(0x1D400, 0x1D41A),  # 𝐀 - 𝐙, 𝐚 - 𝐳
        "𝑰𝒕𝒂𝒍𝒊𝒄 𝑺𝒆𝒓𝒊𝒇": range(0x1D434, 0x1D44E),  # 𝐴 - 𝑍, 𝑎 - 𝑧
        "𝐁𝐨𝐥𝐝 𝐈𝐭𝐚𝐥𝐢𝐜 𝐒𝐞𝐫𝐢𝐟": range(0x1D468, 0x1D482),  # 𝑨 - 𝒁, 𝒂 - 𝒛
        "𝔉𝔯𝔞𝔨𝔱𝔲𝔯": range(0x1D504, 0x1D51E),  # 𝔄 - 𝔷
        "𝔅𝔬𝔩𝔡 𝔉𝔯𝔞𝔨𝔱𝔲𝔯": range(0x1D56C, 0x1D586),  # 𝕬 - 𝖟
        "𝒮𝒸𝓇𝒾𝓅𝓉": range(0x1D49C, 0x1D4B6),  # 𝒜 - 𝓏 (excluding 𝒧 and 𝓌)
        "𝐁𝐨𝐥𝐝 𝒮𝒸𝓇𝒾𝓅𝓉": range(0x1D4D0, 0x1D4EA),  # 𝒜 - 𝓏
        "𝓒𝓾𝓻𝓼𝓲𝓿𝓮":{
        'a': 0x1D4B6, 'b': 0x1D4B7, 'c': 0x1D4B8, 'd': 0x1D4B9, 'e': 0x1D4BA, 'f': 0x1D4BB,
        'g': 0x1D4BC, 'h': 0x1D4BD, 'i': 0x1D4BE, 'j': 0x1D4BF, 'k': 0x1D4C0, 'l': 0x1D4C1,
        'm': 0x1D4C2, 'n': 0x1D4C3, 'o': 0x1D4C4, 'p': 0x1D4C5, 'q': 0x1D4C6, 'r': 0x1D4C7,
        's': 0x1D4C8, 't': 0x1D4C9, 'u': 0x1D4CA, 'v': 0x1D4CB, 'w': 0x1D4CC, 'x': 0x1D4CD,
        'y': 0x1D4CE, 'z': 0x1D4CF,
        'A': 0x1D49C, 'B': 0x1D49D, 'C': 0x1D49E, 'D': 0x1D49F, 'E': 0x1D4A0, 'F': 0x1D4A1,
        'G': 0x1D4A2, 'H': 0x210B, 'I': 0x2110, 'J': 0x1D4A5, 'K': 0x1D4A6, 'L': 0x2112,
        'M': 0x2133, 'N': 0x1D4A9, 'O': 0x1D4AA, 'P': 0x1D4AB, 'Q': 0x1D4AC, 'R': 0x211B,
        'S': 0x1D4AE, 'T': 0x1D4AF, 'U': 0x1D4B0, 'V': 0x1D4B1, 'W': 0x1D4B2, 'X': 0x1D4B3,
        'Y': 0x1D4B4, 'Z': 0x1D4B5,
    },  # 𝓁 - 𝓏 (part of Script)
        "𝕄𝕒𝕥𝕙 𝔹𝕠𝕝𝕕": range(0x1D5D4, 0x1D5EE),  # 𝗔 - 𝗭, 𝗮 - 𝘇
        "𝕀𝕥𝕒𝕝𝕚𝕔 𝕄𝕒𝕥𝕙 𝕊𝕒𝕟𝕤": range(0x1D608, 0x1D622),  # 𝘈 - 𝘡, 𝘢 - 𝘻
        "𝕄𝕠𝕟𝕠𝕤𝕡𝕒𝕔𝕖": range(0x1D670, 0x1D68A),  # 𝚨 - 𝛀, 𝛂 - 𝛑 (Latin and Greek Letters)
        "𝕔𝕠𝕠𝕝": range(0x1D552, 0x1D56C),  # 𝕬 - 𝖟 (bold sans-serif letters)
        "ᴄᴀᴘs": range(0x1C90, 0x1CAA),  # Caps (Adlam Alphabet, partially matches description)
        "sᴍᴀʟʟ ᴄᴀᴘs": range(0x1D00, 0x1D1A),  # Small caps (Phonetic Extensions)
        "uʍop ǝpᴉsdn": {ord(c): ord(c) + 0x02E0 for c in 'abcdefghijklmnopqrstuvwxyz'},  # Upside down
        "𝔻𝕠𝕦𝕓𝕝𝕖-𝕤𝕥𝕣𝕦𝕔𝕜": range(0x1D538, 0x1D552),  # 𝔸 - 𝕫 (double-struck letters)
        "Ⓑⓤⓑⓑⓛⓔ": range(0x24B6, 0x24D0),  # Ⓐ - Ⓩ (Circled letters)
        "🅂🅀🅄🄰🅁🄴🄳": range(0x1F130, 0x1F14A),  # 🄰 - 🅉 (Squared letters)
        "S̶t̶r̶i̶k̶e̶t̶h̶r̶o̶u̶g̶h̶": range(0x0336, 0x0337),  # Combining long strikethrough
        "𝑈𝑛𝑑𝑒𝑟𝑙𝑖𝑛𝑒𝑑": range(0x1D670, 0x1D68A),  # Monospace also serves underlined in some fonts
        "ᵀᶦⁿʸ": range(0x1D67, 0x1D80),  # Superscript letters
        "ⒸⒾⓇⒸⓁⒺⒹ": range(0x24B8, 0x24D2),  # Circled letters
        "🄲🄻🄰🄼🄿🄴🄳": range(0x1F1E6, 0x1F200),  # Regional indicator symbols (used in emoji flags)
        "𝗕𝗼𝗹𝗱 𝗦𝗮𝗻𝘀-𝗦𝗲𝗿𝗶𝗳": range(0x1D5D4, 0x1D5EE),  # Bold sans-serif
        "𝘐𝘵𝘢𝘭𝘪𝘤 𝘚𝘢𝘯𝘴-𝘚𝘦𝘳𝘪𝘧": range(0x1D608, 0x1D622),  # Italic sans-serif
        "𝒜𝓁𝑒𝓍 𝐵𝓇𝓊𝓈𝒽 (Alex Brush)": {
        'A': 0x1D49C, 'B': 0x1D49D, 'C': 0x2102, 'D': 0x1D49F, 'E': 0x2130, 'F': 0x2131, 
        'G': 0x1D4A2, 'H': 0x210B, 'I': 0x2110, 'J': 0x1D4A5, 'K': 0x1D4A6, 'L': 0x2112, 
        'M': 0x2133, 'N': 0x1D4A9, 'O': 0x1D4AA, 'P': 0x1D4AB, 'Q': 0x1D4AC, 'R': 0x211B, 
        'S': 0x1D4AE, 'T': 0x1D4AF, 'U': 0x1D4B0, 'V': 0x1D4B1, 'W': 0x1D4B2, 'X': 0x1D4B3, 
        'Y': 0x1D4B4, 'Z': 0x1D4B5,
        'a': 0x1D4B6, 'b': 0x1D4B7, 'c': 0x1D4B8, 'd': 0x1D4B9, 'e': 0x212F, 'f': 0x1D4BB, 
        'g': 0x210A, 'h': 0x1D4BD, 'i': 0x1D4BE, 'j': 0x1D4BF, 'k': 0x1D4C0, 'l': 0x1D4C1, 
        'm': 0x1D4C2, 'n': 0x1D4C3, 'o': 0x2134, 'p': 0x1D4C5, 'q': 0x1D4C6, 'r': 0x1D4C7, 
        's': 0x1D4C8, 't': 0x1D4C9, 'u': 0x1D4CA, 'v': 0x1D4CB, 'w': 0x1D4CC, 'x': 0x1D4CD, 
        'y': 0x1D4CE, 'z': 0x1D4CF,
    }
    }

    if font_style not in font_styles:
        return text
    
    #formatted_text = ""
    #for char in text:
    #    if char.isalpha():
    #        if font_style == "uʍop ǝpᴉsdn":
    #            formatted_char = chr(font_styles[font_style].get(ord(char.lower()), ord(char)))
    #            formatted_text = formatted_char + formatted_text  # Prepend for upside down
    #        else:
    #            offset = ord(char.lower()) - ord('a')
    #            if 0 <= offset < 26:
    #                formatted_char = chr(font_styles[font_style][offset])
    #                formatted_text += formatted_char
    #            else:
    #                formatted_text += char
    #    else:
    #        if font_style == "uʍop ǝpᴉsdn":
    #            formatted_text = char + formatted_text  # Prepend for upside down
    #        else:
    #            formatted_text += char
    #
    mapping = font_styles[font_style]
    formatted_text = ''.join(chr(mapping[char]) if char in mapping else char for char in text)
    return formatted_text

def create_app():
    with gr.Blocks() as app:
        gr.Markdown("# X (Twitter) Scheduler")
        
        with gr.Tab("User info"):
            user_info_button = gr.Button("Get my info")
            user_info_output = gr.Textbox(label="User info")
            profile_image = gr.Image(label="Profile Image")  # Image component for profile image
            user_info_button.click(user_info, outputs=[user_info_output, profile_image])  # Update outputs to include the image
            
        with gr.Tab("Schedule Tweets"):
            text_input = gr.Textbox(label="Tweet Text")
            media_input = gr.File(label="Media (optional)")
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
            edit_text_input = gr.Textbox(label="New Tweet Text")
            edit_media_input = gr.File(label="New Media (optional)")
            edit_date_input = gr.Textbox(label="New Date (YYYY-MM-DD)")
            edit_time_input = gr.Textbox(label="New Time (HH:MM)")
            edit_button = gr.Button("Edit Tweet")
            delete_button = gr.Button("Delete Tweet")
            edit_output = gr.Textbox(label="Edit/Delete Status")
            edit_button.click(edit_tweet, inputs=[tweet_id_input, edit_text_input, edit_media_input, edit_date_input, edit_time_input], outputs=edit_output)
            delete_button.click(delete_tweet, inputs=[tweet_id_input], outputs=edit_output)

        with gr.Tab("Text Formatter"):
            input_text = gr.Textbox(label="Input Text")
            font_style = gr.Dropdown(
                choices=[
                            "𝐁𝐨𝐥𝐝 𝐒𝐞𝐫𝐢𝐟",
                            "𝑰𝒕𝒂𝒍𝒊𝒄 𝑺𝒆𝒓𝒊𝒇",
                            "𝐁𝐨𝐥𝐝 𝐈𝐭𝐚𝐥𝐢𝐜 𝐒𝐞𝐫𝐢𝐟",
                            "𝔉𝔯𝔞𝔨𝔱𝔲𝔯",
                            "𝐁𝐨𝐥𝐝 𝔉𝔯𝔞𝔨𝔱𝔲𝔯",
                            "𝒮𝒸𝓇𝒾𝓅𝓉",
                            "𝐁𝐨𝐥𝐝 𝒮𝒸𝓇𝒾𝓅𝓉",
                            "𝓒𝓾𝓻𝓼𝓲𝓿𝓮",
                            "𝕄𝕒𝕥𝕙 𝔹𝕠𝕝𝕕",
                            "𝕀𝕥𝕒𝕝𝕚𝕔 𝕄𝕒𝕥𝕙 𝕊𝕒𝕟𝕤",
                            "𝕄𝕠𝕟𝕠𝕤𝕡𝕒𝕔𝕖",
                            "𝕔𝕠𝕠𝕝",
                            "ᴄᴀᴘs",
                            "sᴍᴀʟʟ ᴄᴀᴘs",
                            "uʍop ǝpᴉsdn",
                            "𝔻𝕠𝕦𝕓𝕝𝕖-𝕤𝕥𝕣𝕦𝕔𝕜",
                            "Ⓑⓤⓑⓑⓛⓔ",
                            "🅂🅀🅄🄰🅁🄴🄳",
                            "S̶t̶r̶i̶k̶e̶t̶h̶r̶o̶u̶g̶h̶",
                            "𝑈𝑛𝑑𝑒𝑟𝑙𝑖𝑛𝑒𝑑",
                            "ᵀᶦⁿʸ",
                            "ⒸⒾⓇⒸⓁⒺⒹ",
                            "🄲🄻🄰🄼🄿🄴🄳",
                            "𝗕𝗼𝗹𝗱 𝗦𝗮𝗻𝘀-𝗦𝗲𝗿𝗶𝗳",
                            "𝘐𝘵𝘢𝘭𝘪𝘤 𝘚𝘢𝘯𝘴-𝘚𝘦𝘳𝘪𝘧",
                            "𝒜𝓁𝑒𝓍 𝐵𝓇𝓊𝓈𝒽 (Alex Brush)"
                        ],
                label="Font Style"
            )



            format_button = gr.Button("Format Text")
            output_text = gr.Textbox(label="Formatted Text")



            def format_and_add_emoji(text, style):
                formatted = format_text(text, style)
                return f"{formatted}"

            format_button.click(format_and_add_emoji, inputs=[input_text, font_style], outputs=output_text)

    return app