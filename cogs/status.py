import discord
from discord.ext import commands
from os import environ
import time
import os
import random
import requests

class Status(commands.Cog, name='Status'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='xirp status', description='Give the number of connected players and players in queue.')
    @commands.has_permissions(administrator=True)
    async def status(self, ctx):
        await ctx.channel.purge(limit=1)
        stat = True
        with open('ip.txt', 'rb') as ip:
            url = ip.readlines()
            nurl = str(url[0])[2:len(url[0])+2]
            ip.close

        try:
            i = requests.get(f"{nurl}info.json")
            inf = i.json()
            info = inf["vars"]
        except:
            print("Incorrect IP or server is not responding.", nurl)
            stat = False
        if stat == True:
            queue = info["sv_queueCount"]
            maxcl = info["sv_maxClients"]
            connected = info["sv_queueConnectedCount"]
            temp=discord.Embed(title="Server Status", description=f"Server is up having {connected}/{maxcl} players and {queue} players are still in queue.", color=random.randint(0, 0xffffff))
            msg = await ctx.channel.send(embed=temp, delete_after=10)
        else:
            temp=discord.Embed(title="Server Status", description="**Seems like server is offline...**", color=random.randint(0, 0xffffff))
            msg = await ctx.channel.send(embed=temp, delete_after=10)

    @commands.command(brief='xirp players', description='Give the names of all connected players.')
    @commands.has_permissions(administrator=True)
    async def players(self, ctx):
        #Next two lines are to filter particular admins...
        #name = ['DuB']
        #admin = [626811868249325578]
        author = ctx.message.author
        cit = ''
        with open('ip.txt', 'rb') as ip:
            url = ip.readlines()
            nurl = str(url[0])[2:len(url[0])+2]
            ip.close
        #if author.id in admin:
        if True:
            try:
                i = requests.get(f"{nurl}info.json")
                inf = i.json()
                info = inf["vars"]
                connected = info["sv_queueConnectedCount"]
                p = requests.get(f"{nurl}players.json")
                players = p.json()
                for i in players:
                    pl = f"[{i['id']}] {i['name']}"
                    cit = cit+pl+'\n'
                temp=discord.Embed(title=f"Connected Players - {connected}", description=cit, color=random.randint(0, 0xffffff))
                temp.set_footer(text="Xtreme India", icon_url="https://cdn.discordapp.com/attachments/713333403776319538/856559731166150686/logo.png")
                msg = await ctx.channel.send(embed=temp)
            except:
                print("Incorrect IP or server is not responding.", nurl)
                msg = await ctx.channel.send('Seems like server is offline...')
        else:
            msg = await ctx.channel.send('Your are not authorized...', delete_after=10)

    @commands.command(brief='xirp ip [ip]', description='Change the ip to ping for info.')
    @commands.has_permissions(administrator=True)
    async def ip(self, ctx, arg1):
        await ctx.channel.purge(limit=1)
        with open('ip.txt', 'w') as ip:
            ip.write(f"http://{arg1}/")
            ip.close
        msg = await ctx.channel.send(f'IP udated to {arg1}...', delete_after=2)

def setup(bot):
    bot.add_cog(Status(bot))
