from pandas import json_normalize
import requests, json, os


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
            scene_load_time = 0
            avatar_selected_time = 0
            try:
                clientDF = loadTimeDF.loc[loadTimeDF.client_id == client_id]
                link_access_ts = clientDF.loc[clientDF.event_id == 'link_access']['server_timestamp'].values[0]
                joined_room_ts = clientDF.loc[clientDF.event_id == 'joined_room']['server_timestamp'].values[0]
                scene_load_time = joined_room_ts - link_access_ts
                avatar_selected_time = scene_load_time
                avatar_selected_ts = clientDF.loc[clientDF.event_id == 'avatar_selected']['server_timestamp'].values[0]
                avatar_selected_time = avatar_selected_ts - link_access_ts
                print("Latency: avatar selected {} sec, joining room {} sec".format(avatar_selected_time / 1000,
                                                                                    scene_load_time / 1000))
                out_csv.write("{}, {},{},{}\n".format(client_id, scene_load_time, avatar_selected_time, tabs))
            except:
                out_csv.write("{}, {},{},{}\n".format(client_id, scene_load_time, avatar_selected_time, tabs))
                pass



if __name__ == '__main__':
    dir_name = 'results_conf/synth13'
    isExist = os.path.exists(dir_name)
    if not isExist:
        os.mkdir(dir_name)
    downloadJSON_to_csv(2, 'Hd92wfL', dir_name)