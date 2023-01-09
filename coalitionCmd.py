from ntpath import join
import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from random import randint
from datetime import datetime
import asyncio
from pathlib import Path



class coalitionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.is_owner()
    @commands.command(name = "roleSelection", aliases=["roleselect"])
    async def roleSelect(self, ctx:commands.Context):
        roleSelect=discord.Embed(title="Regiment Role Selection", description="Please react with the below emoji to be assign your regimental role\n\n <:3e:1061865489330094141> - 3e \n <:iff:1061861221420245032> - IFF\n <:CG:1061864620870074429> - CG\n\N{military helmet} - Mercenary", color=0xf1c40f)
        roleSelectMsg = await ctx.send(embed=roleSelect)
        
        await roleSelectMsg.add_reaction("<:3e:1061865489330094141>")
        await roleSelectMsg.add_reaction("<:iff:1061861221420245032>")
        await roleSelectMsg.add_reaction("<:CG:1061864620870074429>")
        await roleSelectMsg.add_reaction("\N{military helmet}")
        
        self.bot.roleSelectMsgId = roleSelectMsg.id
        
        f = open("roleSelectMsgId.txt", "w")
        f.write(str(roleSelectMsg.id))
        f.close()

async def setup(bot):
    await bot.add_cog(coalitionCog(bot))
