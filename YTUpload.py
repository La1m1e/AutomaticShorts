import time
import pyautogui
import pygetwindow as gw
from chatgpttags import *


def upload(title, text, comment):
    tag = tags(text, comment)
    chrome_window = gw.getWindowsWithTitle("Контент на канале - YouTube Studio - Google Chrome")
    chrome_window[0].activate()
    #///
    chrome_window[0].minimize()
