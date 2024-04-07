# me - this DAT
#
# frame - the current frame
# state - True if the timeline is paused
#
# Make sure the corresponding toggle is enabled in the Execute DAT.

import platform
import sys

def onStart():
    if platform.system() == 'Windows':
        mypath = ["src", "venv\Lib\site-packages"]
    elif platform.system() == 'Darwin':
        mypath = ["src", ".venv/lib/python3.11/site-packages"]

    if mypath not in sys.path:
        sys.path = mypath + sys.path

    print(f"Python path is now:")
    for p in sys.path:
        print(p)
        
    return

def onCreate():
    return


def onExit():
    return


def onFrameStart(frame):
    return


def onFrameEnd(frame):
    return


def onPlayStateChange(state):
    return


def onDeviceChange():
    return


def onProjectPreSave():
    return


def onProjectPostSave():
    return

