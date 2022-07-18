import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

spatial_dir_name = 'results_vr_platforms/uldl'
hubs_dir_name = 'results/synth7'
parentDir = os.path.dirname(os.path.realpath(__file__))
ULDL_spatial_PATH = os.path.join(parentDir, '..',spatial_dir_name, 'spatial.uldl_2.log')
ULDL_hubs_PATH = os.path.join(parentDir, '..',hubs_dir_name, 'ULDL_2.log')

spatialUlDlDF = pd.read_csv(ULDL_spatial_PATH, sep=',')
hubsUlDlDF = pd.read_csv(ULDL_hubs_PATH, sep=',')

f, axes = plt.subplots(2,1, figsize=(10,7))
f.text(0.07,0.5,'KB/s', fontsize=15, ha='center',va='center',rotation='vertical')
ax1 = axes[0]
ax2 = axes[1]
font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}

ax1.plot( hubsUlDlDF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Hubs Upload')
ax1.plot( hubsUlDlDF['dl_kBps'], color='red', linewidth=2, label='Hubs Download')
# Hide the right and top spines
ax1.spines.right.set_visible(False)
ax1.spines.top.set_visible(False)
# ax1.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax1.legend(ncol=1, loc='upper right', fontsize='x-large')

NUM_SAMPLES = 60 #[-NUM_SAMPLES:]
SKIP_SAMPLES = 0
spatialUlDlDF = spatialUlDlDF[SKIP_SAMPLES:]


ax2.plot( spatialUlDlDF['ul_kBps'], color='blue', linestyle='dashed', linewidth=2, label='Spatial Upload')
ax2.plot( spatialUlDlDF['dl_kBps'], color='red', linewidth=2, label='Spatial Download')
# Hide the right and top spines
ax2.spines.right.set_visible(False)
ax2.spines.top.set_visible(False)
ax2.legend(ncol=1, loc='upper right', fontsize='x-large')

# ax2.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
Fig_PATH = os.path.join(parentDir, 'figures', 'uldl_tabs.pdf')
# plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()