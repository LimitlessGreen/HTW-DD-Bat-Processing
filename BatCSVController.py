from BatDesigner import BatDesigner
from abc import ABC
import chardet
import pandas as pd


class BatCSVController(ABC):
    __csv_columns = {
        "FilePath": "file_path",
        "FileName": "file_name",
        "Date": "date",
        "Time": "time",
        "Bbar": "Bbar",
        "Malc": "Malc",
        "Mbec": "Mbec",
        "MbraMmys": "MbraMmys",
        "Mdau": "Mdau",
        "Mnat": "Mnat",
        "NSL": "NSL",
        "Paur": "Paur",
        "Ppip": "Ppip",
        "Ppyg": "Ppyg",
        "Rfer": "Rfer",
        "Rhip": "Rhip",
    }

    def __init__(self):
        self.bat_csv = pd.DataFrame()
        self.location = ""
        self.date = ""
        self.designer = BatDesigner()



    def _group_bats(self):
        pass

    def _init_bat_counter(self):
        pass

    def _autofill_results(self):
        pass

    def get_csv(self):
        self.__csv_importer()
        self._group_bats()
        self._init_bat_counter()
        self._autofill_results()

    def __csv_importer(self):
        # print(f"{self.location}/{self.date}/BatClassify_Ergebnisse/Results.csv")
        path = f"{self.location}/{self.date}/BatClassify_Ergebnisse/Results.csv"

        # get encoding of file
        with open(path, 'rb') as f:
            data = f.read()  # or a chunk, f.read(1000000)
        f.close()

        encoding = chardet.detect(data).get("encoding")
        print(encoding)
        self.bat_csv = pd.read_csv(path, encoding=encoding)
        # rename to internal representation
        self.bat_csv.rename(columns=self.__csv_columns, inplace=True)
        print (self.bat_csv)

        # print(self.bat_csv.columns)

