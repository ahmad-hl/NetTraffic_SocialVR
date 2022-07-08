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
            button_sequence = ["Accept", "Enter Room"] #"Join Room",
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

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


def downloadJSON_to_csv(tabs, room_id, out_dir_name):
    # Request the json for this web page:
    get_json_uri = "https://l374gxgvxj.execute-api.us-east-1.amazonaws.com/prod?room_id="
    response = requests.get(get_json_uri + room_id)
    with open("{}/{}_{}.json".format(out_dir_name, tabs, room_id), "w") as f:
        f.write(response.text)

    data = json.loads(response.text)
    data_body = data['body']
    print('\n ***** ***** ***** \n'+data_body)
    data = json.loads(data_body)
    # Use json_normalize() to convert JSON to DataFrame
    loadTimeDF = json_normalize(data['data']['Items'])
    loadTimeDF.to_csv(r'{}/room_access_{}.csv'.format(out_dir_name, tabs), encoding='utf-8', mode='w', index=False, header=True)

    #Compute load time
    loadTimeDF = loadTimeDF.sort_values(by=['client_id', 'server_timestamp', 'event_id'])
    loadTimeDF = loadTimeDF[['client_id', 'event_id', 'client_timestamp', 'server_timestamp']]
    client_ids = loadTimeDF['client_id'].unique()
    print("{} clients: {} \n ********* \n".format(len(client_ids), client_ids))

    #Save load times to csv file
    out_file_name = r'{}/avroom_load_time_{}.csv'.format(dir_name, tabs)
    with open(out_file_name, "w") as out_csv:
        out_csv.write("enter_room_ms,avatar_sel_ms,users_no\n")
    with open(out_file_name, "+a") as out_csv:
        for client_id in client_ids:
            try:
                clientDF = loadTimeDF.loc[loadTimeDF.client_id == client_id]
                link_access_ts = clientDF.loc[clientDF.event_id == 'link_access']['server_timestamp'].values[0]
                avatar_selected_ts = clientDF.loc[clientDF.event_id == 'avatar_selected']['server_timestamp'].values[0]
                joined_room_ts = clientDF.loc[clientDF.event_id == 'joined_room']['server_timestamp'].values[0]
                avatar_selected_time = avatar_selected_ts - link_access_ts
                scene_load_time = joined_room_ts - link_access_ts
                print("Latency: avatar selected {} sec, joining room {} sec".format(avatar_selected_time / 1000,
                                                                                    scene_load_time / 1000))
                out_csv.write("{},{},{}\n".format(scene_load_time, avatar_selected_time, tabs))
            except Exception as ex:
                print('Error: '.format(ex))
                pass

def clear_driversCash():
    for driver in running_drivers:
        clear_cache(driver)
    print("Cash of drivers is clear...")

if __name__ == '__main__':
    tabs = 8
    create_room_uri = 'https://hub.metaust.link/scenes/pKqPdPU'
    new_room_uri = createRoomBy(create_room_uri)
    new_room_uri_comps = new_room_uri.split("//")[1].split("/")
    room_id = new_room_uri_comps[1]
    print("Room url {}, Room ID: {}".format(new_room_uri_comps, room_id))

    #Wait 1 minute to room uri
    Event().wait(90)

    #download json file on exit
    dir_name = 'results/synth6'
    isExist = os.path.exists(dir_name)
    if not isExist:
        os.mkdir(dir_name)
    atexit.register(downloadJSON_to_csv, tabs=tabs*2, room_id=room_id, out_dir_name=dir_name)
    atexit.register(clear_driversCash)

    #create #processes = tabs
    processes = []
    for _ in range(tabs):
        p = Process(target=launchTabs, args=(new_room_uri,))
        p.start()
        processes.append(p)

    # win_iface = "Wi-Fi"
    ubuntu_iface = "wlp10s0"
    # measure_accurate_ul_dl(tabs, interface = ubuntu_iface)
    uldl_process = Process(target=measure_accurate_ul_dl, args=(dir_name, tabs*2, ubuntu_iface,))
    uldl_process.start()

    #Wait 2 minutes
    minutes = 8
    Event().wait(60* minutes)

    print("\n**************** TERMINATE ************************")
    print("\n**************** TERMINATE ************************")
    print("\n**************** TERMINATE ************************")

    # wait for the processes to complete
    for p in processes:
        p.join()
    uldl_process.terminate()

