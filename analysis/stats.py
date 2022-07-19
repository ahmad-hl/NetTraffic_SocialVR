import matplotlib.pyplot as plt
import pandas as pd
import os, math

dir_name = 'results/synth7'
parentDir = os.path.dirname(os.path.realpath(__file__))
ULDL_2_PATH = os.path.join(parentDir, '..',dir_name, 'ULDL_2.log')


uldl2DF = pd.read_csv(ULDL_2_PATH, sep=',')
# uldl2DF = uldl2DF.loc[(uldl2DF['ul_kBps'] >= 0.1) & (uldl2DF['dl_kBps'] >= 0.1)]
uldl2DF['ul_kBps'] = uldl2DF['ul_kBps'] * 8/1024  # KB/s to Mb/s
uldl2DF['dl_kBps'] = uldl2DF['dl_kBps'] * 8/1024 # KB/s to Mb/s


NUM_SAMPLES = 40  #[-NUM_SAMPLES:]
SKIP = 0
print("Loading Stage")
# print(uldl2DF[SKIP:NUM_SAMPLES])
print(uldl2DF[SKIP:SKIP+NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
#*************************************
NUM_SAMPLES = 15
SKIP = 45
print("Idle Stage")
# print(uldl2DF[SKIP:SKIP+NUM_SAMPLES])
print(uldl2DF[SKIP:SKIP+NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
#*************************************
NUM_SAMPLES = 50
SKIP = 60
print("Avatar Loading Stage")
# print(uldl2DF[SKIP:SKIP+NUM_SAMPLES])
print(uldl2DF[SKIP:SKIP+NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
#*************************************
NUM_SAMPLES = 50
SKIP = 60
print("Avatar Loading Stage")
# print(uldl2DF[SKIP:SKIP+NUM_SAMPLES])
print(uldl2DF[SKIP:SKIP+NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
#*************************************
NUM_SAMPLES = 70
SKIP = 130
print("Interaction with U2")
# print(uldl2DF[SKIP:NUM_SAMPLES])
print(uldl2DF[SKIP:SKIP+NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
#*************************************
NUM_SAMPLES = 35
SKIP = 226
print("Interaction with U2 & U3")
# print(uldl2DF[SKIP:NUM_SAMPLES])
print(uldl2DF[SKIP:SKIP+NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
#*************************************
NUM_SAMPLES = 30
SKIP = 260
print("U2 & U3 Left: Idle")
# print(uldl2DF[SKIP:NUM_SAMPLES])
print(uldl2DF[SKIP:SKIP+NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())

print("User study")


def compute_stats(VRsurveyDF, factors):
    user_dict = {}
    user_mean_dict = {}
    user_ci_dict = {}
    user_std_dict = {}

    for factor in factors:
        factSeries = pd.Series(VRsurveyDF[factor])
        factSeries = pd.to_numeric(factSeries)
        stats_fact = factSeries.describe()
        # Frustration
        m, c, s = stats_fact['mean'], stats_fact['count'], stats_fact['std']
        ci95 = 1.96 * s / math.sqrt(c)
        user_dict[factor] = {s, m, ci95}
        user_mean_dict[factor] = m
        user_std_dict[factor] = s
        user_ci_dict[factor] = ci95

    return user_dict, user_mean_dict, user_ci_dict, user_std_dict

def categorize_DF(VRsurveyDF):
    VRloadDF = VRsurveyDF[['frustration', 'load', 'mental']]
    VRloadDF = VRloadDF.assign(type='Load')
    VRmeasureDF = VRsurveyDF[['immersion', 'promise', 'success']]
    VRmeasureDF = VRmeasureDF.assign(type='VRMeasure')

    surveyDF = pd.concat([VRloadDF, VRmeasureDF], ignore_index=True)
    return surveyDF

if __name__ == '__main__':
    in_dir_name = 'results_ux'
    file_name = '../{}/QoE.csv'.format(in_dir_name)
    VRsurveyDF = pd.read_csv(file_name, sep =',')
    factors = ['frustration', 'mental', 'load', 'immersion','success', 'promise']
    user_dict,user_mean_dict,user_ci_dict, user_std_dict = compute_stats(VRsurveyDF, factors=factors)

    loadMeans = tuple(user_mean_dict.values())
    loadCIs = tuple(user_ci_dict.values())
    loadStds = tuple(user_std_dict.values())
    print(user_mean_dict.keys())
    print(loadMeans)
    print(loadStds)
    print(loadCIs)
    print(user_dict)