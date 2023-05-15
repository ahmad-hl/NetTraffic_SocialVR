import matplotlib.pyplot as plt
import pandas as pd
import os

dir_name = 'wifi_data/lab/synth7'
parentDir = os.path.dirname(os.path.realpath(__file__))
ULDL_2_PATH = os.path.join(parentDir, '..',dir_name, 'ULDL_2.log')


uldl2DF = pd.read_csv(ULDL_2_PATH, sep=',')
uldl2DF = uldl2DF.loc[(uldl2DF['ul_kBps'] >= 0.1) & (uldl2DF['dl_kBps'] >= 0.1)]


NUM_SAMPLES = 60 #[-NUM_SAMPLES:]

# f, (ax1, ax2) = plt.subplots(2, sharex=True)
# f, axes = plt.subplots( 2,2,figsize=(25,25))
f, ax1 = plt.subplots(1, 1, figsize=(10,6))
f.text(0.06,0.5,'KB/s', fontsize=18, ha='center',va='center',rotation='vertical')
plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = -5  # pad is in points.


ax1.plot( uldl2DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Headset Upload')
ax1.plot( uldl2DF['dl_kBps'], color='red', linewidth=2, label='Headset Download')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.legend(ncol=1, fontsize='x-large')
# ax1.set_ylabel('KB/s')
ax1.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
# ax1.set_title(' #Tabs: 2', loc='right')
plt.yticks(fontsize=16, rotation=0)
plt.xticks(fontsize=16, rotation=0)


# f.subplots_adjust(hspace=2)

Fig_PATH = os.path.join(parentDir, 'figures', 'uldl_characterize.pdf')
# plt.savefig(Fig_PATH)
Fig_PATH = os.path.join(parentDir, 'figures', 'uldl_characterize.png')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()