# main.py
import os
##from dotenv import load_dotenv
##from keep_alive import keep_alive
import discord
from discord.ext import commands
from random import randint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pandas import isna
import pandas as pd
from pickle import dump as pdump
from pickle import load as pload

#channels = ["arena-leaderboard"]
#mchans = ["arena-dm","ransom-rolling-channel","general-admin"]
#chan2 = ["general"]

##load_dotenv()
##TOKEN = os.getenv('DISCORD_TOKEN')
##GUILD = os.getenv('DISCORD_GUILD')

creds = pload(open('creds.pkl','rb'))
TOKEN = creds['TOKEN']
GUILD = creds['GUILD']

bot = commands.Bot(command_prefix="!", case_insensitive=True)

## Load data
monsters = pload(open('resources/all_monster_data.pkl','rb'))
## items = pickle.load(open('magic-items.pkl','rb'))
spells = pload(open('resources/spells.pkl','rb'))
channel_list = ['general','twsnbn-thursday-afternoon','announcements']
music_list = pd.read_csv('music_meta.csv',delimiter=',')
domt = pd.read_csv('domt/domt.csv',delimiter=',')

## Local fx
def match_term(term,list_names):
    if not isna(term):
        out = process.extractOne(term,list(list_names.keys()),scorer=fuzz.token_sort_ratio)
        return out[0]
    else:
        return 'Failed matching'

def ret_monster_stats(monster_entry,embed):
    temp = monster_entry
    del monster_entry
    strength = temp['strength']
    embed.add_field(name="STR",value=strength)
    dexter = temp['dexterity']
    embed.add_field(name="DEX",value=dexter)
    constit = temp['constitution']
    embed.add_field(name="CON",value=constit)
    intell = temp['intelligence']
    embed.add_field(name="INT",value=intell)
    wisdom = temp['wisdom']
    embed.add_field(name="WIS",value=wisdom)
    charis = temp['charisma']
    embed.add_field(name="CHA",value=charis)
    mtype = temp['type']
    embed.add_field(name="Type",value=mtype)
    msize = temp['size']
    embed.add_field(name="Size",value=msize)
    mac = temp['armor_class']
    embed.add_field(name="AC",value=mac)
    hp = temp['hit_dice']
    embed.add_field(name="Hit Dice",value=hp)
    hpp = temp['hit_points']
    embed.add_field(name="Avg HP",value=hpp)
    speed = temp['speed']
    try:
        for zz in speed:
            try:
                embed.add_field(name=zz,value=speed[zz])
            except:
                print('speed error')
    except:
        embed.add_field(name="Speed",value="Error")
        print('speed error')
    return embed

def ret_monster_stats2(monster_entry,embed):
    temp = monster_entry
    del monster_entry
    mprof = temp['proficiencies']
    try:
      profout = ''
      try:
          for zz in mprof:
              profout = profout + zz['name'] + '\n'
      except:
          print('prof for error')
      try:
          if len(profout) < 2:
              profout = "None"
          embed.add_field(name="Proficiencies",value=profout)
      except:
          print('prof error')
          print(profout)
    except:
        try:
            embed.add_field(name='Proficiencies',value=zz['name'])
        except:
            embed.add_field(name="Proficiencies",value="Error")
            print('prof error')
    vuln = temp['damage_vulnerabilities']
    try:
        embed.add_field(name="Damage Vulnerabilities",value=vuln)
    except:
        print('vuln error')
    try:
        immun = str(temp['damage_immunities'])
        if len(immun) > 5:
            immun = immun[2:-2]
        embed.add_field(name="Damage Immunities",value=immun)
    except:
        print('immun error')
    try:
        resis = str(temp['damage_resistances'])
        if len(resis) > 4:
            resis = resis[2:-2]
        embed.add_field(name="Damage Resistances",value=resis)
    except:
        print('resis error')
    cimmun = temp['condition_immunities']
    cimm = ''
    senses = temp['senses']
    try:
        for zz in senses:
            try:
                embed.add_field(name=zz,value=senses[zz])
            except:
                print('sense error')
    except:
        embed.add_field(name="Senses",value="Error")
        print('sense error')
    langs = temp['languages']
    if len(langs) < 2:
        langs = "None"
    embed.add_field(name="Languages",value=langs)
    mcr = temp['challenge_rating']
    embed.add_field(name="CR",value=mcr)
    return embed

