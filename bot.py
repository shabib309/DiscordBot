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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ASMR"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
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
        else:
            await message.channel.send('U survived...')
    elif message.content == '!help':
        await message.channel.send("!help\n!botinfo\n!print\n!Russisch Roulette")
    elif temp[0] == '!clear':
        if len(temp) == 1:
            await message.channel.purge(limit=1)
        else:
            await message.channel.purge(limit=(int(temp[1]) + 1))
    elif message.content == '!CoinFlip':
        await message.channel.send("Type \"Heads\" or \"Tails\"")
        def check(m):
            return (m.content.lower() == "heads" and m.channel == message.channel) or (m.content.lower() == "tails" and m.channel == message.channel)
        msg = await client.wait_for("message", check=check)
        result = random.randint(1,2)
        if result == 1:
            if msg.content.lower() == "tails":
                await message.channel.purge(limit=1)
                await message.channel.send("U won")
            else:
                await message.channel.send("U lost")

client.run(TOKEN)