# RiBot
bot for https://www.twitch.tv/yuureiriri , one-way automatic translation / interpretation from jp to en.

## HOW TO USE:
1. Open and Edit "config.py"
2. INPUT the Twitch Channel you wish to connect to.       i.e: {Twitch_Channel  = 'Admiral_Nagi'}
3. INPUT the Bot Username you wish to use.                i.e: {Twitch_Nick     = 'NagiBot'}
4. INPUT the OAUTH Key for the Bot you wish to use.       i.e: {Twitch_OAUTH    = '6adshgakd324jduyriewrew543'}
5. Run main.py

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
Lang_Ignore             = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "zh-TW", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "jw", "ko", "kn", "kk", "km", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ps", "fa", "pl", "pt", "ma", "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]
Ignore_Users            = ['Streamelements', 'SoundAlerts']
Ignore_Line             = ['http', 'com', 'www']
Delete_Words            = [':']

Show_ByName             = True                                                  ## DISPLAY USERNAME WITH TRANSLATED TEXT
Debug                   = False                                                 ## DEBUG MODE
```
| Variable               | Description |
|------------------------|-------------|
| Twitch_Channel         | Targeted Twitch Channel |
| Twitch_Nick            | Username of Bot Twitch Account|
| Twitch_OAUTH           | OAUTH Token for twitch IRC, https://twitchtokengenerator.com/    OR    https://twitchapps.com/tmi/|
| DeepL_AUTH             | API Authentication key for DeepL, https://www.deepl.com/pro-api?cta=header-pro-api/ |
| Bot_Prefix             | Prefix for Bot commands, i.e. `"!"` or `"?"`|
| Bot_Color              | Bot username color: `Blue`, `Coral`, `DodgerBlue`, `SpringGreen`, `YellowGreen`, `Green`, `OrangeRed`, `Red`, `GoldenRod`, `HotPink`, `CadetBlue`, `SeaGreen`, `Chocolate`, `BlueViolet`, `Firebrick` |
| Translator             | set DeepL or Google as Translator, `deepl` or `google`|
| GoogleTranslate_Suffix | native suffix for local translate.google. : i.e. `com` or `co.jp`|
| Lang_Home              | Native / Home Language : i.e. `ja` = Japanese, `en` = English |
| Lang_Away              | Foreign / Away Language : i.e. `ja` = Japanese, `en` = English |
| Target_Langs           | set languages you wish to target : see language list bellow |
| Lang_Ignore            | set languages you wish to ignore : see language list bellow |
| Ignore_Users           | if any usernames set here are detected, the message will be ignored |
| Ignore_Line            | if any word set here is detected, the message will be ignored |
| Delete_Words           | set words you wish to remove from translated messages |
| Show_ByName            | enable display of username with trasnalted message |
| Debug                  | to enable Debug mode = `True`, standard operation = `False`|

### DEEPL SUPPORTED LANGUAGE LIST
| ISO-639-1 Code | Language |
|---|---|
| BG | Bulgarian |
| ZH | Chinese |
| CS | Czech |
| DA | Danish |
| NL | Dutch |
| EN-GB | English (British) |
| EN-US | English (American) |
| ET | Estonian |
| FI | Finnish |
| FR | French |
| DE | German |
| EL | Greek |
| HU | Hungarian |
| ID | Indonesian |
| IT | Italian |
| LV | Latvian |
| LT | Lithuanian |
| PL | Polish |
| PT-PT | Portuguese (Portugal) |
| PT-BR | Portuguese (Brazil) |
| RO | Romanian |
| RU | Russian |
| SK | Slovak |
| SL | Slovenian |
| ES | Spanish |
| SV | Swedish |
| TR | Turkish |

### GOOGLE SUPPORTED LANGUAGE LIST
| ISO-639-1 Code | Language |
|---|---|
| af | Afrikaans |
| sq | Albanian |
| am | Amharic |
| ar | Arabic |
| hy | Armenian |
| az | Azerbaijani |
| eu | Basque |
| be | Belarusian |
| bn | Bengali |
| bs | Bosnian |
| bg | Bulgarian |
| ca | Catalan |
| ceb | Cebuano |
| zh-CN | Chinese (Simplified) |
| zh-TW | Chinese (Traditional) |
| co | Corsican |
| hr | Croatian |
| cs | Czech |
| da | Danish |
| nl | Dutch |
| en | English |
| eo | Esperanto |
| et | Estonian |
| fi | Finnish |
| fr | French |
| fy | Frisian |
| gl | Galician |
| ka | Georgian |
| de | German |
| el | Greek |
| gu | Gujarati |
| ht | Haitian Creole |
| ha | Hausa |
| haw | Hawaiian |
| he or iw | Hebrew |
| hi | Hindi |
| hmn | Hmong |
| hu | Hungarian |
| is | Icelandic |
| ig | Igbo |
| id | Indonesian |
| ga | Irish |
| it | Italian |
| ja | Japanese |
| jv | Javanese |
| kn | Kannada |
| kk | Kazakh |
| km | Khmer |
| rw | Kinyarwanda |
| ko | Korean |
| ku | Kurdish |
| ky | Kyrgyz |
| lo | Lao |
| la | Latin |
| lv | Latvian |
| lt | Lithuanian |
| lb | Luxembourgish |
| mk | Macedonian |
| mg | Malagasy |
| ms | Malay |
| ml | Malayalam |
| mt | Maltese |
| mi | Maori |
| mr | Marathi |
| mn | Mongolian |
| my | Myanmar (Burmese) |
| ne | Nepali |
| no | Norwegian |
| ny | Nyanja (Chichewa) |
| or | Odia (Oriya) |
| ps | Pashto |
| fa | Persian |
| pl | Polish |
| pt | Portuguese (Portugal, Brazil) |
| pa | Punjabi |
| ro | Romanian |
| ru | Russian |
| sm | Samoan |
| gd | Scots Gaelic |
| sr | Serbian |
| st | Sesotho |
| sn | Shona |
| sd | Sindhi |
| si | Sinhala (Sinhalese) |
| sk | Slovak |
| sl | Slovenian |
| so | Somali |
| es | Spanish |
| su | Sundanese |
| sw | Swahili |
| sv | Swedish |
| tl | Tagalog (Filipino) |
| tg | Tajik |
| ta | Tamil |
| tt | Tatar |
| te | Telugu |
| th | Thai |
| tr | Turkish |
| tk | Turkmen |
| uk | Ukrainian |
| ur | Urdu |
| ug | Uyghur |
| uz | Uzbek |
| vi | Vietnamese |
| cy | Welsh |
| xh | Xhosa |
| yi | Yiddish |
| yo | Yoruba |
| zu | Zulu |

## SPECIAL THANKS:
* Sayonari: https://github.com/sayonari | https://github.com/sayonari/twitchTransFreeNext
* KaiKendoh : https://github.com/kaikendoh
* ptrstn : https://github.com/ptrstn | https://github.com/ptrstn/deepl-translate
