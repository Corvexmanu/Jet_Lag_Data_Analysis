# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:21:31 2019

@author: corve
"""

import Wrangling_DataSource as WD

teamsDf = {}
teamsPerYear = {}
filesToExtract = {}
eventGames = {}
tableInfo = {}
tableStart = {}
tablePlay = {}
tableSub = {}
tableData = {}

def main():
    #Defining the global variables 
    minimum = 1992
    maximum = 1994
    
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
        tableInfo[year] = dataImported.getTableinfo(year_WD= year, filesToExtract_WD= filesToExtract[year])
        tableStart[year] = dataImported.getTableStart(year_WD= year, filesToExtract_WD= filesToExtract[year])
        tablePlay[year] = dataImported.getTablePlay(year_WD= year, filesToExtract_WD= filesToExtract[year])
        tableSub[year] = dataImported.getTableSub(year_WD= year, filesToExtract_WD= filesToExtract[year])
        tableData[year] = dataImported.getTableData(year_WD= year, filesToExtract_WD= filesToExtract[year])
    
    return tableInfo, tableStart, tablePlay, tableSub, tableData
    '''
    #Extracting EVA and EVN files    
    for year in filesToExtract.keys(): eventGames[year] = dataImported.getEvaEvnData(year_WD= year, filesToExtract_WD= filesToExtract[year])     
    #Create The final Dataset
    dataEvents = dataImported.getfinalDataset(eventGames_WD= eventGames)    
    dataTimeZones = dataImported.insertTimeZoneInfo(Data_WD= dataEvents)
    dataTimeZones.to_csv('Dataset.csv')
    '''    

#Executing the main program.
#if __name__ == "__main__": 
tableInfo, tableStart, tablePlay, tableSub, tableData = main()

