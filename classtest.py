import BatWorkbook
workbook = BatWorkbook.BatWorkbook(path=".")
designer = workbook.get_designer()

designer.color_wheel_classes = ["00ffefd4", "00fffeef", "00eff0ff"]


standort_1 = workbook.new_sheet(".", ".")
standort_1.print_statistics()
standort_1.reduce("Ppip", 0.92)
standort_1.reduce("Ppyg", 0.92)

#print(standort_1.bat_csv["Time"])   
standort_1.print_classification_progress()

standort_1.export_excel("Test_Excel")
