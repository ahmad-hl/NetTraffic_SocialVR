import time
from threading import Event
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import platform
import requests
from clearCash import clear_cache

def createRoomBy(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #Make fake audio
    chrome_options.add_argument('use-fake-device-for-media-stream')
    chrome_options.add_argument('use-fake-ui-for-media-stream')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("detach", True)

    platform_os = platform.system().lower()
    try:
        if platform_os == 'windows':
            chromdriver_path = 'chromedriver.exe'
            driver = webdriver.Chrome(executable_path=chromdriver_path, options=chrome_options)
        else:
            chromdriver_path = 'chromedriver'
            driver = webdriver.Chrome(executable_path=chromdriver_path, options=chrome_options)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get(link)

    button_sequence = ["Create a room with this scene"]  # "Join Room", "Accept", "Enter Room"
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
                except common.exceptions.StaleElementReferenceException:
                    print("Detected loading issue")
                    break


    print("Room is created...")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "a-canvas")))
    Event().wait(10.0)

    driver.switch_to.window(driver.window_handles[-1])
    current_url = driver.current_url
    # Closes the current window
    driver.close()

    # All windows related to driver instance will quit
    # driver.quit()

    return current_url

if __name__ == '__main__':
    create_room_uri = 'https://hub.metaust.link/scenes/pKqPdPU'
    new_room_uri = createRoomBy(create_room_uri)
    new_room_uri_comps = new_room_uri.split("//")[1].split("/")
    room_id = new_room_uri_comps[1]
    print("Room url {}, Room ID: {}".format(new_room_uri_comps, room_id))

    # Request the HTML for this web page:
    response = requests.get("https://l374gxgvxj.execute-api.us-east-1.amazonaws.com/prod?room_id="+room_id)
    out_dir_name = 'test'
    tabs = 1
    with open("{}/{}_{}.json".format(out_dir_name, tabs, room_id), "w") as f:
        f.write(response.text)



