from discord import Member, Embed, Status, Color
from discord.utils import get
from discord.ext import commands

from os import environ
from asyncio import sleep
from sqlite3 import connect
from datetime import datetime
import random

class Help(commands.Cog, name='Help'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='xirp help [category]', description='Show this message')
    async def help(self, ctx, category: str = None):
        embed = Embed(color=0x3498db)
        embed.title = '📋 Category list:' if not category else f'ℹ️ About the {category} category:'
        await ctx.message.delete()
        if not category:
            for cat in self.bot.cogs:
                if cat in ['Test', 'Help', 'auto']:
                    pass
                else:
                    cog = self.bot.get_cog(cat)
                    embed.add_field(name=cat, value=f"{cog.description}\nType `xirp help {cat}` for more informations.", inline=False)
        else:
            for cmd in self.bot.get_cog(category.capitalize()).get_commands():
                embed.add_field(name=f"xirp {cmd.name}", value=f"{cmd.description} (`{cmd.brief}`)", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))