def ret_monster_stats3(monster_entry,embed):
    temp = monster_entry
    del monster_entry
    try:
        specact = temp['special_abilities']
        try:
            for zz in specact:
                try:
                    embed.add_field(name=zz['name'],value=zz['desc'])
                except:
                    print('spec abil error')
        except:
            embed.add_field(name="Special Abilities",value="Nada")
            print('spec abil error')
    except:
        print('No special abilities')
    acts = temp['actions']
    try:
        for zz in acts:
            try:
                embed.add_field(name=zz['name'],value=zz['desc'])
            except:
                print('act error')
    except:
        embed.add_field(name="Actions",value="Error")
        print('action error')
    try:
        legacts = temp['legendary_actions']
        for zz in legacts:
            embed.add_field(name="Legendary Action: " + zz['name'],value=zz['desc'])
    except:
        legacts = "None"
        embed.add_field(name="Legendary Actions",value=legacts)
    return embed

def ret_spell(spell_entry,embed):
    temp = spell_entry
    del spell_entry
    desc = temp['desc']
    embed.add_field(name="Description",value=desc)
    try:
        rng = temp['range']
        embed.add_field(name="Range",value=rng)
    except:
        xyz = 0
    try:
        comps = temp['components']
        embed.add_field(name="Components",value=comps)
    except:
        xyz = 0
    try:
        dur = temp['duration']
        embed.add_field(name="Duration",value=dur)
    except:
        xyz = 0
    try:
        ct = temp['casting-time']
        embed.add_field(name="Casting Time",value=ct)
    except:
        xyz = 0
    try:
        mats = temp['materials']
        embed.add_field(name="Material Components",value=mats)
    except:
        xyz = 0
    try:
        rit = temp['ritual']
        embed.add_field(name="Ritual",value="True")
    except:
        xyz = 0
    try:
        conc = temp['concentration']
        embed.add_field(name="Concentration",value="True")
    except:
        xyz = 0
    try:
        lvl = temp['level']
        embed.add_field(name="Level",value=lvl)
    except:
        xyz = 0
    return embed

def roll_dice(n_die,die_sz,keep_high_b=0,keep_low_b=0,keep_high=0,keep_low=0,sub=0):
    rollstmp = []
    rolls = []
    rolls_all = []
    sign = (-1)**sub
    for yy in range(int(n_die)):
        rollstmp = rollstmp + [int(randint(1,die_sz))*sign]
    if (keep_high_b == 1) and (keep_high < len(rollstmp)):
        rolls = rolls + sorted(rollstmp,reverse=True)[:keep_high]
        rolls_all = rolls_all + rollstmp
    elif (keep_high_b == 1) and (keep_high >= len(rollstmp)):
        rolls = rolls + sorted(rollstmp,reverse=True)
        rolls_all = rolls_all + rollstmp
    elif (keep_low_b == 1) and (keep_low < len(rollstmp)):
        rolls = rolls + sorted(rollstmp)[:keep_low]
        rolls_all = rolls_all + rollstmp
    elif (keep_low_b == 1) and (keep_low >= len(rollstmp)):
        rolls = rolls + sorted(rollstmp)
        rolls_all = rolls_all + rollstmp
    else:
        rolls = rolls + rollstmp
        rolls_all = rolls_all + rollstmp
#    print(rolls)
#    print(rolls_all)
    return rolls, rolls_all

