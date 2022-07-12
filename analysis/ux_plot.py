import pandas as pd
import matplotlib.pyplot as plt
import os, math

def compute_stats(VRsurveyDF, factors):
    user_dict = {}
    user_mean_dict = {}
    user_ci_dict = {}

    for factor in factors:
        factSeries = pd.Series(VRsurveyDF[factor])
        factSeries = pd.to_numeric(factSeries)
        stats_fact = factSeries.describe()
        # Frustration
        m, c, s = stats_fact['mean'], stats_fact['count'], stats_fact['std']
        ci95 = 1.96 * s / math.sqrt(c)
        user_dict[factor] = {m, ci95}
        user_mean_dict[factor] = m
        user_ci_dict[factor] = ci95

    return user_dict, user_mean_dict, user_ci_dict

def categorize_DF(VRsurveyDF):
    VRloadDF = VRsurveyDF[['frustration', 'load', 'mental']]
    VRloadDF = VRloadDF.assign(type='Load')
    VRmeasureDF = VRsurveyDF[['immersion', 'promise', 'success']]
    VRmeasureDF = VRmeasureDF.assign(type='VRMeasure')

    surveyDF = pd.concat([VRloadDF, VRmeasureDF], ignore_index=True)
    return surveyDF

if __name__ == '__main__':

    in_dir_name = 'results_ux'
    file_name = '../{}/VRsurvey.csv'.format(in_dir_name)
    VRsurveyDF = pd.read_csv(file_name, sep =',')
    factors = ['frustration', 'mental', 'load', 'immersion','success']
    user_dict,user_mean_dict,user_ci_dict = compute_stats(VRsurveyDF, factors=factors)

    loadMeans = tuple(user_mean_dict.values())
    loadCIs = tuple(user_ci_dict.values())

    # create figure and axis objects with subplots()
    fig, ax = plt.subplots(figsize=(10,7))
    width = 0.4
    colors = ['skyblue','dodgerblue', 'blue']
    p1 = ax.bar(1, user_mean_dict['frustration'], width, yerr=user_ci_dict['frustration'], color='skyblue', log=False,
                error_kw=dict(elinewidth=2, ecolor='black'))
    p2 = ax.bar(2, user_mean_dict['mental'], width, yerr=user_ci_dict['mental'], color='skyblue', log=False,
                 error_kw=dict(elinewidth=2, ecolor='black'))
    p3 = ax.bar(3, user_mean_dict['success'], width, yerr=user_ci_dict['success'], color='skyblue', log=False,
                 error_kw=dict(elinewidth=2, ecolor='black'))
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.tick_params(axis='both', which='minor', labelsize=12)

    # # twin object for two different y-axis on the sample plot
    ax2 = ax.twinx()
    p4 = ax2.bar(4, user_mean_dict['immersion'], width, yerr=user_ci_dict['immersion'], color='darkblue', log=False,
                 error_kw=dict(elinewidth=2, ecolor='gray'))
    p5 = ax2.bar(5, user_mean_dict['load'], width, yerr=user_ci_dict['load'], color='darkblue', log=False,
                 error_kw=dict(elinewidth=2, ecolor='gray'))
    factors = ['', 'frustration', 'mental', 'success', 'immersion', 'load']
    ax2.spines['top'].set_visible(False)
    ax2.tick_params(axis='both', which='major', labelsize=15)
    ax2.tick_params(axis='both', which='minor', labelsize=12)
    ax.set_xticklabels(factors)

    parentDir = os.path.dirname(os.path.realpath(__file__))
    Fig_PATH = os.path.join(parentDir, 'figures', 'QoE.pdf')
    plt.savefig(Fig_PATH, bbox_inches='tight')
    plt.show()
