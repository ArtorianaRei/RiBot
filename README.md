# RiBot
bot for https://www.twitch.tv/yuureiriri , one-way automatic translation / interpretation from jp to en.

## HOW TO USE:
1. Open and Edit "config.py"
2. INPUT the Twitch Channel you wish to connect to.       i.e: {Twitch_Channel  = 'Admiral_Nagi'}
3. INPUT the Bot Username you wish to use.                i.e: {Twitch_Nick     = 'NagiBot'}
4. INPUT the OAUTH Key for the Bot you wish to use.       i.e: {Twitch_OAUTH    = '6adshgakd324jduyriewrew543'}
5. Run main.py OR RiBot.exe

## CONFIG.PY
```python
Twitch_Channel          = 'INPUT TWITCH CHANNEL'
Twitch_Nick             = 'INPUT BOT USERNAME'
Twitch_OAUTH            = 'INPUT OAUTH KEY'                                   ## https://twitchtokengenerator.com/
DeepL_AUTH              = ''
Bot_Prefix              = "!!"                                                ## i.e. "!" or "?"
Bot_Color               = 'DodgerBlue' 
## Alternate Colors      |  'Blue', 'Coral', 'DodgerBlue', 'SpringGreen', 'YellowGreen', 'Green', 'OrangeRed', 'Red', 'GoldenRod', 'HotPink', 'CadetBlue', 'SeaGreen', 'Chocolate', 'BlueViolet', 'Firebrick'

Translator              = 'deepl'
## Translator            | 'google' or 'deepl'

GoogleTranslate_suffix  = 'com'
Lang_Home               = 'en'
Lang_Away               = 'ja'
TargetLangs             = ['ja']
ReadOnlyTheseLang       = ['ja']
Lang_Ignore             = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "zh-TW", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "jw", "ko", "kn", "kk", "km", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ps", "fa", "pl", "pt", "ma", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]
Ignore_Users            = ['Streamelements', 'SoundAlerts']
Ignore_Line             = ['http', 'com', 'www']
Delete_Words            = [':']

Show_ByName             = True                                                  ## DISPLAY USERNAME WITH TRANSLATED TEXT
Debug                   = False                                                 ## DEBUG MODE
```

## SPECIAL THANKS:
* Sayonari: https://github.com/sayonari | https://github.com/sayonari/twitchTransFreeNext
* KaiKendoh : https://github.com/kaikendoh
* ptrstn : https://github.com/ptrstn | https://github.com/ptrstn/deepl-translate
