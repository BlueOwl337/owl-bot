import discord
import asyncio
import random
import os
import authwriter
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

class RaffleCreation():
    def __init__(self, messageid, hostid, limit, prize, key):
        self.messageid = messageid
        self.hostid = hostid
        self.entries = []
        self.limit = limit
        self.prize = prize
        self.key = key

def sync(dest):
    global drive
    if dest == 'game':
        with open("GameData.json", "r+") as file:
            print(open('GameData.json').read())
            data = json.loads(open('GameData.json').read())
            drive_file = drive.CreateFile({'id': os.environ['GAME_FILE_ID']})
            drive_file.SetContentString(json.dumps(data, default=jdefault, indent=2))
            drive_file.Upload()
    elif dest == 'raffle':
        with open("RaffleData.json", "r+") as file:
            print(open('RaffleData.json').read())
            data = json.loads(open('RaffleData.json').read())
            drive_file = drive.CreateFile({'id': os.environ['RAFFLE_FILE_ID']})
            drive_file.SetContentString(json.dumps(data, default=jdefault, indent=2))
            drive_file.Upload()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='with his Owlets ($help)'))
    data = json.loads(open('GameData.json').read())
    await client.send_message(client.get_channel("498311009635794964"),
                                "[DYNO RESTART] Synced From Google Drive Successfully.\n{}".format(str(data)))
    data = json.loads(open('RaffleData.json').read())
    await client.send_message(client.get_channel("503093220146806794"),
                              "[DYNO RESTART] Synced From Google Drive Successfully.\n{}".format(str(data)))



