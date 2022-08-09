from ast import Delete
from twitchio.ext import commands
from async_google_trans_new import AsyncTranslator, constant
import re
import deepl
import signal
import config
from shutil import rmtree                                                    

url_suffix = config.GoogleTranslate_suffix                              ## LOAD CONFIG SPECIFIED URL SUFFIX FOR GOOGLE TRASNALTE            || i.e. 'com'           or          'co.jp'
translator = AsyncTranslator(url_suffix=url_suffix)                     ## LOAD CONFIG SPECIFIED SUFFIX INTO TRANSLATOR

## CONFIG FORMATTING
Lang_Ignore = [x.strip() for x in config.Lang_Ignore]                   ## LOAD CONFIG SPECIFIED INGORE LANGUAGE LIST                       || IGNORE WHOLE TEXT IF CONFID SPECIFIED LANGUAGE DETECTED
Ignore_Users = [x.strip() for x in config.Ignore_Users]                 ## LOAD CONFIG SPECIFIED INGORE USERS LIST                          || IGNORE WHOLE TEXT IF CONFIG SPECIFIED USER DETECTED
Ignore_Users = [str.lower() for str in Ignore_Users]                    ## FORMAT CONFIG SPECIFIED INGORE USERS LIST TO LOWERCASE
Ignore_Line = [x.strip() for x in config.Ignore_Line]                   ## LOAD CONFIG SPECIFIED INGORE LINE LIST                           || IGNORE WHOLE TEXT IF CONFIG SPECIFED LINE DETECTED
Delete_Words = [x.strip() for x in config.Delete_Words]                 ## LOAD CONFIG SPECIFIED INGORE WORDS LIST                          || IGNORE ONLY CONFIG SPECIFIED WORD
Delete_Words = [str.lower() for str in Delete_Words]                    ## FORMAT CONFIG SPECIFIED INGORE WORDS LIST TO LOWERCASE

class Bot(commands.Bot):

    def __init__(self):                                                 ## TWITCH IRC CONNECTION
        super().__init__(
            token               = config.Twitch_OAUTH,                  ## LOAD OAUTH TOKEN FOR AUTHENTICATION AND CONNECTION, FROM CONFIG SPECIFIED TOKEN
            prefix              = "!",                                  ## DEFINE BOT PREFIX                                                || i.e. "!"
            initial_channels    = [config.Twitch_Channel]               ## LOAD CHANNEL FROM CONFIG SPECIFIED CHANNEL INTO INITIAL CHANNELS VARIABLE
        )

    async def event_ready(self):
        print(f"STATUS       | ONLINE")
        print('###########################')
        channel = self.get_channel(config.Twitch_Channel)               ## LOAD CHANNEL FROM CONFIG SPECIFIED CHANNEL INTO CHANNEL VARIABLE
        await channel.send(f"/color {config.Bot_Color}")                ## SET CONFIG SPECIFIED USERNAME COLOR
        await channel.send(f"/me  is now online! TehePelo")             ## CONNECTION ANNOUNCEMENT TO CHANNEL

    ## MESSAGE PROCESSING
    async def event_message(self, msg):
        if msg.echo:
            return
        if not msg.echo:
            await self.handle_commands(msg)
        if msg.content.startswith('!'):
            return

        message = msg.content.lower()                                   ## LOAD MESSAGE CONTENT INTO VARIABLE AS LOWERCASE
        user    = msg.author.name                                       ## LOAD MESSAGE USER INTO VARIABLE

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
        in_text = message                                               ## PARSE MESSAGE TO TRANSLATION AS IN_TEXT

        ## GOOGLE_TRANS_NEW | LANGUAGE DETECTION & TRANSLATION
        if config.Translator == 'google':
            lang_detect = ''
            try:
                detected = await translator.detect(in_text)             ## AWAIT FOR LANGUAGE DETECTION
                lang_detect = detected[0]                               ## LOAD DETECTED LANGUAGE
            except Exception as e:
                if config.Debug: print(e)

            lang_dest = config.Lang_Home.lower()                        ## LOAD DESTINATION LANGUAGE FROM CONFIG SPECIFIED HOME LANGUAGE, ALSO FORMAT TO LOWERCASE
            if lang_detect == lang_dest:                                ## IGNORE IF DETECTED LANGUAGE = DESTINATION / HOME LANGUAGE
                return
            if lang_detect in Lang_Ignore:                              ## IGNORE IF DETECTED LANGUAGE IN CONFIG SPECIFIED LANGUAGE IGNORE LIST
                return

            if config.Debug: print(f'    LANGUAGE  DETECTION    ')
            if config.Debug: print(f'###########################')
            if config.Debug: print(f'SOURCE LANGUAGE  | {lang_detect.lower()}')                 ## FORMAT DETECTED LANGUAGE SHORTHAND TO LOWERCASE
            if config.Debug: print(f"OUTPUT LANGUAGE  | {lang_dest.lower()}")                   ## FORMAT DESTINATION LANGUAGE SHORTHAND TO LOWERCASE
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
            lang_detect = ''
            try:
                detected = await translator.detect(in_text)             ## AWAIT FOR LANGUAGE DETECTION
                lang_detect = detected[0]                               ## LOAD DETECTED LANGUAGE
            except Exception as e:
                if config.Debug: print(e)

            lang_dest = config.Lang_Home.upper()                        ## LOAD DESTINATION LANGUAGE FROM CONFIG SPECIFIED HOME LANGUAGE, ALSO FORMAT TO UPPERCASE
            if lang_detect in Lang_Ignore:                              ## IGNORE IF DETECTED LANGUAGE IN CONFIG SPECIFIED LANGUAGE IGNORE LIST
                return
            if lang_detect == lang_dest:                                ## IGNORE IF DETECTED LANGUAGE = DESTINATION / HOME LANGUAGE
                return

            if config.Debug: print(f'    LANGUAGE  DETECTION    ')
            if config.Debug: print(f'###########################')
            if config.Debug: print(f"SOURCE LANGUAGE  | {lang_detect.upper()}")                 ## FORMAT DETECTED LANGUAGE SHORTHAND TO UPPERCASE
            if config.Debug: print(f"OUTPUT LANGUAGE  | {lang_dest.upper()}")                   ## FORMAT DESTINATION LANGUAGE SHORTHAND TO UPPERCASE
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
            
            translatedText = deepl.translate(source_language=config.Lang_Away.upper(), target_language=config.Lang_Home.upper(), text=in_text, formality_tone="informal")  
                  
        ## TRANSLATIED OUT TEXT TO CHANNEL
        if config.Debug: print('ENGINE           | {}'.format(config.Translator))
        out_text = translatedText

        if out_text.lower() == in_text.lower():                         ## IGNORE IF OUT_TEXT MATCHES IN_TEXT
            if config.Debug: print(f'STATUS           | IGNORED')
            return

        if config.Show_ByName:
            out_text = '{} [{}]'.format(out_text, user)
        print(out_text)
        if config.Debug: print(f'###########################')
        await msg.channel.send(out_text)

## MAIN
def main():
    try:
        if config.Debug: print('###########################')
        if config.Debug: print('         CONNECTION        ')
        print('###########################')
        print('CHANNEL      | {}'.format(config.Twitch_Channel))
        print('USERNAME     | {}'.format(config.Bot_Username))
        print('ENGINE       | {}'.format(config.Translator))

        bot = Bot()
        bot.run()
        print(f'###########################')

    except Exception as e:
        if config.Debug: print(e)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    (main())
