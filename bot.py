import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import numpy as np
import os
import time
import requests
import datetime
import calendar
import re
from datetime import date
from datetime import datetime as dt,timedelta
from googletrans import Translator

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix = "&",intents = intents)
client.remove_command('help')
killingFloorRoll = random.randint(0,365)

def createEmbed(CustomTitle,Footer,User,Thumbnail,NumOfFields,Author,Field,Inline):
    embed = discord.Embed(
        title = CustomTitle,
        colour = discord.Colour.blue()
    )
    embed.set_footer(text= Footer)
    embed.set_author(name= Author)
    embed.set_thumbnail(url= Thumbnail)

    for i in range(0,NumOfFields):
        embed.add_field(name=f"**{Field[i][0]}**", value=f"**{Field[i][1]}**", inline= Inline)
    return embed

@client.event
async def on_ready():
    print("$$$$$")
    global Start_Time
    activity = discord.Game(name="dead")
    await client.change_presence(status=discord.Status.online, activity=activity)
    Start_Time = datetime.datetime.now()

@client.event
async def on_voice_state_update(member,before,after):
    check = False
    biuk_kanal = 757706472439414804
    biuk = 157558511692283904

    voice_client = client.get_channel(biuk_kanal)

    if (after.channel != None and after.channel.id == biuk_kanal) or (before.channel != None and (after.channel == None or after.channel.id != biuk_kanal)):
        members = voice_client.members
        for member in members:
            if member.id == biuk:
                check = True
        if check and voice_client.name != 'biuk is here':
            await voice_client.edit(name='biuk is here')
        elif check is False and voice_client.name == 'biuk is here':
            await voice_client.edit(name='biuk is not here')

@client.command()
async def roll(ctx,*args):
    if len(args) == 2:
        if args[0].isnumeric() and args[1].isnumeric():
            if int(args[0]) > int(args[1]) :
                min = int(args[1])
                max = int(args[0])
            else:
                min = int(args[0])
                max = int(args[1])
            await ctx.channel.send(f"**{ctx.author.nick} has rolled a {random.randint(min,max)}**")
        else:
            await ctx.channel.send("**Bad Input, type &roll ? for help**")
    elif len(args) == 1:
        if args[0].isnumeric():
            if int(args[0]) >= 0:
                await ctx.channel.send(f"**{ctx.author.nick} has rolled a {random.randint(0,int(args[0]))}**")
            else:
                await ctx.channel.send("**Bad Input, type &roll ? for help**")
        elif args[0] == '?':
            embed = discord.Embed(
                title = "&roll",
                colour = discord.Colour.blue()
            )
            embed.add_field(name=f"**&roll #1 #2**", value="**Roll in range of #1 & #2**", inline= False)
            embed.add_field(name=f"**&roll #1**", value="**Roll in range of 0 & #1**", inline= False)
            embed.add_field(name=f"**&roll**", value="**Roll in range of 1 & 100**", inline= False)
            await ctx.channel.send(embed=embed)

        else:
            await ctx.channel.send("**Bad Input, type &roll ? for help**")
    elif len(args) == 0:
        await ctx.channel.send(f"**{ctx.author.nick} has rolled a {random.randint(1,101)}**")
    else:
        await ctx.channel.send("**Bad Input, type &roll ? for help**")

@client.event
async def on_message(message):
    global channel
    channel = message.channel
    if message.channel.id != 555040966525059072:
        print('{} - {}'.format(message.author,str(message.content)))
    if 'ocelto' in message.content and ':ocelto:' not in message.content:
        await channel.send("<:ocelto:501867638872342568>")

    content = message.content
    content = content.replace(" ","")
    count = 0
    for letter in content:
        if(letter.isupper()):
            count+=1
    #print(content,count,len(content),count/ len(content) * 100)
    if(count > 0 and count/ len(content) * 100 > 80 and len(content) > 30):
        await channel.send(f"Stop spamming <@!{message.author.id}>")
    await client.process_commands(message)

@client.event
async def on_member_update(before,after):
    server = client.get_guild(212958936972656640) 
    if before.guild == server:
        #print(after.nick)
        if after.nick != "ivan" and after.id == 1:
            await after.edit(nick="ivan")
        if before.status != after.status:
            Time = datetime.datetime.now()
            minute = Time.minute if Time.minute >= 10 else '0' + str(Time.minute)
            channel = client.get_channel(555040966525059072)
            print(f"{before.name} : {before.status} --> {after.status} ")
            def CheckStatus(Status):
                if Status == 'idle':
                    newStatus = ":orange_circle:"
                elif Status == 'online':
                    newStatus = ":green_circle:"
                elif Status == 'offline':
                    newStatus = ':black_circle:'
                elif Status == 'dnd':
                    newStatus = ':red_circle:'
                return newStatus
            BStatus = CheckStatus(str(before.status))
            AStatus = CheckStatus(str(after.status))

            User = f"{before.name}"
            Inline = True
            Footer = f"@{Time.hour}:{minute}"
            Thumbnail = f"https://cdn.discordapp.com/avatars/{before.id}/{before.avatar}.png?size=1024"
            FirstField = ["Before",f"{BStatus} "]
            SecondField = ["After",f"{AStatus} "]
            Field = []
            Field.append(FirstField)
            Field.append(SecondField)
            embed = createEmbed(User,Footer,'',Thumbnail,2,'',Field,Inline)
            await channel.send(embed=embed)

