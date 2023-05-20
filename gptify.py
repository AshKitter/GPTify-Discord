import discord
from discord.ext import commands
from gpt4all import GPT4All

# DO NOT FORGET TO REPLACE THE PLACEHOLDER TOKEN WITH YOUR BOT's TOKEN FROM THE DISCORD DEVELOPER PROFILE
# IN ADDITION ENABLE ALL PRIVLEDGED INTENTS FOR THE BOT
TOKEN = "placeholder_token"

# Create a Discord bot.
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Create a GPT-4 model.
gptj = GPT4All("ggml-gpt4all-j-v1.3-groovy")

# Define a function to get the last message in a channel.
async def get_last_message(channel):
  async for message in channel.history(limit=1):
    return message

async def send_message(channel, message):
  # Reply to the original message without mentioning the author
  await channel.send(message, reference=channel.last_message, mention_author=True)

# Define an event handler for incoming messages.
@client.event
async def on_message(message):
  if message.author == client.user:
    return  # Ignore messages sent by the bot itself

  # Check if the message is from a guild (text channel) or a direct message.
  if message.guild is None:
    return  # Ignore direct messages

  # Get the channel that the message was sent in.
  channel = message.channel

  # Get the last message in the channel.
  last_message = await get_last_message(channel)

  # Set the prompt to the last message.
  prompt = last_message.content

  # Generate a response using the GPT-4 model.
  response = gptj.chat_completion([{"role": "user", "content": prompt}])

  # Extract the response from the formatted message.
  response_content = response['choices'][0]['message']['content']

  # Send the response as a reply to the original message.
  await send_message(channel, response_content)

# Connect the bot to Discord.
client.connect()

# Listen for messages in all channels.
client.listen()

# Run the bot.
client.run(TOKEN)
