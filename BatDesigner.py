from abc import ABC


class BatDesigner(ABC):
    def __init__(self):
        self.columns = dict()

        self.columns = {
            "file_path": "FilePath",
            "file_name": "FileName",
            "date": "Date",
            "time": "Time",
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
            "autofilled": "Auto Suggestion",
            "manual_id": "Manual ID",
            "reference_id": "Reference ID",
            "global_10_min_class": "Global 10min Class",
            "*_class": "* Class"
        }
        self.color_wheel_classes = ["00ffefd4", "00fffeef", "00eff0ff"]

    def reversed_columns(self) -> dict:
        values = list(self.columns.values())
        keys = list(self.columns.keys())

        reversed_dict = dict()

        for value in values:
            reversed_dict[value] = keys.pop(0)

        return reversed_dict

    def bat_class(self, bat:str ) -> str:
        format_string = "*_class"
        return format_string.replace("*", bat)

    def bat_class_readable(self, bat: str) -> str:
        format_string = self.columns["*_class"]
        return format_string.replace("*", bat)

    def get_column(self, key: str) -> str:
        split_key = key.split("_")
        if len(split_key) == 2 and split_key[1] == "class":
            return self.bat_class_readable(split_key[0])
        else:
            return self.columns[key]

    def is_row(self, value) -> bool:
        if value in self.columns.keys():
            return True
        else:
            return False
