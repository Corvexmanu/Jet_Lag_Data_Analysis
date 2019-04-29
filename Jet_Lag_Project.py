# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:21:31 2019

@author: corve
"""
import pandas as pd
import Wrangling_DataSource as WD
import Transforming_DataSource as Transformation

minimum = 1992
maximum = 2012
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
dict_offensive_Defensive_Measures ={}
dict_Chronologic_Games = {}
df_timesZonesDayLight_site = pd.DataFrame()
dataset_Constant_Cfip = pd.DataFrame()
dict_Offensive_Defensive_Measure_Jet_Lag = {}
Innings = {}
df_final_Dataset = pd.DataFrame()
df_Offensive_Dataset_Same = pd.DataFrame()
df_Offensive_Dataset_East = pd.DataFrame()
df_Offensive_Dataset_West = pd.DataFrame()
df_Defensive_Dataset_Same = pd.DataFrame()
df_Defensive_Dataset_East = pd.DataFrame()
df_Defensive_Dataset_West = pd.DataFrame()



def dataExtraction():

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
    
    return dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams



def datalocalwrangling():
    
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



def dataTransformation(dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams):

    dict_Play_transformed = Transformation.createNewAttributes(dictPlay, info_teams, minimum, maximum)  
    dict_Play_Grouped, Innings = Transformation.calculatePlayGrouped(dict_Play_transformed, minimum, maximum)
    dataset_Constant_Cfip = Transformation.importConstantCfip()
    dict_Games_Per_Team = Transformation.createOffensiveAndDefensiveVariables(dict_Play_Grouped, dataset_Constant_Cfip, minimum, maximum)    
    df_timesZonesDayLight_site =  Transformation.importtimesZonesDayLight_site()   
    dict_Chronologic_Games = Transformation.createChronologicGamesJetLag(dict_Games_Per_Team, dictInfo, df_timesZonesDayLight_site, minimum, maximum)    
    dict_offensive_Defensive_Measures = Transformation.createFinalVariablesDictionary(dict_Games_Per_Team,  minimum, maximum)
    dict_Offensive_Defensive_Measure_Jet_Lag = Transformation.combineOffensiveDefensiveMeasureJetLag(dict_offensive_Defensive_Measures,dict_Chronologic_Games, minimum, maximum)
    
    return dataset_Constant_Cfip, Innings,dict_Offensive_Defensive_Measure_Jet_Lag, df_timesZonesDayLight_site, dict_Chronologic_Games, dict_Play_transformed, dict_Play_Grouped, dict_Games_Per_Team, dict_offensive_Defensive_Measures

def dataSelectionAndPartitioning(dict_Offensive_Defensive_Measure_Jet_Lag):
    
    df_final_Dataset = Transformation.createFinalDataset(dict_Offensive_Defensive_Measure_Jet_Lag, minimum, maximum)
    
    df_Offensive_Dataset = Transformation.createOffensiveDataset(dict_Offensive_Defensive_Measure_Jet_Lag, minimum, maximum)
    df_Defensive_Dataset = Transformation.createDefensiveDataset(dict_Offensive_Defensive_Measure_Jet_Lag, minimum, maximum)
    
    df_Offensive_Dataset_Same, df_Offensive_Dataset_East, df_Offensive_Dataset_West = Transformation.splitDatasetsbyJetlagDirection(df_Offensive_Dataset, 'Ofensive', minimum, maximum)
    
    df_Defensive_Dataset_Same, df_Defensive_Dataset_East, df_Defensive_Dataset_West = Transformation.splitDatasetsbyJetlagDirection(df_Defensive_Dataset, 'Defensive', minimum, maximum)
    
    return df_final_Dataset, df_Defensive_Dataset_Same, df_Defensive_Dataset_East, df_Defensive_Dataset_West, df_Offensive_Dataset_Same, df_Offensive_Dataset_East, df_Offensive_Dataset_West, df_Offensive_Dataset, df_Defensive_Dataset



#Executing the main program.
#dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams = dataExtraction()
dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams = datalocalwrangling()
dataset_Constant_Cfip, Innings,dict_Offensive_Defensive_Measure_Jet_Lag, df_timesZonesDayLight_site, dict_Chronologic_Games, dict_Play_transformed, dict_Play_Grouped, dict_Games_Per_Team, dict_offensive_Defensive_Measures = dataTransformation(dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams)
df_final_Dataset, df_Defensive_Dataset_Same, df_Defensive_Dataset_East, df_Defensive_Dataset_West, df_Offensive_Dataset_Same, df_Offensive_Dataset_East, df_Offensive_Dataset_West, Offensive_Dataset, Defensive_Dataset = dataSelectionAndPartitioning(dict_Offensive_Defensive_Measure_Jet_Lag)
