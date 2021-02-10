import pandas
import numpy
import tkinter
from tkinter import messagebox

nan = numpy.nan
Frequency_list = ['BCCH', 'TCH1', 'TCH2', 'TCH3', 'TCH4', 'TCH5', 'TCH6', 'TCH7', 'TCH8']
all_basic_data = []
all_frequency_data = []
all_ip_data = []
# file_name = input("Enter file name: ")
file_name = 'Data'

planing_list = pandas.read_csv(f'{file_name}.csv')
planing_list = pandas.DataFrame.to_dict(planing_list)



# Readfile *************************
# Set basic info
with open("./Schema/SET_BASIC_INFO.txt") as basic_file_txt:
    set_basic_info = basic_file_txt.read()

# Set channelDescription
with open("./Schema/SET_CHANNEL.txt") as channel_file_txt:
    set_channel_info = channel_file_txt.read()

# Set IP
with open("./Schema/SET_IP.txt") as ip_file_txt:
    set_ip_info = ip_file_txt.read()


def generate():
    # Loop file
    # loop to get Basic information and append to list
    for row in range(0, len(planing_list['NE_NAME'])):
        new_basic_info = set_basic_info.replace("[LAC]", f"{planing_list['LAC'][row]}")
        new_basic_info = new_basic_info.replace("[MCC]", f"{planing_list['MCC'][row]}")
        new_basic_info = new_basic_info.replace("[MNC]", f"{planing_list['MNC'][row]}")
        new_basic_info = new_basic_info.replace("[NCC]", f"{planing_list['NCC'][row]}")
        new_basic_info = new_basic_info.replace("[BCC]", f"{planing_list['BCC'][row]}")
        new_basic_info = new_basic_info.replace("[CELLID]", f"{planing_list['CELLID'][row]}")
        # print(f"{new_basic_info}")
        all_basic_data.append(new_basic_info)
    # print(all_basic_data[0])

    # Loop to get frequency and append to list
    for frequency in range(0, len(planing_list['NE_NAME'])):
        new_script = ""
        # print(loop)
        time_id = 0
        for lable in planing_list:
            check_nan = planing_list[f"{lable}"]
            # print(lable)
            if check_nan[frequency] == 'None' or check_nan[frequency] is numpy.isnan(0):
                pass
            elif lable in Frequency_list:
                # print(time_id)
                time_id += 1
                script_frequency = f'set Carrier:ARFCN="{planing_list[f"{lable}"][frequency]}", CarrierID="{time_id}";'
                # print(script_frequency)
                new_script += script_frequency
        all_frequency_data.append(new_script)

    # Loop to get IP and append to list
    for ip in range(0, len(planing_list['NE_NAME'])):
        new_ip_info = set_ip_info.replace("[WANIP]", f"{planing_list['WANIP'][ip]}")
        new_ip_info = new_ip_info.replace("[WANGATEWAY]", f"{planing_list['WANGATEWAY'][ip]}")
        all_ip_data.append(new_ip_info)

    all_frequency_data2 = [word.replace(';', ';\n') for word in all_frequency_data]

    # Adding neighbor
    # if


    # print(all_frequency_data2)
    # for i in range(0, len(all_frequency_data)):
    #     final = all_basic_data[i] + '\n' + all_frequency_data2[i] + set_channel_info + '\n' + all_ip_data[i]
    #     name = planing_list['NE_NAME'][i]
    #     with open(f"Results/{name}.txt", mode="w") as make_script:
    #         make_script.write(final)
        # print(final)
        # print("**************************************************")
    for i in range(0, len(all_frequency_data)):

        final = all_basic_data[i] + '\n' + all_frequency_data2[i] + set_channel_info + '\n' + all_ip_data[i]
        name = planing_list['NE_NAME'][i]
        with open(f"Results/{name}.txt", mode="w") as make_script:
            make_script.write(final)

is_not_type = True

print(planing_list['NE_NAME'])
# generate()
# while is_n
# ot_type is True:
#     check = input("Type 'y' to generate script 'n' to exit: ").lower()
#     if check[0] == 'y':
#         generate()
#         print("Finished")
#         # This code is to hide the main tkinter window
#         root = tkinter.Tk()
#         root.withdraw()
#
#         # Message Box
#         is_not_type = False
#         messagebox.showinfo("ETL Generator", "ສຳເລັດການ GENERATE")
#     elif check[0] == 'n':
#         print("NO")
#         is_not_type = False
#         root = tkinter.Tk()
#         root.withdraw()
#
#         # Message Box
#         messagebox.showinfo("ETL Generator", "ເຈົ້າຍັງບໍ່ທັນໃດ້ generate")
