from discord.ext import tasks, commands
import requests
import discord
from os import environ
import time
import os
import random

class auto(commands.Cog, name='auto'):
    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.auto.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(minutes=10.0)
    async def auto(self):
        cit = ''
        with open('ip.txt', 'rb') as ip:
            url = ip.readlines()
            nurl = str(url[0])[2:len(url[0])+2]
            ip.close
        channel = self.bot.get_channel(856557351041105970)
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
            msg = await channel.send(embed=temp)
        except:
            print("Incorrect IP or server is not responding.", nurl)
            msg = await channel.send('Seems like server is offline...')

    @auto.before_loop
    async def before_auto(self):
        print('waiting...')
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(auto(bot))
