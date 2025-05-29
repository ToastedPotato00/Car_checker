import discord
import os
from discord.ext import commands
from car_detector import image_detection
from carbon_check import car_carbon
intents = discord.Intents.default()
intents.message_content = True

SAVE_FOLDER = "saved_images"

def has_image_attachment(message):
    """
    Checks if a message contains an image attachment
    
    Parameters:
    message (discord.Message): The Discord message to check
    
    Returns:
    bool: True if the message contains an image attachment, false otherwise
    """
    # Check if the message has any attachments
    if len(message.attachments) == 0:
        return False
    
    # Array of common image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg']
    
    # Check if any attachment has an image file extension
    for attachment in message.attachments:
        attachment_name = attachment.filename.lower() if attachment.filename else ''
        
        # Check for image extension or content_type
        if any(attachment_name.endswith(ext) for ext in image_extensions) or \
           (attachment.content_type and attachment.content_type.startswith('image/')):
            return True
    
    return False


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        # Get the directory where the script is running
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Create a path to the saved_images folder within that directory
        save_path = os.path.join(script_dir, SAVE_FOLDER)
        # Create the directory
        os.makedirs(save_path, exist_ok=True)
        print(f"Created or verified save folder: {save_path}")
    except Exception as e:
        print(f"Error creating directory: {e}")

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)


@bot.command()
async def check_car(ctx):
    if has_image_attachment(ctx.message):
        saved_files = []
        for attachment in ctx.message.attachments:
            attachment_name = attachment.filename.lower()
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg']
            
            # Only save if it's an image
            if any(attachment_name.endswith(ext) for ext in image_extensions):
                try:
                    # Get the file extension from the original filename
                    file_extension = os.path.splitext(attachment.filename)[1]
                    
                    # Use a fixed filename that will overwrite previous saves
                    filename = f"saved_image_1{file_extension}"
                    filepath = os.path.join(SAVE_FOLDER, filename)
                    
                    # Save the file with the new name
                    await attachment.save(filepath)
                    
                    saved_files.append(filepath)
                    print(f"Image saved to {filepath}")
                    print(f"Original URL: {attachment.url}")
                except Exception as e:
                    print(f"Error saving image: {e}")
            else:
                await ctx.send("error saving image")
            
            car_detected = image_detection(filepath)      
            if car_detected:
                carbon_check = car_carbon(filepath)

                if carbon_check == "Pass":
                    await ctx.send("The car pass the test")
                elif carbon_check == "Didn't pass":
                    await ctx.send("The car didn't pass the test")
                    await ctx.send("You need to change your car")
                
            else:
                await ctx.send("No car detected in the image.")

bot.run("token")