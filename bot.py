import re
import discord
import json
import datetime
import asyncio
import random

from random import choice
from discord import DMChannel
from discord.ext import commands
from discord.flags import Intents


client=commands.Bot(command_prefix=".", intents=discord.Intents.all())

filtered_words = ["asdgfgg"]


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="F-off I'm minting aliens"))
    print(f"logged in")
            

@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
        
        await client.process_commands(msg)

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:

        with open('reactrole.json') as react_file:

            data = json.load(react_file)
            for x in data: 
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):


        with open('reactrole.json') as react_file:

            data = json.load(react_file)
            for x in data: 
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@client.event
async def on_member_join(member):
    guild = client.get_guild(894012048898400298)
    channel = guild.get_channel(894044887127851099)
    await channel.send(f'Welcome to the mothership :alien: {member.mention}')
 

@client.command(aliases=['g'])
@commands.has_permissions(kick_members = True)
async def giveaway(ctx):
    await ctx.send("answer these questions within 30 seconds:")

    questions = ["which channel? #channelname",
                "what duration? (s/m/h/d)",
                "what prize?"]
    
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send ('Answer faster')
            return
        else:
            answers.append(msg.content)

    
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"metion channel better nerd")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"use a proper unit pls (s/m/h/d)")
    elif time == -2:
        await ctx.send(f"time must be an integer")
        return
    prize = answers[2]


    await ctx.send(f"the giveaway will be in {channel.mention} and will last {answers[1]}")

    embed = discord.Embed(title = "Giveaway!", colour = ctx.author.colour)

    embed.add_field(name = f"Enter to win:", value = f"{prize}")

    embed.set_image(url='https://i.ibb.co/GtxcnVy/Giveawayalien2.png')

    embed.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Giveaway ends {answers[1]} from the time this message was sent!")

    my_msg = await channel.send(embed=embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await ctx.channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"{winner.mention}")
    
    embed=discord.Embed(title='Congratulations!', description = f'{winner.mention}')
    embed.set_thumbnail(url=winner.avatar_url)
    embed.add_field(name=f"Your prize is:", value = f"{prize}")
    embed.set_footer(text="Giveaway Ended")
    await channel.send(embed=embed)

    server = channel.message.guild

    await winner.send(f"You've won the giveaway in {server.name}, a mod will be in contact shortly")

@client.command(aliases=['rr'])
@commands.has_permissions(kick_members = True)
async def reroll(ctx, channel: discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was wrong you stupid idiot")
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"The next winner is: {winner.mention}")

    embed=discord.Embed(title='Congratulations!', description = f'{winner.mention}')
    embed.set_thumbnail(url=winner.avatar_url)
    embed.set_footer(text="Giveaway Ended")
    await channel.send(embed=embed)

    server = channel.message.guild

    await winner.send(f"You've won the giveaway in {server.name}, a mod will be in contact shortly")

   
    
    

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m": 60, "h": 3600, "d": 3600*60}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]



@client.command(aliases=['commands'])
@commands.has_permissions(kick_members = True)
async def h(ctx):
    emb=discord.Embed(title="COMMANDS", colour = discord.Colour.red())
    
    emb.add_field(name='.clear (amount)', value='Clears chat, alternative (.c)', inline=False)
    emb.add_field(name='.kick (username)', value='Kicks member, alternative (.k)', inline=False)
    emb.add_field(name='.ban (username)', value='Bans member, alternative (.b)', inline=False)
    emb.add_field(name='.mute (username)', value='Mutes member, alternative (.m)', inline=False)
    emb.add_field(name='.ping', value='Pong! + Bot latency', inline=False)
    emb.add_field(name='.poll (description)', value='Creates a yes or no poll', inline=False)
    emb.add_field(name='.hello', value='Hello!', inline=False)
    emb.add_field(name='.commands', value='Display commands, alternative (.h)', inline=False)
    emb.add_field(name='.giveaway', value='Starts a giveaway: follow instructions sent by bot, alternative(.g)', inline=False)
    emb.add_field(name='.reroll (channel_ID) (Message_ID)', value=' Right click to get IDs of channel and message respectively. Gets another winner for giveaway if you want multiple winners: can be done infinitely, alternative (.rr)', inline=False)

    msg=await ctx.channel.send(embed=emb)
    
    

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.send("You've been kicked because:"+reason)
    await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.send("You've been banned because:"+reason)
    await member.ban(reason=reason)

@client.command(aliases=['m'])
@commands.has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(894032555098116178)

    await member.add_roles(muted_role)

    await ctx.send(member.mention + " has been muted for being a daft cunt")

@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")

@client.command()
async def ping(ctx):
    await ctx.channel.send(f"Pong!  {round(client.latency*1000)}ms")

@client.command()
@commands.has_permissions(kick_members = True)
async def poll(ctx,*,message):
    emb=discord.Embed(title="POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')

@client.command()
async def reactrole(ctx, emoji, role: discord.Role,*,message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {
            'role_name':role.name,
            'role_id':role.id,
            'emoji':emoji,
            'message_id':msg.id
        }

        data.append(new_react_role)


    with open('reactrole.json','w') as j:
        json.dump(data,j,indent=4)



client.run('ODk0MDUyMjAyOTA4MzY0ODIw.YVkY_w.rNaC_955FHK9RvbNnTjmj3rRqqM')
