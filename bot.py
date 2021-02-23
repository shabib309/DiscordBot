import discord
from discord import colour
from discord.ext import commands
from dotenv import load_dotenv
import random
import os
import requests
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

options = {"!help", "!botinfo", "!print <YourText>", "!joke", "!fuckoff", "!Russisch Roulette", "!CoinFlip", "!clear <quantity (limit = 10)>", "!clear_message <message_id>", "!embed <YourText>", "!quote <YourText>"}

actions = ['awesome/', 'because/', 'bye/', 'cool/', 'diabetes/', 'everyone/', 'everything/', 'fascinating/', 'flying/', 'life/', 'pink/', 'thanks/', 'that/', 'this/', 'what/']

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ASMR"))
    print(f'{client.user} has connected to Discord!')


async def botinfo(message):
    await clear_func_call(message)
    await message.channel.send('Alive and happy :)')


async def print_text(message, temp):
    await clear_func_call(message)
    output = ""
    for x in temp[1:]:
        output += (x + " ")
    await message.channel.send(output)


async def roulette(message):
    await clear_func_call(message)
    result = random.randint(1, 6)
    if result == 1:
        await message.channel.send('U died...')
    else:
        await message.channel.send('U survived...')


async def clear(message, temp):
    await clear_func_call(message)
    if len(temp) == 1:
        await message.channel.purge(limit=1)
    else:
        limit = (int(temp[1]) + 1)
        if limit >= 10:
            await message.channel.purge(limit=10)
            return
        await message.channel.purge(limit=(int(temp[1])))


async def coinflip(message):
    await message.channel.send("Type \"Heads\" or \"Tails\"")

    def check(m):
        return m.content.lower() == "heads" or m.content.lower() == "tails"
    msg = await client.wait_for("message", check=check)
    result = random.randint(1, 2)
    if result == 1:
        if msg.content.lower() == "tails":
            await message.channel.purge(limit=5)
            await message.channel.send("U won")
        else:
            await message.channel.send("U lost")


async def help(message):
    await clear_func_call(message)
    output = ""
    for x in options:
        output += x + "\n"
    await message.channel.send(output)


async def clear_message(message, id):
    await clear_func_call(message)
    msg = await message.channel.fetch_message(id)
    await msg.delete()


async def embed(message, content):
    await clear_func_call(message)
    output = ""
    for x in content[1:]:
        output += x + " "
    embedvar = discord.Embed()
    embedvar.add_field(name=format(message.author), value=output)
    await message.channel.send(embed=embedvar)


async def quote(message, content):
    await clear_func_call(message)
    output = ""
    for x in content[1:]:
        output += x + " "
    embed_var = discord.Embed()
    name = "- " + format(message.author) + " 2021"
    embed_var.add_field(name=output, value=name)
    await message.channel.send(embed=embed_var)


async def joke(message):
    await clear_func_call(message)
    from jokeapi import Jokes  # Import the Jokes class
    j = Jokes()
    joke = j.get_joke(lang="en")
    output = ""
    if joke['type'] == 'single':  # Print the joke
        output = joke['joke']
    else:
        output = joke["setup"] + " " + joke["delivery"]
    await message.channel.send(output)


async def fuckoff(message):
    await clear_func_call(message)
    url = "https://foaas.com/" + format(actions[random.randint(1, len(actions)) - 1]) + str(message.author)
    text = requests.get(url).text
    text = re.search("<title>.*</title>", text)
    out = text.group(0)
    out = out[15:-8]
    await message.channel.send(out)


async def clear_func_call(message_for_delete):
    await message_for_delete.channel.purge(limit=1)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    temp = message.content.split()
    option = message.content.lower()
    if option == '!botinfo':
        await botinfo(message)
    elif temp[0] == '!print':
        await print_text(message, temp)
    elif option == '!russisch roulette':
        await roulette(message)
    elif option == '!help':
        await help(message)
    elif temp[0] == '!clear':
        await clear(message, temp)
    elif temp[0] == '!clear_message':
        await clear_message(message, temp[1])
    elif option == '!coinflip':
        await coinflip(message)
    elif temp[0] == '!embed':
        await embed(message, temp)
    elif temp[0] == '!quote':
        await quote(message, temp)
    elif option == '!joke':
        await joke(message)
    elif option == '!fuckoff':
        await fuckoff(message)

client.run(TOKEN)
