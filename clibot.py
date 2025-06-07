# -----------------------------------------------------------------------
#   Cli-Bot - discord bot dedicated to shit posting and other fun
#   Authors: WhiteTrick
#   Contributors: v0idbit
# -----------------------------------------------------------------------
# import packages
import discord
from discord.ext import commands
from discord.ext.commands import bot  # discord API
from discord import opus
import logging  # used for logging errors
from math import e
import matplotlib.pyplot as plt
import numexpr as ne
import numpy as np
# import opus                   #necessary for using voice channel
from random import randint  # generate pseudorandom numbers
import re
import os
import string
import asyncio
from functools import reduce

# set logging level: logs to Command Line Interface
logging.basicConfig(level=logging.INFO)

# instantiate client
clibot = discord.Client(max_messages=10000)

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll',
             'libopus.so.0', 'libopus.0.dylib']


def GCD(a, b):
    if (a < b):
        A = a
        R = B = b
    else:
        A = b
        R = B = a
    while (R != 0):
        R = A % B
        if (R == 0):
            return B
        A = B
        B = R


remove_punctuation = str.maketrans('', '', string.punctuation)


def load_opus_lib(opus_libs=OPUS_LIBS):
    """	loads opus lib	"""
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

    raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))


bot = commands.Bot(command_prefix='#')

# initialize game that Clibot will be playing
playing_game = discord.Game(name="with myself")


# global voice
# global player

@clibot.event
async def on_ready():
    """	called when clibot finishes preparing data received from Discord	"""
    print('Logged in as')
    print(clibot.user.name)
    print(clibot.user.id)
    print('--------')
    print('invite URL')
    print(discord.utils.oauth_url('352256816790503425'))
    load_opus_lib()
    await clibot.change_presence(game=playing_game)


'''

'''


@bot.command(pass_context=True)
async def gcd(ctx, arg):
    mytuple = tuple([int(word) for word in arg.translate(remove_punctuation).split(" ")])
    output = reduce(GCD, mytuple)
    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="Greatest Common Denominator", value="GCD{} = {}".format(mytuple, output))
    await clibot.send_message(ctx.message.channel, embed=embed)


@clibot.event
async def on_message_delete(message):
    """	called when a message is deleted. Keyword arguments:	message -- the message (object) deleted """
    if len(message.content) > 0 and message.author.name != "cli-bot":
        author = message.author.name
        content = message.clean_content
        print('{}\'s message "*{}*" was deleted.'.format(author, content))


