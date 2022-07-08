import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

# in_dir_names = ['results/synth3','results/synth3.2']
# in_dir_names = ['results/synth4','results/synth4.2']
# in_dir_names = ['results/synth5','results/synth5.2']
# in_dir_names = ['results/synth9','results/synth6.2']
in_dir_names = ['results_dthub/synth9']
oculus_dir_name = 'results_dthub/synth9Oculus'

uldl2DF = pd.DataFrame()
uldl4DF = pd.DataFrame()
uldl8DF = pd.DataFrame()
uldl16DF = pd.DataFrame()
parentDir = os.path.dirname(os.path.realpath(__file__))
for in_dir_name in in_dir_names:
    ULDL_2_PATH = os.path.join(parentDir, '..', in_dir_name, 'ULDL_2.log')
    out_uldl2DF = pd.read_csv(ULDL_2_PATH, sep=',')
    uldl2DF = pd.concat([out_uldl2DF, uldl2DF], ignore_index=True)

    ULDL_4_PATH = os.path.join(parentDir, '..', in_dir_name, 'ULDL_4.log')
    out_uldl4DF = pd.read_csv(ULDL_4_PATH, sep=',')
    uldl4DF = pd.concat([out_uldl4DF, uldl4DF], ignore_index=True)

    ULDL_8_PATH = os.path.join(parentDir, '..', in_dir_name, 'ULDL_8.log')
    out_uldl8DF = pd.read_csv(ULDL_8_PATH, sep=',')
    uldl8DF = pd.concat([out_uldl8DF, uldl8DF], ignore_index=True)

    ULDL_16_PATH = os.path.join(parentDir, '..', in_dir_name, 'ULDL_16.log')
    out_uldl16DF = pd.read_csv(ULDL_16_PATH, sep=',')
    uldl16DF = pd.concat([out_uldl16DF, uldl16DF], ignore_index=True)

uldl2DF = uldl2DF.loc[(uldl2DF['ul_kBps'] >= 0.1) & (uldl2DF['dl_kBps'] >= 0.1)]
uldl2DF['ts'] = uldl2DF['ts'].astype('uint64')
uldl2DF = uldl2DF.sort_values(by=['ts'],ignore_index=True)
uldl2DF = uldl2DF.groupby('ts', as_index=False).agg({'ts':'first','ul_kBps':sum,'dl_kBps':np.mean})
print(uldl2DF.head(3))

# uldl4DF = uldl4DF.loc[(uldl4DF['ul_kBps'] >= 0.1) & (uldl4DF['dl_kBps'] >= 0.1)]
uldl4DF['ts'] = uldl4DF['ts'].astype('uint64')
uldl4DF = uldl4DF.sort_values(by=['ts'],ignore_index=True)
uldl4DF = uldl4DF.groupby('ts', as_index=False).agg({'ts':'first','ul_kBps':sum,'dl_kBps':np.mean})

# uldl8DF = uldl8DF.loc[(uldl8DF['ul_kBps'] >= 0.1) & (uldl8DF['dl_kBps'] >= 0.1)]
uldl8DF['ts'] = uldl8DF['ts'].astype('uint64')
uldl8DF = uldl8DF.sort_values(by=['ts'],ignore_index=True)
uldl8DF = uldl8DF.groupby('ts', as_index=False).agg({'ts':'first','ul_kBps':sum,'dl_kBps':np.mean})

# uldl16DF = uldl16DF.loc[(uldl16DF['ul_kBps'] >= 0.1) & (uldl16DF['dl_kBps'] >= 0.1)]
uldl16DF['ts'] = uldl16DF['ts'].astype('uint64')
uldl16DF = uldl16DF.sort_values(by=['ts'],ignore_index=True)
uldl16DF = uldl16DF.groupby('ts', as_index=False).agg({'ts':'first','ul_kBps':sum,'dl_kBps':np.mean})

parentDir = os.path.dirname(os.path.realpath(__file__))
ULDLoculus_2_PATH = os.path.join(parentDir, '..',oculus_dir_name, 'ULDLoculus_2.log')
ULDLoculus_4_PATH = os.path.join(parentDir, '..', oculus_dir_name, 'ULDLoculus_4.log')
ULDLoculus_8_PATH = os.path.join(parentDir, '..', oculus_dir_name, 'ULDLoculus_8.log')
ULDLoculus_16_PATH = os.path.join(parentDir, '..', oculus_dir_name, 'ULDLoculus_16.log')

