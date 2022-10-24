import matplotlib.pyplot as plt
import pandas as pd
import os, math
import numpy as np


# Characterize Hubs stats
def charcterize_hubs_stats(ULDL_2_PATH):
    uldl2DF = pd.read_csv(ULDL_2_PATH, sep=',')
    # uldl2DF = uldl2DF.loc[(uldl2DF['ul_kBps'] >= 0.1) & (uldl2DF['dl_kBps'] >= 0.1)]
    uldl2DF['ul_kBps'] = uldl2DF['ul_kBps'] * 8 / 1024  # KB/s to Mb/s
    uldl2DF['dl_kBps'] = uldl2DF['dl_kBps'] * 8 / 1024  # KB/s to Mb/s

    NUM_SAMPLES = 40  # [-NUM_SAMPLES:]
    SKIP = 0
    print("Loading Stage")
    # print(uldl2DF[SKIP:NUM_SAMPLES])
    print(uldl2DF[SKIP:SKIP + NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
    # *************************************
    NUM_SAMPLES = 15
    SKIP = 45
    print("Idle Stage")
    # print(uldl2DF[SKIP:SKIP+NUM_SAMPLES])
    print(uldl2DF[SKIP:SKIP + NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
    # *************************************
    NUM_SAMPLES = 50
    SKIP = 60
    print("Avatar Loading Stage")
    # print(uldl2DF[SKIP:SKIP+NUM_SAMPLES])
    print(uldl2DF[SKIP:SKIP + NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
    # *************************************
    NUM_SAMPLES = 50
    SKIP = 60
    print("Avatar Loading Stage")
    # print(uldl2DF[SKIP:SKIP+NUM_SAMPLES])
    print(uldl2DF[SKIP:SKIP + NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
    # *************************************
    NUM_SAMPLES = 70
    SKIP = 130
    print("Interaction with U2")
    # print(uldl2DF[SKIP:NUM_SAMPLES])
    print(uldl2DF[SKIP:SKIP + NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
    # *************************************
    NUM_SAMPLES = 35
    SKIP = 226
    print("Interaction with U2 & U3")
    # print(uldl2DF[SKIP:NUM_SAMPLES])
    print(uldl2DF[SKIP:SKIP + NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())
    # *************************************
    NUM_SAMPLES = 30
    SKIP = 260
    print("U2 & U3 Left: Idle")
    # print(uldl2DF[SKIP:NUM_SAMPLES])
    print(uldl2DF[SKIP:SKIP + NUM_SAMPLES][['ul_kBps', 'dl_kBps']].describe())


# Comparative study, Hubs, Spatial and Workrooms
def comparative_stats(ULDL_hubs_PATH, ULDL_spatial_PATH, ULDL_workrooms_PATH ):

    # Spatial Data
    spatialUlDlDF = pd.read_csv(ULDL_spatial_PATH, sep=',')
    spatialUlDlDF['dl_kBps'] = spatialUlDlDF['dl_kBps'] * 8 / 1024
    spatialUlDlDF['ul_kBps'] = spatialUlDlDF['ul_kBps'] * 8 / 1024

    # Hubs data
    hubsUlDlDF = pd.read_csv(ULDL_hubs_PATH, sep=',')
    hubsUlDlDF['dl_kBps'] = hubsUlDlDF['dl_kBps'] * 8 / 1024
    hubsUlDlDF['ul_kBps'] = hubsUlDlDF['ul_kBps'] * 8 / 1024

    # Workrooms data
    workroomsUlDlDF = pd.read_csv(ULDL_workrooms_PATH, sep=',', header=0)
    workroomsUlDlDF.columns = ["ts", "dl_kBps", "ul_kBps", "Downlink_Packet_Size", "Uplink_Packet_Size",
                               "Downlink_Packet_Rate", "Uplink_Packet_Rate"]
    workroomsUlDlDF['dl_kBps'] = workroomsUlDlDF['dl_kBps'] / 1024 / 1024
    workroomsUlDlDF['ul_kBps'] = workroomsUlDlDF['ul_kBps'] / 1024 / 1024

    #Stats
    cols = ['ul_kBps', 'dl_kBps']  # one or more

    SKIP_SAMPLES = 50
    NUM_SAMPLES = 100
    spatialUlDl_50_100_DF = spatialUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = spatialUlDl_50_100_DF[cols].quantile(0.25)
    Q3 = spatialUlDl_50_100_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    spatialUlDl_50_100_DF = spatialUlDl_50_100_DF[~((spatialUlDl_50_100_DF[cols] < (Q1 - 1.5 * IQR)) | (spatialUlDl_50_100_DF[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    spatial_50_100_mean, spatial_50_100_std  = spatialUlDl_50_100_DF[ 'dl_kBps'].agg(['mean', 'std']).values
    # Hubs
    hubsUlDl_50_100_DF = hubsUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = hubsUlDl_50_100_DF[cols].quantile(0.25)
    Q3 = hubsUlDl_50_100_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    hubsUlDl_50_100_DF = hubsUlDl_50_100_DF[
        ~((hubsUlDl_50_100_DF[cols] < (Q1 - 1.5 * IQR)) | (hubsUlDl_50_100_DF[cols] > (Q3 + 1.5 * IQR))).any(
            axis=1)]
    hubs_50_100_mean, hubs_50_100_std = hubsUlDl_50_100_DF['dl_kBps'].agg(['mean', 'std']).values
    # Workrooms
    workroomsUlDl_50_100_DF = workroomsUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = workroomsUlDl_50_100_DF[cols].quantile(0.25)
    Q3 = workroomsUlDl_50_100_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    workroomsUlDl_50_100_DF = workroomsUlDl_50_100_DF[
        ~((workroomsUlDl_50_100_DF[cols] < (Q1 - 1.5 * IQR)) | (workroomsUlDl_50_100_DF[cols] > (Q3 + 1.5 * IQR))).any(
            axis=1)]
    workrooms_50_100_mean, workrooms_50_100_std = workroomsUlDl_50_100_DF['dl_kBps'].agg(
        ['mean', 'std']).values

    SKIP_SAMPLES = 100
    NUM_SAMPLES = 150
    #Spatial
    spatialUlDl_100_150_DF = spatialUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = spatialUlDl_100_150_DF[cols].quantile(0.25)
    Q3 = spatialUlDl_100_150_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    spatialUlDl_100_150_DF = spatialUlDl_100_150_DF[~((spatialUlDl_100_150_DF[cols] < (Q1 - 1.5 * IQR)) | (spatialUlDl_100_150_DF[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    spatial_100_150_mean, spatial_100_150_std  = spatialUlDl_100_150_DF[ 'dl_kBps'].agg(['mean', 'std']).values

    #Hubs
    hubsUlDl_100_150_DF = hubsUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = hubsUlDl_100_150_DF[cols].quantile(0.25)
    Q3 = hubsUlDl_100_150_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    hubsUlDl_100_150_DF = hubsUlDl_100_150_DF[~((hubsUlDl_100_150_DF[cols] < (Q1 - 1.5 * IQR)) | (hubsUlDl_100_150_DF[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    hubs_100_150_mean, hubs_100_150_std = hubsUlDl_100_150_DF['dl_kBps'].agg(['mean', 'std']).values

    #Workrooms
    workroomsUlDl_100_150_DF = workroomsUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = workroomsUlDl_100_150_DF[cols].quantile(0.25)
    Q3 = workroomsUlDl_100_150_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    workroomsUlDl_100_150_DF = workroomsUlDl_100_150_DF[~((workroomsUlDl_100_150_DF[cols] < (Q1 - 1.5 * IQR)) | (workroomsUlDl_100_150_DF[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    workrooms_100_150_mean, workrooms_100_150_std =  workroomsUlDl_100_150_DF[ 'dl_kBps'].agg(['mean', 'std']).values

    SKIP_SAMPLES = 150
    NUM_SAMPLES = 200
    #Spatial
    spatialUlDl_150_200_DF = spatialUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = spatialUlDl_150_200_DF[cols].quantile(0.25)
    Q3 = spatialUlDl_150_200_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    spatialUlDl_150_200_DF = spatialUlDl_150_200_DF[~((spatialUlDl_150_200_DF[cols] < (Q1 - 1.5 * IQR)) | (spatialUlDl_150_200_DF[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    spatial_150_200_mean, spatial_150_200_std  = spatialUlDl_150_200_DF[ 'dl_kBps'].agg(['mean', 'std']).values

    #Hubs
    hubsUlDl_150_200_DF = hubsUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = hubsUlDl_150_200_DF[cols].quantile(0.25)
    Q3 = hubsUlDl_150_200_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    hubsUlDl_150_200_DF = hubsUlDl_150_200_DF[~((hubsUlDl_150_200_DF[cols] < (Q1 - 1.5 * IQR)) | (hubsUlDl_150_200_DF[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    hubs_150_200_mean, hubs_150_200_std = hubsUlDl_150_200_DF['dl_kBps'].agg(
        ['mean', 'std']).values

    # Workrooms
    workroomsUlDl_150_200_DF = workroomsUlDlDF[SKIP_SAMPLES: NUM_SAMPLES]
    Q1 = workroomsUlDl_150_200_DF[cols].quantile(0.25)
    Q3 = workroomsUlDl_150_200_DF[cols].quantile(0.75)
    IQR = Q3 - Q1
    workroomsUlDl_150_200_DF = workroomsUlDl_150_200_DF[~((workroomsUlDl_150_200_DF[cols] < (Q1 - 1.5 * IQR)) | (
                workroomsUlDl_150_200_DF[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]
    workrooms_150_200_mean, workrooms_150_200_std = workroomsUlDl_150_200_DF['dl_kBps'].agg(
        ['mean', 'std']).values


    print("Spatial: 50-100-150 sec")
    print("mean: {}".format([spatial_50_100_mean, spatial_100_150_mean, spatial_150_200_mean]))
    print("std: {}".format([spatial_50_100_std, spatial_100_150_std, spatial_150_200_std]))
    print("Hubs: 50-100-150 sec")
    print("mean: {}".format([hubs_50_100_mean, hubs_100_150_mean, hubs_150_200_mean]))
    print("std: {}".format([hubs_50_100_std, hubs_100_150_std, hubs_150_200_std]))
    print("Workrooms: 50-100-150 sec")
    print("mean: {}".format([workrooms_50_100_mean, workrooms_100_150_mean, workrooms_150_200_mean]))
    print("std: {}".format([workrooms_50_100_std, workrooms_100_150_std, workrooms_150_200_std]))


# User Study Stats
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

    dir_name = 'results/synth7'
    parentDir = os.path.dirname(os.path.realpath(__file__))
    ULDL_2_PATH = os.path.join(parentDir, '..', dir_name, 'ULDL_2.log')
    # charcterize_hubs_stats(ULDL_2_PATH)


    #Comparative Study Stats
    spatial_dir_name = 'results_platforms/uldl'
    hubs_dir_name = 'results_platforms/uldl'
    workrooms_dir_name = 'results_platforms/uldl'
    parentDir = os.path.dirname(os.path.realpath(__file__))
    ULDL_spatial_PATH = os.path.join(parentDir, '..', spatial_dir_name, 'spatial.uldl_4.log')
    ULDL_hubs_PATH = os.path.join(parentDir, '..', hubs_dir_name, 'hubs.uldl_4.log')
    ULDL_workrooms_PATH = os.path.join(parentDir, '..', hubs_dir_name, 'workrooms.uldl_4.log')
    comparative_stats(ULDL_hubs_PATH, ULDL_spatial_PATH, ULDL_workrooms_PATH)

    print("******************************\n User study \n *************************")

    #User Study Stats
    in_dir_name = 'results_ux'
    file_name = '../{}/QoE.csv'.format(in_dir_name)
    VRsurveyDF = pd.read_csv(file_name, sep =',')
    factors = ['frustration', 'mental', 'load', 'immersion','success', 'promise']
    user_dict,user_mean_dict,user_ci_dict, user_std_dict = compute_stats(VRsurveyDF, factors=factors)

    loadMeans = tuple(user_mean_dict.values())
    loadCIs = tuple(user_ci_dict.values())
    loadStds = tuple(user_std_dict.values())
    # print(user_mean_dict.keys())
    # print(loadMeans)
    # print(loadStds)
    # print(loadCIs)
    # print(user_dict)