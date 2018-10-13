import discord
import asyncio
import random
import authwriter
import os
import time
import json
from datetime import datetime, timedelta, date
import sys
from discord.ext import commands
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

client = discord.Client()
StopPermList = ['163227683373711360', '243835208502083585', '300743077990236160', '186766705240834048']
"""                Owl                     Lightkh              Aquatic Panda         SGTVulc"""
raffleArg = 1
raff = 0
salt = False
rafflelist = []
stringid = ""
forceDrawKey = 0
bot_roelof = False
first = True
# password!
hostid = 0
bot_token = ''
# Game essential
buy_confirm_list = []
sell_confirm_list = []
reforge_confirm_list = []
fight_confirm_list = []
choice_list = []


def weaponGen():
    # ‘Prefix|PrefixMultiplier|WeaponType|WeaponName|Rarity|RarityMultiplier|OriginalDamage|Damage|WeaponWorth’
    # Prefix
    prefix_list = ['Hairy|2|', 'Sharp|4|', 'Acute|3|', 'Apical|3|', 'Serrated|3|', 'Dull|1|', 'Dense|2|', "Roelofs|5|",
                   'Solid|2|', 'Micro|3|', 'Wet|5|', 'Meme|2|', 'Thick|4|', 'Shitty|1|', 'Primed|3|', "BullyHunters|6|",
                   "Some Cunts|5|", 'Soft|1|', 'Whale-Killing|7|']
    prefix = random.choice(prefix_list)
    # Weapon Type
    type_list = ['Rock|', 'Gun|', 'Stick|', 'Bow|']
    type = random.choice(type_list)
    # Weapon Name
    name = prefix.strip('|1234567890') + ' ' + type
    # Rarity
    rarity = random.randrange(1, 100)
    if rarity <= 35:
        rarity = 'Common|1|'
    elif rarity > 35 and rarity <= 60:
        rarity = 'Uncommon|2|'
    elif rarity > 60 and rarity <= 80:
        rarity = 'Rare|3|'
    elif rarity > 80 and rarity <= 95:
        rarity = 'Extremely Rare|4|'
    else:
        rarity = 'Allegorical|5|'
    # Damage
    prefix_m = prefix.lower().strip("abcdefghijklmnopqrstuvwxyz| '-")
    rarity_m = rarity.lower().strip("abcdefghijklmnopqrstuvwxyz| '-")
    damage_original = random.randint(1, 1000)
    damage_int = damage_original * int(prefix_m) * int(rarity_m)
    damage = str(damage_int) + '|'
    # Weapon Worth
    worth = str(round(damage_int / 15 * int(rarity_m)))

    # Assembly
    weapon = prefix + type + name + rarity + str(damage_original) + '|' + damage + worth
    return weapon


def formatter(wep, name):
    part = wep.split('|')
    print(part)
    # Type emoji
    if part[2] == 'Stick':
        emoji_1 = u"\U0001F956"
    elif part[2] == 'Bow':
        emoji_1 = u'\U0001F3F9'
    elif part[2] == 'Rock':
        emoji_1 = u"\U0001F316"
    else:
        emoji_1 = u"\U0001F52B"
    # Rarity Emoji
    if part[5] == '1':
        emoji_2 = u'\U0001F32C'
    elif part[5] == '2':
        emoji_2 = u'\U00002728'
    elif part[5] == '3':
        emoji_2 = u'\U0001F31F'
    elif part[5] == '4':
        emoji_2 = u'\U0001F4AB'
    else:
        emoji_2 = u'\U00002604'
    weapon = "**__{}'s {}__** {}\n\
{} **Weapon Types:** {}\n\
{} **Rarity:** {} {}\n\
{} **Rarity Multiplier:** {}\n\
{} **Damage:** {} (Original: {})\n\
{} **Prefix Multiplier:** {}\n\
{} **Resale Value:** {} Tokens\
".format(name, part[3], emoji_1, u'\U0001F397', part[2], u'\U0001F48D', part[4], emoji_2, u'\U0001F4FF', part[5],
         u'\U0001F3AF', part[7], part[6], u'\U0001F4A5', part[1], u'\U0001F39B', part[8])
    return weapon


def jdefault(o):
    return o.__dict__


