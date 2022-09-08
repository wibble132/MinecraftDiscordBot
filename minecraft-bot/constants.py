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
            '    "MaxMemoryMB": 2048\n'
            '  },\n'
            '  "BotSettings": {\n'
            '    "Token": "TOKEN",'
            '    "GuildID": 0'
            '  }'
            '}'
        ))
    raise Exception("config.json does not exist. A template has been created, fill it out")


with open(configFile) as file:
    _rawdata = json.load(file)

print(_rawdata)

MINECRAFT_SETTINGS = _rawdata['MinecraftSettings']
MINECRAFT_FOLDER_DIR = MINECRAFT_SETTINGS['FolderLocation']
MINECRAFT_SERVER_NAME = MINECRAFT_SETTINGS['Filename']
MINECRAFT_START_MEMORY_MB = MINECRAFT_SETTINGS['StartMemoryMB']
MINECRAFT_MAX_MEMORY_MB = MINECRAFT_SETTINGS['MaxMemoryMB']

if MINECRAFT_FOLDER_DIR == "" or MINECRAFT_SERVER_NAME == "":
    raise ValueError("Folder or server name have not been set in config.json")

BOT_SETTINGS = _rawdata['BotSettings']
TOKEN = BOT_SETTINGS['Token']
GUILD_ID = BOT_SETTINGS['GuildID']

if TOKEN == "TOKEN" or GUILD_ID == 0:
    raise ValueError("Token or guild id have not been set in config.json")

print(GUILD_ID)
