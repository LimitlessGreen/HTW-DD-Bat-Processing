# imports

from BatExcelController import BatExcelController
from BatCSVController import BatCSVController
from BatDesigner import BatDesigner

from cmath import nan
import pandas as pd
import numpy as np
import datetime

#beginning_with_B = 0.5
#beginning_with_M = 0.5
#beginning_with_P = 0.92

# accept the max value below them above
#beginning_other = 0.4

# Wenn Ppip und NSL, dann Pnat


class BatWorksheet(BatExcelController, BatCSVController):
    def __init__(self, location, date, designer: BatDesigner, threshold_b=0.5, threshold_m=0.5, threshold_p=0.92, threshold_other=0.4):
        super().__init__()
        self.threshold_b = threshold_b  # default 0.5
        self.threshold_m = threshold_m  # default 0.5
        self.threshold_p = threshold_p  # default 0.92
        self.threshold_other = threshold_other

        self.location = location
        self.date = date
        self.path = f"{self.location}/{self.date}"

        self.bat_counter = dict()
        self.all_bats = list()
        
        self.bat_thresholds = dict()

        self.bat_csv = pd.DataFrame
        self.po_bats = pd.DataFrame
        self.reduced_datasets = list()

        self.ten_minute_intervals = list()
        self.ten_minute_classes = list()

        pd.options.mode.chained_assignment = None  # default='warn'

        self.designer = designer

    def _group_bats(self):
        extra_bats = self.designer.extra_bats       
        header = self.bat_csv.columns.tolist()
        
        for item in extra_bats:
            header.append(item)
        
        bats_with_b = [x for x in header if x.startswith("B")]
        bats_with_m = [x for x in header if x.startswith("M")]
        bats_with_p = [x for x in header if x.startswith("P")]
        other_bats = [x for x in header if x not in header[0:4] + bats_with_b + bats_with_m + bats_with_p]
        self.all_bats = [x for x in header if x not in header[0:4]]
        
        # Sort alphabetically
        bats_with_b.sort()
        bats_with_m.sort()
        bats_with_p.sort()
        self.all_bats.sort()
        other_bats.sort()
        
        for bat in self.all_bats:
            if bat in bats_with_b:
                self.bat_thresholds[bat] = self.threshold_b
            
            elif bat in bats_with_m:
                self.bat_thresholds[bat] = self.threshold_m
            
            elif bat in bats_with_p:
                self.bat_thresholds[bat] = self.threshold_p 
            
            else:
                self.bat_thresholds[bat] = self.threshold_other
        
    def _init_bat_counter(self):
        # initialize bat_counter
        for bat in self.all_bats:
            self.bat_counter[bat] = 0
            
    def _autofill_results(self):
        auto_result = "autofilled"
        ten_min = "global_10_min_class"
       
        last_time = 0
        self.bat_csv[auto_result] = ""
        self.bat_csv["manual_id"] = ""
        self.bat_csv["reference_id"] = ""
        self.bat_csv[ten_min] = ""

        # Columns for 10 min classes
        for bat in self.all_bats:
            class_name = self.designer.bat_class(bat)
            self.bat_csv[class_name] = ""
            self.ten_minute_classes.append(class_name)

        #self.bat_csv["Test"] = ""

        for ind in self.bat_csv.index:
            max_bat_value = 0
            max_bat_name = ""

            for bat in self.all_bats:
                # continue, if bat was not in the original CSV
                if "" in self.bat_csv.get(bat, default=""): continue
                
                value = self.bat_csv[bat][ind]
                if value > max_bat_value:
                    max_bat_value = value
                    max_bat_name = bat

                # Add to auto filled column, if in thresholds
                if self.bat_csv[bat][ind] >= self.bat_thresholds[bat]:
                    self.bat_csv[auto_result][ind] = self.bat_csv[auto_result][ind] + bat + ", "
                    self.bat_counter[bat] += 1

            # Accept also values lower the given
            if (self.bat_csv[auto_result][ind] == '') and max_bat_value >= self.threshold_other:
                self.bat_csv[auto_result][ind] = self.bat_csv[auto_result][ind] + max_bat_name + ", "
                self.bat_counter[max_bat_name] += 1

            # Workaround for special case: Pnat
            if ("Ppip" in self.bat_csv[auto_result][ind]) and ("NSL" in self.bat_csv[auto_result][ind]):
                self.bat_csv[auto_result][ind] = self.bat_csv[auto_result][ind] + "Pnat" + ", "
                self.bat_counter["Pnat"] += 1

            # Remove final ', '
            if self.bat_csv[auto_result][ind] != '':
                self.bat_csv[auto_result][ind] = self.bat_csv[auto_result][ind][:-2]

            ###############
            # Date / Time #  parsed from FileName
            ###############

            file_name = str(self.bat_csv["file_name"][ind])
            split_name = file_name.split("_")
            date = split_name[-3]
            time = split_name[-2]
            date_time = f"{date} {time}"
            date_time_obj = datetime.datetime.strptime(date_time, '%Y%m%d %H%M%S')

            self.bat_csv['date'][ind] = pd.to_datetime(date_time_obj).date()
            self.bat_csv['time'][ind] = pd.to_datetime(date_time_obj).time()
            
            ##################
            # 10 min classes #
            ##################
            
            date_time_obj = date_time_obj.replace(
                second=0,
                minute=date_time_obj.minute//10*10) # round to lower 10 minutes (f.ex. 39 -> 30)
            #self.bat_csv["Test"][ind] = pd.to_datetime(date_time_obj).time()
            
            if last_time == 0:
                last_time = date_time_obj
                self.bat_csv[ten_min][ind] = 1 # first item is always a 10 min class
                self.ten_minute_intervals.append(ind)
                continue
            
            time_delta = date_time_obj - last_time
            time_delta_minutes = time_delta.total_seconds() / 60
            #print(time_delta_minutes)
            
            if time_delta_minutes >= 10:
                self.bat_csv[ten_min][ind] = 1
                self.ten_minute_intervals.append(ind)
                last_time = date_time_obj
                #print(time_delta_minutes)

        # Cut Path to relative
        self.bat_csv["file_path"] = f"{self.location}/{self.date}/Analyse_Ergebnisse"

    def print_statistics(self):
        #print(f"Bats: {self.all_bats}" )
        #print(f"Auto Detected: {self.bat_counter}")
        
        total = sum(self.bat_counter.values())
        
        print("=== Autoanalysed Bats ===")
        for bat in self.bat_counter:
            percent = round((self.bat_counter[bat]/total)*100,2)
            if percent > 0:
                print(f"{bat}:\t{percent}%")
            
    def print_classification_progress(self):
        progress = len(self.bat_csv) - len(self.bat_csv[self.bat_csv['manual_id'] != ''])
        total = len(self.bat_csv)
        percent = round(((total - progress)/total)*100,2)
        print(f"Classification progress: {progress} left of {total} ({percent}%)")

    def reduce(self, bat, threshold):
        self.bat_csv.loc[(self.bat_csv[bat] >= threshold) & (self.bat_csv["autofilled"] == bat) , 'manual_id'] = bat
        self.bat_csv['manual_id'] = self.bat_csv['manual_id'].replace(np.nan, "")
