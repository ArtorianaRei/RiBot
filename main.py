from twitchio.ext import commands
from async_google_trans_new import AsyncTranslator, constant
import deepl
import config
import os
import time
import sys
import signal
import glob
import re
from shutil import rmtree

url_suffix = config.GoogleTranslate_suffix
translator = AsyncTranslator(url_suffix=url_suffix)

## CONFIG FORMATTING
if config.Twitch_OAUTH.startswith('oauth:'):
    config.Twitch_OAUTH = config.Twitch_OAUTH[6:]
Lang_Ignore = [x.strip() for x in config.Lang_Ignore]
Ignore_Users = [x.strip() for x in config.Ignore_Users]
Ignore_Users = [str.lower() for str in Ignore_Users]
Ignore_Line = [x.strip() for x in config.Ignore_Line]
Delete_Words = [x.strip() for x in config.Delete_Words]

class Bot(commands.Bot):

    def __init__(self):                                                 ## TWITCH IRC CONNECTION
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

        if user in Ignore_Users:                                        ## IGNORE CONFIG SPECIFIED USERS
            return
        for w in Ignore_Line:                                           ## IGNORE WHOLE TEXT IF CONFIG SPECIFIED TEXT DETECTED
            if w in message:
                return
        for w in Delete_Words:                                          ## IGNORE CONFIG SPECIFIED WORDS / PHRASES
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

        message = re.sub(r'@\S+', '', message)                          ## REMOVES USERNAME / @USER
        message = " ".join( message.split() )                           ## JOINS MULTIPLE EMPTY STRINGS INTO ONE
        if not message:                                                 ## IGNORE IF MESSAGE IS BLANK
            return
        in_text = message                                               ## PARSE MESSAGE TO TRANSLATION

        ## GOOGLE_TRANS_NEW | LANGUAGE DETECTION & TRANSLATION
        if config.Translator == 'google':
            lang_detect = ''
            try:
                detected = await translator.detect(in_text)
                lang_detect = detected[0]
            except Exception as e:
                if config.Debug: print(e)

            lang_dest = config.Lang_Home.lower()
            if lang_detect == lang_dest:
                return
            if lang_detect in Lang_Ignore:
                return

            if config.Debug: print(f'###########################')
            if config.Debug: print(f'    LANGUAGE  DETECTION    ')
            if config.Debug: print(f'###########################')
            if config.Debug: print(f'SOURCE LANGUAGE  | {lang_detect.lower()}')
            if config.Debug: print(f"OUTPUT LANGUAGE  | {lang_dest.lower()}")
            m = in_text.split(':')
            if len(m) >= 2:
                if m[0] in config.TargetLangs:
                    lang_dest = m[0]
                    in_text = ':'.join(m[1:])
            if config.Debug: print(f"MESSAGE          | {in_text}")
            if config.Debug: print('USER             | {}'.format(user))
            if config.Debug: print(f'###########################')
            if config.Debug: print(f'        TRANSLATION        ')
            if config.Debug: print(f'###########################')
            
            translatedText = await translator.translate(in_text, lang_dest)
        
        ## DEEPL-TRANSLATE | LANGUAGE DETECTION & TRANSLATION
        if config.Translator == 'deepl':
            try:
                detected = await translator.detect(in_text)
                lang_detect = detected[0]
            except Exception as e:
                if config.Debug: print(e)

            lang_dest = config.Lang_Home.upper()
            if lang_detect in Lang_Ignore:
                return
            if lang_detect == lang_dest:
                return

            if config.Debug: print(f'###########################')
            if config.Debug: print(f'    LANGUAGE  DETECTION    ')
            if config.Debug: print(f'###########################')
            if config.Debug: print(f'SOURCE LANGUAGE  | {lang_detect.upper()}')
            if config.Debug: print(f"OUTPUT LANGUAGE  | {lang_dest.upper()}")
            m = in_text.split(':')
            if len(m) >= 2:
                if m[0] in config.TargetLangs:
                    lang_dest = m[0]
                    in_text = ':'.join(m[1:])
            if config.Debug: print(f"MESSAGE          | {in_text}")
            if config.Debug: print('USER             | {}'.format(user))
            if lang_detect == lang_dest:
                return
            if config.Debug: print(f'###########################')
            if config.Debug: print(f'        TRANSLATION        ')
            if config.Debug: print(f'###########################')
            
            translatedText = deepl.translate(source_language=config.Lang_Away.upper(), target_language=config.Lang_Home.upper(), text=in_text, formality_tone="informal")  
                  
        ## TRANSLATED OUT TEXT TO CHANNEL MESSAGE
        if config.Debug: print('ENGINE            | {}'.format(config.Translator))
        out_text = translatedText
        if config.Show_ByName:
            out_text = '{} [{}]'.format(out_text, user)
        print(out_text)
        if config.Debug: print(f'###########################')
        await msg.channel.send(out_text)

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
