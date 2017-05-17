"""
An EDMC Overlay Demo Plugin
"""
import os
import random
import sys
import threading

import time

import math

_thisdir = os.path.abspath(os.path.dirname(__file__))
_overlay_dir = os.path.join(os.path.dirname(_thisdir), "EDMCOverlay")
if _overlay_dir not in sys.path:
    sys.path.append(_overlay_dir)

import edmcoverlay
_overlay = None


def plugin_start():
    """
    Start up our EDMC Plugin
    :return:
    """
    global _overlay
    _overlay = edmcoverlay.Overlay()
    time.sleep(2)
    notify("EDMC Overlay Demo Plugin Loaded")


def notify(text):
    _overlay.send_message("demo1",
                          text,
                          "green",
                          30, 100, ttl=3)


def journal_entry(cmdr, system, station, entry, state):
    """
    Make sure the service is up and running
    :param cmdr:
    :param system:
    :param station:
    :param entry:
    :param state:
    :return:
    """
    if "event" in entry:
        if entry["event"] == "SendText":
            global END
            if "!demo" in entry["Message"]:
                notify("Hello {}, You are in {}, Have a nice day!".format(cmdr, system))
                END = False
                start_demo_thread()
            if "!stop" in entry["Message"]:
                END = True

    if cmdr:
        pass


DEMO = None
END = False


def start_demo_thread():
    """
    Start a thread that runs the demo
    :return:
    """
    global DEMO
    DEMO = threading.Thread(target=demo_script)
    DEMO.setDaemon(True)
    DEMO.start()


def demo_script():
    """
    A retro style demo
    :return:
    """

    class XY(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    SCREENW = 1360
    SCREENH = 990
    class Actor(object):
        def __init__(self, id, text, x, y, size="large", color="green", ttl=3):
            self.pos = XY(x, y)
            self.vel = XY(0, 0)
            self.acc = XY(0, 0)
            self.id = id
            self.text = text
            self.color = color
            self.size = size
            self.ttl = 3

        def update(self):

            self.pos.x += self.vel.x
            self.pos.y += self.vel.y

            self.vel.x += self.acc.x
            self.vel.y += self.acc.y

            self.pos.x %= SCREENW
            self.pos.y %= SCREENH
            _overlay.send_message(self.id,
                                  self.text,
                                  self.color,
                                  int(self.pos.x) - 15, int(self.pos.y) - 15, ttl=int(self.ttl), size=self.size)

    scroller = Actor("scroller", "Hello 1984!", 0, 340, color="red")
    scroller.vel.x = 2

    sinewave = []
    for letter in "This is Elite:Dangerous":
        ch = Actor("sine" + str(len(sinewave)), letter,
                   len(sinewave) * 15,
                   0,
                   size="large", color="yellow")
        ch.vel.x = 8
        sinewave.append(ch)

    wandering = []
    for letter in "EDMC!":
        ch = Actor("wander" + str(len(wandering)), letter,
                   len(wandering) * 30,
                   -10,
                   size="normal", color="green")
        wandering.append(ch)

    ch = Actor("wander" + str(len(wandering)), "EDMCOverlay",
               random.randint(100, 400),
               -20,
               size="large", color="red")
    wandering.append(ch)

    while not END:
        time.sleep(1.0/30)  # 30 fps

        scroller.update()

        for letter in sinewave:
            letter.pos.y = 350 + int(math.sin((letter.pos.x * 7) / float(SCREENW)) * 300.0)
            letter.update()

        for letter in wandering:
            letter.acc.y = random.randint(-10, 10) / 10.0
            letter.acc.x = random.randint(-10, 10) / 10.0
            letter.update()

if __name__ == "__main__":
    plugin_start()
    start_demo_thread()
    while not END:
        time.sleep(1)
    DEMO.join()