class PlayerCreation():
    def __init__(self, id, wep, bank, daily, fight, inventory):
        self.id = id
        self.wep = wep
        self.bank = bank + 300
        self.dailytime = daily
        self.fighttime = fight
        self.temp_wep = ''
        self.inventory = inventory


def sync():
    global drive
    with open("GameData.json", "r+") as file:
        print(open('GameData.json').read())
        data = json.loads(open('GameData.json').read())
        print(data)
        drive_file = drive.CreateFile({'id': os.environ['DRIVE_FILE_ID']})
        drive_file.SetContentString(json.dumps(data, default=jdefault, indent=2))
        drive_file.Upload()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='with his Owlets ($help)'))
    with open("GameData.json", "r+") as file:
        data = json.loads(open('GameData.json').read())
        await client.send_message(client.get_channel("498311009635794964"),
                                  "[DYNO RESTART] Synced From Google Drive Successfully.\n{}".format(str(data)))


@client.event
async def on_message(message):
    global raffleArg
    global raff
    global rafflelist
    global stringid
    global forceDrawKey
    global hostid
    global salt
    global bot_roelof
    global first
    global StopPermList
    # Game essential
    global NewPlayer
    global jdefault
    global buy_confirm_list
    global sell_confirm_list
    global reforge_confirm_list
    global fight_confirm_list
    global formatter
    global weaponGen
    global sync
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    k = False
    while k == True:
        listo = ['**Happy Birthday Aidan**', "**Did you know it is Aidan's Birtday today?**",
                 "**Aidan turned 15 today**", "**Fuck the what**", "**Aidan was born today**"]
        await client.send_message(message.channel, random.choice(listo))
        time.sleep(900)
    if message.author == client.user:
        return
    elif message.content.startswith('$clean'):
        if message.author.id in StopPermList:
            syntax = message.content.split()
            if len(syntax) < 2:
                await client.send_message(message.channel,
                                          "[Syntax Error] Clean Requirement is not specified. E.g '$clean ThisIsSpam 100'")
            elif len(syntax) == 2:
                limit = 25
            else:
                try:
                    await client.send_message(client.get_channel("493017783135764486"),
                                              "Clean Request from {}. {}".format(message.server.name, syntax))
                    limit = round(int(syntax[2]))
                except:
                    await client.send_message(message.channel,
                                              "[Syntax Error] Clean limit is invalid. Must be numbers only. E.g '$clean ThisIsSpam 100'")
            req = syntax[1]
            counter = 0
            async for message in client.logs_from(message.channel, limit=limit, before=message):
                if req in message.content.translate(non_bmp_map):
                    counter += 1
                    await client.delete_message(message)
            await client.send_message(client.get_channel("493017783135764486"),
                                      "{} Messages Searched for '{}', {} Messages have been cleaned.".format(limit, req,
                                                                                                             counter))
            await client.send_message(message.channel,
                                      "{} Messages Searched for '{}', {} Messages have been cleaned.".format(limit, req,
                                                                                                             counter))

    elif message.content.startswith('$stop'):
        PermCheck = str(message.author.id) in StopPermList
        if PermCheck == True:
            currentTime = str(date.today()) + ' by '
            stopID = ''
            stopID = 'Bot Activity Terminated at ' + currentTime + message.author.id
            print(stopID)
            await client.send_message(client.get_channel("493017783135764486"), "{}".format(stopID))
            await client.send_message(message.channel, 'Stopping...')
            client.run(os.environ['BOT_TOKEN'])
        else:
            a = '<@'
            b = str(message.author.id)
            c = '> You do not possess the permissions to perform this command!'
            await client.send_message(message.channel, a + b + c)

    elif message.content.startswith('$owl'):
        syntax = message.content.lower().split()
        if len(syntax) > 1:
            if syntax[1] == 'daily':
                with open("GameData.json", "r+") as file:
                    data = json.loads(open('GameData.json').read())
                    try:
                        match = next(p for p in data['Players'] if p['id'] == message.author.id)
                        if abs(datetime.strptime(match["dailytime"][:10], '%Y-%m-%d').date() - date.today()).days >= 1:
                            match['bank'] += 200
                            match["dailytime"] = str(datetime.today())
                            file.seek(0)  # rewind
                            json.dump(data, file, indent=2)
                            file.truncate()
                            sync()
                            await client.send_message(message.channel,
                                                      '\U0001F4B0 | **{} has received 200 tokens**'.format(
                                                          message.author.name))
                        else:
                            await client.send_message(message.channel,
                                                      '\U0001F550 | {} daily rewards can only be claimed every 24 hours. (Last Claimed: {})'.format(
                                                          message.author.name, match["dailytime"][:15]))
                    except StopIteration:
                        NewPlayer = PlayerCreation(message.author.id, None, 200, str(datetime.today()),
                                                   str(datetime.today() - timedelta(days=2)), None)
                        data["Players"].append(NewPlayer)
                        with open('GameData.json', 'w') as file:
                            file.write(json.dumps(data, default=jdefault, indent=2))
                        sync()
                        await client.send_message(client.get_channel("498311009635794964"),
                                                  "Synced To Google Drive Successfully.\n{}".format(str(data)))
                        await client.send_message(message.channel, '\U0001F4B0 | **{} has received 200 tokens**'.format(
                            message.author.name))

            elif syntax[1].startswith('token'):
                with open("GameData.json", "r+") as file:
                    data = json.loads(open('GameData.json').read())
                    try:
                        match = next(p for p in data['Players'] if p['id'] == message.author.id)
                        await client.send_message(message.channel,
                                                  '\U0001F3E6 | **{}, you currently have {} tokens in your bank account**'.format(
                                                      message.author.name, match["bank"]))
                    except StopIteration:
                        NewPlayer = PlayerCreation(message.author.id, None, 0,
                                                   str(datetime.today() - timedelta(days=2)),
                                                   str(datetime.today() - timedelta(days=2)), None)
                        data["Players"].append(NewPlayer)
                        with open('GameData.json', 'w') as file:
                            file.write(json.dumps(data, default=jdefault, indent=2))
                        sync()
                        await client.send_message(client.get_channel("498311009635794964"),
                                                  "Synced To Google Drive Successfully.\n{}".format(str(data)))
                        await client.send_message(message.channel,
                                                  '\U0001F3E6 | **{}, you currently have 300 tokens in your bank account**'.format(
                                                      message.author.name))

            elif syntax[1] == 'weapon':
                with open("GameData.json", "r+") as file:
                    data = json.loads(open('GameData.json').read())
                    try:
                        match = next(p for p in data['Players'] if p['id'] == message.author.id)
                        if len(syntax) > 2:
                            if syntax[2] == 'buy':
                                if match['bank'] >= 500:
                                    if match['wep'] == None:
                                        await client.send_message(message.channel,
                                                                  "\U0001F4C3 | **Buying a new weapon costs 500 tokens. Would you still like to continue? (React to emoji)**")
                                        buy_confirm_list.append(message.author.id)
                                        await client.add_reaction(message, u"\u2705")
                                        await client.add_reaction(message, u"\u274E")
                                    else:
                                        await client.send_message(message.channel,
                                                                  "\U0001F4C3 | **{} You cannot have 2 weapons at once. If you buy a new weapon you will need to sell one. Would you still like to continue? (React to emoji)**".format(
                                                                      message.author.name))
                                        buy_confirm_list.append(message.author.id)
                                        await client.add_reaction(message, u"\u2705")
                                        await client.add_reaction(message, u"\u274E")
                                else:
                                    await client.send_message(message.channel,
                                                              "\U0001F4C3 | **Buying a new weapon costs 500 tokens. You only have {} Tokens! (Maybe Try $owl daily)**".format(
                                                                  match['bank']))

                            elif syntax[2] == 'sell':
                                if match['wep'] == None:
                                    await client.send_message(message.channel,
                                                              "\U0001F4DC | **{}, you currently do not have a weapon! Use '$owl weapon buy' to buy one**".format(
                                                                  message.author.name))
                                else:
                                    await client.send_message(message.channel,
                                                              "\U0001F4C3 | **Would you really like to sell your weapon? (React to emoji)** \n**Your Current Weapon:**\n {}".format(
                                                                  formatter(match['wep'], message.author.name)))
                                    sell_confirm_list.append(message.author.id)
                                    await client.add_reaction(message, u"\u2705")
                                    await client.add_reaction(message, u"\u274E")

                            elif syntax[2] == 'reforge':
                                if match['wep'] == None:
                                    await client.send_message(message.channel, "\U0001F4DC | **{}, you currently do not have a weapon to reforge! Use '$owl weapon buy' to buy one**".format(message.author.name))
                                else:
                                    await client.send_message(message.channel, "\U0001F528 | **Would you really like to reforge your weapon's prefix? This will cost 500 Tokens (React to emoji)** \n**Your Current Weapon:**\n {}\n \U0001F527 | **Reforging may increase or decrease your overall damage**".format(formatter(match['wep'], message.author.name)))
                                    reforge_confirm_list.append(message.author.id)
                                    await client.add_reaction(message, u"\u2705")
                                    await client.add_reaction(message, u"\u274E")

                        else:
                            if match['wep'] == None:
                                await client.send_message(message.channel,
                                                          "\U0001F4DC | **{}, you currently do not have a weapon! Use '$owl weapon buy' to buy one**".format(
                                                              message.author.name))
                            else:
                                await client.send_message(message.channel,
                                                          "{}".format(formatter(match["wep"], message.author.name)))



                    except StopIteration:
                        NewPlayer = PlayerCreation(message.author.id, None, 0,
                                                   str(datetime.today() - timedelta(days=2)),
                                                   str(datetime.today() - timedelta(days=2)), None)
                        data["Players"].append(NewPlayer)
                        with open('GameData.json', 'w') as file:
                            file.write(json.dumps(data, default=jdefault, indent=2))
                        sync()
                        await client.send_message(client.get_channel("498311009635794964"),
                                                  "Synced To Google Drive Successfully.\n{}".format(str(data)))
                        await client.send_message(message.channel,
                                                  "\U0001F4DC | **{}, you currently do not have a weapon! Use '$owl weapon buy' to buy one**".format(
                                                      message.author.name))

            elif syntax[1] == 'fight':
                with open("GameData.json", "r+") as file:
                    data = json.loads(open('GameData.json').read())
                    try:
                        match = next(p for p in data['Players'] if p['id'] == message.author.id)
                        if match['wep'] == None:
                            await client.send_message(message.channel,
                                                      "{}, you currently do not have a weapon to fight! Use '$owl weapon buy' to buy one".format(
                                                          message.author.name))
                        else:
                            if abs(datetime.strptime(match["fighttime"][:10],
                                                     '%Y-%m-%d').date() - date.today()).days >= 1:
                                enemy_list = [' Sheep', ' Owl', ' Coffee', ' Lucy', ' Dude', ' Ricegum', ' Jake Paul',
                                              ' Goose', ' Knight', ' Panda', ' Roelof', ' Whale', ' Elephant']
                                enemy = weaponGen()
                                type = random.choice(enemy_list)
                                part = enemy.split('|')
                                # Rarity Emoji
                                if part[5] == '1':
                                    emoji_2 = u'\U0001F98B'
                                elif part[5] == '2':
                                    emoji_2 = u'\U0001F47E'
                                elif part[5] == '3':
                                    emoji_2 = u'\U0001F480'
                                elif part[5] == '4':
                                    emoji_2 = u"\u2620\uFE0F"
                                else:
                                    emoji_2 = u'\U0000203C', u'\U0001F4A2', u'\U0000203C'
                                await client.send_message(message.channel, "\U00002694 **{} goes off against {}!**\U00002694 \n\
{} **Difficulty:** {} \n\
{} **Visible Health:** {} (Without Multipliers)\n\
{} **Potential Reward:** {} Tokens \n\
Would you like to **[RUN AWAY]**(Does not Consume Daily Charge) or **[FIGHT]**(Consumes daily charge)?".format(
                                    message.author.name, part[0] + type, u'\U000026A0', emoji_2, u'\U0001F497', part[6],
                                    u'\U0001F4B0', part[8]))
                                # WIN/LOSS Calculations
                                wep = match['wep'].split('|')
                                if int(wep[7]) > int(part[7]):
                                    fight_confirm_list.append(message.author.id)
                                    fight_confirm_list.append('W|' + part[8])
                                else:
                                    fight_confirm_list.append(message.author.id)
                                    fight_confirm_list.append('L|' + str(round((int(part[8]) / 4))))
                                await client.add_reaction(message, u'\U00002694')  # fight
                                await client.add_reaction(message, u'\U0001F3C3')  # run

                            else:
                                await client.send_message(message.channel,
                                                          '\U0001F550 | **{}, you can only fight once every 24 hours. (Last Fight: {})**'.format(
                                                              message.author.name, match["fighttime"][:15]))
                    except StopIteration:
                        NewPlayer = PlayerCreation(message.author.id, None, 0,
                                                   str(datetime.today() - timedelta(days=2)),
                                                   str(datetime.today() - timedelta(days=2)), None)
                        data["Players"].append(NewPlayer)
                        with open('GameData.json', 'w') as file:
                            file.write(json.dumps(data, default=jdefault, indent=2))
                        sync()
                        await client.send_message(client.get_channel("498311009635794964"),
                                                  "Synced To Google Drive Successfully.\n{}".format(str(data)))
                        await client.send_message(message.channel,
                                                  "\U0001F4DC | **{}, you currently do not have a weapon to fight! Use '$owl weapon buy' to buy one**".format(
                                                      message.author.name))
        else:
            await client.send_message(message.channel,
                                      "\U000026A0 | [Syntax Error] $owl command must have atleast 1 syntax! ($help for more Information)")

    elif message.content.startswith('$role'):
        role_match = False
        role_names = ['periokoi', 'hentorn']
        role_proper_names = ['Periokoi', 'Hentorn']
        role_request = message.content
        roles = [
            # Role IDs
            '262743186634440705',  # Periokoi
            '447985460627767296',  # Hen
        ]
        if message.content[6:10].lower() == 'join':
            role = role_request[11:]
            if role.lower() in role_names:
                proper_position = role_names.index(role.lower())
                for r in message.author.roles:
                    if r.id == roles[proper_position]:
                        await client.send_message(message.channel, "You already possess this role {}".format(
                            '<@' + str(message.author.id) + '>'))
                        role_match = True
                        return
                if role_match == False:
                    try:
                        loaded_role = discord.utils.get(message.server.roles, name=role_proper_names[proper_position])
                        await client.add_roles(message.author, loaded_role)
                        await client.send_message(message.channel, "Successfully added role {} to {}".format(
                            role_proper_names[proper_position], '<@' + str(message.author.id) + '>'))
                    except discord.Forbidden:
                        await client.send_message(message.channel, "Insufficient Permissions for adding roles")
            else:
                await client.send_message(message.channel,
                                          "No matching role Found {}".format('<@' + str(message.author.id) + '>'))

        elif message.content[6:11].lower() == 'leave':
            role = role_request[12:]
            if role.lower() in role_names:
                proper_position = role_names.index(role.lower())
                for r in message.author.roles:
                    if r.id == roles[proper_position]:
                        role_match = True
                        try:
                            loaded_role = discord.utils.get(message.server.roles,
                                                            name=role_proper_names[proper_position])
                            await client.remove_roles(message.author, loaded_role)
                            await client.send_message(message.channel, "Successfully removed role {} from {}".format(
                                role_proper_names[proper_position], '<@' + str(message.author.id) + '>'))
                        except discord.Forbidden:
                            await client.send_message(message.channel, "Insufficient Permissions for removing roles")
                if role_match == False:
                    await client.send_message(message.channel,
                                              "You do possess this role {}".format('<@' + str(message.author.id) + '>'))
                    return
            else:
                await client.send_message(message.channel,
                                          "No matching role Found {}".format('<@' + str(message.author.id) + '>'))
        else:
            await client.send_message(message.channel, "No matching syntax Found, (Leave/Join)")

    elif message.content.startswith('$raffle'):
        if raff == 0:
            RRM = str(message.content)
            raffleArg = RRM.strip('$raffle')
            forceDrawKey = random.randint(1, 999999)
            print(str(forceDrawKey))
            print(raffleArg)
            if raffleArg == '':
                raffleArg = 'Unlimited'
                raff = 1
                hostid = message.author.id
                stringid = str(hostid)
                a = '**Raffle started by <@'
                b = ">! "
                c = "[Entry Limit:"
                d = "]"
                e = "\nType '$join' to join in!**"
                await client.send_message(message.channel, a + stringid + b + c + raffleArg + d + e)
            else:
                raff = 1
                hostid = message.author.id
                stringid = str(hostid)
                a = '**Raffle started by <@'
                b = ">! "
                c = "[Entry Limit:"
                d = "]"
                e = "\nType '$join' to join in!**"
                await client.send_message(message.channel, a + stringid + b + c + raffleArg + d + e)
        else:
            await client.send_message(message.channel, '**A raffle is already opened!**')
    elif message.content.startswith('$join'):
        if raff == 1:
            if raffleArg == 'Unlimited':
                userid = message.author.id
                dupecount = rafflelist.count(userid)
                if dupecount >= 1:
                    stringid = str(userid)
                    a = '<@'
                    b = '> You have already entered the raffle!'
                    await client.send_message(message.channel, a + stringid + b)
                else:
                    rafflelist.append(userid)
                    stringid = str(userid)
                    a = '<@'
                    b = '> Succesfully entered the raffle!'
                    await client.send_message(message.channel, a + stringid + b)
            else:
                if len(rafflelist) < int(raffleArg):
                    userid = message.author.id
                    dupecount = rafflelist.count(userid)
                    if dupecount >= 1:
                        stringid = str(userid)
                        a = '<@'
                        b = '> You have already entered the raffle!'
                        await client.send_message(message.channel, a + stringid + b)
                    else:
                        rafflelist.append(userid)
                        stringid = str(userid)
                        a = '<@'
                        b = '> Succesfully entered the raffle!'
                        await client.send_message(message.channel, a + stringid + b)
                else:
                    a = '**The current raffle opened by <@'
                    b = '> is full!**'
                    await client.send_message(message.channel, a + hostid + b)
        else:
            await client.send_message(message.channel, '**There are no current raffles!**')
    elif message.content.startswith('$draw'):
        RDM = str(message.content)
        keyCheck = str(message.content).strip('$draw')
        if str(keyCheck) == str(forceDrawKey):
            if raff == 1:
                if len(rafflelist) == 0:
                    await client.send_message(message.channel, '**No one has yet joined the raffle!**')
                else:
                    await client.send_message(message.channel, '**Drawing Winner...**')
                    time.sleep(2)
                    winnerid = random.choice(rafflelist)
                    stringid = str(winnerid)
                    a = '__**<@'
                    b = '> Won the raffle! Congratulations!**__'
                    await client.send_message(message.channel, a + stringid + b)
                    rafflelist = []
                    raff = 0
            else:
                await client.send_message(message.channel, '**There are no current raffles!**')
        else:
            if raff == 1:
                checkid = message.author.id
                if hostid == checkid:
                    if raff == 1:
                        if len(rafflelist) == 0:
                            await client.send_message(message.channel, '**No one has yet joined the raffle!**')
                        else:
                            await client.send_message(message.channel, '**Drawing Winner...**')
                            time.sleep(2)
                            winnerid = random.choice(rafflelist)
                            stringid = str(winnerid)
                            a = '__**<@'
                            b = '> Won the raffle! Congratulations!**__'
                            await client.send_message(message.channel, a + stringid + b)
                            rafflelist = []
                            raff = 0
                    else:
                        await client.send_message(message.channel, '**There are no current raffles!**')
                else:
                    await client.send_message(message.channel, '**Only the host of the raffle can draw the winner!**')
            else:
                await client.send_message(message.channel, '**There are no current raffles!**')

    elif message.content.startswith('$help'):
        await client.send_message(message.channel, "__**List of Commands**__\n\
----------------------------\n\
**Raffle Commands**\n\
**$raffle** - Starts a raffle\n\
**$join** - Joins an open raffle \n\
**$draw** - Draws the winner of the raffle \n\
----------------------------\n\
**Administrative Commands**\n\
**$stop** - Stops all activities and terminates\n\
**$clean [CLEANPHRASE] [NO. OF MESSAGES TO BE SEARCHED]** - Cleans messages containing specified phrase\n\
**$bot** - Defines a lock on Roelof's speech permissions\n\
----------------------------\n\
**Game Commands**\n\
**$owl daily** - Gives a daily reward of 200 Tokens\n\
**$owl tokens** - Shows the user's current Token Balance\n\
**$owl fight** - Daily fights that can grant/take away tokens\n\
**$owl weapon buy/sell** - Buys/sells a weapon for tokens (500 Token to Buy)\n\
----------------------------\n\
**Role Commands**\n\
**$role [JOIN/LEAVE] [ROLE]** - Adds/Removes the defined role to the user\n\
----------------------------\n\
***Custom Commands can be added if wished (PM BlueOwl)***")
    elif message.content.startswith('$salt'):
        if salt == True:
            try:
                loaded_role = discord.utils.get(message.server.roles, name='Salty')
                loaded_user = discord.utils.get(message.server.members, id='233781837892288523')
                await client.remove_roles(loaded_user, loaded_role)
                await client.add_reaction(message, u"\u2705")
                salt = False
            except discord.Forbidden:
                await client.send_message(message.channel, "Insufficient Permissions for adding roles")
        elif salt == False:
            try:
                loaded_role = discord.utils.get(message.server.roles, name='Salty')
                loaded_user = discord.utils.get(message.server.members, id='233781837892288523')
                await client.add_roles(loaded_user, loaded_role)
                await client.add_reaction(message, u"\u2705")
                salt = True
            except discord.Forbidden:
                await client.send_message(message.channel, "Insufficient Permissions for adding roles")
    elif 'woojin' in message.content.lower():
        if 'happy birthday' in message.content.lower():
            await client.delete_message(message)
    elif 'almonds' in message.content.lower():
        await client.delete_message(message)
    elif os.environ['PROTECTION'] in message.content.lower():
        await client.delete_message(message)


