import pandas as pd
import matplotlib.pyplot as plt
import os, math
import seaborn as sns

in_dir_names = ['results/synth3','results/synth4','results/synth5','results/synth6']
dthub_dir_names = ['results_dthub/synth8','results_dthub/synth9','results_dthub/synth10']
conf_dir_names = ['results_conf/synth11','results_conf/synth12','results_conf/synth13']
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
    dthub_roomaccessDF =  roomaccessDF.assign(network='DT-Hub WiFi')
roomaccessDF = pd.DataFrame()
for conf_dir_name in conf_dir_names:
    for user_number in user_numbers:
        file_name = '../{}/avroom_load_time_{}.csv'.format(conf_dir_name, user_number)
        out_roomaccessDF = pd.read_csv(file_name, sep=',')
        roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)
    conf_roomaccessDF =  roomaccessDF.assign(network='Conference WiFi')

#concatenate dataframes
roomaccessDF = pd.concat([lab_roomaccessDF, conf_roomaccessDF, dthub_roomaccessDF], ignore_index=True)
roomaccessDF['enter_room_ms'] = roomaccessDF['enter_room_ms'] / 1000
roomaccessDF['avatar_sel_ms'] = roomaccessDF['avatar_sel_ms'] / 1000

sns.set_theme(style="whitegrid")
font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}

# Draw a nested barplot by species and sex
g = sns.catplot(
    data=roomaccessDF, kind="bar",
    x="network", y="enter_room_ms", hue="users_no",
    ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("Access Network", "Scene Loading Latency (sec)", fontsize=15, fontweight='bold')
g.legend.remove()
# g.legend.set_title("Concurrent Users")
plt.legend(loc='upper right', title='Concurrent Users')

parentDir = os.path.dirname(os.path.realpath(__file__))
Fig_PATH = os.path.join(parentDir, 'figures', 'network_load_latency.pdf')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()
