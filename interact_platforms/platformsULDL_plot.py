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
ULDL_workrooms_PATH = os.path.join(parentDir, '..',hubs_dir_name, 'workrooms.uldl_4.log')

#Spatial Data
NUM_SAMPLES = 60 #[-NUM_SAMPLES:]
SKIP_SAMPLES = 20
spatialUlDlDF = pd.read_csv(ULDL_spatial_PATH, sep=',')
# spatialUlDlDF['dl_kBps'] = spatialUlDlDF['dl_kBps'] * 8/1024
# spatialUlDlDF['ul_kBps'] = spatialUlDlDF['ul_kBps']* 8/1024
spatialUlDlDF = spatialUlDlDF[SKIP_SAMPLES:]

#Hubs data
hubsUlDlDF = pd.read_csv(ULDL_hubs_PATH, sep=',')
# hubsUlDlDF['dl_kBps'] = hubsUlDlDF['dl_kBps'] * 8/1024
# hubsUlDlDF['ul_kBps'] = hubsUlDlDF['ul_kBps']* 8/1024
hubsUlDlDF = hubsUlDlDF[SKIP_SAMPLES:]

#Workrooms data
workroomsUlDlDF = pd.read_csv(ULDL_workrooms_PATH, sep=',', header=0)
workroomsUlDlDF.columns = ["ts","dl_kBps","ul_kBps","Downlink_Packet_Size","Uplink_Packet_Size","Downlink_Packet_Rate","Uplink_Packet_Rate"]
workroomsUlDlDF['dl_kBps'] = workroomsUlDlDF['dl_kBps']/1024/1024
workroomsUlDlDF['ul_kBps'] = workroomsUlDlDF['ul_kBps']/1024/1024
print(workroomsUlDlDF.head(10))

f, axes = plt.subplots(3,1, figsize=(10,7))
# f.text(0.07,0.5,'KB/s', fontsize=15, ha='center',va='center',rotation='vertical')
ax1 = axes[0]
ax2 = axes[1]
ax3 = axes[2]
font_dict = {'fontsize': 13,
 'fontweight' : 'bold'}


ax1.plot( hubsUlDlDF['ul_kBps'], color='blue', linestyle='dashed', linewidth=3, label='Upload')
ax1.plot( hubsUlDlDF['dl_kBps'], color='red', linewidth=3, label='Download')
# Hide the right and top spines
ax1.spines.right.set_visible(False)
ax1.spines.top.set_visible(False)
ax1.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax1.legend(ncol=2, loc='upper right', fontsize='x-large')
ax1.set_ylabel('KBps', fontdict={'fontsize': 14, 'fontweight': 'medium'})
ax1.set_title('Hubs Bitrate', fontsize = 15, x=.44, y= .85) #, loc='right'

ax2.plot( spatialUlDlDF['ul_kBps'], color='blue', linestyle='dashed', linewidth=3) #, label='Spatial Upload'
ax2.plot( spatialUlDlDF['dl_kBps'], color='red', linewidth=3) #, label='Spatial Download'
# Hide the right and top spines
ax2.spines.right.set_visible(False)
ax2.spines.top.set_visible(False)
ax2.legend(ncol=2, loc='upper right', fontsize='x-large')
ax2.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax2.set_ylabel('KBps', fontdict={'fontsize': 14, 'fontweight': 'medium'})
ax2.set_title('Spatial Bitrate', fontsize = 15, y= .85) #, loc='right'

ax3.plot( workroomsUlDlDF['ul_kBps'], color='blue', linestyle='dashed', linewidth=3) #, label='Workrooms Upload'
ax3.plot( workroomsUlDlDF['dl_kBps'], color='red', linewidth=3) #, label='Workrooms Download'
# Hide the right and top spines
ax3.spines.right.set_visible(False)
ax3.spines.top.set_visible(False)
ax3.legend(ncol=2, loc='upper right', fontsize='x-large')
# ax3.set_yscale('symlog')  #"linear", "log", "symlog", "logit",
ax3.set_ylabel('Mbps', fontdict={'fontsize': 14, 'fontweight': 'medium'})
ax3.set_title('Workrooms Bitrate', fontsize = 15, y= .85) #, loc='right'

Fig_PATH = os.path.join(parentDir, '..','analysis','figures', 'uldl_5users_platforms.pdf')
plt.savefig(Fig_PATH, bbox_inches='tight')
plt.show()