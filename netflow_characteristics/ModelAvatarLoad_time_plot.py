import pandas as pd
import matplotlib.pyplot as plt
import os, math
import seaborn as sns
import numpy as np

in_dir_names = ['wifi_data/lab/synth3','wifi_data/lab/synth4','wifi_data/lab/synth5','wifi_data/lab/synth6']
user_numbers = [2,4,8,16]

avatar_dict = {}
avatar_mean_dict = {}
avatar_ci_dict = {}

load_dict = {}
load_mean_dict = {}
load_ci_dict = {}

roomaccessDF = pd.DataFrame()
#Data Collection & Aggregation
for user_number in user_numbers:
    for in_dir_name in in_dir_names:
        file_name = '../{}/avroom_load_time_{}.csv'.format(in_dir_name, user_number)
        out_roomaccessDF = pd.read_csv(file_name, sep=',')
        roomaccessDF = pd.concat([out_roomaccessDF, roomaccessDF], ignore_index=True)

roomJoinDF = roomaccessDF[['users_no','enter_room_ms']]
roomJoinDF =  roomJoinDF.assign(type='join')
avatarSelDF = roomaccessDF[['users_no','avatar_sel_ms']]
avatarSelDF =  avatarSelDF.assign(type='avatar')
print(roomJoinDF.head())
print(roomJoinDF.columns)
newLoadDF = pd.DataFrame(np.concatenate([roomJoinDF.values, avatarSelDF.values]), columns=roomJoinDF.columns)
newLoadDF['enter_room_ms'] = newLoadDF['enter_room_ms'] / 1000


# Plot figure
ind = []
for key in user_numbers:
    ind.append('{}'.format(key))
print(ind)
width = 0.4  # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots(1) #, figsize=(10,7)
plt.margins(0.01, 0)

sns.set_theme(style="whitegrid")
font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}

# Draw a nested barplot by species and sex
g = sns.catplot(
    data=newLoadDF, kind="bar",
    x="users_no", y="enter_room_ms", hue="type",
    ci=95, palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("Concurrent Users", "Loading Latency (sec)", fontsize=15, fontweight='bold')
g.legend.remove()
# g.legend(labels=['Download Model', 'Download Avatar'])
# g.legend.set_title("Concurrent Users")
L= plt.legend(loc='upper left', title='', fontsize=14)
L.get_texts()[0].set_text('Download Model')
L.get_texts()[1].set_text('Download Avatar')
plt.xticks(fontsize=16, rotation=0)
plt.yticks(fontsize=16, rotation=20)

parentDir = os.path.dirname(os.path.realpath(__file__))
Fig_PATH = os.path.join(parentDir, 'figures', 'load_latency.pdf')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()
