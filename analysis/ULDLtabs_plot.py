import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

dir_name = 'results/synth6'
parentDir = os.path.dirname(os.path.realpath(__file__))
ULDL_2_PATH = os.path.join(parentDir, '..',dir_name, 'ULDL_2.log')
ULDL_4_PATH = os.path.join(parentDir, '..', dir_name, 'ULDL_4.log')
ULDL_8_PATH = os.path.join(parentDir, '..', dir_name, 'ULDL_8.log')
ULDL_16_PATH = os.path.join(parentDir, '..', dir_name, 'ULDL_16.log')


uldl2DF = pd.read_csv(ULDL_2_PATH, sep=',')
# uldl2DF = uldl2DF.loc[(uldl2DF['ul_kBps'] >= 0.1) & (uldl2DF['dl_kBps'] >= 0.1)]
uldl4DF = pd.read_csv(ULDL_4_PATH, sep=',')
# uldl4DF = uldl4DF.loc[(uldl4DF['ul_kBps'] >= 0.1) & (uldl4DF['dl_kBps'] >= 0.1)]
uldl8DF = pd.read_csv(ULDL_8_PATH, sep=',')
# uldl8DF = uldl8DF.loc[(uldl8DF['ul_kBps'] >= 0.1) & (uldl8DF['dl_kBps'] >= 0.1)]
uldl16DF = pd.read_csv(ULDL_16_PATH, sep=',')
# uldl16DF = uldl16DF.loc[(uldl16DF['ul_kBps'] >= 0.1) & (uldl16DF['dl_kBps'] >= 0.1)]
# uldlDF.columns = ['ts','ul_kBps','dl_kBps']


NUM_SAMPLES = 60 #[-NUM_SAMPLES:]

# f, (ax1, ax2) = plt.subplots(2, sharex=True)
# f, axes = plt.subplots( 2,2,figsize=(25,25))
f, axes = plt.subplots(2, 2, figsize=(10,7))
f.text(0.07,0.5,'KB/s', fontsize=15, ha='center',va='center',rotation='vertical')
plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = -5  # pad is in points.
ax1 = axes[0][0]
ax2 = axes[0][1]
ax3 = axes[1][0]
ax4 = axes[1][1]

font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}

ax1.plot( uldl2DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Acc Upload')
ax1.plot( uldl2DF['dl_kBps'], color='red', linewidth=2, label='Acc Download')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
# ax1.legend(ncol=2)
# ax1.set_ylabel('KB/s')
ax1.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax1.set_title('Desktop users: 2', font_dict, loc='right')
# We change the fontsize of minor ticks label
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.tick_params(axis='both', which='minor', labelsize=10)

ax2.plot( uldl4DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Acc Upload')
ax2.plot( uldl4DF['dl_kBps'], color='red',linewidth=2, label='Acc Download')
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.legend(ncol=2, loc='lower right')
# ax2.set_ylabel('KB/s')
ax2.set_yscale('symlog')
ax2.set_title('Desktop users: 4', font_dict, loc='right')
# We change the fontsize of minor ticks label
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.tick_params(axis='both', which='minor', labelsize=10)

# {"linear", "log", "symlog", "logit"

ax3.plot( uldl8DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Acc Upload')
ax3.plot( uldl8DF['dl_kBps'], color='red',linewidth=2, label='Acc Download')
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
# ax3.legend(ncol=2)
# ax3.set_ylabel('KB/s')
ax3.set_yscale('symlog')
ax3.set_title('Desktop users: 8', font_dict, loc='right')
# We change the fontsize of minor ticks label
ax3.tick_params(axis='both', which='major', labelsize=12)
ax3.tick_params(axis='both', which='minor', labelsize=10)

ax4.plot( uldl16DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Acc Upload')
ax4.plot( uldl16DF['dl_kBps'], color='red',linewidth=2, label='Acc Download')
ax4.spines['right'].set_visible(False)
ax4.spines['top'].set_visible(False)
# ax4.legend(ncol=2)
# ax4.set_ylabel('KB/s')
ax4.set_yscale('symlog')
ax4.set_title('Desktop users: 16', font_dict, loc='right')
# We change the fontsize of minor ticks label
ax4.tick_params(axis='both', which='major', labelsize=12)
ax4.tick_params(axis='both', which='minor', labelsize=10)


# f.subplots_adjust(hspace=2)

Fig_PATH = os.path.join(parentDir, 'figures', 'uldl_tabs.pdf')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()