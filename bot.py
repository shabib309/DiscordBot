import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import os
import requests
import re
import translators as ts
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
NASA_TOKEN = os.getenv('NASA_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

options = {"!help", "!cat", "!botinfo", "!init_daily (Can only be started once) <channelID>", "!dog", "!steam <YourSteamLink>", "!print <YourText>", "!donate", "!weather <cityName>", "!ip <ip-address>", "!translate <YourText>", "!pin <message_id>", "!joke", "!fuckoff", "!Russisch Roulette", "!CoinFlip", "!clear <quantity (limit = 10)>", "!clear_message <message_id>", "!embed <YourText>", "!quote <YourText>"}
options = sorted(options, key=str.lower)

actions = ['awesome/', 'because/', 'bye/', 'cool/', 'diabetes/', 'everyone/', 'everything/', 'fascinating/', 'flying/', 'life/', 'pink/', 'thanks/', 'that/', 'this/', 'what/']

client = commands.Bot(command_prefix='!')

global daily_running, coinflip_running, delete_id, quote_id
coinflip_running = False
daily_running = False
delete_id = 0
quote_id = 0


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ASMR"))
    global nasa_id
    nasa_id = 0
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

async def coinflip_init(message):
    await clear_func_call(message)
    global coinflip_running
    if coinflip_running:
        await coinflip(message)
    else:
        msg = await message.channel.send("Type \"Heads\" or \"Tails\"")
        global delete_id
        delete_id = msg.id
        coinflip_running = True

async def coinflip(message):
    result = random.randint(0, 1)
    if result == 0:
        if message.content.lower() == "heads":
            await message.channel.send("U won")
        else:
            await message.channel.send("U lost")
    else:
        if message.content.lower() == "tails":
            await message.channel.send("U won")
        else:
            await message.channel.send("U lost")
    await clear_message(message, delete_id, False)
    global coinflip_running
    coinflip_running = False


async def help(message):
    await clear_func_call(message)
    output = ""
    for x in options:
        output += x + "\n"
    await message.channel.send(output)


async def clear_message(message, id, clear_call=True):
    if clear_call:
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
    out = await request_call("https://foaas.com/" + format(actions[random.randint(1, len(actions)) - 1]) + str(message.author), "<title>.*</title>", 15, -8)
    await message.channel.send(out)

async def pin(message, id):
    await clear_func_call(message)
    msg_to_pin = await message.channel.fetch_message(int(id))
    await msg_to_pin.pin()

async def apod(id):
    await client.wait_until_ready()
    global nasa_id
    channel = client.get_channel(int(id))
    if nasa_id != 0:
        old_msg = await channel.fetch_message(nasa_id)
        await old_msg.delete()
    out = ""
    url = "https://api.nasa.gov/planetary/apod?api_key=" + NASA_TOKEN
    text = requests.get(url).text
    explanation = re.search("\"explanation\":\".*\",\"h", text)
    image = re.search("\"url\":\".*\"}", text)
    out += explanation.group(0)[15:-4] + "\n"
    out += image.group(0)[7:-2]
    msg = await channel.send(out)
    nasa_id = msg.id
    while client.is_ready:
        await asyncio.sleep(60 * 60 * 24)
        await apod(id)

async def donate(message):
    await clear_func_call(message)
    await message.channel.send("https://paypal.me/Shabib309?locale.x=de_DE")

async def ip(message, ip):
    await clear_func_call(message)
    out = ""
    out = await request_call("http://ip-api.com/json/" + ip, "\"country\".*", 0, -1)
    out = out.replace("\"", "")
    out = out.replace(",", "\n")
    out = out.replace(":", " : ")
    await message.channel.send(out)

async def weather(message, cityName):
    await clear_func_call(message)
    response = cityName + " Wetter:\n"
    response += await request_call("http://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + WEATHER_TOKEN + "&units=metric", "\"temp\":.*,\"deg", 0, -5)
    old = [",", "{", "}", "\"temp\"", "\"feels_like\"", "\"temp_min\"", "\"temp_max\"", "\"pressure\"", "\"humidity\"", "\"visibility\"", "\"wind\":\"speed\"", ":"]
    new = ["\n", "", "", "Temperatur", "Gefühlt", "Minimum", "Maximum", "Druck", "Luftfeuchtigkeit", "Sichtweite", "Windgeschwindigkeit", " : "]
    i = 0
    for i in range(len(old)):
        response = response.replace(old[i], new[i])
    await message.channel.send(response)   

async def translate(message, text):
    await clear_func_call(message)
    temp = ""
    for x in text[1:]:
        temp += (x + " ")
    text = temp
    result = ts.google(text, to_language='de')
    await message.channel.send(result)

async def qotd(id):
    global quote_id
    channel = client.get_channel(int(id))
    if quote_id != 0:
        old_msg = await channel.fetch_message(quote_id)
        await old_msg.delete()
    out = ""
    out = await request_call("https://quotes.rest/qod?language=en", "\"quote\": \".*\",", 10, -2)
    msg = await channel.send(out)
    quote_id = msg.id
    while client.is_ready:
        await asyncio.sleep(60 * 60 * 24)
        await apod(id)

async def steam(message, link):
    await clear_func_call(message)
    if "http" in link:
        link = link[36:-1]
    response = await request_call("https://steamsignature.com/sig/" + link + "/", "value=\"http://steamsignature.com/card/0/.*.png", 7 ,0)
    await message.channel.send(response)

async def dog(message):
    await clear_func_call(message)
    result = await request_call("https://random.dog/woof.json", "\"url\":.*\"}", 7, -2)
    await message.channel.send(result)

async def fact(message):
    await clear_func_call(message)
    result = await request_call("http://api.fungenerators.com/fact/random", "\"fact\": \".*\",", 9, -2)
    await message.channel.send(result)

async def cat(message):
    await clear_func_call(message)
    id = random.randint(1, 1500)
    result = await request_call("http://random.cat/view/" + str(id), "><img src=\"https://purr.objects.*\" alt=", 11 , -6)
    await message.channel.send(result)

async def request_call(url="", search="", startOffset=0,endOffset=0):
    if url == "":
        return ""
    response = requests.get(url).text
    if search != "":
        result = re.search(search, response)
    content = ""
    try:
        if endOffset != 0:
            content = result.group(0)[startOffset:endOffset]
        else:
            content = result.group(0)[startOffset:]
    except:
        return response
    return content

async def init_daily(message, id):
    await clear_func_call(message)
    global daily_running
    if daily_running:
        return
    client.loop.create_task(apod(id))
    client.loop.create_task(qotd(id))
    daily_running = True

async def clear_func_call(message_for_delete):
    await message_for_delete.channel.purge(limit=1)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    temp = message.content.split()
    option = message.content.lower()
    temp[0] = temp[0].lower()
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
    elif temp[0] == '!clear_message' and temp[1] != 0:
        await clear_message(message, temp[1], True)
    elif option == '!coinflip' or option == 'heads' or option == 'tails':
        await coinflip_init(message)
    elif temp[0] == '!embed':
        await embed(message, temp)
    elif temp[0] == '!quote':
        await quote(message, temp)
    elif option == '!joke':
        await joke(message)
    elif option == '!fuckoff':
        await fuckoff(message)
    elif temp[0] == '!pin':
        await pin(message, temp[1])
    elif temp[0] == '!init_daily' and temp[1] != 0:
        await init_daily(message, temp[1])  
    elif option == '!donate':
        await donate(message)
    elif temp[0] == '!ip' and temp[1] != 0:
        await ip(message, temp[1])
    elif temp[0] == '!weather' and temp[1] != "":
        await weather(message, temp[1])
    elif temp[0] == '!translate' and temp[1] != 0:
        await translate(message, temp)
    elif temp[0] == '!steam' and temp[1] != "":
        await steam(message, temp[1])
    elif option == '!dog':
        await dog(message)
    elif option == '!fact':
        await fact(message)
    elif option == '!cat':
        await cat(message)

client.run(TOKEN)
