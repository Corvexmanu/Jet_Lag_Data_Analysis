# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 14:48:58 2019

@author: corve
"""
import requests, zipfile, io, os, glob
#The glob module finds all the pathnames matching a specified pattern
#The requests module allows you to send organic, grass-fed HTTP/1.1 requests, without the need for manual labor
#

import pandas as pd 


class Wrangling_DataSource():
    
    def __init__(self,minrange,maxrange):
        self.minrange = minrange
        self.maxrange = maxrange
        self.strRef = ["https://www.retrosheet.org/events/",#Webpage data origin
                       "eve.zip",#Extension file zip to download
                       ".\Resources\\",#local folder to store the data
                       "TEAM",#Name of the main file in the zip folder
                       ["ID","First Letter","City","Team Name"]]#Labels from TEAM file.
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
    
    def getTeams(self,year_WD):
        listString = []
        path = self.strRef[2] + str(year_WD)
        for infile in glob.glob(os.path.join(path, self.strRef[3] + str(year_WD) + "*")):
            stringFile = open(infile, 'r').read()
            for i in range(0,len(stringFile.splitlines())):
                listString.append(stringFile.splitlines()[i].split(","))
            df = pd.DataFrame.from_records(listString, columns = self.strRef[4] )
        return df 
    
    def getTeamsPerYear(self,year_WD,teamsDf_WD):
        teamsPerYear = teamsDf_WD[year_WD]["ID"].tolist() 
        return teamsPerYear
        
    def getEva(self,year):
        return
        
    def getRos(self,year):
        return