def roller(msg):
    nn = msg.split('+')
    rolls_all = []
    rolls = []
    mod = 0
    for xx in nn:
        if '-' in xx:
            mm = xx.split('-')
            yy = mm[0]
            yy1 = mm[1]
            keep_high_b = 0
            keep_low_b = 0
            keep_high = 0
            keep_low = 0
            interm = yy.split('d')
            if len(interm) == 2:
                try:
                    n_die = int(interm[0])
                except:
                    n_die = 1
                if 'kh' in interm[1]:
                    temp = interm[1].split('kh')
                    keep_high = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_high_b = 1
                elif 'kl' in interm[1]:
                    temp = interm[1].split('kl')
                    keep_low = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_low_b = 1
                die_sz = int(interm[1])
                rolls_t, rolls_all_t = roll_dice(n_die=n_die,die_sz=die_sz,keep_high_b=keep_high_b,
                          keep_low_b=keep_low_b,keep_high=keep_high,keep_low=keep_low,sub=0)
                rolls = rolls + rolls_t
                rolls_all = rolls_all + rolls_all_t
            elif len(interm) == 1:
                mod = int(interm[0])
            keep_high_b = 0
            keep_low_b = 0
            keep_high = 0
            keep_low = 0
            interm = yy1.split('d')
            if len(interm) == 2:
                try:
                    n_die = int(interm[0])
                except:
                    n_die = 1
                if 'kh' in interm[1]:
                    temp = interm[1].split('kh')
                    keep_high = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_high_b = 1
                elif 'kl' in interm[1]:
                    temp = interm[1].split('kl')
                    keep_low = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_low_b = 1
                die_sz = int(interm[1])
                rolls_t, rolls_all_t = roll_dice(n_die=n_die,die_sz=die_sz,keep_high_b=keep_high_b,
                          keep_low_b=keep_low_b,keep_high=keep_high,keep_low=keep_low,sub=1)
                rolls = rolls + rolls_t
                rolls_all = rolls_all + rolls_all_t
            elif len(interm) == 1:
                mod = int(interm[0]) * -1
        else:
            keep_high_b = 0
            keep_low_b = 0
            keep_high = 0
            keep_low = 0
            interm = xx.split('d')
            if len(interm) == 2:
                try:
                    n_die = int(interm[0])
                except:
                    n_die = 1
                if 'kh' in interm[1]:
                    temp = interm[1].split('kh')
                    keep_high = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_high_b = 1
                elif 'kl' in interm[1]:
                    temp = interm[1].split('kl')
                    keep_low = int(temp[1])
                    interm[1] = int(temp[0])
                    keep_low_b = 1
                die_sz = int(interm[1])
                rolls_t, rolls_all_t = roll_dice(n_die=n_die,die_sz=die_sz,keep_high_b=keep_high_b,
                          keep_low_b=keep_low_b,keep_high=keep_high,keep_low=keep_low,sub=0)
                rolls = rolls + rolls_t
                rolls_all = rolls_all + rolls_all_t
            elif len(interm) == 1:
                mod = interm[0]
#    print(rolls)
#    print(rolls_all)
    return rolls, rolls_all, mod

## Discord fx
## Check if User Message List Exists
def load_users():
    if os.path.exists('user_list.pkl'):
        user_list = list(set(pload(open('user_list.pkl','rb'))))
    else:
        user_list = []
        pdump(user_list,open('user_list.pkl','wb'))
    return user_list

## Check if Bot is Connected to Guild VC
def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

## Join VC
@bot.command(name="join",description="Join VC")
async def join(ctx):
    vc = ctx.author.voice.channel
    await vc.connect()

## Leave VC
@bot.command(name="leave",description="Leave VC")
async def leave(ctx):
    await ctx.voice_client.disconnect()
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## List Music
##@bot.command(name="list_music",description="List all music available")
##async def list_music(ctx):
##    for xx in music_list.itertuples():
##        msg = str(xx.Index+1)+" - "+xx.song
##        await ctx.send(msg)

## Join VC and Play Mood Music
@bot.command(name="play",description="Play Mood Music")
async def play(ctx,*,arg):
    # Gets voice channel of message author
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    song = music_list.iloc[int(arg)-1]
    if cid in user_list:
        if ctx.message.author.voice and (not ctx.message.guild.voice_client) and (int(arg) < 50):
            embed = discord.Embed(title="Now Playing")
            embed.add_field(name="Title",value=song['song'])
            embed.add_field(name="Link",value=song['link'])
            embed.add_field(name="License",value=song['license'])
            await ctx.author.voice.channel.connect()
            await ctx.send(content=None,embed=embed)
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
            vc = server.voice_client
            vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song['location']))
        elif ctx.message.author.voice and ctx.message.guild.voice_client and (not voice_channel.is_playing()) \
             and (int(arg) < 50):
            embed = discord.Embed(title="Now Playing")
            embed.add_field(name="Title",value=song['song'])
            embed.add_field(name="Link",value=song['link'])
            embed.add_field(name="License",value=song['license'])
            await ctx.send(content=None,embed=embed)
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song['location']))
        elif ctx.message.author.voice and voice_channel.is_playing() and (int(arg) < 50):
            embed = discord.Embed(title="Now Playing")
            embed.add_field(name="Title",value=song['song'])
            embed.add_field(name="Link",value=song['link'])
            embed.add_field(name="License",value=song['license'])
            await ctx.send(content=None,embed=embed)
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
            voice_channel.stop()
            voice_channel.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=song['location']))
        elif int(arg) > 49:
            await ctx.send("No such song")
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
        else:
            await ctx.send(str(ctx.author.name) + "is not in a channel.")
            try:
                await ctx.message.delete()
            except Exception as err:
                print(str(err)[:250])
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
        try:
            await ctx.message.delete()
        except Exception as err:
            print(str(err)[:250])

