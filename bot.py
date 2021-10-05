import discord
import json
from discord.ext import commands
from discord.flags import Intents

client=commands.Bot(command_prefix=".", intents=discord.Intents.all())

filtered_words = ["asdgfgg"]

@client.event
async def on_ready():
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
