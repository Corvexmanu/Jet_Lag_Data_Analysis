# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 14:48:58 2019

@author: corve
"""
import requests, zipfile, io, os
import pandas as pd
import numpy as np 
#The glob module finds all the pathnames matching a specified pattern
#The requests module allows you to send organic, grass-fed HTTP/1.1 requests, without the need for manual labor


class Wrangling_DataSource():
    
    def __init__(self,minrange,maxrange):
        self.minrange = minrange
        self.maxrange = maxrange
        self.strRef = ["https://www.retrosheet.org/events/",#Webpage data origin
                       "eve.zip",#Extension file zip to download
                       ".\Resources\\",#local folder to store the data
                       "TEAM",#Name of the main file in the zip folder
                       ["teamID","league","city","teamname"],
                       ".\Timezones\\",
                       ["timesZonesDayLight.xlsx", "timeZonesStandard.xlsx"]]#Labels from TEAM file.
        self.years = list(range(self.minrange,self.maxrange))
    
    def createUrlDest(self):        
        url = {}
        for year in self.years:
            url[year]=  (self.strRef[0] + str(year) + self.strRef[1] , self.strRef[2] + str(year))
        return url

    def getData(self,url_WD,destination_WD):
        r = requests.get(url_WD)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(destination_WD)
    
    def getDirLength(self, destination_WD):
        return len(os.listdir(destination_WD))       
    
    def getTeams(self,year_WD):
        path = self.strRef[2] + str(year_WD) + "\\" + self.strRef[3] + str(year_WD)
        print("Extracting teams from " + str(path))
        df = pd.read_csv(path, header= None)
        df.columns = self.strRef[4]
        return df 
    
    def getTeamsPerYear(self,year_WD,teamsDf_WD):
        teamsPerYear = teamsDf_WD[year_WD][[self.strRef[4][0],self.strRef[4][1]]]        
        return teamsPerYear
        
    def getNameFiles(self,year_WD, teamsPerYear_WD): 
        filesList = []
        teamsPerYear_WD["evxFiles"] = str(year_WD) + teamsPerYear_WD.loc[:,"teamID"] + ".EV" + teamsPerYear_WD.loc[:,"league"] 
        teamsPerYear_WD["rosFiles"] = teamsPerYear_WD.loc[:,"teamID"] + str(year_WD) + ".ROS"
        filesList.append(list(teamsPerYear_WD["evxFiles"]))
        filesList.append(list(teamsPerYear_WD["rosFiles"]))        
        filesList.append([str(year_WD) + ".EDA", str(year_WD) + ".EDN"])
        return filesList
    
    #This table has a structure info,column,value.
    def getTableinfo(self,year_WD, filesToExtract_WD):
        print("################## Creating Table Info #####################")
        dic_temp = {}
        info_col = []  
        
        for file in filesToExtract_WD[0]:
            #Extracting the columns and the index for the dataframe
            f = open(self.strRef[2] + str(year_WD)+ "\\" + file , 'r')
            for line in f:
                line = line.strip().split(",")                
                if line[0] == "info" and line[1] not in info_col: 
                    info_col.append(line[1])     
            f.close()
            
        dftemp = pd.DataFrame(columns= info_col) 
        
        for file in filesToExtract_WD[0]:
            print(str(file) + " file in process.")
            #Extracting the columns and the index for the dataframe                       
            g = open(self.strRef[2] + str(year_WD) + "\\" + file , 'r')        
            for line in g:
                line = line.strip().split(",")
                if line[0]=="id":   
                    guide = line[1]
                if line[0]=="info":
                   dic_temp[line[1]] = line[2]  
                   dftemp.loc[guide] = pd.Series(dic_temp)
            g.close()
            
        dftemp['Game_ID'] = dftemp.index
        dftemp = dftemp.reindex_axis(['Game_ID'] + list(dftemp.columns[:-1]), axis=1)      
        info_teams = dftemp[["Game_ID","hometeam", "visteam"]]
        info_teams.set_index("Game_ID", inplace = True)
        
        return dftemp, info_teams
    
    #This table has a structure info,value,value,value
    def getTableStart(self,year_WD, filesToExtract_WD):
        print("################## Creating Table Start #####################")
        new_row = []
        count = 0
        
        start_col = ["Game_ID","Table_ID","start_playerid", 
                            "start_playersname", 
                            "start_visithometeam", 
                            "start_battingposition", 
                            "start_fieldingposition"]
        
        dftemp = pd.DataFrame(columns= start_col)        
        
        for file in filesToExtract_WD[0]:
            print(str(file) + " file in process.")            
            g = open(self.strRef[2] + str(year_WD) + "\\" + file , 'r')        
            for line in g:
                line = line.strip().split(",")
                if line[0] == "id": 
                    guide = line[1]
                if line[0]=="start": 
                    new_row.append(guide)
                    new_row.extend(line)
                    dftemp.loc[count]= new_row
                    new_row = []
                    count = count + 1
            g.close()
            
        return dftemp
    
    #This table has a structure info,value,value,value
    def getTablePlay(self,year_WD, filesToExtract_WD):
        print("################## Creating Table Play #####################")
        new_row = []
        count = 0
        
        start_col = ["Game_ID","Table_ID","play_inning", 
                            "play_homevisitor", 
                            "play_playerid", 
                            "play_count", 
                            "play_pitches",
                            "play_event"]
        
        dftemp = pd.DataFrame(columns= start_col)   
        
        for file in filesToExtract_WD[0]:
            print(str(file) + " file in process.")            
            g = open(self.strRef[2] + str(year_WD) + "\\" + file , 'r')        
            for line in g:
                line = line.strip().split(",")
                if line[0] == "id": 
                    guide = line[1]
                if line[0]=="play": 
                    new_row.append(guide)
                    new_row.extend(line)
                    dftemp.loc[count]= new_row
                    new_row = []
                    count = count + 1
            g.close()
            
        return dftemp
    
    #This table has a structure info,value,value,value
    def getTableSub(self,year_WD, filesToExtract_WD):
        print("################## Creating Table Sub #####################")
        new_row = []
        count = 0
        
        start_col = ["Game_ID","Table_ID","sub_playerid", 
                            "sub_playersname", 
                            "sub_homevisitor", 
                            "sub_battingposition", 
                            "sub_fieldingposition"]
        
        dftemp = pd.DataFrame(columns= start_col)     
        
        for file in filesToExtract_WD[0]:
            print(str(file) + " file in process.")            
            g = open(self.strRef[2] + str(year_WD) + "\\" + file , 'r')        
            for line in g:
                line = line.strip().split(",")
                if line[0] == "id": 
                    guide = line[1]
                if line[0]=="sub": 
                    new_row.append(guide)
                    new_row.extend(line)
                    dftemp.loc[count]= new_row
                    new_row = []
                    count = count + 1
            g.close()
            
        return dftemp
    
    #This table has a structure info,value,value,value
    def getTableData(self,year_WD, filesToExtract_WD):
        print("################## Creating Table Data #####################")
        new_row = []
        count = 0
        start_col = ["Game_ID","er","Table_ID","data_playerid", 
                            "data_earnedruns"]
        dftemp = pd.DataFrame(columns= start_col)        
        for file in filesToExtract_WD[0]:
            print(str(file) + " file in process.")            
            g = open(self.strRef[2] + str(year_WD) + "\\" + file , 'r')        
            for line in g:
                line = line.strip().split(",")
                if line[0] == "id": 
                    guide = line[1]
                if line[0]=="data": 
                    new_row.append(guide)
                    new_row.extend(line)
                    dftemp.loc[count]= new_row
                    new_row = []
                    count = count + 1
            g.close()
        return dftemp
    
    def getEvaEvnData(self,year_WD, filesToExtract_WD):       
        dicEvaEvnData = {}
        for file in filesToExtract_WD[0]:
            print(str(file) + " file in process.")
            index = []
            infocol = []
            dictemp = {}
            #Extracting the columns and the index for the dataframe
            f = open(self.strRef[2] + str(year_WD)+ "\\" + file , 'r')
            for line in f:
                line = line.strip().split(",")
                if line[0]=="id":   index.append(line[1])
                if line[0]=="info" and line[1] not in infocol: infocol.append(line[1])     
            f.close()
            
            #Adding Columns for start data.
            infocol.extend(["start_playerid", 
                            "start_playersname", 
                            "start_visithometeam", 
                            "start_battingposition", 
                            "start_fieldingposition"])
            
            #Adding Columns for sub data.
            infocol.extend(["sub_playerid", 
                            "sub_playersname", 
                            "sub_homevisitor", 
                            "sub_battingposition", 
                            "sub_fieldingposition"])
            
            #Adding Columns for play data.
            infocol.extend(["play_inning", 
                            "play_homevisitor", 
                            "play_playerid", 
                            "play_count", 
                            "play_pitches",
                            "play_event"])
            
            #Adding Columns for field data.
            infocol.extend(["data_playerid", 
                            "data_earnedruns"])
            
            #Creating the initial dataframe structure.
            dftemp = pd.DataFrame(columns= infocol , index= index)
            
            #Extracting the data from each ection.
            g = open(self.strRef[2] + str(year_WD) + "\\" + file , 'r')        
            for line in g:
                line = line.strip().split(",")
                if line[0]=="id":   guide = line[1]  
                
                if line[0]=="info":
                    dictemp[line[1]] = line[2]
                    dftemp.loc[guide] = pd.Series(dictemp)
                    
                if line[0]=="start":
                    dictemp["start_playerid"] = line[1]
                    dictemp["start_playersname"] = line[2]
                    dictemp["start_visithometeam"] = line[3]
                    dictemp["start_battingposition"] = line[4]
                    dictemp["start_fieldingposition"] = line[5]
                    dftemp.loc[guide] = pd.Series(dictemp)
                    
                if line[0]=="play":
                    dictemp["play_inning"] = line[1]
                    dictemp["play_homevisitor"] = line[2]
                    dictemp["play_playerid"] = line[3]
                    dictemp["play_count"] = line[4]
                    dictemp["play_pitches"] = line[5]
                    dictemp["play_event"] = line[6]
                    dftemp.loc[guide] = pd.Series(dictemp)
                
                if line[0]=="sub":
                    dictemp["sub_playerid"] = line[1]
                    dictemp["sub_playersname"] = line[2]
                    dictemp["sub_homevisitor"] = line[3]
                    dictemp["sub_battingposition"] = line[4]
                    dictemp["sub_fieldingposition"] = line[5]
                    dftemp.loc[guide] = pd.Series(dictemp)  
                
                if line[0]=="data":
                    dictemp["data_playerid"] = line[2]
                    dictemp["data_earnedruns"] = line[3]
                    dftemp.loc[guide] = pd.Series(dictemp) 
                    
            g.close()
            
            dicEvaEvnData[file] = dftemp
        
        return dicEvaEvnData
    
    def getRosData():
        dicRosData = {}
        return dicRosData
    
    def getfinalDataset(self,eventGames_WD):
        yearsData = {}
        for i in range(self.minrange, self.maxrange): 
            yearsData[i] = pd.concat(eventGames_WD[i], axis=0)
        Data = pd.concat(yearsData, axis=0)
        return Data
    
    def insertTimeZoneInfo(self,Data_WD):
        path = self.strRef[5] + self.strRef[6][0]
        print("Data of timezons in " + path + " extracted")
        timesZonesDayLight = pd.read_excel(path, index_col=0)
        Data_WD['jetLag'] = None        
        
        for index in Data_WD.index.values:
            Data_WD.loc[index , 'jetLag'] = timesZonesDayLight.loc[Data_WD.loc[index,'hometeam'],Data_WD.loc[index,'visteam']]
        
        return Data_WD
