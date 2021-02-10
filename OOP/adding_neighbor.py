import pandas
from read import Readfile

readfile = Readfile()
m_neighbor = readfile.schema_info()
neightbor_list = readfile.neigbor_list()
DATA = pandas.DataFrame(neightbor_list)

NE_NAME = list(neightbor_list['SITE_NAME'])
NAME_LIST = []
INFO_EM = []
myDict = {}
toDict = {}

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

nb = []
def add_n():
    for get_name in myDict:
        number_of_list = len(myDict[f'{get_name}']['NeighborCellID'])
        for i in range(0, number_of_list):
            HONeighborCellID = i + 1
            new_neighbor = m_neighbor.replace("[NBC_ARFCN_LIST]",
                                              f"{str(myDict[f'{get_name}']['NeighborCellARFCN'])[1:-1]}")
            new_neighbor = new_neighbor.replace(f"[HONeighborCellID]", f"{HONeighborCellID}")
            new_neighbor = new_neighbor.replace("[NeighborCellID]",
                                                f"{str(myDict[f'{get_name}']['NeighborCellID'][i])}")
            new_neighbor = new_neighbor.replace("[NeighborCellBSIC]",
                                                f"{str(myDict[f'{get_name}']['NeighborCellBSIC'][i])}")
            new_neighbor = new_neighbor.replace("[NeighborCellARFCN]",
                                                f"{str(myDict[f'{get_name}']['NeighborCellARFCN'][i])}")
            new_neighbor = new_neighbor.replace("[NeighborCellLAC]",
                                                f"{str(myDict[f'{get_name}']['NeighborCellLAC'][i])}")
            # print(i)
            # print(new_neighbor)
            nb.append(f"{new_neighbor}")
add_n()
# print(nb[0])
for i in range(0, len(nb)):
    print(nb[i])


