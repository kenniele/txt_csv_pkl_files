import csv
import pickle
import functools
from copy import deepcopy
class Table:
    def __init__(self):
        self.filename = ""
        self.data = []
        self.header = []
    def load_table(self, filename):
        self.filename = filename
        self.data = []
        if self.filename.endswith(".txt"):
            with open(self.filename, encoding="utf-8") as f:
                self.header = f.readline().split()
                temp = [x.split() for x in f]
                for row in temp:
                    self.data.append({})
                    for pair in zip(self.header, row):
                        self.data.update({pair[0]: pair[1]})
        elif self.filename.endswith(".csv"):
            with open(self.filename, encoding="utf-8") as f:
                temp = csv.DictReader(f, quotechar='"')
        elif self.filename.endswith(".pkl"):
            with open(self.filename, 'rb') as f:
                self.data = pickle.load(f)
                self.header = list(self.data.keys())
        else:
            raise ValueError("Недоступное расширение!")
    def save_table(self, new_filename):
        if new_filename.endswith(".txt"):
            with open(new_filename, 'w', encoding='utf-8') as f:
                f.write('\t'.join(self.data[0].keys()))
                for row in self.data:
                    f.write('\t'.join(row.values()))
        elif new_filename.endswith(".csv"):
            with open(new_filename, 'w', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)
                for row in self.data:
                    writer.writerow(row.values())
    def get_rows_by_number(self, start, stop=None, copy_table=False):
        new_d = self.data.copy() if copy_table else deepcopy(self.data)
        stop = stop if stop else len(new_d)
        return [new_d[i] for i in range(start, stop)]
    def get_rows_by_index(self, *args, copy_table=False):
        new_d = self.data.copy() if copy_table else deepcopy(self.data)
        res = []
        for lst in new_d:
            if lst[self.header[0]] in args:
                res.append(lst)
        return res
    def get_column_types(self, by_number=True):
        res = {}
        for i in range(len(self.header)):
            try:
                tpy = ''
                if self.data[0][self.header[i]] in ('True', 'False', 'true', 'false'):
                    tpy = 'bool'
                elif str(int(self.data[0][self.header[i]])) == self.data[0][self.header[i]]:
                    tpy = 'int'
                elif str(float(self.data[0][self.header[i]])) == self.data[0][self.header[i]]:
                    tpy = 'float'
            except ValueError:
                tpy = 'str'
            if by_number:
                res[i] = tpy
            else:
                res[self.header[i]] = tpy
        return res
    def set_column_types(self, types_dict, by_number=True):
        for lst in self.data:
            for i in len(self.header):
                exec(f"lst[self.header[i]] = {types_dict[[self.header[i], i][by_number]]}(lst[self.header[i]])")
