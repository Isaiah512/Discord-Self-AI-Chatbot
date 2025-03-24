"""
Bot commands
"""
from bot.memory import get_user_memory, get_channel_context
from bot.ai_service import process_text_query, process_image_query
from bot.image_service import generate_image
from utils.helpers import send_chunked_message, extract_user_info
import discord

async def handle_help_command(message):
    """Display help message."""
    help_text = (
        "**How to use me**\n"
        "`help` - Show this help message\n"
        "`your text` - Chat with the bot\n"
        "`prompt + image attachment` - Analyze an image\n"
        "`imagine` - Generate an image\n"
    )
    await message.channel.send(help_text)

async def handle_text_command(message, query):
    """Handle text messages."""
    if not query:
        await message.channel.send("Please provide a message after mentioning me.")
        return
    
    try:
        user_id = str(message.author.id)
        conversation_memory = get_user_memory(user_id)
        channel_context = get_channel_context(str(message.channel.id))
        user_info = extract_user_info(message.author)
        
        response_content = await process_text_query(
            conversation_memory, 
            query, 
            channel_context,
            user_info
        )
        
        await send_chunked_message(message.channel, response_content)
        
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")
        print(f"Error in text processing: {e}")

async def handle_image_command(message, prompt):
    """Handle computer vision."""
    attachments = message.attachments
    
    try:
        channel_context = get_channel_context(str(message.channel.id))
        user_info = extract_user_info(message.author)
        
        if len(attachments) > 1:
            await message.channel.send(f"Processing {len(attachments)} attachments...")
        
        response_text = await process_image_query(
            prompt,
            attachments,
            channel_context,
            user_info
        )
        
        await send_chunked_message(message.channel, response_text)
        
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")
        print(f"Error in image processing: {e}")

async def handle_image_generation_command(message, prompt):
    """Handle image generation."""
    if not prompt:
        await message.channel.send("Please provide a prompt for image generation.")
        return
    
    try:
        processing_msg = await message.channel.send("Generating image, please wait...")
        image_path = await generate_image(prompt)

        await processing_msg.delete()
        if not image_path.endswith('.png'):
            await message.channel.send(image_path)
            return
        
        with open(image_path, 'rb') as image_file:
            picture = discord.File(image_file, filename='generated_image.png')
            await message.channel.send(f"Generated image for prompt: *{prompt}*", file=picture)
        
    except Exception as e:
        await message.channel.send(f"An error occurred during image generation: {str(e)}")
        print(f"Image generation error: {e}")
