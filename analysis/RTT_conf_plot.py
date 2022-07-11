import pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, math

user_numbers = [2, 4, 8, 16]
in_dir_names = ['results_conf/synth11Oculus', 'results_conf/synth12Oculus', 'results_conf/synth13Oculus']

avatar_dict = {}
avatar_mean_dict = {}
avatar_ci_dict = {}

rtt_dict = {}
rtt_mean_dict = {}
rtt_ci_dict = {}

proc_rtt_dict = {}
proc_rtt_mean_dict = {}
proc_rtt_ci_dict = {}

for user_number in user_numbers:
    netRTTDF = pd.DataFrame(columns=['rtt_ms'])
    procRTTDF = pd.DataFrame(columns=['rtt_ms'])
    for in_dir_name in in_dir_names:
        #Network Round-trip time
        file_name = '../{}/netRTT_{}.csv'.format(in_dir_name, user_number)
        out_netRTTDF = pd.read_csv(file_name, sep =',')
        out_netRTTDF.columns=['rtt_ms']
        netRTTDF = pd.concat([out_netRTTDF, netRTTDF], ignore_index=True)
        # Process Round-trip time
        file_name = '../{}/procRTT_{}.csv'.format(in_dir_name, user_number)
        out_procRTTDF = pd.read_csv(file_name, sep=',')
        out_procRTTDF.columns = ['rtt_ms']
        procRTTDF = pd.concat([out_procRTTDF, procRTTDF], ignore_index=True)

    netRTTDF = netRTTDF.loc[netRTTDF['rtt_ms'] != 'timed']
    netRTTseries = pd.Series(netRTTDF['rtt_ms'])
    netRTTseries = pd.to_numeric(netRTTseries)
    stats_rtt = netRTTseries.describe()
    # RTT
    m, c, s = stats_rtt['mean'], stats_rtt['count'], stats_rtt['std']
    ci95 = 1.96 * s / math.sqrt(c)
    rtt_dict[user_number] = {m, ci95}
    rtt_mean_dict[user_number] = m
    rtt_ci_dict[user_number] = ci95

    procRTTDF = procRTTDF.loc[procRTTDF['rtt_ms'] != 'timed']
    procRTTseries = pd.Series(procRTTDF['rtt_ms'])
    procRTTseries = pd.to_numeric(procRTTseries)
    proc_stats_rtt = procRTTseries.describe()
    # RTT
    m_proc, c_proc, s_proc = proc_stats_rtt['mean'], proc_stats_rtt['count'], proc_stats_rtt['std']
    ci95_proc = 1.96 * s_proc / math.sqrt(c_proc)
    proc_rtt_dict[user_number] = {m_proc, ci95_proc}
    proc_rtt_mean_dict[user_number] = m_proc
    proc_rtt_ci_dict[user_number] = ci95_proc


rttMeans = tuple(rtt_mean_dict.values())
rttCIs = tuple(rtt_ci_dict.values())
print([rttMeans, rttCIs])

proc_rttMeans = tuple(proc_rtt_mean_dict.values())
proc_rttCIs = tuple(proc_rtt_ci_dict.values())
print([proc_rttMeans, proc_rttCIs])

# Plot figure
ind = [] #list(load_ci_dict.keys())
for key in rtt_ci_dict.keys():
    ind.append('{}'.format(key))
print(ind)
width = 0.4  # the width of the bars: can also be len(x) sequence

f, axes = plt.subplots(2, 1) #, figsize=(10,7)
plt.margins(0.01, 0)
# color='skyblue': indianred, dodgerblue, turquoise, mediumseagreen, lightgreen
p1 = axes[0].bar(ind, rttMeans, width, yerr=rttCIs, color='dodgerblue', log=False,
            capsize=3, error_kw=dict(elinewidth=1, ecolor='blue'), label='Avatar Selected')
p2 = axes[1].bar(ind, proc_rttMeans, width, yerr=proc_rttCIs, color='skyblue', log=False,
            capsize=3, error_kw=dict(elinewidth=1, ecolor='black'), label='Room Joined')
plt.margins(0.01, 0)

# Optional code - Make plot look nicer
i = 0.01
for rtt, proc_rtt in zip(rttMeans,proc_rttMeans):
    axes[0].text(i, rtt, "{0:.0f}".format(rtt), color='black', fontsize=16)
    axes[1].text(i, proc_rtt, "{0:.0f}".format(proc_rtt), color='black', fontsize=16)
    i = i + 1

axes[0].spines['right'].set_visible(False)
axes[0].spines['top'].set_visible(False)
axes[0].tick_params(axis='both', which='major', labelsize=15)
axes[0].tick_params(axis='both', which='minor', labelsize=12)
axes[0].set_ylabel('Network RTT (ms)', fontsize=14, labelpad=-1)

axes[1].spines['right'].set_visible(False)
axes[1].spines['top'].set_visible(False)
axes[1].tick_params(axis='both', which='major', labelsize=15)
axes[1].tick_params(axis='both', which='minor', labelsize=12)
axes[1].set_ylabel('Application RTT (ms)', fontsize=14, labelpad=-1)

# Tick rotation on axes
for tick in axes[0].get_yticklabels():
    tick.set_rotation(20)
for tick in axes[1].get_yticklabels():
    tick.set_rotation(20)

# f.text(0.07,0.5,'RTT (ms)', fontsize=18, ha='center',va='center',rotation='vertical')
# plt.legend(loc='upper left', fontsize=13, title="Latency", fancybox=True)
parentDir = os.path.dirname(os.path.realpath(__file__))
Fig_PATH = os.path.join(parentDir, 'figures', 'RTT.pdf')
# plt.savefig(Fig_PATH)
plt.show()
