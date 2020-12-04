import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ppcs_data = {}
agc_data = {}
normal_signal = None

ppcs_conf = {'signal_start' : 200, 'signal_end' : 1500, 'col_freq' : 2, 'lower_step' : 15, 'delay_start': 800, 'delay_range' : 50}
agc_conf = {'signal_start' : 20, 'signal_end' : 300, 'col_freq' : 4, 'lower_step' : 4, 'delay_start': 100, 'delay_range' : 10}

def get_array_from_str(inp_str):
    arr = []
    term_arr = inp_str.split("\n")
    for ele in term_arr:
        temp = ele
        temp = temp.replace('[', '')
        temp = temp.replace(']', '')
        arr.append(float(temp))
    return arr

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def load_data():
    global ppcs_data
    global agc_data
    global normal_signal

    data_df = pd.read_csv('polls/dataset/ppcs_with_predictions.csv')
    for index, row in data_df.iterrows():
        # print(row[:10])
        row_arr = np.array(row)
        # print(row_arr[:20])
        # exit()
        ppcs_data[(int(row['delay']), int(row['delay_st']))] = (row_arr[9+2*651:9+3*651], row['reg_loc_arr'], row['cls_loc_arr'],
                                                                row['reg_out_arr'], row['cls_out_arr'],
                                                                get_array_from_str(row['reg_complete_arr']), get_array_from_str(row['cls_complete_arr']))
        # exit()

    data_df = pd.read_csv('polls/dataset/agc_with_predictions.csv')
    for index, row in data_df.iterrows():
        # print(row[:10])
        row_arr = np.array(row)
        # print(row_arr[:20])
        # exit()
        agc_data[(int(row['delay']), int(row['delay_st']))] = (row_arr[9+1*76:9+1*76+71], row['reg_loc_arr'], row['cls_loc_arr'],
                                                                row['reg_out_arr'], row['cls_out_arr'],
                                                                get_array_from_str(row['reg_complete_arr']), get_array_from_str(row['cls_complete_arr']))
        # exit()


    # for ele in ppcs_data:
    #     if(ele[0]==0):
    #         normal_signal = ppcs_data[ele][0]

    # average_normal = moving_average(normal_signal, 50)

def plot_main_signal(signal_arr, gt_data, conf, protection):
    global normal_signal

    y_arr = range(conf['signal_start'], conf['signal_end'] + conf['col_freq'], conf['col_freq'])
    # print(signal_arr[0])
    ymax = np.max(signal_arr[0])
    ymin = np.min(signal_arr[0])
    yrange = ymax - ymin
    plt.plot(y_arr, signal_arr[0], color='brown')
    # plt.plot(y_arr[49:], moving_average(normal_signal, 50), color='green')
    plt.vlines(x=gt_data[1], ymin=ymin, ymax=ymax, color='red')
    plt.text(conf['signal_start'], ymin + yrange*0.12, "Delay Attack : " + str(gt_data[0]) + " sec, launched at t=" + str(gt_data[1]), color="red")
    print(protection)
    if(signal_arr[4]==1 and protection=="True"):
        plt.vlines(x=signal_arr[2] + conf['col_freq']*conf['lower_step'], ymin=ymin, ymax=ymax, color='blue')
        plt.text(conf['signal_start'], ymin + yrange*0.06, "Attack Detected at t=" + str(signal_arr[2]), color="blue")
        plt.vlines(x=signal_arr[1] + conf['col_freq']*conf['lower_step'], ymin=ymin, ymax=ymax, color='green')
        plt.text(conf['signal_start'], ymin, "Delay Value Predicted : " + str(int(signal_arr[3])) + " sec, at t=" + str(signal_arr[1]), color="green")

    plt.title("Original Signal Input")

    fig = plt.gcf()
    fig.set_facecolor("yellow")
    fig.set_size_inches(12, 4)
    # os.remove('polls/static/polls/signal.png')
    fig.savefig('polls/static/polls/signal.png')
    fig.clf()

def plot_classification(signal_arr, gt_data, conf):
    y_arr = range(conf['signal_start'], conf['signal_end'] + conf['col_freq'], conf['col_freq']*conf['lower_step'])
    x_arr = []
    # print(signal_arr)
    counter = 0
    for ele in y_arr:
        if(counter>=len(signal_arr[6])):
            break
        # if(ele <= (conf['delay_start'] + conf['col_freq']*conf['lower_step'])):
        if(ele <= (conf['delay_start'])):
            x_arr.append('No Attack')
            continue
        elif(signal_arr[6][counter] > 0.5):
            x_arr.append('Attack')
        else:
            x_arr.append('No Attack')
        counter += 1

    plt.plot(y_arr[-len(x_arr):], x_arr, color='blue')
    # plt.yticks([0, 1])
    plt.title("Classification Head Output (Updated every " +  str(conf['col_freq']*conf['lower_step']) + " sec)")
    fig = plt.gcf()
    fig.set_facecolor("yellow")
    fig.set_size_inches(12, 2)
    # os.remove('polls/static/polls/classification.png')
    fig.savefig('polls/static/polls/classification.png')
    fig.clf()

def plot_regression(signal_arr, gt_data, conf):
    y_arr = range(conf['signal_start'], conf['signal_end'] + conf['col_freq'], conf['col_freq']*conf['lower_step'])
    x_arr = []
    counter = 0
    for ele in y_arr:
        if(counter>=len(signal_arr[6])):
            break
        # if(ele <= (conf['delay_start'] + conf['col_freq']*conf['lower_step'])):
        if(ele <= (conf['delay_start'])):
            x_arr.append(0)
            continue
        else:
            x_arr.append(signal_arr[5][counter]*conf['delay_range'])
        counter += 1

    plt.plot(y_arr[-len(x_arr):], x_arr, color='green')
    plt.yticks([0, 10, 20, 30, 40, 50])
    plt.title("Regression Head Output (Updated every " +  str(conf['col_freq']*conf['lower_step']) + " sec)")
    fig = plt.gcf()
    fig.set_facecolor("yellow")
    fig.set_size_inches(12, 2)
    # os.remove('polls/static/polls/classification.png')
    fig.savefig('polls/static/polls/regression.png')
    fig.clf()

def create_graphs(arg_dict):
    global ppcs_data
    global agc_data
    global ppcs_conf
    global agc_conf

    if(arg_dict["system"]=='ppcs'):
        system_conf = ppcs_conf
        data_dict = ppcs_data
    else:
        system_conf = agc_conf
        data_dict = agc_data

    best_match = None
    min_distance = 5000
    for ele in data_dict:
        if(ele[0]==arg_dict["tda_value"]):
            if(abs(ele[1] - arg_dict['tda_location']) < min_distance):
                min_distance = abs(ele[1] - arg_dict['tda_location'])
                best_match = (ele[0], ele[1])

    print("Best Match : ", best_match)

    plot_main_signal(data_dict[best_match], best_match, system_conf, arg_dict["protection"])

    if(arg_dict["protection"]=="True"):
        plot_classification(data_dict[best_match], best_match, system_conf)
        plot_regression(data_dict[best_match], best_match, system_conf)
