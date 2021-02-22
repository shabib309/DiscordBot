# bot.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
        temp = message.content.split()
        if message.content == '!botinfo':
            await message.channel.send('Alive and happy :)')
        elif temp[0] == 'print':
            output = ""
            for x in temp[1:]:
                output += (x + " ")

            await message.channel.send(output)


client.run(TOKEN)