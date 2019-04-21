# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:21:31 2019

@author: corve
"""
import pandas as pd
import Wrangling_DataSource as WD
import Transforming_DataSource as Transformation
minimum = 1998
maximum = 1999
teamsDf = {}
teamsPerYear = {}
filesToExtract = {}
eventGames = {}
dictInfo = {}
dictStart = {}
dictPlay = {}
dictSub = {}
dictData = {}
info_teams = {}
dict_Play_Grouped = {}
dict_Play_transformed = {}
dict_Games_Per_Team = {}
dict_offensive_Measures ={}
dict_Chronologic_Games = {}
df_timesZonesDayLight_site = pd.DataFrame()
dataset_Constant_Cfip = pd.DataFrame()
dict_Offensive_Measure_Jet_Lag = {}
Innings = {}


def dataExtraction():
    #Defining the global variables 
    
    #USING THE CLASS WRANGLING DATASOURCE
    dataImported = WD.Wrangling_DataSource(minimum,maximum)  
    
    #Creating Dictionary of url and destination
    dictUrlsDest = dataImported.createUrlDest()  
    
    ##Downloading and storing data 
    for year,url_Des in dictUrlsDest.items(): dataImported.getData(url_WD= url_Des[0],destination_WD= url_Des[1])
    
    #Pre-Processing file Teams per each year.
    for year in dictUrlsDest.keys(): teamsDf[year] = dataImported.getTeams(year_WD= year)
    for year in dictUrlsDest.keys(): teamsPerYear[year] = dataImported.getTeamsPerYear(year_WD= year, teamsDf_WD= teamsDf)
    
    #Creating Structure of List of list of Files from each season. [[EVA and EVN],[ROS],[EDA and EDN]]
    for year in teamsPerYear.keys(): filesToExtract[year] = dataImported.getNameFiles(year_WD= year, teamsPerYear_WD= teamsPerYear[year] )  
      
    for year in filesToExtract.keys(): 
        dictInfo[year], info_teams[year] = dataImported.getTableinfo(year_WD= year, filesToExtract_WD= filesToExtract[year])
        dictStart[year] = dataImported.getTableStart(year_WD= year, filesToExtract_WD= filesToExtract[year])
        dictPlay[year] = dataImported.getTablePlay(year_WD= year, filesToExtract_WD= filesToExtract[year])
        dictSub[year] = dataImported.getTableSub(year_WD= year, filesToExtract_WD= filesToExtract[year])
        dictData[year] = dataImported.getTableData(year_WD= year, filesToExtract_WD= filesToExtract[year])
    
    #Printing Files for the first year
    dictInfo[minimum].to_csv(r'.\tables\dictInfo.csv')
    dictStart[minimum].to_csv(r'.\tables\dictStart.csv')
    dictSub[minimum].to_csv(r'.\tables\dictSub.csv')
    dictData[minimum].to_csv(r'.\tables\dictData.csv')
    dictPlay[minimum].to_csv(r'.\tables\dictPlay.csv')
    info_teams[minimum].to_csv(r'.\tables\infoteams.csv')
    
    return dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams



def datalocalwrangling():
    
    dictInfo[minimum] = pd.read_csv(r'.\tables\dictInfo.csv')
    dictInfo[minimum].set_index("Unnamed: 0", inplace = True)
    
    dictPlay[minimum] = pd.read_csv(r'.\tables\dictPlay.csv')
    dictPlay[minimum].drop("Unnamed: 0", axis=1, inplace=True)
    
    dictStart[minimum] = pd.read_csv(r'.\tables\dictStart.csv')
    dictStart[minimum].drop("Unnamed: 0", axis=1, inplace=True)
    
    dictSub[minimum] = pd.read_csv(r'.\tables\dictSub.csv')
    dictSub[minimum].drop("Unnamed: 0", axis=1, inplace=True)
    #dictSub[minimum].set_index("Game_ID", inplace = True)
    
    dictData[minimum] = pd.read_csv(r'.\tables\dictData.csv')
    dictData[minimum].drop("Unnamed: 0", axis=1, inplace=True)
    
    info_teams[minimum] = pd.read_csv(r'.\tables\infoteams.csv')
    info_teams[minimum].set_index("Game_ID", inplace = True)
    
    return dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams



def dataTransformation(dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams):
    #USING THE CLASS TRANSFORMING_DATASOURCES
    dict_Play_transformed = Transformation.createNewAttributes(dictPlay, info_teams, minimum, maximum)  
    dict_Play_Grouped, Innings = Transformation.calculatePlayGrouped(dict_Play_transformed, minimum, maximum)
    dataset_Constant_Cfip = Transformation.importConstantCfip()
    dict_Games_Per_Team = Transformation.createOffensiveAndDefensiveVariables(dict_Play_Grouped, dataset_Constant_Cfip, minimum, maximum)    
    df_timesZonesDayLight_site =  Transformation.importtimesZonesDayLight_site()   
    dict_Chronologic_Games = Transformation.createChronologicGamesJetLag(dict_Games_Per_Team, dictInfo, df_timesZonesDayLight_site, minimum, maximum)
    
    
    dict_offensive_Measures = Transformation.createOffensiveDataset(dict_Games_Per_Team,  minimum, maximum)
    dict_Offensive_Measure_Jet_Lag = Transformation.combineOffensiveMeasureJetLag(dict_offensive_Measures,dict_Chronologic_Games, minimum, maximum)
    

    return dataset_Constant_Cfip, Innings,dict_Offensive_Measure_Jet_Lag, df_timesZonesDayLight_site, dict_Chronologic_Games, dict_Play_transformed, dict_Play_Grouped, dict_Games_Per_Team, dict_offensive_Measures





#Executing the main program.
#dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams = dataExtraction()
dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams = datalocalwrangling()
dataset_Constant_Cfip, Innings,dict_Offensive_Measure_Jet_Lag, df_timesZonesDayLight_site, dict_Chronologic_Games, dict_Play_transformed, dict_Play_Grouped, dict_Games_Per_Team, dict_offensive_Measures = dataTransformation(dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams)





#dict_Chronologic_Games[1998].info()






