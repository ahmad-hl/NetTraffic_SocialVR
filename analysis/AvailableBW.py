import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns

in_dir_names = ['results/synth3','results/synth4','results/synth5','results/synth6']
dthub_dir_names = ['results_dthub/synth8','results_dthub/synth9','results_dthub/synth10']
conf_dir_names = ['results_conf/synth12','results_conf/synth13']

user_number = 16
NUM_SAMPLES = 60
lab_uldl16DF = pd.DataFrame()
dthub_uldl16DF = pd.DataFrame()
conf_uldl16DF = pd.DataFrame()

parentDir = os.path.dirname(os.path.realpath(__file__))
for in_dir_name in in_dir_names:
    ULDL_16_PATH = os.path.join(parentDir, '..', in_dir_name, 'ULDL_{}.log'.format(user_number))
    lab_uldl16DF = pd.read_csv(ULDL_16_PATH, sep=',')
    lab_uldl16DF =  lab_uldl16DF[:NUM_SAMPLES]
    lab_uldl16DF =  lab_uldl16DF.assign(network='Lab WiFi')

for dthub_dir_name in dthub_dir_names:
    ULDL_16_PATH = os.path.join(parentDir, '..', dthub_dir_name, 'ULDL_{}.log'.format(user_number))
    dthub_uldl16DF = pd.read_csv(ULDL_16_PATH, sep=',')
    dthub_uldl16DF = dthub_uldl16DF[:NUM_SAMPLES]
    dthub_uldl16DF = dthub_uldl16DF.assign(network='DT-Hub WiFi')

for conf_dir_name in conf_dir_names:
    ULDL_16_PATH = os.path.join(parentDir, '..', conf_dir_name, 'ULDL_{}.log'.format(user_number))
    conf_uldl16DF = pd.read_csv(ULDL_16_PATH, sep=',')
    conf_uldl16DF = conf_uldl16DF[:NUM_SAMPLES]
    conf_uldl16DF = conf_uldl16DF.assign(network='Conference WiFi')

uldl16DF = pd.concat([lab_uldl16DF, dthub_uldl16DF, conf_uldl16DF], ignore_index=True)
uldl16DF['dl_kBps'] = uldl16DF['dl_kBps'] * 8 / 1024 # KB/s to Mb/s

print(uldl16DF.groupby(by=["network"], dropna=False).describe())
print(uldl16DF.loc[uldl16DF.network=='Lab WiFi'].describe())

# Draw a nested barplot by species and sex
g = sns.barplot(
    data=uldl16DF, x="network", y="dl_kBps",
    ci=95, palette="dark", alpha=.6)
# g.despine(left=True)
plt.ylabel( "Download (Mb/s)", fontsize=15, fontweight='bold')
plt.xlabel("Access Network", fontsize=15, fontweight='bold')
g.spines['right'].set_visible(False)
g.spines['top'].set_visible(False)

# Fig_PATH = os.path.join(parentDir, 'figures', 'network_load_latency.pdf')
# plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()


#
# parentDir = os.path.dirname(os.path.realpath(__file__))
# for in_dir_name in in_dir_names:
#     ULDL_16_PATH = os.path.join(parentDir, '..', in_dir_name, 'ULDL_{}.log'.format(user_number))
#     uldl16DF = pd.read_csv(ULDL_16_PATH, sep=',')
#     uldl16DF = lab_uldl16DF[:NUM_SAMPLES]
#
#     ULDL_2_16_PATH = os.path.join(parentDir, '..', in_dir_name+'.2', 'ULDL_{}.log'.format(user_number))
#     uldl16_2DF = pd.read_csv(ULDL_2_16_PATH, sep=',')
#
#
#     uldl16DF = pd.concat([uldl16DF, uldl16_2DF], ignore_index=True)
#     uldl16DF['ts'] = uldl16DF['ts'].astype('uint64')
#     uldl16DF = uldl16DF.sort_values(by=['ts'],ignore_index=True)
#     uldl16DF = uldl16DF.groupby('ts', as_index=False).agg({'ts':'first','ul_kBps':sum,'dl_kBps':sum})
#     lab_uldl16DF = pd.concat([lab_uldl16DF,uldl16DF ], ignore_index=True)
#     lab_uldl16DF = lab_uldl16DF.assign(network='Lab WiFi')
#     lab_uldl16DF = lab_uldl16DF[:NUM_SAMPLES]