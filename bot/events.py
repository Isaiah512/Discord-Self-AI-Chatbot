"""
Discord event handlers
"""
from bot.memory import store_channel_message, store_user_info
from bot.commands import (
    handle_help_command, 
    handle_text_command, 
    handle_image_command,
    handle_image_generation_command
)
from utils.helpers import extract_user_info

async def on_ready(client):
    """Called when the client has successfully connected to Discord."""
    print(f'Logged in as {client.user.name} (ID: {client.user.id})')
    print('------')
    print('Ready to respond to messages..')

async def on_message(client, message):
    """Process incoming messages."""
    # Store the message in channel history
    store_channel_message(message)
    
    # Skip processing if message is from the client itself
    if message.author.id == client.user.id:
        return
    
    # Store user info
    user_id = str(message.author.id)
    user_info = extract_user_info(message.author)
    store_user_info(user_id, user_info)
        
    # Process commands when the client is mentioned
    if client.user in message.mentions:
        content = message.content.replace(f'<@{client.user.id}>', '').strip()
        
        if content.lower() == 'help':
            await handle_help_command(message)
        elif content.lower().startswith(('imagine ')):
            gen_prompt = content.split(' ', 1)[1] if len(content.split()) > 1 else ''
            await handle_image_generation_command(message, gen_prompt)
        elif message.attachments:
            await handle_image_command(message, content)
        else:
            await handle_text_command(message, content)
