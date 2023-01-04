import json
from os.path import exists

configFile = "config.json"

if not exists(configFile):
    with open(configFile, 'w') as file:
        file.write((
            '{\n'
            '  "MinecraftSettings": {\n'
            '    "FolderLocation": "",\n'
            '    "Filename": "",\n'
            '    "StartMemoryMB": 1024,\n'
            '    "MaxMemoryMB": 1024,\n'
            '    "ExtraJavaOptions": ""\n'
            '  },\n'
            '  "BotSettings": {\n'
            '    "Token": "TOKEN",\n'
            '    "GuildID": 0,\n'
            '    "AllowGetIpAddressCommand": false\n'
            '  }\n'
            '}\n'
        ))
    raise Exception("config.json does not exist. A template has been created, fill it out")

with open(configFile) as file:
    _rawdata = json.load(file)

MINECRAFT_SETTINGS: dict[str, any] = _rawdata.get('MinecraftSettings', {})
MINECRAFT_FOLDER_DIR: str = MINECRAFT_SETTINGS.get('FolderLocation', '')
MINECRAFT_SERVER_NAME: str = MINECRAFT_SETTINGS.get('Filename', '')
MINECRAFT_START_MEMORY_MB: int = MINECRAFT_SETTINGS.get('StartMemoryMB', 1024)
MINECRAFT_MAX_MEMORY_MB: int = MINECRAFT_SETTINGS.get('MaxMemoryMB', 1024)
MINECRAFT_EXTRA_OPTIONS: str = MINECRAFT_SETTINGS.get('ExtraJavaOptions', "")

if MINECRAFT_FOLDER_DIR == "" or MINECRAFT_SERVER_NAME == "":
    raise ValueError("Folder or server name have not been set in config.json")

BOT_SETTINGS: dict[str, any] = _rawdata.get('BotSettings', {})
TOKEN: str = BOT_SETTINGS.get('Token', "TOKEN")
GUILD_ID: int = BOT_SETTINGS.get('GuildID', 0)
ALLOW_GET_IP: bool = BOT_SETTINGS.get('AllowGetIpAddressCommand', False)

if TOKEN == "TOKEN" or GUILD_ID == 0:
    raise ValueError("Token or guild id have not been set in config.json")
