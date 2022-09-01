import sys

print("Hello the process basicRepeater.py is starting")

while True:
    text = input()
    print("Wow you sent", text)

    if text[0] == "2":
        print("that started with a 2")
    if text[0] == "3":
        print("This is on stderr", file=sys.stderr)
    if text[0] == "4":
        raise IOError
    if text == "stop":
        break

print("Stopping! :0")