uldlOculus2DF = pd.read_csv(ULDLoculus_2_PATH, sep=',')
# uldlOculus2DF = uldlOculus2DF.loc[(uldlOculus2DF['ul_kBps'] >= 0.1) & (uldlOculus2DF['dl_kBps'] >= 0.1)]
uldlOculus4DF = pd.read_csv(ULDLoculus_4_PATH, sep=',')
# uldlOculus4DF = uldlOculus4DF.loc[(uldlOculus4DF['ul_kBps'] >= 0.1) & (uldlOculus4DF['dl_kBps'] >= 0.1)]
uldlOculus8DF = pd.read_csv(ULDLoculus_8_PATH, sep=',')
# uldlOculus8DF = uldlOculus8DF.loc[(uldlOculus8DF['ul_kBps'] >= 0.1) & (uldlOculus8DF['dl_kBps'] >= 0.1)]
uldlOculus16DF = pd.read_csv(ULDLoculus_16_PATH, sep=',')
# uldlOculus16DF = uldlOculus16DF.loc[(uldlOculus16DF['ul_kBps'] >= 0.1) & (uldlOculus16DF['dl_kBps'] >= 0.1)]


NUM_SAMPLES = 60 #[-NUM_SAMPLES:]
f, axes = plt.subplots(2, 2, figsize=(10,7))
f.text(0.07,0.5,'KB/s', fontsize=16, ha='center',va='center',rotation='vertical')
ax1 = axes[0][0]
ax2 = axes[0][1]
ax3 = axes[1][0]
ax4 = axes[1][1]

font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}

ax1.plot( uldl2DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Desktop Users Upload')
ax1.plot( uldlOculus2DF['ul_kBps'], color='brown', linestyle='dotted', linewidth=2, label='Headset Upload')
ax1.plot( uldlOculus2DF['dl_kBps'], color='red', label='Headset Download')
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
# ax1.legend(ncol=2, loc='lower right')
# ax1.set_ylabel('KB/s')
ax1.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax1.set_title('2 Desktop Users', font_dict, loc='right', pad=1, y= 0.95)
# We change the fontsize of minor ticks label
ax1.tick_params(axis='both', which='major', labelsize=12)
ax1.tick_params(axis='both', which='minor', labelsize=10)

ax2.plot( uldl4DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Desktop Users Upload')
ax2.plot( uldlOculus4DF['ul_kBps'], color='brown', linestyle='dotted', linewidth=2, label='Headset Upload')
ax2.plot( uldlOculus4DF['dl_kBps'], color='red', label='Headset Download')
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.legend(ncol=1, loc='upper right', fontsize='medium', columnspacing=0)
# ax2.set_ylabel('KB/s')
ax2.set_yscale('symlog')
ax2.set_title('4 Desktop Users', font_dict,  loc='right', pad=1, y= 1)
# We change the fontsize of minor ticks label
ax2.tick_params(axis='both', which='major', labelsize=12)
ax2.tick_params(axis='both', which='minor', labelsize=10)

# {"linear", "log", "symlog", "logit"

# ax3.plot( uldl8DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Desktop Users Upload')
ax3.plot( uldlOculus8DF['ul_kBps'], color='brown', linestyle='dotted', linewidth=2, label='Headset Upload')
ax3.plot( uldlOculus8DF['dl_kBps'], color='red', label='Headset Download')
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
# ax3.legend(ncol=2, loc='lower right')
# ax3.set_ylabel('KB/s')
ax3.set_yscale('symlog')
ax3.set_title('8 Desktop Users', font_dict,  loc='right', pad=1, y= 0.95)
# We change the fontsize of minor ticks label
ax3.tick_params(axis='both', which='major', labelsize=12)
ax3.tick_params(axis='both', which='minor', labelsize=10)

# ax4.plot( uldl16DF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Desktop Users Upload')
ax4.plot( uldlOculus16DF['ul_kBps'], color='brown', linestyle='dotted', linewidth=2, label='Headset Upload')
ax4.plot( uldlOculus16DF['dl_kBps'], color='red', label='Headset Download')
ax4.spines['right'].set_visible(False)
ax4.spines['top'].set_visible(False)
# ax4.legend(ncol=2, loc='lower right')
# ax4.set_ylabel('KB/s')
ax4.set_yscale('symlog')
ax4.set_title('16 Desktop Users', font_dict,  loc='right', pad=1, y= 0.95 )
# We change the fontsize of minor ticks label
ax4.tick_params(axis='both', which='major', labelsize=12)
ax4.tick_params(axis='both', which='minor', labelsize=10)

# f.subplots_adjust(hspace=2)

Fig_PATH = os.path.join(parentDir, 'figures', 'uldl_tabs2oculus.pdf')
# plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()