@client.event
async def on_reaction_add(reaction,user):
    message = reaction.message
    if reaction.emoji == "????":
        translator = Translator()
        word = translator.translate(reaction.message.content,dest='en')
        sen = word.text

        for member in reaction.message.mentions:
           sen = sen.replace(f"<@! {member.id}>",f"<@!{member.id}>")
        await reaction.message.reply(sen, mention_author=False)
@client.command()
async def uptime(ctx):
    Current_Time = datetime.datetime.now()
    Time = dt(1,1,1) + timedelta(seconds=int((Current_Time - Start_Time).total_seconds()))
    await channel.send(f"```DAYS:HOURS:MIN:SEC\n{Time.day-1}:{Time.hour}:{Time.minute}:{Time.second}```")

@client.command()
async def help(ctx):
    RemindMeExample = "&remindme 20 write help command"
    CountdownExample = "&countdown 5"
    embed = discord.Embed(
        title = "Available commands",
        colour = discord.Colour.blue()
    )
    embed.set_footer(text="Powered by a very fast hamster")
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png?size=1024")
    embed.set_author(name= f"Called by {ctx.author.display_name}")
    embed.add_field(name=f"**&roll**", value=f"**&roll**", inline= False)
    embed.add_field(name=f"**&uptime**", value=f"**&uptime**", inline= False)
    embed.add_field(name=f"**&countdown**", value=f"**{CountdownExample}**", inline= False)
    embed.add_field(name=f"**&killingfloor2**", value=f"**&killingfloor2**", inline= False)
  

    await ctx.channel.send(embed=embed)


@client.command()
async def killingfloor2(ctx):
    domePick = 2
    winQuotes = [
        "IT'S KILLING FLOOR TIME!!!!",
        "You did your best, it was not enough",
        "Another day, another failure",
        "Nope",
        "Better luck next time",
        "Soon COPIUM",
        "Yes but actually no",
        "8 ball says Ask Again Later",
        "Not today",
        "In football it's called nuttmeg but in tennis it is hot dog, also no kf2 today"
    ]
    print(killingFloorRoll,domePick)
    if(killingFloorRoll == domePick):
        await ctx.channel.send("IT'S KILLING FLOOR TIME!!!!")
    else:
        index = random.randint(0,len(winQuotes)-1)
        if(index == 0):
            msg = await ctx.channel.send(winQuotes[index])
            time.sleep(3)
            string = winQuotes[0] + " is what it would say if you got the correct roll"
            await msg.edit(content = string)
        else:
            await ctx.channel.send(winQuotes[index])


@client.command()
async def temp(ctx,*args):  
    string = ' '.join(args)
    query = string if len(string) > 0 else "Split"
    params = {
    'access_key': '6e37604c0ca0bf0aede1174f16bd65ae',
    'query': f'{query}'
    }   
    api_result = requests.get('http://api.weatherstack.com/current', params)
    output = api_result.json()
    icon = output['current']['weather_icons'][0]
    desc = output['current']['weather_descriptions']
    temp = output['current']['temperature']
    time = output['current']['observation_time']
    feelsLike = output['current']['feelslike']
    city = output['request']['query']
    humidity = output['current']['humidity']

    embed = discord.Embed(
        title = f'???? {city}',
        colour = discord.Colour.blue(),
        description= f"??????? Temperature: {temp}??C\n??????? Feels like: {feelsLike}??C\n???? Humidity: {humidity}% \n\n\nCondition: {desc[0]}"
    )

    embed.set_thumbnail(url= icon) 
    embed.set_footer(text=f"Observed at {time}")
    await ctx.channel.send(embed=embed)
@client.command()
async def countdown(ctx,message):
    tristo = 178210330399211520
    try:
        Time = float(message)
        Msg = await ctx.channel.send(f"Countdown of {Time} minute(s) has started")
        await asyncio.sleep(float(Time)*60)
        await Msg.delete()
        if ctx.author.id == tristo:
            await ctx.channel.send(f"Countdown of {Time} minute(s) has ended! Dobar tek <@{ctx.author.id}>")
        else:
            await ctx.channel.send(f"<@{ctx.author.id}> - Countdown of {Time} minute(s) has ended! ")
    except:
        await ctx.channel.send("Invalid input")

client.run(os.getenv('TOKEN'))


