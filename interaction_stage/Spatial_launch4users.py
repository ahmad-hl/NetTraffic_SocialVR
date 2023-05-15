from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from utils.clearCash import clear_cache
import atexit
from threading import Event

running_drivers = []
def launchTab(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #Make fake audio
    chrome_options.add_argument('use-fake-device-for-media-stream')
    chrome_options.add_argument('use-fake-ui-for-media-stream')
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(link)
    running_drivers.append(driver)

    success = False
    while not success:
        WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.NAME, "name")))
        inputElement = driver.find_element_by_name("name")
        inputElement.send_keys('ahmad')
        inputElement.send_keys(Keys.ENTER)
        try:
            inputElement.submit()
            print("{} is entered".format('ahmad'))
            success = True
            break
        except common.exceptions.StaleElementReferenceException:
            print("Detected loading issue")
            break

    # walk around
    # WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Leave")))
    while True:
        ActionChains(driver).key_down(Keys.ARROW_RIGHT).perform()
        ActionChains(driver).key_down(Keys.ARROW_UP).perform()

def clear_driversCash():
    for driver in running_drivers:
        clear_cache(driver)
    print("Cash of drivers is clear...")

if __name__ == '__main__':
    room_uri = 'https://spatial.io/rooms/6226a6d81d7048000115b255?share=7771562277452031497'
    concurrent_users = 4

    #clear driver on exit
    atexit.register(clear_driversCash)

    #create #processes = tabs
    processes = []
    for _ in range(concurrent_users):
        Event().wait(50)
        p = Process(target=launchTab, args=(room_uri,))
        p.start()
        processes.append(p)

    # wait for the processes to complete
    for p in processes:
        p.join()