@client.event
async def on_reaction_add(reaction, user):
    global buy_confirm_list
    global sell_confirm_list
    global reforge_confirm_list
    global fight_confirm_list
    global choice_list
    global weaponGen
    global sync
    with open("GameData.json", "r+") as file:
        data = json.loads(open('GameData.json').read())
        if user.id in buy_confirm_list:
            if reaction.emoji == u"\u2705":
                match = next(p for p in data['Players'] if p['id'] == user.id)
                match['temp_wep'] = weaponGen()
                with open('GameData.json', 'w') as file:
                    file.write(json.dumps(data, default=jdefault, indent=2))
                sync()
                await client.send_message(client.get_channel("498311009635794964"),
                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                buy_confirm_list.remove(user.id)
                if match['wep'] == None:
                    match['wep'] = match['temp_wep']
                    match['bank'] -= 500
                    with open('GameData.json', 'w') as file:
                        file.write(json.dumps(data, default=jdefault, indent=2))
                    sync()
                    await client.send_message(client.get_channel("498311009635794964"),
                                              "Synced To Google Drive Successfully.\n{}".format(str(data)))
                    await client.send_message(reaction.message.channel,
                                              "\U0001F4EC | **{} has received a new weapon!**\n{}".format(user.name,
                                                                                                          formatter(
                                                                                                              match[
                                                                                                                  'temp_wep'],
                                                                                                              user.name)))
                else:
                    await client.send_message(reaction.message.channel,
                                              "\U0001F6AB | **You cannot have 2 weapons at once! You will need to choose which to keep. (React to Emoji)**\n**__1. Original Weapon__**\n{}\n\n**__2. New Weapon__**\n{}".format(
                                                  formatter(match["wep"], user.name),
                                                  formatter(match["temp_wep"], user.name)))
                    choice_list.append(user.id)
                    async for message in client.logs_from(reaction.message.channel, limit=5):
                        if message.author.id == '357697820938993666':
                            await client.add_reaction(message, u'\U0001F195')
                            await client.add_reaction(message, u'\U0001F502')
                            break
            elif reaction.emoji == u"\u274E":
                buy_confirm_list.remove(user.id)
                await client.send_message(reaction.message.channel, "\U0001F44D | **Weapon purchase cancelled**")

        elif user.id in sell_confirm_list:
            if reaction.emoji == u"\u2705":
                match = next(p for p in data['Players'] if p['id'] == user.id)
                part = match['wep'].split('|')
                match['bank'] += int(part[8])
                match['wep'] = None
                with open('GameData.json', 'w') as file:
                    file.write(json.dumps(data, default=jdefault, indent=2))
                sync()
                await client.send_message(client.get_channel("498311009635794964"),
                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                sell_confirm_list.remove(user.id)
                await client.send_message(reaction.message.channel,
                                          "\U0001F4B0 | **{} has sold a weapon for {} Tokens**".format(user.name,
                                                                                                       part[8]))

            elif reaction.emoji == u"\u274E":
                sell_confirm_list.remove(user.id)
                await client.send_message(reaction.message.channel, "\U0001F44D | **Weapon sale cancelled**")

        elif user.id in reforge_confirm_list:
            if reaction.emoji == u"\u2705":
                match = next(p for p in data['Players'] if p['id'] == user.id)
                old = match['wep'].split('|')
                new = weaponGen().split('|')
                #Renamed
                old[3] = str(new[0]+' '+old[2])
                #Damage with New
                damage_int = int(old[6])*int(new[1])*int(old[5])
                damage = str(damage_int)
                #Weapon Worth
                worth = str(round(damage_int/15*int(old[5])))
                #reassembly
                reforged = new[0]+'|'+new[1]+'|'+old[2]+'|'+old[3]+'|'+old[4]+'|'+old[5]+'|'+old[6]+'|'+damage+'|'+worth
                match['wep'] = reforged
                match['bank'] -= 500
                with open('GameData.json', 'w') as file:
                    file.write(json.dumps(data, default=jdefault, indent=2))
                sync()
                await client.send_message(client.get_channel("498311009635794964"),
                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                reforge_confirm_list.remove(user.id)
                await client.send_message(reaction.message.channel,
                                          "\U0001F528 | **{} has reforged a weapon and got the {} Prefix**".format(user.name,
                                                                                                       new[0]))
            
            elif reaction.emoji == u"\u274E":
                reforge_confirm_list.remove(user.id)
                await client.send_message(reaction.message.channel, "\U0001F44D | **Weapon Reforge Cancelled**")

        elif user.id in fight_confirm_list:
            if reaction.emoji == u'\U00002694':  # fight
                match = next(p for p in data['Players'] if p['id'] == user.id)
                pos = fight_confirm_list.index(user.id) + 1
                result = fight_confirm_list.pop(pos)
                fight_confirm_list.remove(user.id)
                part = result.split('|')
                if part[0] == 'W':
                    match['bank'] += int(part[1])
                    await client.send_message(reaction.message.channel,
                                              "\U0001F4B0 | **{} has won a fight and received a bounty of {} Tokens!**".format(
                                                  user.name, part[1]))
                else:
                    match['bank'] -= int(part[1])
                    await client.send_message(reaction.message.channel,
                                              "\U0001F3F3 | **{} has lost a fight and lost {} Tokens. (Maybe try running next time)**".format(
                                                  user.name, part[1]))
                match['fighttime'] = str(datetime.today())
                with open('GameData.json', 'w') as file:
                    file.write(json.dumps(data, default=jdefault, indent=2))
                sync()
                await client.send_message(client.get_channel("498311009635794964"),
                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))

            elif reaction.emoji == u'\U0001F3C3':  # run
                fight_confirm_list.remove(user.id)
                await client.send_message(reaction.message.channel,
                                          "\U0001F3C3 | **{} Safely ran away**".format(user.name))


        elif user.id in choice_list:
            if reaction.emoji == u'\U0001F195':  # new
                data = json.loads(open('GameData.json').read())
                match = next(p for p in data['Players'] if p['id'] == user.id)
                part = match['wep'].split('|')
                sale = part[8]
                match['wep'] = match['temp_wep']
                match['bank'] -= 500
                match['bank'] += int(sale)
                with open('GameData.json', 'w') as file:
                    file.write(json.dumps(data, default=jdefault, indent=2))
                sync()
                await client.send_message(client.get_channel("498311009635794964"),
                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                choice_list.remove(user.id)
                await client.send_message(reaction.message.channel,
                                          "\U00002694 | **{} has sold his old weapon for {} and received a new weapon!**\n{}".format(
                                              user.name, sale, formatter(match['temp_wep'])))
            elif reaction.emoji == u'\U0001F502':  # old
                choice_list.remove(user.id)
                await client.send_message(reaction.message.channel,
                                          "\U0001F44D | **{} decides to keep his old weapon**".format(user.name))


gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Handles authentication.
drive = GoogleDrive(gauth)
drive_file = drive.CreateFile({'id': os.environ['DRIVE_FILE_ID']})
drive_content = drive_file.GetContentString()
with open('GameData.json', 'w') as file:
    data = json.loads(drive_content)
    file.write(json.dumps(data, default=jdefault, indent=2))

client.run(os.environ['BOT_TOKEN'])

