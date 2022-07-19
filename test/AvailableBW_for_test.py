import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns


def compute_bw( conf_dir_names):

    user_number = 8
    NUM_SAMPLES = 50
    SKIP = 7
    lab_uldl16DF = pd.DataFrame()
    dthub_uldl16DF = pd.DataFrame()
    conf_uldl16DF = pd.DataFrame()

    parentDir = os.path.dirname(os.path.realpath(__file__))
    for conf_dir_name in conf_dir_names:
        ULDL_16_PATH = os.path.join(parentDir, '..', conf_dir_name, 'ULDL_{}.log'.format(user_number))
        conf_uldl16DF = pd.read_csv(ULDL_16_PATH, sep=',')
        conf_uldl16DF = conf_uldl16DF[SKIP: SKIP+NUM_SAMPLES]
        conf_uldl16DF = conf_uldl16DF.assign(network='Classroom WiFi')

    uldl16DF = pd.concat([lab_uldl16DF, conf_uldl16DF, dthub_uldl16DF], ignore_index=True)
    uldl16DF['dl_kBps'] = uldl16DF['dl_kBps'] * 8 / 1024 # KB/s to Mb/s

    return uldl16DF


if __name__ == '__main__':
    conf_dir_names = ['results_conf/synth19']
    uldl16DF = compute_bw( conf_dir_names)

    print(uldl16DF.groupby(by=["network"], dropna=False).describe())
    sns.set(font_scale=1.4)
    # Draw a nested barplot by species and sex
    g = sns.barplot(
        data=uldl16DF, x="network", y="dl_kBps",
        ci=95, palette="dark", alpha=.6)
    # g.despine(left=True)
    plt.ylabel("Download (Mb/s)", fontsize=18, fontweight='bold')
    plt.xlabel("Access Network", fontsize=18, fontweight='bold')
    g.spines['right'].set_visible(False)
    g.spines['top'].set_visible(False)

    parentDir = os.path.dirname(os.path.realpath(__file__))
    Fig_PATH = os.path.join(parentDir, '../analysis/figures', 'network_bw_test.pdf')
    plt.savefig(Fig_PATH, bbox_inches='tight')
    plt.show()
