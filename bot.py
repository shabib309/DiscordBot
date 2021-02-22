# bot.py
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.member, *,reason="None"):
    await member.kick(reason=reason)


@client.event
async def on_message(message):
    temp = message.content.split()
    if message.content == '!botinfo':
        await message.channel.send('Alive and happy :)')
    elif temp[0] == '!print':
        output = ""
        for x in temp[1:]:
            output += (x + " ")
        await message.channel.send(output)
    elif message.content == '!Russisch Roulette':
        result = random.randint(1, 6)
        if result == 1:
            await message.channel.send('U died...')
            return
        await message.channel.send('U survived...')
    elif message.content == '!help':
        await message.channel.send("!botinfo\n!print\n!Russisch Roulette\n!help")

client.run(TOKEN)
