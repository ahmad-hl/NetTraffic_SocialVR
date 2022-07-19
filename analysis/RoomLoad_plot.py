import pandas as pd
import matplotlib.pyplot as plt
import os, math

in_dir_names = ['results/synth3','results/synth4','results/synth5','results/synth6']
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

#Statistics
for user_number in user_numbers:
    temp_roomaccessDF = roomaccessDF.loc[roomaccessDF.users_no == user_number]
    # Room Joined
    stats_load = temp_roomaccessDF['enter_room_ms'].agg(['mean', 'count', 'std'])
    m, c, s = stats_load.values
    stats_load['ci95'] = 1.96 * s / math.sqrt(c)
    load_dict[user_number] = {m, stats_load['ci95']}
    load_mean_dict[user_number] = m / 1000  # ms to sec
    load_ci_dict[user_number] = stats_load['ci95'] / 1000  # ms to sec

    # AVatar Selected
    stats_avatar_select = temp_roomaccessDF['avatar_sel_ms'].agg(['mean', 'count', 'std'])
    av_m, av_c, av_s = stats_avatar_select.values
    stats_avatar_select['ci95'] = 1.96 * av_s / math.sqrt(av_c)
    avatar_dict[user_number] = {av_m, stats_avatar_select['ci95']}
    avatar_mean_dict[user_number] = av_m / 1000  # ms to sec
    avatar_ci_dict[user_number] = stats_avatar_select['ci95'] / 1000  # ms to sec


avatarMeans = tuple(avatar_mean_dict.values())
avatarCIs = tuple(avatar_ci_dict.values())

loadMeans = tuple(load_mean_dict.values())
loadCIs = tuple(load_ci_dict.values())
print([avatarMeans, avatarCIs])

# Plot figure
ind = []
for key in load_ci_dict.keys():
    ind.append('{}'.format(key))
print(ind)
width = 0.4  # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots(1) #, figsize=(10,7)
plt.margins(0.01, 0)
# color='skyblue': indianred, dodgerblue, turquoise, mediumseagreen, lightgreen
p1 = ax.bar(ind, avatarMeans, width, yerr=avatarCIs, color='dodgerblue', log=False,
            capsize=3, error_kw=dict(elinewidth=1, ecolor='blue'), label='Avatar Download')
p2 = ax.bar(ind, loadMeans, width, yerr=loadCIs, color='skyblue', log=False,
            capsize=3, error_kw=dict(elinewidth=1, ecolor='black'), label='Model Download')
plt.margins(0.01, 0)

# Optional code - Make plot look nicer
i = 0.01
for load, av in zip(loadMeans,avatarMeans):
    ax.text(i, load, "{0:.1f}".format(load), color='black', fontsize=16)
    ax.text(i, av+15, "{0:.1f}".format(av), color='gray', fontsize=16)
    i = i + 1

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.xticks(fontsize=15, rotation=0)
plt.yticks(fontsize=15, rotation=20)

ax.set_ylabel('Loading Latency (sec)', fontsize=14, labelpad=-1)
plt.legend(loc='upper left', fontsize=13, title="Latency", fancybox=True)
parentDir = os.path.dirname(os.path.realpath(__file__))
Fig_PATH = os.path.join(parentDir, 'figures', 'load_latency.pdf')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()
