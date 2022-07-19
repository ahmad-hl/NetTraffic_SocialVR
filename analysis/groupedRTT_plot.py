import pandas as pd
import matplotlib.pyplot as plt
import os, math
import seaborn as sns

in_dir_names = ['results/synth2Oculus','results/synth3Oculus','results/synth4Oculus','results/synth5Oculus','results/synth6Oculus']
dthub_dir_names = ['results_dthub/synth8Oculus','results_dthub/synth9Oculus','results_dthub/synth10Oculus']
conf_dir_names = ['results_conf/synth11Oculus','results_conf/synth12Oculus','results_conf/synth13Oculus']
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
        try:
            file_name = '../{}/netRTT_{}.csv'.format(in_dir_name, user_number)
            out_roomaccessDF = pd.read_csv(file_name, sep=',')
            out_roomaccessDF.columns = ['rtt']
            out_roomaccessDF = out_roomaccessDF.assign(users_no=user_number)
            roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)
        except FileNotFoundError as err:
            print(err)
            pass
    lab_roomaccessDF =  roomaccessDF.assign(network='Lab WiFi')
roomaccessDF = pd.DataFrame()
for dthub_dir_name in dthub_dir_names:
    for user_number in user_numbers:
        try:
            file_name = '../{}/netRTT_{}.csv'.format(dthub_dir_name, user_number)
            out_roomaccessDF = pd.read_csv(file_name, sep=',')
            out_roomaccessDF.columns = ['rtt']
            out_roomaccessDF = out_roomaccessDF.assign(users_no=user_number)
            roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)
        except FileNotFoundError as err:
            print(err)
            pass
    dthub_roomaccessDF =  roomaccessDF.assign(network='Office WiFi')
roomaccessDF = pd.DataFrame()
for conf_dir_name in conf_dir_names:
    for user_number in user_numbers:
        try:
            file_name = '../{}/netRTT_{}.csv'.format(conf_dir_name, user_number)
            out_roomaccessDF = pd.read_csv(file_name, sep=',')
            out_roomaccessDF.columns = ['rtt']
            out_roomaccessDF = out_roomaccessDF.assign(users_no=user_number)
            roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)
        except FileNotFoundError as err:
            print(err)
            pass
    conf_roomaccessDF =  roomaccessDF.assign(network='Classroom WiFi')

#concatenate dataframes
roomaccessDF = pd.concat([lab_roomaccessDF, conf_roomaccessDF, dthub_roomaccessDF], ignore_index=True)
roomaccessDF = roomaccessDF.loc[roomaccessDF['rtt'] != 'timed']
roomaccessDF['rtt'] = pd.to_numeric(roomaccessDF['rtt'])


print(roomaccessDF.loc[roomaccessDF.users_no==2].describe())
roomaccessDF['rtt'] = roomaccessDF['rtt'] / 1000

sns.set_theme(style="whitegrid")
font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}

fig, axes = plt.subplots( )
sns.set(font_scale = 1.2)
# Draw a nested barplot by species and sex
g = sns.catplot(
    data=roomaccessDF, kind="bar",
    x="network", y="rtt", hue="users_no",
    ci="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("Access Network", "Round-trip Latency (sec)", fontsize=15, fontweight='bold')
g.legend.remove()

# g.legend.set_title("Concurrent Users")
plt.legend(loc='upper right', title='Concurrent Users', fontsize=16)

parentDir = os.path.dirname(os.path.realpath(__file__))
Fig_PATH = os.path.join(parentDir, 'figures', 'network_netRTT.pdf')
# plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()
