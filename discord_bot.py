import discord
from discord.ext import commands
# import asyncio

from dotenv import load_dotenv
import os

from utils import format_to_table
from find_who_is_out import get_who_is_out

load_dotenv()

# Replace the following with your bot's token and the target channel ID
BOT_TOKEN = os.getenv("DISCORD_TOKEN")  # Replace with your bot token
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Replace with the target channel ID


if not isinstance(CHANNEL_ID, int):
    try:
        CHANNEL_ID = int(CHANNEL_ID)
    except Exception as exp:
        raise ValueError(f"Channel id is incorrect. {exp}")


who_is_out = get_who_is_out()
MESSAGE = format_to_table(who_is_out)



# Create an instance of the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    try:
        # Fetch the channel using its ID
        channel = bot.get_channel(CHANNEL_ID)
        if channel is None:
            print("Channel not found. Make sure the CHANNEL_ID is correct.")
            return

        # Send the message
        await channel.send(MESSAGE, silent=True)
        print("Message sent successfully!")

        # Close the bot after sending the message
        await bot.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the bot
bot.run(BOT_TOKEN)