## Pause Music
@bot.command(name="pause",description="Pause Mood Music")
async def pause(ctx):
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    if cid in user_list:
        if voice_channel:
            if voice_channel.is_playing():
                voice_channel.pause()
            else:
                await ctx.send("No music playing")
        else:
            await ctx.send("Bot is not connected to a VC")
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Resume Music
@bot.command(name="resume",description="Resume Mood Music")
async def resume(ctx):
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    if cid in user_list:
        if voice_channel:
            if voice_channel.is_paused():
                voice_channel.resume()
            else:
                await ctx.send("No music to resume")
        else:
            await ctx.send("Bot is not connected to a VC")
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Stop Music
@bot.command(name="stop",description="Stop Mood Music")
async def pause(ctx):
    cid = str(ctx.author.id)
    server = ctx.message.guild
    voice_channel = server.voice_client
    user_list = load_users()
    if cid in user_list:
        if voice_channel:
            if voice_channel.is_playing():
                voice_channel.stop()
                await voice_channel.disconnect()
            else:
                await ctx.send("No music playing")
        else:
            await ctx.send("Bot is not connected to a VC")
    else:
        await ctx.send(str(ctx.author.name)+" is not authorized to use this bot.")
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Add User to User Message List
@bot.command(name="add_user",description="Add user to DM list")
async def add_user(ctx,*args):
    user_list = load_users()
    list_users = [str(user_mentioned.id) for user_mentioned in ctx.message.mentions]
    for xx in list_users:
#        print(xx)
        if xx not in user_list:
#            print(xx)
            user_list = user_list + [xx]
    pdump(user_list,open('user_list.pkl','wb'))
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## List Users
@bot.command(name="list_users",description="List All DM Users")
async def list_users(ctx,*args):
    user_list = load_users()
    for xx in user_list:
        await ctx.author.send(xx)
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

## Set Text Channel
@bot.command(name="set_channel",description="Set Channel for Bot Commands")
async def set_channel(ctx):
    user_list = load_users()
    cid = str(ctx.author.id)
    if cid in user_list:
        channel = str(ctx.channel)
        await ctx.send('Channel set')
    else:
        await ctx.send('User not authorized to perform this action')
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

@bot.command(name="roll",description="Roll dice")
async def roll(ctx,*args):
    msg = ''.join(args).lower()
    cid = str(ctx.author.id)
    embed = discord.Embed(title="Roll",description=msg)
    rolls, rolls_all, mod = roller(msg)
    if len(str(rolls_all)) < 20:
        embed.add_field(name="Dice rolled",value=rolls_all)
    else:
        embed.add_field(name="Dice rolled",value="Too many dice to display")
    rolls_sum = sum(rolls)
    embed.add_field(name="Outcome",value=rolls_sum+int(mod))
    embed.add_field(name="Rolled By",value="<@!"+cid+">")
    await ctx.send(content=None,embed=embed)
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

@bot.command(name="r",description="Roll dice")
async def r(ctx,*args):
    msg = ''.join(args).lower()
    cid = str(ctx.author.id)
    embed = discord.Embed(title="Roll",description=msg)
    rolls, rolls_all, mod = roller(msg)
    if len(str(rolls_all)) < 20:
        embed.add_field(name="Dice rolled",value=rolls_all)
    else:
        embed.add_field(name="Dice rolled",value="Too many dice to display")
    rolls_sum = sum(rolls)
    embed.add_field(name="Outcome",value=rolls_sum+int(mod))
    embed.add_field(name="Rolled By",value="<@!"+cid+">")
    await ctx.send(content=None,embed=embed)
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

@bot.command(name="pmr",description="Privately roll dice")
async def pmr(ctx,*args):
    msg = ''.join(args).lower()
    cid = str(ctx.author.id)
    embed = discord.Embed(title="Roll",description=msg)
    rolls, rolls_all, mod = roller(msg)
    if len(str(rolls_all)) < 20:
        embed.add_field(name="Dice rolled",value=rolls_all)
    else:
        embed.add_field(name="Dice rolled",value="Too many dice to display")
    rolls_sum = sum(rolls)
    embed.add_field(name="Outcome",value=rolls_sum+int(mod))
    embed.add_field(name="Rolled By",value="<@!"+cid+">")
    await ctx.author.send(content=None,embed=embed)
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

