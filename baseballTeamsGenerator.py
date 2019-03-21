# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 18:19:36 2019

@author: corve
"""
import pandas as pd

def readTeams(year_WD):
        path = ".\Resources\\" + str(year_WD) + "\\TEAM" + str(year_WD)
        print("Extracting teams from " + str(path))
        df = pd.read_csv(path, header= None)
        df.columns = ["teamID","league","city","teamname"]
        return df

def getTeams(minimum,maximum):
    yearsData = {}    
    for years in range(minimum,maximum):
        yearsData[years] = readTeams(years)
        print("Data of teams in " + str(years) + " extracted")
    Datos = pd.concat(yearsData, axis=0)
    baseballTeams = Datos.drop_duplicates('teamID').sort_values(by = 'teamID')
    baseballTeams.to_csv('baseballTeams.csv', index = False) 
    return Datos