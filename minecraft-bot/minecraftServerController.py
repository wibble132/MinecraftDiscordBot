import os
import subprocess
import time

import IOThreads

# Use a full path
MINECRAFT_FOLDER_DIR = "C:\\Users\\Dan\\Documents\\Programming\\Python\\DiscordBot\\Minecraft Server Files"
# MINECRAFT_FOLDER_DIR = "C:\\Users\\Dan\\Documents\\Programming\\Python\\SubprocessIOStreamTest\\Server Copy\\2"
MINECRAFT_SERVER_NAME = "minecraft_server.1.19.2.jar"
MINECRAFT_START_MEMORY_MB = 1024
MINECRAFT_MAX_MEMORY_MB = 4096

RUN_COMMAND = [
    "java",
    f"-Xmx{MINECRAFT_MAX_MEMORY_MB}M",
    f"-Xms{MINECRAFT_START_MEMORY_MB}M",
    "-jar", MINECRAFT_SERVER_NAME,
    "--nogui",
]
os.chdir(MINECRAFT_FOLDER_DIR)

# noinspection PyRedeclaration
# RUN_COMMAND = "python C:\\Users\\Dan\\Documents\\Programming\\Python\\DiscordBot\\basicRepeater.py"


class MinecraftServerController:
    def __init__(self) -> None:
        self.inputThread = IOThreads.IOThread(IOThreads.inputThreadFunction)
        self.outputThread = IOThreads.IOThread(IOThreads.outputThreadFunction)
        self.errorThread = IOThreads.IOThread(IOThreads.errorThreadFunction)

        self.minecraft_process: subprocess.Popen | None = None

    def isRunning(self) -> bool:
        return self.minecraft_process is not None and self.minecraft_process.poll() is None

    def startServer(self) -> bool:
        if self.isRunning():
            return False

        print("Starting Server")
        self.minecraft_process = subprocess.Popen(
            RUN_COMMAND,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.inputThread.startThread(self.minecraft_process)
        self.outputThread.startThread(self.minecraft_process)
        self.errorThread.startThread(self.minecraft_process)

    def stopServer(self):
        if self.isRunning():
            if not self.inputThread.active:
                self.inputThread.startThread(self.minecraft_process)
            self.inputThread.queue.put("stop")

        while self.minecraft_process.poll() is None:
            time.sleep(0.5)

        self.inputThread.stopThread()
        self.outputThread.stopThread()
        self.errorThread.stopThread()

        return self.minecraft_process.poll()

