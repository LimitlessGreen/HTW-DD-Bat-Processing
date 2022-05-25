from BatWorksheet import BatWorksheet


class BatWorkbook:
    def __init__(self, path):
        self.base_path = path
        self.sheets = dict()

    def new_sheet(self, location, date, threshold_b=0.5, threshold_m=0.5,  threshold_p=0.92, threshold_other=0.4) -> BatWorksheet:
        sheet = BatWorksheet(f"{self.base_path}/{location}", date, threshold_b, threshold_m, threshold_p, threshold_other)
        self.sheets[location] = sheet
        sheet.get_csv()
        return sheet