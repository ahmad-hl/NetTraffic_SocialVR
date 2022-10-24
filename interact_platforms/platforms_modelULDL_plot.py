import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

spatial_dir_name = 'results_platforms/uldl'
hubs_dir_name = 'results_platforms/uldl'
workrooms_dir_name = 'results_platforms/uldl'
parentDir = os.path.dirname(os.path.realpath(__file__))
ULDL_spatial_PATH = os.path.join(parentDir, '..',spatial_dir_name, 'spatial.uldl_4.log')
ULDL_hubs_PATH = os.path.join(parentDir, '..',hubs_dir_name, 'hubs.uldl_4.log')

#Spatial Datar
NUM_SAMPLES = 100 #[-NUM_SAMPLES:]
# SKIP_SAMPLES = 50
spatialUlDlDF = pd.read_csv(ULDL_spatial_PATH, sep=',')
# spatialUlDlDF['dl_kBps'] = spatialUlDlDF['dl_kBps'] * 8/1024
# spatialUlDlDF['ul_kBps'] = spatialUlDlDF['ul_kBps']* 8/1024
spatialUlDlDF = spatialUlDlDF[:NUM_SAMPLES]

#Hubs data
hubsUlDlDF = pd.read_csv(ULDL_hubs_PATH, sep=',')
# hubsUlDlDF['dl_kBps'] = hubsUlDlDF['dl_kBps'] * 8/1024
# hubsUlDlDF['ul_kBps'] = hubsUlDlDF['ul_kBps']* 8/1024
hubsUlDlDF = hubsUlDlDF[:NUM_SAMPLES]

f, axes = plt.subplots(2,1, figsize=(10,7))
# f.text(0.07,0.5,'KB/s', fontsize=15, ha='center',va='center',rotation='vertical')
ax1 = axes[0]
ax2 = axes[1]
font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}


ax1.plot( hubsUlDlDF['ul_kBps'], color='blue', linestyle='dashed', linewidth=3, label='Upload') #, label='Hubs Upload'
ax1.plot( hubsUlDlDF['dl_kBps'], color='red', linewidth=3, label='Download') #, label='Hubs Download'
# Hide the right and top spines
ax1.spines.right.set_visible(False)
ax1.spines.top.set_visible(False)
ax1.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax1.legend(ncol=2, loc='upper right', fontsize='x-large')
ax1.set_ylabel('KBps', fontdict={'fontsize': 14, 'fontweight': 'medium'})
ax1.set_title('Hubs Bitrate', fontsize = 15,x=.44, y= .85) #, loc='right'

ax2.plot( spatialUlDlDF['ul_kBps'], color='blue', linestyle='dashed', linewidth=3) #, label='Spatial Upload'
ax2.plot( spatialUlDlDF['dl_kBps'], color='red', linewidth=3) #, label='Spatial Download'
# Hide the right and top spines
ax2.spines.right.set_visible(False)
ax2.spines.top.set_visible(False)
ax2.legend(ncol=2, loc='upper right', fontsize='x-large')
ax2.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax2.set_ylabel('KBps', fontdict={'fontsize': 14, 'fontweight': 'medium'})
ax2.set_title('Spatial Bitrate', fontsize = 15, x=.44, y= .85) #, loc='right'

Fig_PATH = os.path.join(parentDir, '..','analysis','figures', 'uldl_model_platforms.pdf')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()