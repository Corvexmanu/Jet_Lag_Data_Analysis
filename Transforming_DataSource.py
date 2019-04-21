# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 21:12:05 2019

@author: corve
"""
import pandas as pd 
dictPlayGrouped = {}
dictOffensiveMeasures ={}
dictChronologicGamesGrouped = {}
dictOffensiveMeasureJetLag = {}
Innings = {}

def createNewAttributes(dictPlay, info_teams, minimum,maximum):
    for year in range(minimum,maximum):
        print("######################## Creating the new columns in {} #####################".format(year))
              
        dictPlay[year]['Singles'] =  dictPlay[year]['play_event'].str.count('^S[1-9]')
        dictPlay[year]['Doubles'] =  dictPlay[year]['play_event'].str.count('^D[1-9]')
        dictPlay[year]['Triples'] =  dictPlay[year]['play_event'].str.count('^T[1-9]')
        dictPlay[year]['Home_Runs'] =  dictPlay[year]['play_event'].str.count('^HR|^H')
        dictPlay[year]['hits'] =  dictPlay[year][['Singles','Doubles','Triples','Home_Runs']].sum(axis=1)
        
        dictPlay[year]['Errors'] =  dictPlay[year]['play_event'].str.count('^FLE|^E[1-9]|\(E[1-9]|[1-9]E[1-9]')
        dictPlay[year]['Reached_on_error'] =  dictPlay[year]['play_event'].str.count('^E[1-9]|\(E[1-9]|[1-9]E[1-9]')
        dictPlay[year]['Home_Reaches'] =  dictPlay[year]['play_event'].str.count('B-H|1-H|2-H|3-H')        
        dictPlay[year]['Walks'] =  dictPlay[year]['play_event'].str.count('^I|^IW|^W')
        dictPlay[year]['Strikeouts'] =  dictPlay[year]['play_event'].str.count('^K')
        dictPlay[year]['Stolen_bases'] =  dictPlay[year]['play_event'].str.count('SB')
        dictPlay[year]['Caught_Stealing'] =  dictPlay[year]['play_event'].str.count('CS')
        dictPlay[year]['Sacrifice_hits'] =  dictPlay[year]['play_event'].str.count('SH')
        dictPlay[year]['Sacrifice_flies'] =  dictPlay[year]['play_event'].str.count('SF')
        dictPlay[year]['GIDP'] =  dictPlay[year]['play_event'].str.count('GDP')
        dictPlay[year]['Balk'] =  dictPlay[year]['play_event'].str.count('BK')
        dictPlay[year]['Catcher_intereference'] =  dictPlay[year]['play_event'].str.count('C/E2')
        dictPlay[year]['Hit_by_Pitch'] =  dictPlay[year]['play_event'].str.count('HP')
        
        
        dictPlay[year]["Fielders_Choice"] =  dictPlay[year]['play_event'].str.count('^FC')
        dictPlay[year]["Fly_ball_out"] =  dictPlay[year]['play_event'].str.count('^[1-9]/')
        dictPlay[year]["Gound_out"] =  dictPlay[year]['play_event'].str.count('^[1-9]{2,}(?!.*(?:FO|SH|GDP|LDP).*).*$')
        
        
        
        
        dictPlay[year]['at_bats_substractor'] = dictPlay[year][['Catcher_intereference','Sacrifice_hits','Sacrifice_flies','Hit_by_Pitch','Walks']].sum(axis=1)
        dictPlay[year] = pd.merge(dictPlay[year], info_teams[year], on='Game_ID') 
        
    dictPlay[minimum].to_csv(r'.\tables\dictPlay_transformed.csv')
        
    return dictPlay



def calculatePlayGrouped(dictPlay, minimum, maximum):    
    for year in range(minimum,maximum):
        dictPlayGrouped[year] = dictPlay[year].groupby(["Game_ID","hometeam", "visteam", "play_homevisitor"],  as_index= True).sum()[['Singles', 'Doubles', 'Triples', 'Home_Runs', 'hits', 
                       'Errors', 'Reached_on_error', 'Home_Reaches', 'Walks', 'Strikeouts', 'Stolen_bases', 'Caught_Stealing', 'Sacrifice_hits', 'Sacrifice_flies',
                       'GIDP', 'Balk', 'Catcher_intereference', 'Hit_by_Pitch', 'Fielders_Choice', 'Fly_ball_out', 'Gound_out', 'at_bats_substractor']].reset_index()        
        dictPlayGrouped[year]['Team'] =  dictPlayGrouped[year][['hometeam','visteam', 'play_homevisitor']].apply(lambda x: x['hometeam'] if x['play_homevisitor'] == 1 else x['visteam'], axis=1)
        
        Innings[year] = dictPlay[year].groupby(["Game_ID"],  as_index= True).max()['play_inning'].reset_index()
        Innings[year].rename(columns ={'play_inning': 'Innings'}, inplace=True)
        dictPlayGrouped[year] = pd.merge(dictPlayGrouped[year], Innings[year], on = 'Game_ID')
        
    dictPlayGrouped[minimum].to_csv(r'.\tables\dictPlay_Grouped.csv')
    Innings[minimum].to_csv(r'.\tables\Innings.csv')
    
    return dictPlayGrouped, Innings

def importConstantCfip():
    dataset_Constant_Cfip = pd.read_excel(r'.\Cfip\cfip.xlsx', index_col = 0, header = 0)
    
    return dataset_Constant_Cfip        


def createOffensiveAndDefensiveVariables(df, cfip, minimum, maximum):

    for year in range(minimum,maximum):
        
        df[year]["Plate_appeareances"] = df[year][['Strikeouts','hits','Fielders_Choice','Walks','Hit_by_Pitch','Sacrifice_hits','Sacrifice_flies','Fly_ball_out','Gound_out','Catcher_intereference','Reached_on_error']].sum(axis=1)
        
        df[year]['At_bats'] = df[year]['Plate_appeareances'] - df[year]['at_bats_substractor']
        
        df[year]['Batting_Average_BA'] = df[year]['hits'] / df[year]['At_bats']
        
        df[year]['On_Base_OBP'] = (df[year]['hits'] + df[year]['Walks'] + df[year]['Hit_by_Pitch'])/(df[year]['At_bats'] + df[year]['Walks'] + df[year]['Hit_by_Pitch'] + df[year]['Sacrifice_hits'] + df[year]['Sacrifice_flies'])
        
        df[year]['Slugging_SLG'] = (df[year]['Singles'] + (2*df[year]['Doubles']) + (3*df[year]['Triples']) + (4*df[year]['Home_Runs']))/(df[year]['At_bats'])
        
        df[year]['Runs_scored'] = df[year]['Home_Runs'] + df[year]['Home_Reaches']
        
        print(cfip.loc[year,'cfip'])
        df[year]['FIP'] = (((13*df[year]['Home_Runs']) + (3*(df[year]['Walks'] + df[year]['Hit_by_Pitch'])) - (2*df[year]['Strikeouts']))/df[year]["Innings"]) / cfip.loc[year,'cfip']
    
    df[minimum].to_csv(r'.\tables\dict_GamesPerTeam.csv')
    
    return df


def createOffensiveDataset(dict_Games_Per_Team,  minimum, maximum):
    for year in range(minimum,maximum):
        dictOffensiveMeasures[year] = dict_Games_Per_Team[year][['Game_ID', 'Team', 'Runs_scored', 'Batting_Average_BA', 'On_Base_OBP', 'Slugging_SLG']].copy()
    
    dictOffensiveMeasures[minimum].to_csv(r'.\tables\dict_OffensiveMeasures.csv')
    
    return dictOffensiveMeasures

def importtimesZonesDayLight_site():
    timesZonesDayLight_site = pd.read_excel(r'.\Timezones\timesZonesDayLight_site.xlsx', index_col = 0, header = 0)
    
    return timesZonesDayLight_site

def createChronologicGamesJetLag(dict_Games_Per_Team, dictInfo, timesZonesDayLight_site, minimum, maximum):
    dictTempInfo = {}
    dictTemp_Games_Per_Team = {}
    dictChronologicGames = {}
    
    for year in range(minimum,maximum):
        #Preparing the datasets to be used
        dictTemp_Games_Per_Team[year] = dict_Games_Per_Team[year][['Game_ID', 'Team', 'hometeam', 'visteam', 'play_homevisitor']]
        dictTempInfo[year] = dictInfo[year][['Game_ID','site','date']].copy()
        dictTempInfo[year].rename(columns ={'date': 'date_game', 'site': 'site_game'}, inplace=True)
        
        #Merging the information of site and date in the Games_per_team dataset.
        dictChronologicGames[year] = pd.merge(dictTemp_Games_Per_Team[year], dictTempInfo [year], on = 'Game_ID')
        
        #Sorting the dataset by Team and Date.
        dictChronologicGamesGrouped[year] = dictChronologicGames[year].sort_values(by = ['Team', 'date_game'], ascending=[True, True])
        
        
        #Creating the shifted columns or site and date. 
        dictChronologicGamesGrouped[year]['site_before'] = dictChronologicGamesGrouped[year]['site_game'].shift(periods= 1).fillna(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[0],'site_game'])
        dictChronologicGamesGrouped[year]['date_travel'] = dictChronologicGamesGrouped[year]['date_game'].shift(periods= 1).fillna(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[0],'date_game'])
        
        
        #Calculating the compensation value.
        dictChronologicGamesGrouped[year]['date_travel'] =  pd.to_datetime(dictChronologicGamesGrouped[year]['date_travel'], format='%Y/%m/%d')
        dictChronologicGamesGrouped[year]['date_game'] = pd.to_datetime(dictChronologicGamesGrouped[year]['date_game'], format='%Y/%m/%d')
        dictChronologicGamesGrouped[year]['Compensation']  = (dictChronologicGamesGrouped[year]['date_game'] - dictChronologicGamesGrouped[year]['date_travel']).dt.days
        
        #Inserting the Jet_Lag Value and the direction. 
        dictChronologicGamesGrouped[year] = dictChronologicGamesGrouped[year].join(timesZonesDayLight_site.stack().rename('Jet_Lag').rename_axis(('site_before','site_game')), on=['site_before','site_game'])
        
        def func(x):
            if x > 0:
                return "East"
            elif x < 0:
                return "West"
            else:
                return 'Same'            
        dictChronologicGamesGrouped[year]['Direction'] =  dictChronologicGamesGrouped[year]['Jet_Lag'].apply(func)
        
        #Inserting the JetLag Numeric Variable. 
        dictChronologicGamesGrouped[year]['Jet_Lag_numeric'] =  dictChronologicGamesGrouped[year]['Jet_Lag'].abs()
        
        #Inserting the JetLag boolean variable.
        dictChronologicGamesGrouped[year]['Jet_Lag_boolean'] =  dictChronologicGamesGrouped[year]['Jet_Lag_numeric'].apply(lambda x: 1 if x > 0 else 0)
        
        #Inserting the compensation.
        dictChronologicGamesGrouped[year]['Jet_Lag_Compensed'] =  dictChronologicGamesGrouped[year][['Compensation','Jet_Lag_numeric']].apply(lambda x: 0 if x['Jet_Lag_numeric'] == 0 else x['Jet_Lag_numeric'] - x['Compensation'], axis=1)
        dictChronologicGamesGrouped[year]['Jet_Lag_Compensed'] =  dictChronologicGamesGrouped[year]['Jet_Lag_Compensed'].apply(lambda x: 0 if x < 0 else x)
        
        #Solving issues due to the existence of different teams in the same file.
        dictChronologicGamesGrouped[year]['Jet_Lag'] =  dictChronologicGamesGrouped[year][['Jet_Lag','Compensation']].apply(lambda x: 0 if x['Compensation'] < 0 else x['Jet_Lag'], axis =1)
        dictChronologicGamesGrouped[year]['Direction'] =  dictChronologicGamesGrouped[year][['Direction','Compensation']].apply(lambda x: 'Same' if x['Compensation'] < 0 else x['Direction'], axis =1)
        dictChronologicGamesGrouped[year]['Jet_Lag_numeric'] =  dictChronologicGamesGrouped[year][['Jet_Lag_numeric','Compensation']].apply(lambda x: 0 if x['Compensation'] < 0 else x['Jet_Lag_numeric'], axis =1)
        dictChronologicGamesGrouped[year]['Jet_Lag_boolean'] =  dictChronologicGamesGrouped[year][['Jet_Lag_boolean','Compensation']].apply(lambda x: 0 if x['Compensation'] < 0 else x['Jet_Lag_boolean'], axis =1)
        dictChronologicGamesGrouped[year]['Jet_Lag_Compensed'] =  dictChronologicGamesGrouped[year][['Jet_Lag_Compensed','Compensation']].apply(lambda x: 0 if x['Compensation'] < 0 else x['Jet_Lag_Compensed'], axis =1)
        dictChronologicGamesGrouped[year]['Compensation'] =  dictChronologicGamesGrouped[year]['Compensation'].apply(lambda x: 0 if x < 0 else x)
       
        
        
                
    dictChronologicGamesGrouped[minimum].to_csv(r'.\tables\dict_ChronologicGamesGrouped.csv')
    
    return dictChronologicGamesGrouped

def combineOffensiveMeasureJetLag(dict_offensive_measures,dict_Chronologic_Games, minimum, maximum):
    
    for year in range(minimum,maximum):
        pass
        #Selecting the relevant columns from both datasets
        dict_offensive_measures[year].index = range(len(dict_offensive_measures[year]))
        dict_Chronologic_Games[year].index = range(len(dict_Chronologic_Games[year]))
        dict_Chronologic_Games[year] = dict_Chronologic_Games[year][['Game_ID','Team','Jet_Lag_numeric','Direction']]
        dictOffensiveMeasureJetLag[year] = pd.merge(dict_offensive_measures[year], dict_Chronologic_Games[year], on=['Game_ID','Team'])
        #dictOffensiveMeasureJetLag[year] = dict_offensive_measures[year].join(dict_Chronologic_Games[year], on=['Game_ID','Team'])
    
    dictOffensiveMeasureJetLag[minimum].to_csv(r'.\tables\dict_OffensiveMeasureJetLag.csv')
    
    return dictOffensiveMeasureJetLag

