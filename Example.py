# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 18:19:36 2019

@author: corve
"""
import pandas as pd
import numpy as np

def insertTimeZoneInfo():
    pathDataset = ".\Dataset.csv"
    Data_WD = pd.read_csv(pathDataset)
    pathTimeZone = ".\Timezones\\" + "timesZonesDayLight.xlsx"
    print("Data of timezons in " + pathTimeZone + " extracted")
    timesZonesDayLight = pd.read_excel(pathTimeZone, index_col=0)
    Data_WD['jetLag'] = None        
    for index in Data_WD.index.values:
        Data_WD.loc[index , 'jetLag'] = timesZonesDayLight.loc[Data_WD.loc[index,'hometeam'],Data_WD.loc[index,'visteam']]

    return Data_WD



def doSomething():
    Data = pd.read_csv('parkcode.csv')
    
    return Data
    
    
Data = doSomething()