"""
An EDMC Overlay Demo Plugin
"""
import os
import sys
import threading

import time

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
            if "!demo" in entry["Message"]:
                notify("Hello {}, You are in {}, Have a nice day!".format(cmdr, system))

    if cmdr:
        pass


if __name__ == "__main__":
    plugin_start()
