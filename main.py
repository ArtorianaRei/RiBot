from twitchio.ext import commands
from async_google_trans_new import google_translator
import deepl
import config
import os
import time
import sys
import signal
import glob
from shutil import rmtree
from dbd import *

url_suffix = config.GoogleTranslate_suffix
translator = google_translator(url_suffix=url_suffix)

## CONFIG FORMATTING
if config.Twitch_OAUTH.startswith('oauth:'):
    config.Twitch_OAUTH = config.Twitch_OAUTH[6:]
Lang_Ignore = [x.strip() for x in config.Lang_Ignore]
Ignore_Users = [x.strip() for x in config.Ignore_Users]
Ignore_Users = [str.lower() for str in Ignore_Users]
Ignore_Line = [x.strip() for x in config.Ignore_Line]
Delete_Words = [x.strip() for x in config.Delete_Words]

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token               = "oauth:" + config.Twitch_OAUTH,
            nick                = config.Twitch_Nick,
            prefix              = "!",
            initial_channels    = [config.Twitch_Channel]
        )

    async def event_ready(self):
        print(f"STATUS       | ONLINE")
        print('###########################')
        channel = self.get_channel(config.Twitch_Channel)
        await channel.send(f"/color {config.Bot_Color}")
        await channel.send(f"/me  is now online! TehePelo")

    ## MESSAGE PROCESSING
    async def event_message(self, msg):
        if msg.echo:
            return
        if not msg.echo:
            await self.handle_commands(msg)
        if msg.content.startswith('!'):
            return

        message = msg.content
        user    = msg.author.name.lower()

        if user in Ignore_Users:
            return
        for w in Ignore_Line:
            if w in message:
                return
        for w in Delete_Words:
            message = message.replace(w, '')

        ## EMOTE PROCESSING & REMOVAL
        emote_list = []
        if msg.tags:
            if msg.tags['emotes']:
                emotes_s = msg.tags['emotes'].split('/')
                for emo in emotes_s:
                    e_id, e_pos = emo.split(':')
                    if ',' in e_pos:
                        ed_pos = e_pos.split(',')
                        for e in ed_pos:
                            e_s, e_e = e.split('-')
                            emote_list.append(msg.content[int(e_s):int(e_e)+1])
                    else:
                        e = e_pos
                        e_s, e_e = e.split('-')
                        emote_list.append(msg.content[int(e_s):int(e_e)+1])
                for w in sorted(emote_list, key=len, reverse=True):
                    message = message.replace(w, '')

        message = " ".join( message.split() )
        in_text = message

        ## LANGUAGE DETECTION
        if config.Debug: print(f'    LANGUAGE  DETECTION    ')
        if config.Debug: print(f'###########################')
        lang_detect = ''

        ## GOOGLE_TRANS_NEW | LANGUAGE DETECTION & TRANSLATION
        if config.Translator == 'google':
            try:
                detected = await translator.detect(in_text)
                lang_detect = detected[0]
            except Exception as e:
                if config.Debug: print(e)
            if config.Debug: print(f'SOURCE LANGUAGE  | {lang_detect.lower()}')
            lang_dest = config.Lang_Home.lower() if lang_detect != config.Lang_Home.lower() else config.Lang_Away.lower()
            if config.Debug: print(f"OUTPUT LANGUAGE  | {lang_dest.lower()}")
            m = in_text.split(':')
            if len(m) >= 2:
                if m[0] in config.TargetLangs:
                    lang_dest = m[0]
                    in_text = ':'.join(m[1:])
            else:
                if lang_detect in Lang_Ignore:
                    return
            if config.Debug: print(f"MESSAGE          | {in_text}")
            if config.Debug: print('USER             | {}'.format(user))
            if lang_detect == lang_dest:
                return
            if config.Debug: print(f'###########################')
            if config.Debug: print(f'        TRANSLATION        ')
            if config.Debug: print(f'###########################')
            
            if not in_text:
                return
            else:
                translatedText = await translator.translate(in_text, lang_dest)
        
        ## DEEPL-TRANSLATE | LANGUAGE DETECTION & TRANSLATION
        if config.Translator == 'deepl':
            try:
                detected = await translator.detect(in_text)
                lang_detect = detected[0]
            except Exception as e:
                if config.Debug: print(e)
            if config.Debug: print(f'SOURCE LANGUAGE  | {lang_detect.upper()}')
            lang_dest = config.Lang_Home.upper() if lang_detect != config.Lang_Home.upper() else config.Lang_Away.upper()
            if config.Debug: print(f"OUTPUT LANGUAGE  | {lang_dest.upper()}")
            m = in_text.split(':')
            if len(m) >= 2:
                if m[0] in config.TargetLangs:
                    lang_dest = m[0]
                    in_text = ':'.join(m[1:])
            else:
                if lang_detect in Lang_Ignore:
                    return
            if config.Debug: print(f"MESSAGE          | {in_text}")
            if config.Debug: print('USER             | {}'.format(user))
            if lang_detect == lang_dest:
                return
            if config.Debug: print(f'###########################')
            if config.Debug: print(f'        TRANSLATION        ')
            if config.Debug: print(f'###########################')
            
            if not in_text:
                return
            else:
                translatedText = deepl.translate(source_language=config.Lang_Away.upper(), target_language=config.Lang_Home.upper(), text=in_text, formality_tone="informal")  
                  
        ## TRANSLATED OUT TEXT
        if config.Debug: print('ENGINE            | {}'.format(config.Translator))
        out_text = translatedText
        if config.Show_ByName:
            out_text = '{} [{}]'.format(out_text, user)
        print(out_text)
        if config.Debug: print(f'###########################')
        await msg.channel.send(out_text)

        # shrine command
    @commands.command()
    async def shrine(self, ctx: commands.Context):
        sos_list, remaining = shrine_scrape()
        await ctx.send(f"The current perks in the Shrine of Secrets are: {sos_list}. The Shrine will refresh in {remaining}.")

    # killers command
    @commands.command()
    async def killers(self, ctx: commands.Context):
        killer = killer_scrape()
        print(len(killer))
        await ctx.send(f'The current killers are: {killer}.')

    # survivors command
    @commands.command()
    async def survivors(self, ctx: commands.Context):
        survivor = survivor_scrape()
        print(len(survivor))
        await ctx.send(f'The current survivors are: {survivor}.')
    
    # perkhelp command
    @commands.command()
    async def perkhelp(self, ctx: commands.Context):
        await ctx.send(perkhelp)

    # statushelp
    @commands.command()
    async def statushelp(self, ctx: commands.Context):
        await ctx.send(statushelp)

    # perk command
    # @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def perk(self, ctx:commands.Context, *, perk):
        if perk.lower() == 'help':
            await ctx.send(perkhelp)
        else:
            # take perk from chat message and run through perk_scrape function
            try:
                perk_name, perk_desc = perk_scrape(perk.lower())
                perk_full = perk_name + ' - ' + perk_desc

                # if description is below twitch's character limit, send it to twitch chat
                if len(perk_full) <= 500:
                    await ctx.send(perk_full)

                # If greater than twitch's char limit, split it up
                else:
                    # Check how many messages will need to be sent
                    sets = round(len(perk_full)/500 + 0.5)

                    # Split up the description by the last space in each 500 characters
                    for i in range(sets):
                        if i == 0:
                            s_index = perk_desc[:491 - len(perk_name)].rfind(' ')
                            await ctx.send(perk_name + ' (' + str(i + 1) + '/' + str(sets) + ') - ' + perk_desc[:s_index])
                            i += 1
                            perk_desc = perk_desc[s_index + 1:]
                        elif i == sets - 1:
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + perk_desc)
                        else:
                            s_index = perk_desc[:494].rfind(' ')
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + perk_desc[:s_index])
                            i += 1
                            perk_desc = perk_desc[s_index + 1:]
            
            except AttributeError:
                await ctx.send('No perk found!')


    # status command
    # @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command()
    async def status(self, ctx:commands.Context, *, status):
        if status.lower() == 'help':
            await ctx.send(statushelp)
        else:
            try:
                status_name, status_desc = status_scrape(status.lower())
                status_full = status_name + ' - ' + status_desc

                # if description is below twitch's character limit, send it to twitch chat
                if len(status_full) <= 500:
                    await ctx.send(status_full)

                # If greater than twitch's char limit, split it up
                else:
                    # Check how many messages will need to be sent
                    sets = round(len(status_full)/500 + 0.5)

                    # Split up the description by the last space in each 500 characters
                    for i in range(sets):
                        if i == 0:
                            s_index = status_desc[:491 - len(status_name)].rfind(' ')
                            await ctx.send(status_name + ' (' + str(i + 1) + '/' + str(sets) + ') - ' + status_desc[:s_index])
                            i += 1
                            status_desc = status_desc[s_index + 1:]
                        elif i == sets - 1:
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + status_desc)
                        else:
                            s_index = status_desc[:494].rfind(' ')
                            await ctx.send('(' + str(i + 1) + '/' + str(sets) + ') - ' + status_desc[:s_index])
                            i += 1
                            status_desc = status_desc[s_index + 1:]
            except AttributeError:
                await ctx.send('No status found!')

