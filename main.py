import csv
import pickle
import functools
from copy import deepcopy
class Table:
    def __init__(self, data=[]):
        self.filename = ""
        self.data = []
        self.header = []
        self.column_types = {}
    def load_table(self, *filenames):
        try:
            for filename in filenames:
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
                        temp = csv.DictReader(f, delimiter=";", quotechar='"')
                        for x in temp:
                            self.data.append(x)
                elif self.filename.endswith(".pkl"):
                    with open(self.filename, 'rb') as f:
                        self.data = pickle.load(f)
                        self.header = list(self.data.keys())
                else:
                    raise AttributeError("Недоступное расширение!")
            self.header = list(self.data[0].keys())
            self.column_types = self.get_column_types(by_number=False)
        except:
            raise KeyError("Несовместимые имена таблицы!")
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
        elif new_filename.endswith(".pkl"):
            with open(new_filename, "wb") as f:
                pickle.dump(self.data, f)
        else:
            raise AttributeError("Недоступное расширение!")
    @staticmethod
    def concat(table1, table2):
        if isinstance(table1, Table) and isinstance(table2, Table):
            for x in table2.data:
                table1.data.append(x)
        else:
            raise TypeError("Один из элементов не является таблицей!")
    def split(self, row_number):
        other = Table()
        if row_number < len(self.data):
            for i in range(row_number, len(self.data)):
                other.data.append(self.data[i])
            self.data = self.data[:row_number]
            return self, other
        raise ValueError("Некорректный номер строки!")
    def get_rows_by_number(self, start, stop=None, copy_table=False):
        try:
            new_d = self.data.copy() if copy_table else deepcopy(self.data)
            stop = stop if stop else len(new_d) - 1
            return [new_d[i] for i in range(start, stop + 1)]
        except:
            raise ValueError("Произошла непредвиденная ошибка при получении данных из файла")
    def get_rows_by_index(self, *args, copy_table=False):
        try:
            new_d = self.data.copy() if copy_table else deepcopy(self.data)
            res = []
            for lst in new_d:
                if lst[self.header[0]] in args:
                    res.append(lst)
            return res
        except:
            raise ValueError("Произошла непредвиденная ошибка при получении данных из файла")
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
    def get_values(self, column=0):
        if isinstance(column, int):
            column = list(self.data[0].keys())[column]
        return [self.data[i][column] for i in range(len(self.data))]
    def get_value(self, column=0):
        if isinstance(column, int):
            column = list(self.data[0].keys())[column]
        return self.data[0][column]
    def set_values(self, values, column=0):
        if isinstance(column, int):
            column = list(self.data[0].keys())[column]
        for i in range(len(self.data)):
            self.data[i][column] = values[i % len(values)]
    def set_value(self, value, column=0):
        if isinstance(column, int):
            column = list(self.data[0].keys())[column]
        self.data[0][column] = value
    def print_table(self):
        print(*list(self.header), sep=" ")
        for i in range(len(self.data)):
            print(*list(self.data[i].values()), sep=" ")
    @staticmethod
    def merge_tables(table1, table2, by_number=True):
        if isinstance(table1, Table) and isinstance(table2, Table):
            eq_col = list(table1.data.keys()) == list(table2.data.keys())
            if eq_col:
                for x in table2.data:
                    table1.data.append(x)
            raise KeyError("Столбцы не равны или расположены в неправильном порядке!")
        raise TypeError("Один из элементов не является таблицей!")