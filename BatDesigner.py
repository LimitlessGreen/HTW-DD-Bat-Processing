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

    def bat_class(self, bat):
        format_string = "*_class"
        return format_string.replace("*", bat)

    def bat_class_readable(self, bat):
        format_string = self.columns["*_class"]
        return format_string.replace("*", bat)
