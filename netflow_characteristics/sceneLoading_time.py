import pandas as pd
import matplotlib.pyplot as plt
import os, math
import seaborn as sns

in_dir_names = ['wifi_data/lab/synth3','wifi_data/lab/synth4','wifi_data/lab/synth5','wifi_data/lab/synth6']
dthub_dir_names = ['wifi_data/office/synth8','wifi_data/office/synth9','wifi_data/office/synth10']
conf_dir_names = ['wifi_data/classroom/synth11','wifi_data/classroom/synth12','wifi_data/classroom/synth13']
user_numbers = [2,4,8,16]

avatar_dict = {}
avatar_mean_dict = {}
avatar_ci_dict = {}

load_dict = {}
load_mean_dict = {}
load_ci_dict = {}

roomaccessDF = pd.DataFrame()
#Data Collection & Aggregation

for in_dir_name in in_dir_names:
    for user_number in user_numbers:
        file_name = '../{}/avroom_load_time_{}.csv'.format(in_dir_name, user_number)
        out_roomaccessDF = pd.read_csv(file_name, sep=',')
        roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)
    lab_roomaccessDF =  roomaccessDF.assign(network='Lab WiFi')
roomaccessDF = pd.DataFrame()
for dthub_dir_name in dthub_dir_names:
    for user_number in user_numbers:
        try:
            file_name = '../{}/avroom_load_time_{}.csv'.format(dthub_dir_name, user_number)
            out_roomaccessDF = pd.read_csv(file_name, sep=',')
            roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)
        except FileNotFoundError as err:
            print(err)
            pass
    dthub_roomaccessDF =  roomaccessDF.assign(network='Office WiFi')
roomaccessDF = pd.DataFrame()
for conf_dir_name in conf_dir_names:
    for user_number in user_numbers:
        file_name = '../{}/avroom_load_time_{}.csv'.format(conf_dir_name, user_number)
        out_roomaccessDF = pd.read_csv(file_name, sep=',')
        roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)
    conf_roomaccessDF =  roomaccessDF.assign(network='Classroom WiFi')

#concatenate dataframes
roomaccessDF = pd.concat([lab_roomaccessDF, conf_roomaccessDF, dthub_roomaccessDF], ignore_index=True)
roomaccessDF['enter_room_ms'] = roomaccessDF['enter_room_ms'] / 1000
roomaccessDF['avatar_sel_ms'] = roomaccessDF['avatar_sel_ms'] / 1000

sns.set_theme(style="whitegrid")
font_dict = {'fontsize': 15,
 'fontweight' : 'bold'}

fig, axes = plt.subplots( )
# Draw a nested barplot by species and sex
g = sns.catplot(
    data=roomaccessDF, kind="bar",
    x="network", y="enter_room_ms", hue="users_no",
    ci="sd", palette="dark", alpha=.6, height=4, aspect=1.5
)
g.despine(left=True)
g.set_axis_labels("Access Network", "Scene Loading Latency (sec)", fontsize=16, fontweight='bold')
# g.set_yticklabels(g.get_yticks(), size = 15)
# get label text
yticks, ylabels = plt.yticks()
xticks, xlabels = plt.xticks()
g.set_xticklabels(xlabels, size=15)
g.set_yticklabels(ylabels, size=15)
g.set(ylim=(0, 360))
g.legend.remove()

# g.legend.set_title("Concurrent Users")
plt.legend(loc='upper right', title='Concurrent Users', fontsize=16)

parentDir = os.path.dirname(os.path.realpath(__file__))
Fig_PATH = os.path.join(parentDir, 'figures', 'network_load_latency.pdf')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()
