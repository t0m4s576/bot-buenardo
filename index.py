import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
import asyncio
from discord.utils import get
import random

bot = commands.Bot(command_prefix='*')
bot.remove_command("help")

class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name}{1.signature}'.format(self, command)
class Mycog(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

@bot.command()
async def help(ctx):
    await ctx.send("I will pass you the information in your dm")
    author = ctx.message.author
    helpText = discord.Embed(title="Command list", description="There is all my commands",timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
    helpText.add_field(name="Fun Commands", value="*say, *meme" )
    helpText.add_field(name="Moderation Commands", value="*mute, *ban, *kick, *unmute")
    helpText.add_field(name="Utils Commands", value="*info, *clean, *ping, *invite")
    helpText.add_field(name="Search Commands", value="*youtube") 
    DMchannel = await author.create_dm()
    await DMchannel.send(embed=helpText)
             



#multifuctions and fun


@bot.command()
async def ping(ctx):
    pong = discord.Embed(title=":ping_pong:", description="PONG!!!", color=discord.Color.blue())
    await ctx.send(embed=pong)

    

@bot.command()
async def say(ctx, *, mensaje):
    await ctx.send(mensaje)


#a simple meme command
@bot.command()
async def meme(ctx):
    memes = []#put some memes here
    chosenMeme = random.choice(memes)
    memeText = discord.Embed(title="Your meme", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    memeText.set_image(url=chosenMeme)
    await ctx.send(embed=memeText)



#Moderation 

@commands.has_permissions(kick_members=True)
@bot.command()
async def mute(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        try:
            muted = await ctx.guild.create_role(name="Muted", reason="To mute users", colour=discord.Colour(0x818386))
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages=False, read_message_history=True, read_messages=True)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make roles")
        await member.add_roles(muted)
        muteText = discord.Embed(title="User has been muted", color=discord.Color.green())
        await ctx.send(embed=muteText)
    else:
        await member.add_roles(role)
        muteText = discord.Embed(title="User has been muted", color=discord.Color.green())
        await ctx.send(embed=muteText)



@commands.has_permissions(ban_members=True)
@bot.command()
async def ban(ctx, member : discord.Member):
    banMessage = discord.Embed(title="The user has been baned", color=discord.Color.green())
    await member.ban()
    await ctx.send(embed=banMessage)




@commands.has_permissions(kick_members=True)
@bot.command()
async def kick(ctx, member : discord.Member):
    kickMessage = discord.Embed(title="The user has been kicked", color=discord.Color.green())
    await member.kick()
    await ctx.send(embed=kickMessage)





@commands.has_permissions(kick_members=True)
@bot.command()
async def unmute(ctx, member : discord.Member):
    await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
    unMute = discord.Embed(title="User has been unmuted", color=discord.Color.green())
    await ctx.send(embed=unMute)


#Utils

@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    embed.add_field(name="Server created at", value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server Channels", value=len(ctx.guild.channels))
    embed.add_field(name="Server Roles", value=len(ctx.guild.roles))
    embed.add_field(name="Server Users", value=sum(not member.bot for member in ctx.guild.members))
    embed.add_field(name="Server BOTS", value=sum(member.bot for member in ctx.guild.members))
    embed.add_field(name="All Members", value=f"{ctx.guild.member_count}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    await ctx.send(embed=embed)


@commands.has_permissions(manage_channels=True)
@bot.command(pass_context=True)
async def clean(ctx, amount):
    msg = []
    amount = int(amount)
    channel = ctx.message.channel
    async for x in ctx.message.channel.history(limit=int(amount)):
        msg.append(x)
    await channel.delete_messages(msg)
    await ctx.send("Messages deleted")


@bot.command()
async def invite(ctx):
    await ctx.send("The invite of the bot: https://discord.com/api/oauth2/authorize?client_id=754513471806111865&permissions=8&scope=bot")

#search

@bot.command()
async def youtube(ctx, *, search):
    query_string = parse.urlencode({"search_query": search})
    html_content = request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
    await ctx.send("http://www.youtube.com/watch?v=" + search_results[0])


# Events
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Alpha versions||0.0.1"))
    print("I'm Ready")
    bot.run()#token of your bot
