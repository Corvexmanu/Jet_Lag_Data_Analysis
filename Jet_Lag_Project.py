# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:21:31 2019

@author: corve
"""

import Wrangling_DataSource as WD


def main():
    #Defining the range of years to be evaluated.
    min, max = 2017,2019
    
    #Using the class Weangling DataSource.
    dataImported = WD.Wrangling_DataSource(min,max)    
    dictOfUrls = dataImported.createRange()    
    for year,url_Des in dictOfUrls.items():
        dataImported.getData(url_Des[0],url_Des[1])
        print("Data from " + str(year) + " imported and stored inside of" + str(url_Des[1]))
    
    
    

#Executing the main program.
if __name__ == "__main__": 
    main()
        
