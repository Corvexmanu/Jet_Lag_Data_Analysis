# -*- coding: utf-8 -*-
"""
Created on Sat May 11 12:52:14 2019

@author: corve
"""

import pandas as pd

def importLocalData(minimum,maximum):
        
        dictInfo = {}
        dictPlay = {}
        dictStart = {}
        dictSub = {}
        dictData = {}
        info_teams = {}
        
        for year in range(minimum,maximum):
        
            pathInfo = r'.\tables\dictionaries\dictInfo_' + str(year) + '.csv'
            dictInfo[year] = pd.read_csv(pathInfo)
            dictInfo[year].set_index("Unnamed: 0", inplace = True)
            
            pathPlay = r'.\tables\dictionaries\dictPlay_' + str(year) + '.csv'
            dictPlay[year] = pd.read_csv(pathPlay)
            dictPlay[year].drop("Unnamed: 0", axis=1, inplace=True)
            
            pathStart = r'.\tables\dictionaries\dictStart_' + str(year) + '.csv'
            dictStart[year] = pd.read_csv(pathStart)
            dictStart[year].drop("Unnamed: 0", axis=1, inplace=True)
            
            pathSub = r'.\tables\dictionaries\dictSub_' + str(year) + '.csv'
            dictSub[year] = pd.read_csv(pathSub)
            dictSub[year].drop("Unnamed: 0", axis=1, inplace=True)
            
            pathData = r'.\tables\dictionaries\dictData_' + str(year) + '.csv'
            dictData[year] = pd.read_csv(pathData)
            dictData[year].drop("Unnamed: 0", axis=1, inplace=True)
            
            pathInfoTeams = r'.\tables\dictionaries\dictInfoTeams_' + str(year) + '.csv'
            info_teams[year] = pd.read_csv(pathInfoTeams)
            info_teams[year].set_index("Game_ID", inplace = True)
    
        return dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams

def importConstantCfip():
    
    print("######################## Importing CFIP Information #####################")
    dataset_Constant_Cfip = pd.read_excel(r'.\Cfip\cfip.xlsx', index_col = 0, header = 0)
    
    return dataset_Constant_Cfip        

def importtimesZonesDayLight_site():
    
    print("######################## Importing TimeZones Information #####################")
          
    timesZonesDayLight_site = pd.read_excel(r'.\Timezones\timesZonesDayLight_site.xlsx', index_col = 0, header = 0)
    
    return timesZonesDayLight_site

def importElo():
    
    print("######################## Importing ELO Information #####################")
          
    Elo = pd.read_excel(r'.\ELO\ELO_Ratings_Final.xlsx', index_col = 0, header = 0)
    Elo = Elo.stack().reset_index()
    Elo.rename(columns ={'level_1': 'Team', 0: 'Elo'}, inplace=True)
    
    return Elo