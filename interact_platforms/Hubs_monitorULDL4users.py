from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from MeasureULDL import measure_accurate_ul_dl
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
import os
from clearCash import clear_cache


running_drivers = []

def launchTab(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #Make fake audio
    chrome_options.add_argument('use-fake-device-for-media-stream')
    chrome_options.add_argument('use-fake-ui-for-media-stream')
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        # enter room
    button_sequence = ["Join Room", "Accept", "Enter Room"]
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
                except common.exceptions.StaleElementReferenceException:
                    print("Detected loading issue")
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
    link = 'https://hub.metaust.link/eJ9JEUa/711-demo'
    dir_name = '../results_platforms/uldl'
    file_name = 'hubs.uldl'
    concurrent_users = 4
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    win_iface = "Wi-Fi"
    # ubuntu_iface = "wlp10s0"
    # measure download upload
    uldl_process = Process(target=measure_accurate_ul_dl, args=(dir_name, file_name, concurrent_users, win_iface, ))
    uldl_process.start()

    #create processes = oculus tab
    hubsTab_proc = Process(target=launchTab, args=(link,))
    hubsTab_proc.start()

    # wait for the processes to complete
    hubsTab_proc.join()
    uldl_process.terminate()



