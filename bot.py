import discord
from discord.ext import commands
import time
import os
import random

bot = commands.Bot(command_prefix=['xirp '])
bot.remove_command('help')
#initial_extensions = ['cogs.status', 'cogs.leaderboard', 'cogs.auto']
initial_extensions = ['cogs.status', 'cogs.auto', 'cogs.admin','cogs.Help']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\nLogged as: {bot.user.name} - {bot.user.id}\nConnected to:')
    for i in bot.guilds:
        print(
        f'{i}'
        )
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Xtreme India Roleplay."))
    print(f'Bot is ready to go!')

@bot.event
async def on_message(message):
    #channel = bot.get_channel(856557351041105970)
    if (message.channel.id == 850838004843151370) and message.author != bot.user:
        if len(message.attachments) == 0:
            await message.delete()
            await message.channel.send("```You can't chat in screenshot channel...```", delete_after=10)
    else:
        await bot.process_commands(message)

@bot.command(hidden=True)
async def reload(ctx, extension):
    bot.reload_extension(extension)

@bot.command(hidden=True)
async def activity(ctx, arg, arg2, arg3=None):
    author = ctx.message.author
    if author.id == 626811868249325578:
        if arg == 'playing':
            await bot.change_presence(activity=discord.Game(name=arg2))
        elif arg == 'streaming':
            await bot.change_presence(activity=discord.Streaming(name=arg2, url=arg3))
        elif arg == 'listening':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=arg2))
        elif arg == 'watching':
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg2))
        await ctx.send('Status Updated')
        time.sleep(0.5)
        await ctx.channel.purge(limit=2)
    else:
        msg = await ctx.send('Fuck off. You are not authorized', delete_after=10)

bot.run('NzkyNDY2MDY4MzE2MzU2NjQ5.X-eHiQ.jmI4mgql2lkO-4naCDy-YiBhxCU', bot=True, reconnect = True)
