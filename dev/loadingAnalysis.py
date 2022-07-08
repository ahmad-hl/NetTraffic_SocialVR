import pandas as pd


user_numbers = [2,4,8,16] #synth:[2,4,6,20]
dir_name = 'synth2'
for user_number in user_numbers:
    file_name = '../{}/room_access_{}.csv'.format(dir_name, user_number)
    df = pd.read_csv(file_name, sep =',')
    df = df.sort_values(by=['client_id','server_timestamp','event_id'])
    df = df[['client_id','event_id','client_timestamp','server_timestamp']]
    client_ids = df['client_id'].unique()
    print("{} clients: {} \n ********* \n".format(len(client_ids), client_ids))

    out_file_name = r'../{}/avroom_load_time_{}.csv'.format(dir_name, user_number)

    with open(out_file_name, "w") as out_csv:
        out_csv.write("enter_room_ms,avatar_sel_ms,users_no\n")
    with open(out_file_name, "+a") as out_csv:
        for client_id in client_ids:
            try:
                clientDF = df.loc[df.client_id == client_id]
                link_access_ts = clientDF.loc[clientDF.event_id == 'link_access']['server_timestamp'].values[0]
                avatar_selected_ts = clientDF.loc[clientDF.event_id == 'avatar_selected']['server_timestamp'].values[0]
                joined_room_ts = clientDF.loc[clientDF.event_id == 'joined_room']['server_timestamp'].values[0]
                print("client accessed at {}, joined at {}".format(link_access_ts,joined_room_ts ))
                avatar_selected_time = avatar_selected_ts - link_access_ts
                scene_load_time =  joined_room_ts - link_access_ts
                print("Latency: avatar selected {} sec, joining room {} sec".format(avatar_selected_time/1000, scene_load_time/1000))
                out_csv.write("{},{},{}\n".format(scene_load_time,avatar_selected_time , user_number))
            except:
                pass


    df2 = pd.read_csv(out_file_name, sep =',')
    print(df2.head())