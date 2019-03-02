# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 14:48:58 2019

@author: corve
"""
import requests, zipfile, io

class Wrangling_DataSource():
    
    def __init__(self,minrange,maxrange):
        self.minrange = minrange
        self.maxrange = maxrange     
    
    def createRange(self):
        years = list(range(self.minrange,self.maxrange))
        url = {}
        for year in years:
            url[year]=  ("https://www.retrosheet.org/events/" + str(year) + "eve.zip", ".\Resources\\" + str(year))
        return url

    def getData(self,url,destination):
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(destination)
