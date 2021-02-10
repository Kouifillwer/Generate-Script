import pandas
import tkinter
from tkinter import messagebox
from OOP.read import Readfile


# Readfile
file_name = input("Enter file name: ")
# file_name = 'ETL_DATA_PLANING'
planing_list = pandas.read_excel(f'{file_name}.xlsx', sheet_name='Planning')
planing_list = pandas.DataFrame.to_dict(planing_list)

# Declare
# planning_name = list(planing_list['NE_NAME'])
planning_name = planing_list['NE_NAME']
# nan = numpy.nan
Frequency_list = ['BCCH', 'TCH1', 'TCH2', 'TCH3', 'TCH4', 'TCH5', 'TCH6', 'TCH7', 'TCH8']
all_basic_data = []
all_frequency_data = []
all_ip_data = []

readfile = Readfile()
m_neighbor = readfile.schema_info()
m_McellList = readfile.schema_MCellList()
neightbor_list = readfile.neigbor_list(file_name)
DATA = pandas.DataFrame(neightbor_list)

NE_NAME = list(neightbor_list['SITE_NAME'])
NAME_LIST = []
INFO_EM = []
myDict = {}
toDict = {}

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


for name in NE_NAME:
    if name not in NAME_LIST:
        NAME_LIST.append(name)
    pass

for name in NAME_LIST:
    myDict[name] = {
        "NeighborCellID": list(DATA.NeighborCellID[DATA['SITE_NAME'] == f"{name}"]),
        "NeighborCellBSIC": list(DATA.NeighborCellBSIC[DATA['SITE_NAME'] == f"{name}"]),
        "NeighborCellARFCN": list(DATA.NeighborCellARFCN[DATA['SITE_NAME'] == f"{name}"]),
        "NeighborCellLAC": list(DATA.NeighborCellLAC[DATA['SITE_NAME'] == f"{name}"])
    }

def adding_neighbor(passingname):
    global m_neighbor
    neighbors = []
    if passingname in myDict:
        number_of_list = len(myDict[f'{passingname}']['NeighborCellID'])
        Mlist_neighbor = m_McellList.replace("[NBC_ARFCN_LIST]",
                                      f"{str(myDict[f'{passingname}']['NeighborCellARFCN'])[1:-1]}")
        neighbors.append(f"{Mlist_neighbor}" + "\n")
        for i in range(0, number_of_list):
            HONeighborCellID = i + 1
            new_neighbor = m_neighbor.replace(f"[HONeighborCellID]", f"{HONeighborCellID}")
            new_neighbor = new_neighbor.replace("[NeighborCellID]",
                                                f"{str(myDict[f'{passingname}']['NeighborCellID'][i])}")
            new_neighbor = new_neighbor.replace("[NeighborCellBSIC]",
                                                f"{str(myDict[f'{passingname}']['NeighborCellBSIC'][i])}")
            new_neighbor = new_neighbor.replace("[NeighborCellARFCN]",
                                                f"{str(myDict[f'{passingname}']['NeighborCellARFCN'][i])}")
            new_neighbor = new_neighbor.replace("[NeighborCellLAC]",
                                                f"{str(myDict[f'{passingname}']['NeighborCellLAC'][i])}")
            neighbors.append(f"{new_neighbor}" + "\n")
    return neighbors

def generate():
    # Loop file
    # loop to get Basic information and append to list
    global final
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
            if check_nan[frequency] == 'None':
                pass
            elif lable in Frequency_list:
                time_id += 1
                script_frequency = f'set Carrier:ARFCN="{planing_list[f"{lable}"][frequency]}", CarrierID="{time_id}";'
                new_script += script_frequency
        all_frequency_data.append(new_script)

    # Loop to get IP and append to list
    for ip in range(0, len(planing_list['NE_NAME'])):
        new_ip_info = set_ip_info.replace("[WANIP]", f"{planing_list['WANIP'][ip]}")
        new_ip_info = new_ip_info.replace("[WANGATEWAY]", f"{planing_list['WANGATEWAY'][ip]}")
        all_ip_data.append(new_ip_info)

    # Do this to enter new line for each line
    all_frequency_data2 = [word.replace(';', ';\n') for word in all_frequency_data]


    # Loop all planning name and make script
    for i in planning_name:
        if planning_name[i] in NAME_LIST:
            passingname = planning_name[i]
            # print(passingname)
            # print("ok")
            neighbors = adding_neighbor(passingname)
            # print(print(len(neighbors)))
            neigbor_each_row = ''
            for nei in range(0, len(neighbors)):
                # print(nei)
                neigbor_each_row += neighbors[nei]
                final = all_basic_data[i] + '\n' + all_frequency_data2[i] + set_channel_info + '\n' \
                        + all_ip_data[i]  + neigbor_each_row
            # print(final)
            name = passingname
            with open(f"Results/{name}.txt", mode="w") as make_script:
                make_script.write(final)

        elif planning_name[i] not in NAME_LIST:
            final = all_basic_data[i] + '\n' + all_frequency_data2[i] + set_channel_info + '\n' \
                    + all_ip_data[i]
            name = planning_name[i]
            with open(f"Results/{name}.txt", mode="w") as make_script:
                make_script.write(final)
            pass
is_not_type = True
# generate()

while is_not_type is True:
    check = input("Type 'y' to generate script 'n' to exit: ").lower()
    if check[0] == 'y':
        generate()
        print("Finished")
        # This code is to hide the main tkinter window
        root = tkinter.Tk()
        root.withdraw()

        # Message Box
        is_not_type = False
        messagebox.showinfo("ETL Generator", "ສຳເລັດການ GENERATE")
    elif check[0] == 'n':
        print("NOT GENERATE YET")
        is_not_type = False
        root = tkinter.Tk()
        root.withdraw()

        # Message Box
        messagebox.showinfo("ETL Generator", "ເຈົ້າຍັງບໍ່ທັນໃດ້ generate")
