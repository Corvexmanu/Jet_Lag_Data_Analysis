# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:21:31 2019

@author: corve
"""

import Wrangling_DataSource as WD

def main():
    #Defining the global variables 
    min, max = 1950,1952
    teamsDf = {}
    teamsPerYear = {}
    
    #USING THE CLASS WRANGLING DATASOURCE
    dataImported = WD.Wrangling_DataSource(min,max)  
    
    #Creating Dictionary of url and destination
    dictUrlsDest = dataImported.createUrlDest()  
    
    ##Downloading and storing data 
    for year,url_Des in dictUrlsDest.items():
        dataImported.getData(url_WD= url_Des[0],destination_WD= url_Des[1])
        print("Data from " + str(year) + " imported and stored inside of" + str(url_Des[1]))
    
    #Pre-Processing file Teams per each year.
    for year in dictUrlsDest.keys():    
        teamsDf[year] = dataImported.getTeams(year_WD= year) 
        teamsPerYear[year] = dataImported.getTeamsPerYear(year_WD= year, teamsDf_WD= teamsDf)
    
    for k,v in teamsPerYear.items():
        print(str(k) + " => " + str(v))
        
        
    

#Executing the main program.
if __name__ == "__main__": 
    main()
        
