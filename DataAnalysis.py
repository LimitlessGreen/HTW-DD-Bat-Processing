#!/usr/bin/env python3
"""
Module Docstring
"""


__author__ = "Jairus Behrisch"
__version__ = "0.0.1"
#__license__ = "MIT"

import pandas as pd

from os.path import exists



from abc import ABC

from itertools import islice

from Aufnahme import Aufnahme
from Standort import Standort
from ExcelImport import ExcelImport



class Projekt(ExcelImport):
    def __init__(self, name:str) -> None:
        self.name = name
        self.standorte = dict()
        self.standort_namen = list()
        
    def import_excel(self, path: str):
        self.standorte = super().import_excel(path)
        
        for standort in self.standorte:
            self.standort_namen.append(self.standorte.get(standort).name)
        
    def get_standort(self, name:str) -> Standort:
        return self.standorte.get(name)
    
    def get_aufnahme(self, standort:str, aufnahme:str) -> Aufnahme:
        return self.get_standort(standort).get_aufnahme(aufnahme)
        
    def print_tree(self):
        print("===============")
        print(f"Projekt: {self.name}")
        print(f"\tStandorte:")
        for standort in self.standorte:
            standort = self.standorte[standort]
            print(f"\t\t- {standort.name}")
            
            for aufnahme in standort.aufnahmen:
                aufnahme = standort.aufnahmen[aufnahme]
                print(f"\t\t\t- {aufnahme.name}")
    
    def get_data(self) -> pd.DataFrame:
        first_run = True
        df = pd.DataFrame
        
        for standort in self.standorte.values():
            if first_run:
                df = standort.get_data()
                df["Standort"] = standort.name
                first_run = False
                continue
            df_tmp = standort.get_data()
            df["Standort"] = standort.name
            df = pd.concat([df, df_tmp], ignore_index=True)
            
        return df
    

        

                
                
    
def main():
    """ Main entry point of the app """
    my_proj = Projekt(name="Fledermausprojekt")
    my_proj.import_excel(path="../Fledermausrufanalyse - Kopie.xlsx")
    
    for standort in my_proj.standorte.values():
        for aufnahme in standort.aufnahmen.values():
            #print(aufnahme.get_data()["Manual_ID"])
            #print(f"{standort.name} - {aufnahme.name}: {aufnahme.bat_counter}")
            print(f"{standort.name} - {aufnahme.name}:\n{aufnahme.get_counts()}\n")
            print(aufnahme.get_x_minute_classes("10T"))
            print(aufnahme.get_x_minute_classes_range(1,10))
            
        print("================================================\n")
            
    data = my_proj.get_data()
    print (data["Manual_ID"].value_counts())
    
    



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
