from Aufnahme import Aufnahme
import pandas as pd

class Standort:
    def __init__(self, name:str) -> None:
        self.name = name
        self.aufnahmen = dict()
        
    def add_aufnahme(self, aufnahme:Aufnahme):
        self.aufnahmen[aufnahme.name] = aufnahme
        
    def get_aufnahme(self, name:str):
        return self.aufnahmen.get(name)
        
    def get_data(self) -> pd.DataFrame:
        df = pd.DataFrame
        first_run = True
        for aufnahme in self.aufnahmen.values():
            if first_run:
                df = aufnahme.get_data()
                first_run = False
                continue
            df["Aufnahme"] = aufnahme.name
            df = pd.concat([df, aufnahme.get_data()], ignore_index=True)
            
        return df
    
    def get_x_minute_classes_range(self, start:int, end:int):
        min_interval = f"{start}T"
        output = DataFrame
        first_run=True
        
        for aufnahme in self.aufnahmen.values():
            if first_run:
                output = aufnahme.get_x_minute_classes_range(start, end)
                first_run = False
                output["Aufnahme"] = aufnahme.name
                continue
            
            df = aufnahme.get_x_minute_classes_range0(start, end)
            df["Aufnahme"] = aufnahme.name
            
            output = pd.concat([output, df], ignore_index=True)
            
        output["Standort"] = self.name
        return output