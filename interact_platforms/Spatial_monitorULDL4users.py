from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from MeasureULDL import measure_accurate_ul_dl
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
from selenium.webdriver.common.keys import Keys
import os
from selenium.webdriver.common.action_chains import ActionChains
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
        ActionChains(driver).key_down('w').perform()
        ActionChains(driver).key_down('q').perform()
        ActionChains(driver).key_down('q').perform()


def clear_driversCash():
    for driver in running_drivers:
        clear_cache(driver)
    print("Cash of drivers is clear...")

if __name__ == '__main__':
    # link = 'https://spatial.io/rooms/6226a6d81d7048000115b255?share=7771562277452031497'
    link = 'https://spatial.io/s/names-Lo-Fi-Meetup-62d665622eeb4a0001f588dc?share=2513047764259295594'
    dir_name = '../results_platforms/uldl'
    file_name = 'spatial.uldl'
    concurrent_users = 2

    win_iface = "Wi-Fi"
    # ubuntu_iface = "wlp10s0"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    # measure download upload
    uldl_process = Process(target=measure_accurate_ul_dl, args=(dir_name,file_name, concurrent_users, win_iface, ))
    uldl_process.start()

    #create processes = oculus tab
    spatialTab_proc = Process(target=launchTab, args=(link,))
    spatialTab_proc.start()

    # wait for the processes to complete
    spatialTab_proc.join()



