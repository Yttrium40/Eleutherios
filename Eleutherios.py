import asyncio
import json
import logging
import random
import string
import sys

import discord
from discord.ext import commands

import markov


logging.basicConfig(level=logging.INFO)
TOKEN = ''                               # Put the bot's token here!
bot = commands.Bot(command_prefix = "E.")


"""INIT"""

random.seed()

markov_dictionary = markov.load_dictionary()
"""
Format of the Markov dictionary:
{"word": {"next": 2, ".": 5, "no": 1},
"": {...},              #empty string here indicates the start of a phrase
"another": {"": 2}}     #empty string here indicates the end of a phrase,
                         with no additional punctuation
"""

@bot.event
async def on_ready():
    print("Eleutherios ready.")


"""COMMANDS"""

@bot.command()
async def save(ctx):
    if await bot.is_owner(ctx.message.author):
        print("Saving data.")
        markov.save_dictionary(markov_dictionary)
        print("Data saved!")

@bot.command()
async def off(ctx):
    if await bot.is_owner(ctx.message.author):
        await bot.logout()
        quit()


"""EVENTS"""

@bot.event
async def on_disconnect():
    print("Saving data.")
    markov.save_dictionary(markov_dictionary)
    print("Data saved!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # send a message if channel name includes bot
    if isinstance(message.channel, discord.TextChannel):
        if message.channel.name.lower().find("bot") != -1:
            print("Saying a phrase.")
            phrase = markov.get_phrase(message.content, None, False, markov_dictionary)
            ctx = await bot.get_context(message)
            await ctx.send(phrase)
        markov.learn_phrase(message.content, markov_dictionary)
        print("I learned something.")
        
    await bot.process_commands(message)


bot.run(TOKEN)
