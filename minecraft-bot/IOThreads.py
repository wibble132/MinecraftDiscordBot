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
        print(f"Starting IO thread {self.__hash__()}, {self.io_function.__name__}")
        while self.active and self.process is not None:
            if not self.io_function(self.process, self.queue):
                break
            time.sleep(0.1)
        self.active = False
        print(f"stopped IO Thread {self.__hash__()}, {self.io_function.__name__}")


def inputThreadFunction(process: subprocess.Popen, que: queue.Queue):
    if not que.empty():
        process.stdin.write((que.get() + "\r\n").encode())
        process.stdin.flush()
    return True


def outputThreadFunction(process: subprocess.Popen, que: queue.Queue[str]):
    line = process.stdout.readline()
    if line == b'':
        return False
    print(f"Output thread: {line}")
    que.put(str(line))
    return True


def errorThreadFunction(process: subprocess.Popen, que: queue.Queue[str]):
    line = process.stderr.readline()
    if line == b'':
        return False
    print(f"Error thread: {line}")
    que.put(str(line))
    return True
