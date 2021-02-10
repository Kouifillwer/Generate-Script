import pandas
import csv

class Readfile:

    def neigbor_list(self, inputName):
        self.neigbor_list = pandas.read_excel(f'{inputName}.xlsx', sheet_name='Neighbor')
        return self.neigbor_list

    def schema_info(self):
        with open('Schema/SET_Neighbor.txt') as neighbor_txt:
            self.set_neigbor = neighbor_txt.read()
            return self.set_neigbor

    def schema_MCellList(self):
        with open('Schema/MCellList.txt') as mcell_txt:
            self.Mcell_neighbor = mcell_txt.read()
            return self.Mcell_neighbor




