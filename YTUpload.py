import time
import os
from time import sleep

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Start the Selenium WebDriver (keeps running)
def fix_del(self):
    try:
        self.service.process.kill()
    except:  # noqa
        pass
    pass  # This is the modification
    self.quit()

def start_browser():
    uc.Chrome.__del__ = fix_del
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={os.path.dirname(os.path.abspath(__file__))}/chrome_data")
    options.add_argument(r'--profile-directory=chrome_data')
    driver = uc.Chrome(options=options)
    driver.set_window_size(800,600)
    driver.get("https://studio.youtube.com")
    sleep(1)
    return driver

# Function to upload a single video
def upload_video(driver, video_title, video_description, video_tags):
    print(f"📤 Uploading: {video_title}")

    # Go to YouTube Studio
    driver.get("https://studio.youtube.com")
    time.sleep(3)


    upload_button = driver.find_element(By.XPATH, '//*[@id="create-icon"]/ytcp-button-shape/button')
    upload_button.click()
    time.sleep(1)
    upload_button = driver.find_element(By.XPATH, '//*[@id="text-item-0"]')
    upload_button.click()
    time.sleep(1)



    file_input = driver.find_element(By.XPATH, '//*[@id="content"]/input')
    abs_path = os.path.abspath(f'{os.path.dirname(os.path.abspath(__file__))}/temp/result.mp4')
    file_input.send_keys(abs_path)
    time.sleep(7)  # Wait for the upload process
    input_ = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
    input_.clear()
    time.sleep(1)
    input_.send_keys(video_title)
    time.sleep(1)

    input_ = driver.find_element(By.XPATH,'/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
    input_.clear()
    time.sleep(1)
    input_.send_keys(video_description)
    time.sleep(1)

    button = driver.find_element(By.XPATH, '//*[@id="audience"]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')
    button.click()
    time.sleep(0.6)
    button = driver.find_element(By.XPATH,'//*[@id="toggle-button"]/ytcp-button-shape/button')
    button.click()
    time.sleep(1)
    button = driver.find_element(By.XPATH, '//*[@id="details"]/div/ytcp-video-metadata-editor-advanced/div[2]/ytkp-altered-content-select/div[2]/div[2]')
    button.click()
    time.sleep(0.6)

    input_ = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input')
    input_.clear()
    input_.send_keys(video_tags)
    time.sleep(1)

    next_ = driver.find_element(By.XPATH, '//*[@id="next-button"]/ytcp-button-shape')
    next_.click()
    sleep(0.6)
    next_ = driver.find_element(By.XPATH, '//*[@id="next-button"]/ytcp-button-shape')
    next_.click()
    sleep(0.6)
    next_ = driver.find_element(By.XPATH, '//*[@id="next-button"]/ytcp-button-shape')
    next_.click()
    sleep(0.6)

    button = driver.find_element(By.XPATH, '//*[@id="privacy-radios"]/tp-yt-paper-radio-button[3]')
    button.click()
    sleep(0.6)
    button = driver.find_element(By.XPATH, '//*[@id="done-button"]')
    button.click()

    print(f"✅ {video_title} uploaded successfully!")

#driver = start_browser()
#input()
#upload_video(driver, "temp/result.mp4")
#input()