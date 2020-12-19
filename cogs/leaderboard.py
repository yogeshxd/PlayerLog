from discord import Embed, Colour
from discord.ext import commands
from discord.utils import get
import discord

from datetime import datetime, timezone
from sqlite3 import connect
import random

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_embed(title, description=None):
        embed = Embed(
            title=title,
            description=description,
            color=random.randit(0, 0xffffff),
        )
        return embed

    @staticmethod
    def get_data(player_id):
        with connect('data.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE ID=?", (player_id,))
            return c.fetchone()

    @commands.command(brief = '-profile', description = 'Returns your score with current rank...')
    async def profile(self, ctx):
        try:
            data = get_data(ctx.author.id)
            e = create_embed(f"{ctx.author.name}'s profile:")
            e.set_author(name = ctx.author.name, icon = ctx.author.avatar.icon)
            e.add_field(name="Score", value=str(data[2]), inline=False)
        except:
            e = create_embed(f"{ctx.author.name} doesn't exists", 'Tip: Check if you are registered or not...')
        
        msg = await ctx.channel.send(embed=e, delete_after=30)
        

    @commands.has_permissions(administrator=True)
