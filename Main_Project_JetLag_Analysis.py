# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:21:31 2019

@author: corve
"""
import pandas as pd
import Wrangling_DataSource as WD
import Transforming_DataSource as Transformation
import Importing_ExternalData as ImportingExternalData

minimum = 2000
maximum = 2004
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
df_ELO = pd.DataFrame()
dataset_Constant_Cfip = pd.DataFrame()
dict_Offensive_Defensive_Measure_Jet_Lag = {}
Innings = {}
df_final_Dataset = pd.DataFrame()



def dataSelection():

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
    
    dataset_Constant_Cfip = ImportingExternalData.importConstantCfip()
    df_timesZonesDayLight_site =  ImportingExternalData.importtimesZonesDayLight_site()
    df_Elo = ImportingExternalData.importElo()
    
    return dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams, dataset_Constant_Cfip, df_timesZonesDayLight_site, df_Elo



def datalocalwrangling():
    
    dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams = ImportingExternalData.importLocalData(minimum,maximum)
    dataset_Constant_Cfip = ImportingExternalData.importConstantCfip()
    df_timesZonesDayLight_site =  ImportingExternalData.importtimesZonesDayLight_site()
    df_Elo = ImportingExternalData.importElo()
    
    return dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams, dataset_Constant_Cfip, df_timesZonesDayLight_site, df_Elo



def dataPreparation(dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams, dataset_Constant_Cfip, df_timesZonesDayLight_site, df_Elo):
    
    #Importing External sources of information required to be included in the transformation.       
    dict_Play_transformed = Transformation.createNewAttributes(dictPlay, info_teams, minimum, maximum)  
    dict_Play_Grouped, Innings = Transformation.calculatePlayGrouped(dict_Play_transformed, minimum, maximum)    
    dict_Games_Per_Team = Transformation.createOffensiveAndDefensiveVariables(dict_Play_Grouped, dataset_Constant_Cfip, minimum, maximum)     
    dict_Chronologic_Games = Transformation.createChronologicGamesJetLag(dict_Games_Per_Team, dictInfo, df_timesZonesDayLight_site, df_Elo, minimum, maximum)    
    dict_offensive_Defensive_Measures = Transformation.createStatisticlVariables(dict_Games_Per_Team,  minimum, maximum)
    dict_Offensive_Defensive_Measure_Jet_Lag = Transformation.combineOffensiveDefensiveMeasureJetLag(dict_offensive_Defensive_Measures,dict_Chronologic_Games, minimum, maximum)
    df_final_Dataset = Transformation.createFinalDataset(dict_Offensive_Defensive_Measure_Jet_Lag, minimum, maximum)
    
    return df_final_Dataset


#Executing the main program.
#@dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams, dataset_Constant_Cfip, df_timesZonesDayLight_site, df_Elo = dataSelection()
dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams, dataset_Constant_Cfip, df_timesZonesDayLight_site, df_Elo = datalocalwrangling()
df_final_Dataset = dataPreparation(dictInfo, dictStart, dictPlay, dictSub, dictData, info_teams, dataset_Constant_Cfip, df_timesZonesDayLight_site, df_Elo)
