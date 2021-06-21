from discord import Member, Embed, Status, Color
from discord.utils import get
from discord.ext import commands

from os import environ
from asyncio import sleep
from sqlite3 import connect
from datetime import datetime
import random

class Admin(commands.Cog, name='Admin'):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def mute_handler(ctx, member, messages=False):
        role = get(member.guild.roles, name='Muted')
        if not role in member.roles:
            await member.add_roles(role)
            await member.remove_roles(get(member.guild.roles, name='Citizen'))
        else:
            await member.add_roles(get(member.guild.roles, name='Citizen'))
            await member.remove_roles(role)
            

    @commands.command(aliases=['purge'], brief='xirp clear [x]', description='Delete the [x] previous messages')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, x: int):
        await ctx.channel.purge(limit=x+1)

    @commands.command(brief='xirp mute [member] [duration] [reason]', description='Mute a member for the specified duration')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: Member, time: str, *, reason: str = None):
        units = {"s": [1, 'seconds'], "m": [60, 'minutes'], "h": [3600, 'hours']}
        duration = int(time[:-1]) * units[time[-1]][0]
        time = f"{time[:-1]} {units[time[-1]][1]}"
        await self.mute_handler(ctx, member)
        embed = Embed(title=":mute: User muted", description=f'{ctx.author.mention} muted **{member}** for {time}.\nReason: {reason}', color=0xe74c3c)
        await ctx.send(embed=embed)
        await sleep(duration)
        await self.mute_handler(ctx, member, True)
        embed = Embed(color=0xe74c3c, description=f'{member.mention} has been unmuted.')
        await ctx.send(embed=embed)

    @commands.command(brief='xirp kick [member] [reason]', description='Kick a member from the server')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason: str = None):
        embed = Embed(title="User kicked", description=f'{ctx.author.mention} kicked **{member}**.\nReason: {reason}', color=0xe74c3c)
        await member.kick(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(brief='xirp ban [member] [reason]', description='Ban a member from the server')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member, *, reason: str = None):
        embed = Embed(title=":man_judge: User banned", description=f'{ctx.author.mention} banned **{member}**.\nReason: {reason}', color=0xe74c3c)
        await member.ban(reason=reason)
        await ctx.send(embed=embed)

    @commands.command(brief='xirp unban [member] [reason]', description='Unban a member from the server')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str, *, reason: str = None):
        ban_list = await ctx.guild.bans()
        if not ban_list:
            embed = Embed(title="Something went wrong:", description="No banned users!", color=0xe74c3c)
            await ctx.send(embed=embed); return
        for entry in ban_list:
            if member.lower() in entry.user.name.lower():
                embed = Embed(title=":man_judge: User unbanned", description=f'{ctx.author.mention} unbanned **{entry.user.mention}**.\nReason: {reason}', color=0xe74c3c)
                await ctx.guild.unban(entry.user, reason=reason)
                await ctx.send(embed=embed); return
        embed = Embed(title="Something went wrong:", description="No matching user!", color=0xe74c3c)
        await ctx.send(embed=embed); return


#Announcements Commands Start
    @commands.command(brief='xirp admin [text]', description='Make an announcement as admin')
    @commands.has_permissions(administrator=True)
    async def admin(self, ctx, *, text):
        embed = (Embed(title=text, color=0xff9900)
                 .set_author(name=f'Notification from {ctx.author.display_name}', icon_url=ctx.author.avatar_url))
        embed.set_footer(text="Administartion | Xtreme India", icon_url="https://cdn.discordapp.com/attachments/713333403776319538/856559731166150686/logo.png")
        await ctx.message.delete()
        await ctx.send('@here', embed=embed)

    @commands.command(brief='xirp chief [text]', description='Make an announcement as chief admin')
    @commands.has_permissions(administrator=True)
    async def chief(self, ctx, *, text):
        embed = (Embed(title=text, color=0xff0000)
                 .set_author(name=f'Notification from {ctx.author.display_name}', icon_url=ctx.author.avatar_url))
        embed.set_footer(text="Chief Administartion | Xtreme India", icon_url="https://cdn.discordapp.com/attachments/713333403776319538/856559731166150686/logo.png")
        await ctx.message.delete()
        await ctx.send('@here', embed=embed)

    @commands.command(brief='xirp dev [text]', description='Make an announcement as devloper')
    @commands.has_permissions(administrator=True)
    async def dev(self, ctx, *, text):
        embed = (Embed(title="Server Update Log", description=text, color=0x0013ff)
                 .set_author(name=f'Notification from {ctx.author.display_name}', icon_url=ctx.author.avatar_url))
        embed.set_footer(text="Development Team | Xtreme India", icon_url="https://cdn.discordapp.com/attachments/713333403776319538/856559731166150686/logo.png")
        await ctx.message.delete()
        await ctx.send('@here', embed=embed)

    @commands.command(brief='xirp mag [text]', description='Make an announcement as management')
    @commands.has_permissions(administrator=True)
    async def mag(self, ctx, *, text):
        embed = (Embed(title=text, color=0x02f8f8)
                 .set_author(name=f'Notification from {ctx.author.display_name}', icon_url=ctx.author.avatar_url))
        embed.set_footer(text="Management | Xtreme India", icon_url="https://cdn.discordapp.com/attachments/713333403776319538/856559731166150686/logo.png")
        await ctx.message.delete()
        await ctx.send('@here', embed=embed)
#Announcements Commands End

    @commands.command(brief='xirp embed [text]', description='Make an embed')
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx, *, text):
        embed = (Embed(title=text, color=random.randint(0, 0xffffff)))
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(brief='xirp console [text]', description='Send text in console box')
    @commands.has_permissions(administrator=True)
    async def console(self, ctx, *, text):
        await ctx.message.delete()
        text = "```"+text+"```"
        await ctx.send(text)

    # @commands.command(brief='Du announce [text]', description='Make an announcement')
    # @commands.has_permissions(administrator=True)
    # async def roles(self, ctx):
    #     for y in ctx.author.roles:
    #         await ctx.send(y)

def setup(bot):
    bot.add_cog(Admin(bot))