bot = Bot()

## CLEANUP
def cleanup():
    print("!!!CLEANING!!!")
    time.sleep(1)
    print("!!!CLEAN FINISHED!!!")

## SIG HANDLER 
def sig_handler(signum, frame) -> None:
    sys.exit(1)

## _MEI cleaner https://stackoverflow.com/questions/57261199/python-handling-the-meipass-folder-in-temporary-folder
def CLEANMEIFOLDERS():
    try:
        base_path = sys._MEIPASS 
    except Exception:
        base_path = os.path.abspath(".")
    if config.Debug: print(f'_MEI base path: {base_path}')
    base_path = base_path.split("\\")
    base_path.pop(-1)
    temp_path = ""
    for item in base_path:
        temp_path = temp_path + item + "\\"
    mei_folders = [f for f in glob.glob(temp_path + "**/", recursive=False)]
    for item in mei_folders:
        if item.find('_MEI') != -1 and item != sys._MEIPASS + "\\":
            rmtree(item)

## MAIN
def main():
    signal.signal(signal.SIGTERM, sig_handler)

    try:
        CLEANMEIFOLDERS()
        if config.Debug: print('###########################')
        if config.Debug: print('         CONNECTION        ')
        print('###########################')
        print('CHANNEL      | {}'.format(config.Twitch_Channel))
        print('USERNAME     | {}'.format(config.Twitch_Nick))
        print('ENGINE       | {}'.format(config.Translator))
        bot.run()
        print(f'###########################')

    except Exception as e:
        if config.Debug: print(e)
        input()

    finally:
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        cleanup()
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    sys.exit(main())
