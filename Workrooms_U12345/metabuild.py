#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time     :2022/1/2 5:45 PM
# @Author   :Ruizhi Cheng




import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
# ROOT = '../'
# FOLDER = 'VC-G2-plain'
U1_FILENAME = 'U1.csv'
U2_FILENAME = 'U2.csv'



#[[trace,label],[trace,label],[trace,label]]
def plot_trace(trace_and_label,xlabel,ylabel):
    x = np.arange(1, len(trace_and_label[0][0]) + 1, 1)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel(xlabel, fontsize=15)
    ax1.set_ylabel(ylabel, fontsize=15)
    for i in range(len(trace_and_label)):
        ax1.plot(x, trace_and_label[i][0],label=trace_and_label[i][1],linewidth = 4)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.tick_params(axis='x', labelsize = 15)
    ax1.tick_params(axis='y', labelsize = 15)
    #ax1.set_ylim([0, 0.031])
    ax1.set_xlim([0, 201])
    plt.grid()

    #this is for G2 share screen
    #plt.legend(fontsize=67,loc='best',bbox_to_anchor=(0.205, 0.60))


    plt.legend(fontsize=18, loc='upper center',ncol=3) #, bbox_to_anchor=(0.5, 1.2)
    #plt.legend(fontsize=60, loc='upper left', bbox_to_anchor=(0, 1.22))

    #this is for change bg
    #plt.legend(fontsize=95, loc='best',bbox_to_anchor=(0.4, 0.43))
    #plt.legend(fontsize=95, loc='upper left',bbox_to_anchor=(0, 1.1))
    plt.show()

def get_col(filename,col_index):
    data = pd.read_csv(filename, encoding='gbk', engine='python', header=None)
    x = data.iloc[1:, col_index].astype(float)
    return np.array(x)

def get_col_label(filename,col_index):
    data = pd.read_csv(filename, encoding='gbk', engine='python', header=None)
    x = data.iloc[0, col_index].astype(str)
    return x

#########it is for U1-U2 bitrate##########
xlabel = 'Time (s)'
ylabel = 'Bitrate (Mbps)'

u1_file = os.path.join(U1_FILENAME)

u1_up_bits = get_col(u1_file,2) /1000000
u1_down_bits = get_col(u1_file,1)/1000000

# u2_file = os.path.join(ROOT,FOLDER,U2_FILENAME)
# u2_up_bits = get_col(u2_file,2)/1000000
# u2_down_bits = get_col(u2_file,1) /1000000
trace1=[[u1_down_bits,'Video Session I'],[u1_up_bits,'Video Session II']]
# trace2=[[u2_up_bits,'Uplink'],[u2_down_bits,'Downlink']]

#########it is for U1-U2 packets##########
# xlabel = 'Time (s)'
# ylabel = 'Packets/s'
#
# u1_file = os.path.join(ROOT,FOLDER,U1_FILENAME)
#
# u1_up_packets = get_col(u1_file,2)
# u1_down_packets = get_col(u1_file,1)
#
# u2_file = os.path.join(ROOT,FOLDER,U2_FILENAME)
# u2_up_packets = get_col(u2_file,2)
# u2_down_packets = get_col(u2_file,1)
# trace1=[[u1_up_packets,'Uplink'],[u1_down_packets,'Downlink']]
# trace2=[[u2_up_packets,'Uplink'],[u2_down_packets,'Downlink']]


#########it is for bit-pakcets plot##########
# xlabel = 'Time (s)'
# ylabel1 = 'Bitrate (Mbit/s)'
# ylabel2 = 'Packets/s'
# bitrate_file = os.path.join(ROOT,FOLDER,U1_FILENAME)
#
# bit_probe = get_col(bitrate_file,1)/1000000
# bit_video = get_col(bitrate_file,2)/1000000
#
# packet_file = os.path.join(ROOT,FOLDER,U2_FILENAME)
# packet_probe = get_col(packet_file,1)
# packet_video = get_col(packet_file,2)
#
#
# trace1 = [[bit_video,'Uplink'],[bit_probe,'Dowlink']]
# trace2 = [[packet_video,'Uplink'],[packet_probe,'Dowlink']]

#########it is for sharing screen ##########
# xlabel = 'Time (s)'
# ylabel = 'Bitrate (Mbit/s)'
# u1_file = os.path.join(ROOT,FOLDER,U1_FILENAME)
#
# u1_sec = get_sec(u1_file)
# u1_probe = get_second_col(u1_file) /1000000
# u1_video = get_third_col(u1_file)/1000000
# u1_sharing_bits = get_fourth_col(u1_file)/1000000
#
# u2_file = os.path.join(ROOT,FOLDER,U2_FILENAME)
# u2_sec = get_sec(u1_file)
# u2_probe = get_second_col(u2_file) /1000000
# u2_video = get_third_col(u2_file)/1000000
# u2_sharing_bits = get_fourth_col(u2_file)/1000000
# trace1=[[u1_probe,'Probe Session'],[u1_video,'Video Session'],[u1_sharing_bits,'Sharing Screen Session']]
# trace2=[[u2_probe,'Probe Session'],[u2_video,'Video Session'],[u2_sharing_bits,'Sharing Screen Session']]
# plot_trace(trace1,xlabel,ylabel)
# plot_trace(trace2,xlabel,ylabel)

########it is for distrupt#######
# xlabel = 'Time (s)'
# ylabel = 'Bitrate (Mbit/s)'
# u1_file = os.path.join(ROOT,FOLDER,U1_FILENAME)
#
# u1_probe = get_second_col(u1_file) /1000000
# u1_video = get_third_col(u1_file)/1000000
# u1_vb_downlink = get_fourth_col(u1_file)/1000000
#
# u2_file = os.path.join(ROOT,FOLDER,U2_FILENAME)
# u2_probe = get_second_col(u2_file) /1000000
# u2_video = get_third_col(u2_file)/1000000
# u2_vb_downlink = get_fourth_col(u2_file)/1000000
# trace1=[[u1_probe,'Probe Session'],[u1_video,'Video Session'],[u1_vb_downlink,'VB Flow Downlink']]
# trace2=[[u2_probe,'Probe Session'],[u2_video,'Video Session'],[u2_vb_downlink,'VB Flow Downlink']]



plot_trace(trace1,xlabel,ylabel)
# plot_trace(trace2,xlabel,ylabel)
