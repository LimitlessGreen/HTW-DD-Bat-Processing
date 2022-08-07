import BatWorkbook
workbook = BatWorkbook.BatWorkbook(path=".")
designer = workbook.get_designer()

designer.color_wheel_classes = ["00ffefd4", "00fffeef", "00eff0ff"]
designer.add_extra_bats(["Pnat", "Nnoc", "Nlei", "Vmur", "Eser", "Enil", "NSL(unbestimmt)", "Hsav", "Mmyo", "Mdas"])

standort_1 = workbook.new_sheet(".", ".")
standort_1.print_statistics()
standort_1.reduce("Ppip", 0.92)
standort_1.reduce("Ppyg", 0.92)

#print(standort_1.bat_csv["Time"])   
#standort_1.print_classification_progress()

#standort_1.export_excel("Test_Excel")
standort_1.import_excel(f"{standort_1.path}/Test_Excel.xlsx", one_file=True)
