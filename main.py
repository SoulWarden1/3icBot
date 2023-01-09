from datetime import datetime
import sys
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from typing import Literal, Optional
from discord import app_commands
from random import randint
import platform


from dotenv import load_dotenv
from os import getenv
import os
from pathlib import Path

# Variables
coalitionGuild = 1061208309346078801

load_dotenv()
token = os.getenv("TOKEN")
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('_'),
            description="""A bot developed by SoulWarden for the 3rd Coalition""",
            intents=discord.Intents.all(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="me start up"),
            status=discord.Status.online,
            owner_id=499816773122654219,
            help_command=None
            )
        self.cogList = ["randomCmd", "coalitionCmd"]
        self.synced = False
        
    async def setup_hook(self): 
        for cog in self.cogList:
            await self.load_extension(cog)
        self.tree.copy_global_to(guild=discord.Object(coalitionGuild))
        await self.tree.sync(guild=discord.Object(coalitionGuild))
        print("Cogs loaded and tree synced")
        
bot = MyBot()
tree = bot.tree
bot.roleSelectMsgId = 0

# Bot starting
@bot.event
async def on_ready():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print(f"Started at {current_time}")

    # Sets prefix
    if platform.system() == 'Windows':
        bot.command_prefix = commands.when_mentioned_or('-')
        print("Platform: Windows")
    else:
        bot.command_prefix = commands.when_mentioned_or('_')
        print("Platform: Linux")
        
    f = open("roleSelectMsgId.txt")
    bot.roleSelectMsgId = int(f.read())
    f.close()
    print("Role selection recovered")
    
    print("Bot ready")
    

# Prints out errors to console
@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    Parameters
    ------------
    ctx: commands.Context
        The context used for command invocation.
    error: commands.CommandError
        The Exception raised.
    """

    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    # This prevents any cogs with an overwritten cog_command_error being handled here.
    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    ignored = (commands.CommandNotFound, )

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except discord.HTTPException:
            pass

    # For this error example we check to see where it came from...
    elif isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
            await ctx.send('I could not find that member. Please try again.')

    else:
        # All other Errors not returned come here. And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            
# Prints when a guild is joined
@bot.event
async def on_guild_join(ctx, error):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Bot has joined {ctx.guild} at {current_time}")


# Prints when a guild if left
@bot.event
async def on_guild_remove(ctx, error):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Bot has left {ctx.guild} at {current_time}")
    
@bot.event
async def on_raw_reaction_add(payload):
    if (
        payload.channel_id == 1061867579733450782
        and payload.message_id == bot.roleSelectMsgId
    ):  
        coalitionGuild = bot.get_guild(1061208309346078801)
        iffRole = coalitionGuild.get_role(1061228377400414289)
        cgRole = coalitionGuild.get_role(1061228513597861939)
        threeERole = coalitionGuild.get_role(1061228621022380103)
        #3e
        if payload.emoji.id == 1061865489330094141 and iffRole not in payload.member.roles and cgRole not in payload.member.roles:
            await payload.member.add_roles(threeERole, reason = "Giving user regiment role")
        #IFF
        elif payload.emoji.id == 1061861221420245032 and threeERole not in payload.member.roles and cgRole not in payload.member.roles:
            await payload.member.add_roles(iffRole, reason = "Giving user regiment role")
        #CG
        elif payload.emoji.id == 1061864620870074429 and iffRole not in payload.member.roles and threeERole not in payload.member.roles:
            await payload.member.add_roles(cgRole, reason = "Giving user regiment role")
        


@bot.event
async def on_raw_reaction_remove(payload):
    if (
        payload.channel_id == 1061867579733450782
        and payload.message_id == bot.roleSelectMsgId
    ):  
        coalitionGuild = bot.get_guild(1061208309346078801)
        iffRole = coalitionGuild.get_role(1061228377400414289)
        cgRole = coalitionGuild.get_role(1061228513597861939)
        threeERole = coalitionGuild.get_role(1061228621022380103)
        member = coalitionGuild.get_member(payload.user_id)
        #3e
        if payload.emoji.id == 1061865489330094141:
            await member.remove_roles(threeERole, reason = "Removing user regiment role")
        #IFF
        elif payload.emoji.id == 1061861221420245032:
            await member.remove_roles(iffRole, reason = "Removing user regiment role")
        #CG
        elif payload.emoji.id == 1061864620870074429:
            await member.remove_roles(cgRole, reason = "Removing user regiment role")
    
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    
@bot.command()
@commands.is_owner()
async def clear(ctx):
    tree.clear_commands(guild=discord.Object(id = coalitionGuild))
    await tree.sync(guild=discord.Object(id = coalitionGuild))
    await ctx.reply("Tree cleared")
    
# Reload cogs command
@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(
            title="Reload", description="Reloaded cogs: ", color=0xFF00C8
        )
        for x in bot.cogList:
            await bot.reload_extension(x)
            embed.add_field(name=f"**#{count}**", value=f"{x} reloaded", inline=False)
            count += 1
        await ctx.send(embed=embed)
        print("All cogs reloaded")
    else:
        await bot.reload_extension(f"{extension}")
        embed = discord.Embed(
            title="Reload",
            description=f"{extension} successfully reloaded",
            color=0xFF00C8,
        )
        await ctx.send(embed=embed)
        print(f"{extension} reloaded")

# Unload cogs command
@bot.command()
@commands.is_owner()
async def unload(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(
            title="Unload", description="Unloaded cogs", color=0x109319
        )
        for x in bot.cogList:
            try:
                await bot.unload_extension(x)
            except commands.ExtensionNotLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already unloaded", inline=False
                )
                count += 1
            else:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} unloaded", inline=False
                )
                count += 1
        await ctx.send(embed=embed)
    else:
        await bot.unload_extension(extension)
        embed = discord.Embed(
            title="Unload", description=f"{extension} cog unloaded", color=0x109319
        )
        await ctx.reply(embed=embed)


# Load cogs command
@bot.command()
@commands.is_owner()
async def load(ctx, extension: str = None):
    count = 1
    if extension is None:
        embed = discord.Embed(title="Load", description="Loaded cogs", color=0x109319)
        for x in bot.cogList:
            try:
                await bot.load_extension(x)
            except commands.ExtensionAlreadyLoaded:
                embed.add_field(
                    name=f"**#{count}**", value=f"{x} is already loaded", inline=False
                )
                count += 1
            else:
                embed.add_field(name=f"**#{count}**", value=f"{x} loaded", inline=False)
                count += 1
        await ctx.send(embed=embed)
    else:
        await bot.load_extension(extension)
        embed = discord.Embed(
            title="Load", description=f"{extension} cog loaded", color=0x109319
        )
        await ctx.reply(embed=embed)


bot.run(token)
