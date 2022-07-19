from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UploadDownload import measure_accurate_ul_dl
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
import platform, requests, json
from createRoom import createRoomBy
import atexit, os
from pandas import json_normalize
from threading import Event
from clearCash import clear_cache

running_drivers = []

def launchTabs(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #Make fake audio
    chrome_options.add_argument('use-fake-device-for-media-stream')
    chrome_options.add_argument('use-fake-ui-for-media-stream')
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    button_sequence = ["Accept", "Enter Room"]  # "Join Room",
    driver.get(link)
    running_drivers.append(driver)


    for button_text in button_sequence:
        success = False
        while not success:
            WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
            buttons_list = driver.find_elements(By.TAG_NAME, "button")

            for button in buttons_list:
                try:
                    if button.text == button_text:
                        button.click()
                        print(button_text + " is clicked")
                        success = True
                        break
                except common.exceptions.StaleElementReferenceException as ex:
                    print("Detected loading issue: {}".format(ex.stacktrace))
                    break

    # walk around
    WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.CLASS_NAME, "a-canvas")))
    print("Entered room")

    while True:
        driver.execute_script("document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'w'}))")
        driver.execute_script("document.dispatchEvent(new KeyboardEvent('keyup', {'key': 'w'}))")
        driver.execute_script("document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'q'}))")
        driver.execute_script("document.dispatchEvent(new KeyboardEvent('keyup', {'key': 'q'}))")


def clear_driversCash():
    for driver in running_drivers:
        clear_cache(driver)
    print("Cash of drivers is clear...")

if __name__ == '__main__':
    tabs = 4
    room_uri = 'https://hub.metaust.link/eJ9JEUa/711-demo'

    #download json file on exit
    dir_name = 'results_platforms/uldl'
    isExist = os.path.exists(dir_name)
    if not isExist:
        os.mkdir(dir_name)
    atexit.register(clear_driversCash)

    #create #processes = tabs
    processes = []
    for _ in range(tabs):
        p = Process(target=launchTabs, args=(room_uri,))
        p.start()
        processes.append(p)
        Event().wait(50)


    # wait for the processes to complete
    for p in processes:
        p.join()


