import json, os
from pandas import json_normalize
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

dir_name = '../results_dthub/synth10/'
out_dir_name = '../results_dthub/synth10Oculus/'
out_file_name = r'{}avroom_OculusLoad_time.csv'.format(out_dir_name)
fileExt = r".json"
file_names =  [_ for _ in os.listdir(dir_name) if _.endswith(fileExt)]

def downloadJSON_to_csv():

    with open(out_file_name, "w") as out_csv:
        out_csv.write("enter_room_ms,avatar_sel_ms,users_no\n")

    # Opening JSON file
    for file_name in file_names:
        json_file_path = '{}{}'.format(dir_name,file_name)
        infile = open(json_file_path)
        data = json.load(infile)
        print(json_file_path)
        data_body = data['body']
        print('\n ***** ***** ***** \n'+data_body)
        data = json.loads(data_body)

        # Use json_normalize() to convert JSON to DataFrame
        loadTimeDF = json_normalize(data['data']['Items'])
        loadTimeDF = loadTimeDF.sort_values(by=['client_id', 'server_timestamp', 'event_id'])
        loadTimeDF = loadTimeDF[['client_id', 'event_id', 'client_timestamp', 'server_timestamp']]
        loadTimeDF = loadTimeDF[loadTimeDF['client_id'].apply(lambda x: x.startswith('Windows'))]
        client_ids = loadTimeDF['client_id'].unique()
        print("{} clients: {} \n ********* \n".format(len(client_ids), client_ids))

        try:
            tabs_number = int(file_name[0:2])
        except:
            tabs_number = int(file_name[0:1])
        # Compute load time & save to csv file
        with open(out_file_name, '+a') as out_csv:
            for client_id in client_ids:
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
                    out_csv.write("{},{},{}\n".format(scene_load_time, avatar_selected_time, tabs_number))
                except:
                    pass

if __name__ == '__main__':
    downloadJSON_to_csv()
    roomaccessDF = pd.read_csv(out_file_name, sep=',')
    sns.set_theme(style="whitegrid")
    # ax = sns.barplot(x="users_no", y="enter_room_ms", data=roomaccessDF)
    ax2 = sns.barplot(x="users_no", y="avatar_sel_ms", data=roomaccessDF)
    plt.show()

