from ast import Str
from pandas import DataFrame
import pandas as pd
import numpy as np

class Aufnahme:
    def __init__(self, name:str) -> None:
        self.name = name
        self.__data = DataFrame
        self.arten = list()
        self.__arten_columns = list()
        self.bat_counter = dict()
        self.aufnahmne_counter = 0
        pd.options.mode.chained_assignment = None  # default='warn'

        
    def __extract_sozialruf(self, name:str, empty_if_no_sozialruf=True):
        # Does Sozialrufe_Ppip_unsicher or Ppip_unsicher_Sozialruf -> Ppip_unsicher
        if "Sozialruf" in name:
            l1 = name.split("_")
            for item in l1:
                if "Sozialruf" in item:
                    l1.remove(item)
            return "_".join(l1)
            
        else:
            if empty_if_no_sozialruf:
                pass
            else:
                return name
            
    
    def get_x_minute_classes(self, interval:str, spacing = 0) -> DataFrame:
        output = pd.DataFrame
        first_run = True
        
        
        
        minutes = interval[:-1]
        for art in self.arten:           
            df = self.__data[['DateTime', f"Single_{art}"]] [ self.__data["Manual_ID"] == art ]
            df = df.resample(interval, on="DateTime").sum()
            
            if spacing != 0:
                df = df.resample(spacing).pad()
                
            df = df.reset_index() # it does a ReIndex on DateTime
            
                
            
            df = df.rename(columns = {f"Single_{art}":f"Count"})
            df["Manual_ID"] = art
            df["Class"] = minutes
            
            if art == "Ppip":
                pass
                #print(df)
        
            if first_run:
                first_run = False
                output = df
                continue
            output = pd.concat([output, df], ignore_index=True)
            
        return output
    
    def get_x_minute_classes_range(self, start:int, end:int):
        min_interval = f"{start}T"
        output = DataFrame
        first_run=True
        
        for i in range(start, end+1):
            interval = f"{i}T"
            df = self.get_x_minute_classes(interval, "1T")
                       
            if first_run:
                first_run = False
                output = df
                continue
            
            output = pd.concat([output, df], ignore_index=True)
            
        return output
        
        
        
    def add_data(self, data:DataFrame):
        self.__data = data
        # Spacebar to '_'
        self.__data.columns = [c.replace(' ', '_') for c in self.__data.columns]
        
        # Combine Date and Time
        self.__data["DateTime"] = pd.to_datetime(self.__data.Date.astype(str) + ' ' + self.__data.Time.astype(str))
        
        # Strings to list ( NSL (unbestimmt), Ppip -> ["NSL (unbestimmt)","Ppip"])
        self.__data["Manual_ID"] = self.__data.Manual_ID.apply(lambda x: x.split(', '))
        self.aufnahmne_counter = len(self.__data)
        
        # Insert multiple rows for ["NSL (unbestimmt)","Ppip"] -> r1: NSL_(unbestimmt), r2: Ppip
        self.__data = self.__data.explode('Manual_ID', ignore_index=True)
        self.__data["Manual_ID"] = self.__data.Manual_ID.apply(lambda x: x.replace(" ", "_"))
        
        # Sozialruf Column and remove string part "Spzialruf" from Manual_ID
        self.__data["Sozialruf"] = self.__data.Manual_ID.apply(lambda x: self.__extract_sozialruf(x))
        self.__data["Manual_ID"] = self.__data.Manual_ID.apply(lambda x: self.__extract_sozialruf(x, empty_if_no_sozialruf=False))
        
        
        for ind in self.__data.index:
            bat = self.__data["Manual_ID"][ind]
            bat_column = f"Single_{bat}"
            try:
                self.__data[bat_column][ind] = 1
                self.bat_counter[bat] += 1
            except:
                self.__data[bat_column] = 0
                self.__data[bat_column][ind] = 1
                self.arten.append(bat)
                self.__arten_columns.append(bat_column)
                self.bat_counter[bat] = 1
                    
                
        
    def get_data(self) -> DataFrame:
        return self.__data
    
    def set_temperature(self, df:DataFrame):
        # resample to 1 second
        df = df.resample('1S').max()
        
        
    
    def get_counts(self):
        return self.__data['Manual_ID'].value_counts()