import queue
import subprocess
import threading
import time
from typing import Callable, Any


class IOThread:
    def __init__(self, io_function: Callable[[subprocess.Popen, queue.Queue[str]], Any]):
        self.io_function = io_function
        self.queue: queue.Queue[str] = queue.Queue()
        self.active: bool = False
        self.process: subprocess.Popen | None = None
        self.thread: threading.Thread | None = None

    def startThread(self, process: subprocess.Popen):
        if self.active:
            return

        self.active = True
        self.process = process
        self.thread = threading.Thread(target=self.threadFunction, daemon=True)
        self.thread.start()

    def stopThread(self):
        self.active = False

    def threadFunction(self):
        print(f"Starting IO thread {self.process}")
        while self.active and self.process is not None:
            self.io_function(self.process, self.queue)
            time.sleep(0.1)
        self.active = False
        print("IO Thread stopped")


def inputThreadFunction(process: subprocess.Popen, que: queue.Queue):
    if not que.empty():
        process.stdin.write((que.get() + "\r\n").encode())
        process.stdin.flush()


def outputThreadFunction(process: subprocess.Popen, que: queue.Queue[str]):
    line = process.stdout.readline()
    print(f"Output thread: {line}")
    que.put(str(line))


def errorThreadFunction(process: subprocess.Popen, que: queue.Queue[str]):
    line = process.stderr.readline()
    print(f"Error thread: {line}")
    que.put(str(line))
