
import discord
from discord.ext import commands 
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build 
import random

# load tokens
load_dotenv()
api_key = os.getenv('YOUTUBE_KEY')
discord_token = os.getenv('DISCORD_TOKEN')

youtube = build('youtube', 'v3', developerKey = api_key)

intents=discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents)


def search(video_type):
    """
    Given a string, the function will request the API to search and provide a
    list of 25 Youtube Videos that best match the prompt. A random video is
    chosen from the list, and a url of the video is returned.

    Args:
        video_type: A string representing the prompt to be searched on Youtube.
    Returns:
        A string representing a url of a randomly chosen video.
    """
    # request is made to youtube and executed
    request = youtube.search().list(
        part='snippet',
        maxResults=25,
        order='relevance',
        q=video_type,
        type='video'
    ).execute()

    # random number/index is chosen
    random_idx = random.randrange(26)

    return "https://www.youtube.com/watch?v=" + request['items'][random_idx]['id']['videoId']

@bot.event
async def on_ready():  #upon bot startup
    print('logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    """
    Shows bot response latency time. 
    """
    await ctx.send(f'pong! {round(bot.latency * 1000)}ms')

@bot.command(aliases=['cutedogs', 'cutedog', 'cutepuppies', 'cutepup'])
async def dog(ctx):        # context passed in automatically by discord
    """
    Sends a random video of cute dogs.
    """
    url = search("cute dogs")
    await ctx.send(url)

@bot.command(aliases=['cutecat', 'cutecats', 'cutekittens', 'cutekitties'])
async def cat(ctx):
    """
    Sends a random youtube video of cute cats.
    """
    url = search("cute cats")
    await ctx.send(url)

@bot.command(aliases=['cuteracoons','cuteracoon'])
async def racoon(ctx):
    """
    Sends a random youtube video of cute racoons.
    """
    url = search("cute racoons")
    await ctx.send(url)

@bot.command(aliases=['cuteducks','cuteduck', 'cuteduckling'])
async def duck(ctx):
    """
    Sends a random youtube video of cute ducks.
    """
    url = search("cute ducks")
    await ctx.send(url)

@bot.command()
async def unhinged(ctx):
    """
    Sends a random youtube short of unhinged memes.
    """
    url = search("unhinged memes shorts") 
    await ctx.send(url)

@bot.event
async def on_message(message):
    '''
    When prompted with a command by user, bot will send a list of commands.
    '''
      # when message received 
    if message.author == bot.user:  #if the message is from bot/bot user
        return
    if message.content.startswith('.commands'):
        await message.channel.send('hello!')
    await bot.process_commands(message)

bot.run(discord_token)