@client.event
async def on_message(message):
    global salt
    global bot_roelof
    global first
    global StopPermList
    # Raffle essential
    global RaffleCreation
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
                            sync('game')
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
                        sync('game')
                        await client.send_message(client.get_channel("498311009635794964"),
                                                  "Synced To Google Drive Successfully.\n{}".format(str(data)))
                        await client.send_message(message.channel, '\U0001F4B0 | **{} has received 200 tokens**'.format(
                            message.author.name))

            elif syntax[1].startswith('token'):
                with open("GameData.json", "r+") as file:
                    data = json.loads(open('GameData.json').read())
                if len(syntax) > 2:
                    if syntax[2] == 'gift':
                        if len(syntax) == 5:
                            try:
                                amount = round(int(syntax[4]))
                                recipient = next(p for p in data['Players'] if p['id'] == syntax[3].strip('<@>'))
                            except ValueError:
                                await client.send_message(message.channel, 'Invalid Amount!')
                                return
                            except StopIteration:
                                await client.send_message(message.channel, 'Invalid Recipient!')
                                return
                            try:
                                sender = next(p for p in data['Players'] if p['id'] == message.author.id)
                            except StopIteration:
                                NewPlayer = PlayerCreation(message.author.id, None, 200, str(datetime.today() - timedelta(days=2)),
                                                           str(datetime.today() - timedelta(days=2)), None)
                                data["Players"].append(NewPlayer)
                                with open('GameData.json', 'w') as file:
                                    file.write(json.dumps(data, default=jdefault, indent=2))
                                sync('game')
                                await client.send_message(client.get_channel("498311009635794964"),
                                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                                sender = next(p for p in data['Players'] if p['id'] == message.author.id)
                            if sender['bank'] > amount:
                                recipient['bank'] += amount
                                sender['bank'] -= amount
                                with open('GameData.json', 'w') as file:
                                    file.write(json.dumps(data, default=jdefault, indent=2))
                                await client.send_message(message.channel, '\U0001F381 | {} Gifted {} Tokens to {}!'.format(message.author.name, amount, syntax[3]))
                                sync('game')
                                await client.send_message(client.get_channel("498311009635794964"),
                                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                            else:
                                await client.send_message(message.channel, 'You do not have enough tokens to gift that many!')

                        else:
                            await client.send_message(message.channel, 'Invalid Usage of Command, Correct Usage: $owl token gift [RECIPiENT] [AMOUNT]')


                else:
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
                            sync('game')
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
                                    await client.send_message(message.channel,
                                                              "\U0001F4DC | **{}, you currently do not have a weapon to reforge! Use '$owl weapon buy' to buy one**".format(
                                                                  message.author.name))
                                else:
                                    if match['bank'] > 500:
                                        await client.send_message(message.channel,
                                                                  "\U0001F528 | **Would you really like to reforge your weapon's prefix? This will cost 500 Tokens (React to emoji)** \n**Your Current Weapon:**\n {}\n \U0001F527 | **Reforging may increase or decrease your overall damage**".format(
                                                                      formatter(match['wep'], message.author.name)))
                                        reforge_confirm_list.append(message.author.id)
                                        await client.add_reaction(message, u"\u2705")
                                        await client.add_reaction(message, u"\u274E")
                                    else:
                                        await client.send_message(message.channel,
                                                                  '**You do not have enough tokens to Reforge! (500 Tokens)**')

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
                        sync('game')
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
                        sync('game')
                        await client.send_message(client.get_channel("498311009635794964"),
                                                  "Synced To Google Drive Successfully.\n{}".format(str(data)))
                        await client.send_message(message.channel,
                                                  "\U0001F4DC | **{}, you currently do not have a weapon to fight! Use '$owl weapon buy' to buy one**".format(
                                                      message.author.name))
                        
            elif syntax[1] == 'stats':
                data = json.loads(open('GameData.json').read())
                if len(syntax) < 3:
                    bank_list = []
                    for player in data['Players']:
                        bank_list.append(player['bank'])
                    print(bank_list)
                    bank_list.sort()
                    print(bank_list)
                    counter = 5
                    top = []
                    while counter > 0:
                        match = next(p for p in data['Players'] if p['bank'] == bank_list[counter])
                        user = await client.get_user_info(match['id'])
                        top.insert(0, user.name)
                        top.insert(1, str(bank_list[counter]))
                        counter -= 1
                    print(top)
                    await client.send_message(message.channel,
                                              "\U0001F4CB **__Top 5 LeaderBoards__**\U0001F4CB \n\
    **Current Leaderboards For tokens:**\n\
    \U0001F947 | **{} | {} Tokens \U0001F3C6**\n\
    \U0001F948 | **{} | {} Tokens \U0001F4B0**\n\
    \U0001F949 | **{} | {} Tokens \U0001F4B8**\n\
    -------------------------\n\
    \U00000034\U000020E3 | **{} | {} Tokens**\n\
    \U00000035\U000020E3 | **{} | {} Tokens**".format(top[0], top[1], top[2], top[3], top[4], top[5], top[6], top[7],
                                                      top[8], top[9]))
                else:
                    # indivisual stats
                    target = next(p for p in data['Players'] if p['id'] == syntax[2].strip('<@>'))
                    target_user = await client.get_user_info(target['id'])
                    last_daily = target['dailytime']
                    last_fight = target['fighttime']
                    await client.send_message(message.channel,
                                              "**__Profile & Statistics for {}__**\n\
    :crossed_swords: | **Weapon:**\n\
    {}\n\
    :bank: | **Bank: {} Tokens**\n\
    :calendar_spiral: | **Last Daily Claim: {}**\n\
    :alarm_clock: | **Last Fight: {}**".format(target_user, formatter(target["wep"], target_user.name), target['bank'],
                                               last_daily[:16], last_fight[:16]))
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
        syntax = message.content.split()
        syntax_len = len(syntax)
        if syntax_len > 1:
            if syntax[1] == 'start':
                with open("RaffleData.json", "r+") as file:
                    data = json.loads(open('RaffleData.json').read())
                    try:
                        match = next(p for p in data['Raffles'] if p['hostid'] == message.author.id)
                        await client.send_message(message.channel, "**{} You already have an ongoing raffle! Please draw it before opening a new one**".format(message.author.name))
                    except StopIteration:
                        limit = None
                        prize = None
                        if "\"" in message.content:
                            split = message.content.split("\"")
                            prize = split[1]
                            no_prize = message.content.replace("\"" + prize + "\"", '').split()
                            if len(no_prize) == 3:
                                limit = int(no_prize[2])
                        elif syntax_len > 2 and syntax_len < 4:
                            limit = int(syntax[2])
                        key = random.randint(1, 999999)
                        if prize == None:
                            await client.send_message(message.channel,
                                                      "\U0001F3B2 | **Raffle started by {}! [Entry Limit: {}]\nReact to the emoji to join!**".format(
                                                          '<@' + message.author.id + '>', limit))
                        else:
                            await client.send_message(message.channel,
                                                  "\U0001F3B2 | **Raffle started by {} for {}! [Entry Limit: {}]\nReact to the emoji to join!**".format(
                                                      '<@' + message.author.id + '>', prize, limit))

                        async for msg in client.logs_from(message.channel, limit=5):
                            if msg.author.id == '357697820938993666':
                                await client.add_reaction(msg, u'\U0001F39F')
                                data["Raffles"].append(RaffleCreation(msg.id, message.author.id, limit, prize, str(key)))
                                with open('RaffleData.json', 'w') as file:
                                    file.write(json.dumps(data, default=jdefault, indent=2))
                                sync('raffle')
                                data = json.loads(open('RaffleData.json').read())
                                await client.send_message(client.get_channel("503093220146806794"),
                                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                                break
                        await client.send_message(message.author,
                                                  "Your Raffle has been Successfully Created with the Force Draw Key of **{}**. You can share this key with anyone and they will be able to draw your raffle at any time using `$raffle draw {}`".format(
                                                      key, key))
            elif syntax[1] == 'draw':
                with open("RaffleData.json", "r+") as file:
                    data = json.loads(open('RaffleData.json').read())
                    try:
                        match = next(p for p in data['Raffles'] if p['hostid'] == message.author.id)

                    except StopIteration:
                        if syntax_len > 2:
                            try:
                                match = next(p for p in data['Raffles'] if p['key'] == syntax[3])
                            except StopIteration:
                                await client.send_message(message.channel,
                                                          "\U0001F6AB | **Invalid Force Draw Key**")
                                return
                        else:
                            await client.send_message(message.channel,
                                                  "**{} Only the host can draw the winner!**".format(
                                                      message.author.name))
                            return
                    try:
                        msg = await client.get_message(message.channel, id=match['messageid'])
                    except:
                        await client.send_message(message.channel, "**The Raffle Message cannot be found. Please try the channel the raffle was started in. (Contact BlueOwl if Issue Persists)**")
                    reaction_object = msg.reactions[0]
                    users = await client.get_reaction_users(reaction_object)
                    entries = []
                    for user in users:
                        entries.append(user.id)
                    if len(entries) == 1:
                        await client.send_message(message.channel, "**No one has yet entered the raffle!**")
                        return
                    entries.remove('357697820938993666')
                    winner = random.choice(entries)
                    if match['prize'] == None:
                        # no Prize no limit
                        if match['limit'] == None:
                            print('nothin')
                            await client.send_message(message.channel,
                                                      "\U0001F389 | __**{} Won the Raffle! Congratulations!**__".format(
                                                          '<@' + winner + '>'))
                        else:
                            # no Prize yes limit
                            print('limit')
                            late = 0
                            while match['limit'] < len(entries):
                                entries.pop()
                                late += 1
                            if late > 0:
                                await client.send_message(message.channel,
                                                          "\U0001F389 | __**{} Won the Raffle! Congratulations!**__\n**The last {} entrants were elimated as the raffle defined a maximum limit of entrants to {}.**".format(
                                                              '<@' + winner + '>', late, match['limit']))
                            else:
                                await client.send_message(message.channel,
                                                          "\U0001F389 | __**{} Won the Raffle! Congratulations!**__".format(
                                                              '<@' + winner + '>'))
                    else:
                        #yes Prize no limit
                        if match['limit'] == None:
                            print('prize')
                            await client.send_message(message.channel,
                                                      "\U0001F389 | __**{} Won the Raffle for {}! Congratulations!**__".format(
                                                          '<@' + winner + '>', match['prize']))
                        else:
                            #yes Prize yes limit
                            print('prize limit')
                            late = 0
                            while match['limit'] < len(entries):
                                entries.pop()
                                late += 1
                            if late > 0:
                                await client.send_message(message.channel,
                                                          "\U0001F389 | __**{} Won the Raffle for {}! Congratulations!**__\n**The last {} entrants were elimated as the raffle defined a maximum limit of entrants to {}.**".format(
                                                              '<@' + winner + '>', match['prize'], late, match['limit']))
                            else:
                                await client.send_message(message.channel,
                                                          "\U0001F389 | __**{} Won the Raffle for {}! Congratulations!**__".format(
                                                              '<@' + winner + '>', match['prize']))
                    host = await client.get_user_info(match['hostid'])
                    winner_name = await client.get_user_info(winner)
                    await client.send_message(host, "Your raffle has ended with {} as the winner! (ID: {}). You can now start a new raffle".format(winner_name, winner))
                    data['Raffles'].remove(match)
                    with open('RaffleData.json', 'w') as file:
                        file.write(json.dumps(data, default=jdefault, indent=2))
                    sync('raffle')
                    data = json.loads(open('RaffleData.json').read())
                    await client.send_message(client.get_channel("503093220146806794"),
                                              "Synced To Google Drive Successfully.\n{}".format(str(data)))

    elif message.content.startswith('$help'):
        await client.send_message(message.channel, "__**List of Commands**__\n\
----------------------------\n\
**Raffle Commands**\n\
**$raffle start <LIMIT> <PRIZE>** - Starts a raffle\n\
**$raffle draw <FORCE DRAW KEY>** - Draws the winner of the raffle \n\
----------------------------\n\
**Administrative Commands**\n\
**$stop** - Stops all activities and terminates\n\
**$clean [CLEANPHRASE] [NO. OF MESSAGES TO BE SEARCHED]** - Cleans messages containing specified phrase\n\
**$bot** - Defines a lock on Roelof's speech permissions\n\
----------------------------\n\
**Game Commands**\n\
**$owl daily** - Gives a daily reward of 200 Tokens\n\
**$owl tokens** - Shows the user's current Token Balance\n\
**$owl token gift [USER(Ping)] [AMOUNT]** - Shows the user's current Token Balance\n\
**$owl fight** - Daily fights that can grant/take away tokens\n\
**$owl weapon buy/sell** - Buys/sells a weapon for tokens (500 Token to Buy)\n\
**$owl weapon reforge** - Reforges a weapon for tokens (500 Token to Reforge)\n\
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
                sync('game')
                await client.send_message(client.get_channel("498311009635794964"),
                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                buy_confirm_list.remove(user.id)
                if match['wep'] == None:
                    match['wep'] = match['temp_wep']
                    match['bank'] -= 500
                    with open('GameData.json', 'w') as file:
                        file.write(json.dumps(data, default=jdefault, indent=2))
                    sync('game')
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
                sync('game')
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
                # Renamed
                old[3] = str(new[0] + ' ' + old[2])
                # Damage with New
                damage_int = int(old[6]) * int(new[1]) * int(old[5])
                damage = str(damage_int)
                # Weapon Worth
                worth = str(round(damage_int / 15 * int(old[5])))
                # reassembly
                reforged = new[0] + '|' + new[1] + '|' + old[2] + '|' + old[3] + '|' + old[4] + '|' + old[5] + '|' + \
                           old[6] + '|' + damage + '|' + worth
                match['wep'] = reforged
                match['bank'] -= 500
                with open('GameData.json', 'w') as file:
                    file.write(json.dumps(data, default=jdefault, indent=2))
                sync('game')
                await client.send_message(client.get_channel("498311009635794964"),
                                          "Synced To Google Drive Successfully.\n{}".format(str(data)))
                reforge_confirm_list.remove(user.id)
                await client.send_message(reaction.message.channel,
                                          "\U0001F528 | **{} has reforged a weapon and got the {} Prefix**".format(
                                              user.name,
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
                sync('game')
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
                sync('game')
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

def authentication():
    global drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    #Game Sync
    drive_file = drive.CreateFile({'id': os.environ['GAME_FILE_ID']})
    drive_content = drive_file.GetContentString()
    with open('GameData.json', 'w') as file:
        data = json.loads(drive_content)
        file.write(json.dumps(data, default=jdefault, indent=2))
    #Raffle Sync
    drive_file = drive.CreateFile({'id': os.environ['RAFFLE_FILE_ID']})
    drive_content = drive_file.GetContentString()
    with open('RaffleData.json', 'w') as file:
        data = json.loads(drive_content)
        file.write(json.dumps(data, default=jdefault, indent=2))


authentication()
client.run(os.environ['BOT_TOKEN'])

