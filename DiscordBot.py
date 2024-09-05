import os
import discord
from discord.ext import commands
import requests

# Remember to replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token
BOT_TOKEN = "YOUR_REAL_BOT_TOKEN"
CHANNEL_ID = "YOUR_REAL_CHANNEL_ID"  # Use integer, not string
file_path = r"YOUR_REAL_DIRECTORY"


intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())



async def fetch_messages():
    print(f'Current working directory: {os.getcwd()}')
    channel = bot.get_channel(CHANNEL_ID)
    
    if not channel:
        print("Channel not found.")
        return
    
    messages = []
    last_message = None

    while True:
        # Fetch messages in batches of 100
        fetched_messages = channel.history(limit=100, after=last_message)
        batch = []
        async for message in fetched_messages:
            batch.append(message)
            last_message = message  # Update the last message to fetch the next batch

        if not batch:
            break  # No more messages to fetch

        messages.extend(batch)

    print(f'Fetched {len(messages)} messages.')

    dir_name = os.path.dirname(file_path)
    if not os.path.exists(dir_name):
        print(f"Error: Directory '{dir_name}' does not exist.")
        return

    try:
        # Write messages to a text file at the specified path
        with open(file_path, 'w', encoding='utf-8') as f:
            for message in messages:
                f.write(f'{message.author} ({message.created_at}): {message.content}\n')
                
                for attachment in message.attachments:
                    if attachment.url.endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Check for common video file extensions
                        f.write(f'{message.author} ({message.created_at}): Video attachment - {attachment.url}\n')

        print(f"Messages have been written to '{file_path}'.")
        print(f"File location: {file_path}")

    except IOError as e:
        print(f"Error: Unable to write to file '{file_path}'. Details: {e}")



@bot.event

async def on_ready():
    while True:
        print("\nMenu:")
        print("1. Fetch messages")
        print("2. Option 2 - Coming Soon")
        print("3. Option 3 - Coming Soon")
        
        user_input = input("Please select an option (1, 2, or 3): ")
        
        if user_input.isdigit():
            choice = int(user_input)
            if choice == 1:
                print("Fetching messages...")
                await fetch_messages()
            elif choice == 2 or choice == 3:
                print("Coming Soon")
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
                continue  # Prompt user again
            
            break  # Exit the loop and end the program
        else:
            print("Invalid input. Please enter an integer.") # Error Handling






bot.run(BOT_TOKEN)