@bot.command(name="randchar",description="Generate Random Character Stats")
async def randchar(ctx):
    cid = str(ctx.author.id)
    embed = discord.Embed(title="Random Character Stats",description="<@!"+cid+">")
    stats = []
    for jj in range(6):
        rolls = []
        for ii in range(4):
            temp = 1
            while temp == 1:
                temp = randint(1,6)
            rolls = rolls + [temp]
        stats = stats + [sum(sorted(rolls,reverse=True)[:3])]
        embed.add_field(name="Stat",value=sum(sorted(rolls,reverse=True)[:3]))
    embed.add_field(name="Total",value=sum(stats))
    await ctx.send(content=None,embed=embed)
    try:
        await ctx.message.delete()
    except Exception as err:
        print(str(err)[:250])

@bot.command(name="spell",description="Get spell definition")
async def spell(ctx,*,arg):
#    cid = str(ctx.author.id)
    spell_list = list(spells.keys())
    spell = str(arg)
    if spell in spell_list:
        cont = spell
        temp = spells[spell]
        embed = discord.Embed(title=cont,description="Spell Stats")
        embed = ret_spell(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        try:
            await ctx.message.delete()
        except:
            xyz = 0
    else:
        matched_spell = match_term(spell,spells)
        cont = matched_spell
        try:
            await ctx.send(content='Did you mean '+matched_spell+'?')
        except Exception as err:
            print(str(err)[:250])
        temp = spells[matched_spell]
        embed = discord.Embed(title=cont,description="Spell Stats")
        embed = ret_spell(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        try:
            await ctx.message.delete()
        except:
            xyz = 0

@bot.command(name="monster",description="Get spell definition")
async def monster(ctx,*,arg):
#    cid = str(ctx.author.id)
    monster_list = list(monsters.keys())
    monster = str(arg)
    if monster in monster_list:
        cont = monster
        temp = monsters[monster]
        embed = discord.Embed(title=cont,description="Monster Stats")
        embed = ret_monster_stats(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        embed = discord.Embed(title=cont,description="Monster Stats")
        embed = ret_monster_stats2(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        embed = discord.Embed(title=cont,description="Monster Stats")
        embed = ret_monster_stats3(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        try:
            await ctx.message.delete()
        except:
            xyz = 0
    else:
        matched_monster = match_term(monster,monsters)
        cont = matched_monster
        try:
            await ctx.send(content='Did you mean '+matched_monster+'?')
        except Exception as err:
            print(str(err)[:250])
        temp = monsters[matched_monster]
        embed = discord.Embed(title=cont,description="Monster Stats")
        embed = ret_monster_stats(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        embed = discord.Embed(title=cont,description="Monster Stats")
        embed = ret_monster_stats2(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        embed = discord.Embed(title=cont,description="Monster Stats")
        embed = ret_monster_stats3(temp,embed)
        try:
            await ctx.send(content=None, embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        try:
            await ctx.message.delete()
        except:
            xyz = 0

@bot.command(name="pog",description="pog")
async def pog(ctx):
    cid = str(ctx.author.id)
    val = "<@!"+cid+">"
    aa,bb = domt.shape
    card = domt.iloc[randint(0,aa-1)]
##    card = domt.sample()
    embed = discord.Embed(title=card.card,description=card.definition)
    embed.add_field(name="Card For",value="<@!"+cid+">")
    try:
        await ctx.send(file=discord.File(card.path),embed=embed)
    except Exception as err:
        print(str(err))
        print('msg send error')
    try:
        await ctx.message.delete()
    except:
        xyz = 0

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title='ERROR!',
                              description='Command not found. Did you mean:',
                              color=ctx.author.color)
        embed.add_field(name="`!pog`",value='Roll on the Deck of Many Things')
        embed.add_field(name="`!roll`",value='Roll dice')
        embed.add_field(name="`!monster`",value='Retrieve monster stats')
        embed.add_field(name="`!spell`",value='Retrieve spell details')
        embed.add_field(name="`!play`",value='Play music')
        embed.add_field(name="`!pause`",value='Pause music')
        embed.add_field(name="`!resume`",value='Resume music')
        embed.add_field(name="`!stop`",value='Stop music')
        try:
            await ctx.send(embed=embed)
        except Exception as err:
            print(str(err))
            print('msg send error')
        try:
            await ctx.message.delete()
        except:
            xyz = 0

## Run bot
#keep_alive()
bot.run(TOKEN)