@clibot.event
async def on_message(message):
    await bot.process_commands(message)
    spongerob = randint(1, 100)
    kisses = randint(1, 100)
    if (len(message.content) > 0 and spongerob == 1
            and message.author.name != "cli-bot"):
        # 1% chance of cli-bot mocking a non-blank message, given
        #    it's not from cli-bot itself
        msg = message.clean_content
        print(msg)
        new_msg = list(msg)

        for i in range(0, len(msg)):
            # iterates over the message as a char array and swaps the
            #    case of alpha characters ~67% of the time
            r = randint(1, 3)
            if r <= 2:
                if new_msg[i].isupper():
                    # swap from upper to lower
                    new_msg[i] = new_msg[i].lower()
                else:
                    # swap from lower to upper
                    new_msg[i] = new_msg[i].upper()

        new_msg = "".join(new_msg)  # joins char array back into string
        file = './spongerob.jpg'
        await clibot.send_file(message.channel, file,
                               content=new_msg, tts=True)
    if (len(message.content) > 0 and (kisses in range(1, 4))
            and message.author.name != "cli-bot"):
        await clibot.add_reaction(message, '\U0001F48b')

    # if (any(word in ['cli', 'clibot', 'cli-bot'] for word in
    #         message.content.lower().translate(remove_punctuation).split())
    #         and message.author.name != "cli-bot"):
    if re.search(r"cli", message.content, re.I) and message.author.name != "cli-bot":
        if re.search(r"l[ou]v", message.content, re.I):
            await clibot.add_reaction(message, '\U0001F633')
        if (
                any(word in ['annoy', 'annoying'] for word in
                    message.content.lower().translate(remove_punctuation).split())):
            await clibot.add_reaction(message, '😘')

    if re.search(r"better.*idea|idea.*better", message.content, re.I) and message.author.name != "cli-bot":
        await clibot.add_reaction(message, emoji=':helno:370408318352490496')

    matchObj = re.match(r'^cli-plot ([^=]+)=([\d\+\-\*\%/\^()\.[a-zA-Z]+);?\s?(xlab=\'[^,]*\')?,?\s?(ylab=\'[^,]*\')?,?\s?(title=\'[^,]*\')?,?\s?(range\(([\+\-]?[(\d*\.?\d*)|(\d*)]{1,}),\s?([\+\-]?[(\d*\.?\d*)|(\d*)]{1,})\))?,?\s?(--autoscale)?$', message.content, re.I)
    if matchObj:
        # cli-plot event
        # cli-plot <f(x)>=<function>; xlab='<label>', ylab='<label>', title='<title>', range(<a>,<b>), <--autoscale>
        print("matched Object: {}".format(matchObj))
        with plt.xkcd():
            lhs = matchObj.group(1)
            rhs = matchObj.group(2)
            rhs = rhs.replace('^', '**')
            print("lhs: {}; rhs: {}".format(lhs, rhs))
            if matchObj.group(3):
                print("group3: {}".format(matchObj.group(3)))
                xlab = matchObj.group(3)[6:-1]
                plt.xlabel(xlab)
            else:
                plt.xlabel('x')
            if matchObj.group(4):
                print("group4: {}".format(matchObj.group(4)))
                ylab = matchObj.group(4)[6:-1]
                plt.ylabel(ylab)
            else:
                plt.ylabel(lhs)
            if matchObj.group(5):
                print("group5: {}".format(matchObj.group(5)))
                plt.title(matchObj.group(5)[7:-1])
            if matchObj.group(6):
                print("group6: {}".format(matchObj.group(6)))
                if float(matchObj.group(7)) <= float(matchObj.group(8)):
                    a = float(matchObj.group(7))
                    b = float(matchObj.group(8))
                    print("{} < {}".format(a, b))
                else:
                    b = float(matchObj.group(7))
                    a = float(matchObj.group(8))
                    print("{} < {}".format(a, b))
                x = np.arange(a, b, .01)
            else:
                x = np.arange(-1, 1, .01)
            y = ne.evaluate(rhs)
            if not matchObj.group(9):
                plt.axes().set_aspect('equal')
            #            plt.autoscale(False, 'x', True)
            #            plt.autoscale(True, 'y')
            plt.xlim((np.amin(x), np.amax(x)))
            plt.ylim((np.amin(y), np.amax(y)))
            plt.grid(True)
            plt.plot(x, y)
            file = './fig.png'
            plt.savefig(file, bbox_inches="tight")
            plt.close()
            await clibot.send_file(message.channel, file)
    elif message.content.startswith('plot'):
        msg = 'gay'
        await clibot.send_message(message.channel, msg)

    if re.match(r'^cliroll \d+d\d+(?:[\+-]\d+)*$', message.content, re.I):
        roll = 0
        findOperand = re.findall(r'[\d]+', message.content)
        findOperator = re.findall(r'[\+-]', message.content)
        try:
            if int(findOperand[0]) <= 300:
                rolls = []
                mods = ''
                for n in range(int(findOperand[0])):
                    nroll = randint(1, int(findOperand[1]))
                    roll += nroll
                    if int(findOperand[0]) <= 275:
                        rolls.append(nroll)
                i = 2
                for s in findOperator:
                    op = int(findOperand[i])
                    if s == '+':
                        roll += op
                        if int(findOperand[0]) <= 275:
                            mods += '+{}'.format(op)
                    else:
                        roll -= op
                        if int(findOperand[0]) <= 275:
                            mods += '-{}'.format(op)

                msg = '{} → Σ{}{} ({})'.format(message.content[7:], rolls, mods, roll)
                msg = msg if int(findOperand[0]) <= 275 else '{}'.format(roll)
            else:
                msg = 'too many dice will spoil the broth'

            await clibot.send_message(message.channel, msg)
        except:
            msg = 'but they\'ll fill our hearts with so much so much lo-ove'
            await clibot.send_message(message.channel, msg)
            pass
    elif message.content.startswith('cliroll'):
        await clibot.send_message(message.channel, 'wrong')

    ree = re.findall(r"re{2,}", message.content, re.I)
    if ree and message.author.name != "cli-bot":
        reee = ''.join(ree)
        ree_trigger = reee.count('r')
        # awaiting images to trigger with
        if ree_trigger > 2000:
            for member in message.server.members:
                if member.id == "352256816790503425":
                    target = member
            for channel in message.server.channels:
                # print(channel.permissions_for(target).send_messages)
                if channel.type == message.channel.type and channel.permissions_for(target).send_messages:
                    await clibot.send_message(channel, reee.upper(), tts=True)
        else:
            await clibot.send_message(message.channel, reee.upper(), tts=True)

    matchObj = re.match(r'^\.\.(-?\d+),(\s?(TRUE,)?\s?.+)$', message.content, re.I)
    if matchObj:
        content = matchObj.group(2)
        offset = int(matchObj.group(1))
        user = message.author.name
        abc = string.printable
        if (matchObj.group(3)):
            content = content[len(matchObj.group(3)):]
        else:
            await clibot.delete_message(message)
        if offset < -1 * len(abc):
            offset = len(abc) - (-1 * offset % len(abc))
        elif offset < 0:
            offset = len(abc) + offset
        elif offset > len(abc):
            offset = offset % len(abc)
        trns = str.maketrans(''.join(abc), ''.join(abc[offset:] + abc[:offset]))
        content = content.translate(trns)
        msg = '*{}: {}*'.format(user, content)
        await clibot.send_message(message.channel, msg)

    elif message.content.startswith('..'):
        content = message.content[2:]
        await clibot.delete_message(message)
        msg = '{}'.format(content)
        await clibot.send_message(message.channel, msg)

    elif message.mention_everyone:
        # cli-bot will complain if a message mentions everyone
        reactionImages = os.listdir('./everyone')
        everyone = randint(0, len(reactionImages) - 1)
        if everyone == 0 and spongerob > 1:
            everyone = randint(1, len(reactionImages) - 1)
        file = './everyone/{}.jpg'.format(everyone)
        await clibot.send_file(message.channel, file)

    # elif ('boys' in message.content.lower()):
    # elif (any(word in ['boys', 'bois', 'boyz', 'boiz'] for word in
    #           message.content.lower().translate(remove_punctuation).split())):
    # elif re.search(r'^.*bo[yi][sz][\W]?$', message.content, re.I):
    elif re.search(r'bo[yi][sz]', message.content, re.I):
        # cli-bot will mention everyone if a message contains "boys"
        # consequently, cli-bot will then complain about itself
        #    mentioning everyone; this is intentional
        content = '@everyone'
        await clibot.send_message(message.channel, content)

    # elif any(word in ['dick', 'cheney'] for word in message.content.lower().translate(remove_punctuation).split()):
    elif re.search(r'dick|cheney', message.content, re.I):
        # cli-bot responds appropriately to someone referring to our
        #    lord and saviour Dick Cheney
        reactionImages = os.listdir('./dickpics')
        everyone = randint(0, len(reactionImages) - 1)
        file = './dickpics/{}.jpg'.format(everyone)
        await clibot.send_file(message.channel, file)

    elif ((clibot.user.mentioned_in(message)) and
          ('heal all' in message.content.lower())
          and (message.author.name != 'cli-bot')):
        # cli-bot responds to being mentioned in a message that includes
        #    "heal all"
        twentyD4 = 0
        async for i in range(0, 20):
            # simulate 20d4
            twentyD4 = twentyD4 + randint(1, 4)
        r = randint(1, 100)
        heal = 'self'
        if r == 1:
            heal = 'all'
        content = '*heals {} for {}*'.format(heal, twentyD4)
        await clibot.send_message(message.channel, content)

    elif ((clibot.user.mentioned_in(message))
          and ('help' in message.content.lower())
          and message.author.name != 'cli-bot'):
        # cli-bot responds (poorly) to being mentioned in a message that
        #    includes "help"
        author = message.author.nick
        content = 'No. Fuck you {}.'.format(author)
        await clibot.send_message(message.channel, content)

    elif clibot.user.mentioned_in(message) and message.author.name != 'cli-bot':
        # cli-bot responds with a greeting when mentioned in a message
        #    that contains no trigger words
        # author = message.author.name # this is the original line
        author = message.author.nick
        userID = message.author.id
        print("author: {}".format(author))
        print("userID: {}".format(userID))
        content = 'Cli {}!'.format(author)
        if userID == '191213417099427840':
            # check if the story has reached its climax
            content = 'Climax!'
        await clibot.send_message(message.channel, content)

    elif message.content.startswith('.sneeze'):
        content = 'Bless Dustin!'
        await clibot.send_message(message.channel, content)

    elif (('praise the sun' in message.content.lower().translate(remove_punctuation))
          and message.author.name != 'cli-bot'):
        file = './praisethesun.jpg'
        await clibot.send_file(message.channel, file,
                               content='Praise the sun!')

    elif (('cheese pizza' in message.content.lower().translate(remove_punctuation))
          and message.author.name != 'cli-bot'):
        file = './immediately.png'
        await clibot.send_file(message.channel, file)


@bot.command(pass_context=True)
async def repeater(ctx, arg):
    """ Stop repeating me """
    await clibot.send_message(ctx.message.channel, arg)

clibot.run(CATHOLOCISM)
