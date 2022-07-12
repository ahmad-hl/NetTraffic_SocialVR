from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UploadDownload import measure_accurate_ul_dl
from webdriver_manager.chrome import ChromeDriverManager
from multiprocessing import Process
import platform
from PingServerProcess import tcping_subproc, netping, process_RTT_csv, network_RTT_csv
import atexit, os

def launchTab(link):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    #Make fake audio
    # chrome_options.add_argument('use-fake-device-for-media-stream')
    # chrome_options.add_argument('use-fake-ui-for-media-stream')
    chrome_options.add_experimental_option("detach", True)

    platform_os = platform.system().lower()
    try:
        if platform_os == 'windows':
            chromdriver_path = 'chromedriver.exe'
            driver = webdriver.Chrome(executable_path=chromdriver_path, options=chrome_options)
            # enter room
            button_sequence = ["Accept", "Enter Room"]  # "Join Room",
        else:
            #cash /home/symlab/.wdm/drivers/chromedriver/linux64/102.0.5005.61/chromedriver
            chromdriver_path = 'chromedriver'
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

    # while True:
    #     driver.execute_script("document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'w'}))")
    #     driver.execute_script("document.dispatchEvent(new KeyboardEvent('keyup', {'key': 'w'}))")
    #     driver.execute_script("document.dispatchEvent(new KeyboardEvent('keydown', {'key': 'q'}))")
    #     driver.execute_script("document.dispatchEvent(new KeyboardEvent('keyup', {'key': 'q'}))")


def save_RTT_to_csv(proc_log_path, net_log_path, procRTT_csv_path, netRTT_csv_path):
    # Compute net and process RTT to CSV
    process_RTT_csv(in_log_path=proc_log_path, out_csv_path=procRTT_csv_path)
    network_RTT_csv(in_log_path=net_log_path, out_csv_path=netRTT_csv_path)

if __name__ == '__main__':
    link = 'https://hub.metaust.link/eJ9JEUa/711-demo'
    dir_name = 'results_ux/synth15Oculus'
    concurrent_users = 16

    win_iface = "Wi-Fi"
    # ubuntu_iface = "wlp10s0"
    oculus = True
    # measure download upload
    uldl_process = Process(target=measure_accurate_ul_dl, args=(dir_name, concurrent_users, win_iface,oculus, ))
    uldl_process.start()

    #measure Process and Network RTT
    seconds = 15 * 60   # num pings = 10 minutes
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    # process Ping
    proc_log_path = '{}/procping_{}.txt'.format(dir_name,concurrent_users)
    procRTT_process = Process(target=tcping_subproc, args=(seconds, proc_log_path,))
    procRTT_process.start()

    # Network Ping
    net_log_path  = '{}/netping_{}.txt'.format(dir_name,concurrent_users)
    rtt_process = Process(target=netping, args=('{}'.format(seconds),  net_log_path, ))
    rtt_process.start()

    procRTT_csv_path = '{}/procRTT_{}.csv'.format(dir_name, concurrent_users)
    netRTT_csv_path = '{}/netRTT_{}.csv'.format(dir_name, concurrent_users)
    atexit.register(save_RTT_to_csv, proc_log_path=proc_log_path, net_log_path=net_log_path, procRTT_csv_path=procRTT_csv_path, netRTT_csv_path=netRTT_csv_path)

    #create processes = oculus tab
    oculus_proc = Process(target=launchTab, args=(link,))
    oculus_proc.start()

    # wait for the processes to complete
    oculus_proc.join()
    procRTT_process.join()
    rtt_process.join()
    uldl_process.terminate()



