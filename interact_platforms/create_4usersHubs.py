from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Spatial_ULDL import measure_accurate_ul_dl
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
import platform
from PingServerProcess import process_RTT_csv, network_RTT_csv
import os

def launchTab(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #Make fake audio
    chrome_options.add_argument('use-fake-device-for-media-stream')
    chrome_options.add_argument('use-fake-ui-for-media-stream')
    chrome_options.add_experimental_option("detach", True)

    platform_os = platform.system().lower()
    try:
        if platform_os == 'windows':
            chromdriver_path = '../chromedriver.exe'
            driver = webdriver.Chrome(executable_path=chromdriver_path, options=chrome_options)
            # enter room
            button_sequence = ["Accept", "Enter Room"]  # "Join Room",
        else:
            #cash /home/symlab/.wdm/drivers/chromedriver/linux64/102.0.5005.61/chromedriver
            chromdriver_path = '../chromedriver'
            driver = webdriver.Chrome(executable_path=chromdriver_path, options=chrome_options)
            # enter room
            button_sequence = ["Accept", "Enter Room"]
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get(link)



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


def save_RTT_to_csv(proc_log_path, net_log_path, procRTT_csv_path, netRTT_csv_path):
    # Compute net and process RTT to CSV
    process_RTT_csv(in_log_path=proc_log_path, out_csv_path=procRTT_csv_path)
    network_RTT_csv(in_log_path=net_log_path, out_csv_path=netRTT_csv_path)

if __name__ == '__main__':
    link = 'https://hub.metaust.link/eJ9JEUa/711-demo'
    dir_name = '../results_vr_platforms/uldl'
    file_name = 'hubs.uldl'  #
    concurrent_users = 4
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # win_iface = "Wi-Fi"
    ubuntu_iface = "wlp10s0"
    # measure download upload
    uldl_process = Process(target=measure_accurate_ul_dl, args=(dir_name, file_name, concurrent_users, ubuntu_iface, ))
    uldl_process.start()

    #create processes = oculus tab
    hubsTab_proc = Process(target=launchTab, args=(link,))
    hubsTab_proc.start()

    # wait for the processes to complete
    hubsTab_proc.join()
    uldl_process.terminate()



