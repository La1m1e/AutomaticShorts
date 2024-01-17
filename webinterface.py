import os
import time

import pyautogui
from seleniumwire.undetected_chromedriver.v2 import Chrome, ChromeOptions


def openchrome():
    options = {}
    script_directory = os.path.dirname(os.path.abspath(__file__))
    user_data_dir = os.path.join(script_directory, 'user_data')

    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
    width = 1280
    height = 720

    chrome_options = ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    chrome_options.add_argument('--ignore-certificate-errors')
    driver = Chrome(seleniumwire_options=options, options=chrome_options, use_subprocess=True, AcceptInsecureCerts=True)
    time.sleep(0.01)
    driver.maximize_window()
    time.sleep(1)
    driver.set_window_size(width, height)
    driver.set_window_position(0, 0)

    driver.get('https://studio.youtube.com/')
    time.sleep(2)
    pyautogui.click(x=124, y=543)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass