# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 21:12:05 2019

@author: corve
"""
import pandas as pd 
dictPlayGrouped = {}
dictFinalVariables ={}
dictChronologicGamesGrouped = {}
dictOffensiveDefensiveMeasureJetLag = {}
dictInings = {}

dfOfensiveDataset = pd.DataFrame()
dfDefensiveDataset = pd.DataFrame()
Same = pd.DataFrame()
East = pd.DataFrame()
West = pd.DataFrame()



def createNewAttributes(dictPlay, info_teams, minimum,maximum):
    for year in range(minimum,maximum):
        print("######################## Creating the new columns in {} #####################".format(year))
              
        dictPlay[year]['Singles'] =  dictPlay[year]['play_event'].str.count('^S[1-9]')
        dictPlay[year]['Doubles'] =  dictPlay[year]['play_event'].str.count('^D[1-9]')
        dictPlay[year]['Triples'] =  dictPlay[year]['play_event'].str.count('^T[1-9]')
        dictPlay[year]['Home_Runs'] =  dictPlay[year]['play_event'].str.count('^HR|^H(?!P)')
        dictPlay[year]['hits'] =  dictPlay[year][['Singles','Doubles','Triples','Home_Runs']].sum(axis=1)
        
        dictPlay[year]['Errors'] =  dictPlay[year]['play_event'].str.count('^FLE|^E[1-9]|\(E[1-9]|[1-9]E[1-9]')
        dictPlay[year]['Reached_on_error'] =  dictPlay[year]['play_event'].str.count('^E[1-9]|\(E[1-9]|[1-9]E[1-9]')
        dictPlay[year]['Home_Reaches'] =  dictPlay[year]['play_event'].str.count('B-H|1-H|2-H|3-H')        
        dictPlay[year]['Walks'] =  dictPlay[year]['play_event'].str.count('^I|^IW|^W')
        dictPlay[year]['Strikeouts'] =  dictPlay[year]['play_event'].str.count('^K')
        dictPlay[year]['Stolen_bases'] =  dictPlay[year]['play_event'].str.count('SB|DI')
        dictPlay[year]['Caught_Stealing'] =  dictPlay[year]['play_event'].str.count('CS')
        dictPlay[year]['Sacrifice_hits'] =  dictPlay[year]['play_event'].str.count('(?<!C)SH')
        dictPlay[year]['Sacrifice_flies'] =  dictPlay[year]['play_event'].str.count('SF')
        dictPlay[year]['GIDP'] =  dictPlay[year]['play_event'].str.count('GDP')
        dictPlay[year]['Balk'] =  dictPlay[year]['play_event'].str.count('BK')
        dictPlay[year]['Catcher_intereference'] =  dictPlay[year]['play_event'].str.count('C/E2')
        dictPlay[year]['Hit_by_Pitch'] =  dictPlay[year]['play_event'].str.count('^HP')
        
        
        dictPlay[year]["Fielders_Choice"] =  dictPlay[year]['play_event'].str.count('^FC')
        dictPlay[year]["Fly_ball_out"] =  dictPlay[year]['play_event'].str.count('^[1-9]/')
        dictPlay[year]["Gound_out"] =  dictPlay[year]['play_event'].str.count('^[1-9]{2,}(?!.*(?:FO|SH|GDP|LDP).*).*$')
        
        
        
        
        dictPlay[year]['at_bats_substractor'] = dictPlay[year][['Catcher_intereference','Sacrifice_hits','Sacrifice_flies','Hit_by_Pitch','Walks']].sum(axis=1)
        dictPlay[year] = pd.merge(dictPlay[year], info_teams[year], on='Game_ID') 
        
        pathdictPlaytransformed = r'.\tables\output\dictPlay_transformed_' + str(year) + '.csv'
        dictPlay[year].to_csv(pathdictPlaytransformed)
        
        
    return dictPlay



def calculatePlayGrouped(dictPlay, minimum, maximum):    
    
    for year in range(minimum,maximum):
        
        print("######################## Grouping and Summing play variables in {} #####################".format(year))
              
        dictPlayGrouped[year] = dictPlay[year].groupby(["Game_ID","hometeam", "visteam", "play_homevisitor"],  as_index= True).sum()[['Singles', 'Doubles', 'Triples', 'Home_Runs', 'hits', 
                       'Errors', 'Reached_on_error', 'Home_Reaches', 'Walks', 'Strikeouts', 'Stolen_bases', 'Caught_Stealing', 'Sacrifice_hits', 'Sacrifice_flies',
                       'GIDP', 'Balk', 'Catcher_intereference', 'Hit_by_Pitch', 'Fielders_Choice', 'Fly_ball_out', 'Gound_out', 'at_bats_substractor']].reset_index()        
        dictPlayGrouped[year]['Team'] =  dictPlayGrouped[year][['hometeam','visteam', 'play_homevisitor']].apply(lambda x: x['hometeam'] if x['play_homevisitor'] == 1 else x['visteam'], axis=1)
        dictPlayGrouped[year]['Team_against'] =  dictPlayGrouped[year][['hometeam','visteam', 'play_homevisitor']].apply(lambda x: x['visteam'] if x['play_homevisitor'] == 1 else x['hometeam'], axis=1)
        
        dictInings[year] = dictPlay[year].groupby(["Game_ID"],  as_index= True).max()['play_inning'].reset_index()
        dictInings[year].rename(columns ={'play_inning': 'Innings'}, inplace=True)
        dictPlayGrouped[year] = pd.merge(dictPlayGrouped[year], dictInings[year], on = 'Game_ID')
        
        pathdictPlayGrouped = r'.\tables\output\dictPlay_Grouped_' + str(year) + '.csv'
        dictPlayGrouped[year].to_csv(pathdictPlayGrouped)
        
        pathdictInings = r'.\tables\output\dict_Innings_' + str(year) + '.csv'
        dictInings[year].to_csv(pathdictInings)

    
    return dictPlayGrouped, dictInings


def createOffensiveAndDefensiveVariables(df, cfip, minimum, maximum):

    for year in range(minimum,maximum):
        
        print("######################## Creating the Offensive and Deffensive Variables in {} #####################".format(year))
        
        df[year]["Plate_appeareances"] = df[year][['Strikeouts','hits','Fielders_Choice','Walks','Hit_by_Pitch','Sacrifice_hits','Sacrifice_flies','Fly_ball_out','Gound_out','Catcher_intereference','Reached_on_error']].sum(axis=1)
        
        df[year]['At_bats'] = df[year]['Plate_appeareances'] - df[year]['at_bats_substractor']
        
        df[year]['Batting_Average_BA'] = df[year]['hits'] / df[year]['At_bats']
        
        df[year]['On_Base_OBP'] = (df[year]['hits'] + df[year]['Walks'] + df[year]['Hit_by_Pitch'])/(df[year]['At_bats'] + df[year]['Walks'] + df[year]['Hit_by_Pitch'] + df[year]['Sacrifice_hits'] + df[year]['Sacrifice_flies'])
        
        df[year]['Slugging_SLG'] = (df[year]['Singles'] + (2*df[year]['Doubles']) + (3*df[year]['Triples']) + (4*df[year]['Home_Runs']))/(df[year]['At_bats'])
        
        df[year]['Runs_scored'] = df[year]['Home_Runs'] + df[year]['Home_Reaches']            
        
        df[year]['downShift'] = df[year]['Runs_scored'].shift(periods= 1).fillna(0)
        df[year]['upShift'] = df[year]['Runs_scored'].shift(periods= -1).fillna(0)
        df[year]['Runs_allowed'] =  df[year][['play_homevisitor','downShift', 'upShift']].apply(lambda x: x['upShift'] if x['play_homevisitor'] == 0 else x['downShift'], axis=1)
        
        df[year]['OPA'] = (df[year]['Singles'] + (2*df[year]['Doubles']) + (2.5*df[year]['Triples']) + (3.5*df[year]['Home_Runs']) + (0.8 * (df[year]['Walks'] + df[year]['Hit_by_Pitch'])) + (0.5 * df[year]['Stolen_bases']))/(df[year]['At_bats'] + df[year]['Walks'] + df[year]['Hit_by_Pitch'])
        
        df[year]['ERPA'] = ((0.499* df[year]['Singles']) + (0.728*df[year]['Doubles']) + (1.265*df[year]['Triples']) + (1.499*df[year]['Home_Runs']) + (0.353*(df[year]['Walks']) + (0.362*df[year]['Hit_by_Pitch']) + (0.1266*df[year]['Stolen_bases']) + (0.394*df[year]['Sacrifice_flies']) - (0.395*df[year]["Gound_out"]) - (0.085*(df[year]['At_bats'] - df[year]['hits']  - df[year]["Gound_out"])) - 67))/(df[year]['At_bats'] + df[year]['Walks'] + df[year]['Hit_by_Pitch'] + df[year]['Sacrifice_flies'])        
        
        df[year]['OA'] = ((df[year]['Singles'] + (2*df[year]['Doubles']) + (3*df[year]['Triples']) + (4*df[year]['Home_Runs'])) + df[year]['Walks'] + df[year]['Stolen_bases'])/(df[year]['At_bats'] + df[year]['Walks'])
        
        df[year]['Winning'] = df[year][['Runs_scored','Runs_allowed']].apply(lambda x: 1 if x['Runs_scored'] >= x['Runs_allowed'] else 0, axis=1)

        df[year]['FIP'] = (((13*df[year]['Home_Runs']) + (3*(df[year]['Walks'] + df[year]['Hit_by_Pitch'])) - (2*df[year]['Strikeouts']))/df[year]["Innings"]) + cfip.loc[year,'cfip']
        
        df[year]['BABIP'] =  (df[year]['hits']  - df[year]['Home_Runs'])/(df[year]['At_bats']  - df[year]['Home_Runs'] - df[year]['Strikeouts'] + df[year]['Sacrifice_flies'])
        
        pathGamesPerTeam = r'.\tables\output\dict_Games_Per_Team_' + str(year) + '.csv'
        df[year].to_csv(pathGamesPerTeam)
    
    
    return df



def createChronologicGamesJetLag(dict_Games_Per_Team, dictInfo, timesZonesDayLight_site, df_Elo, minimum, maximum):
    dictTempInfo = {}
    dictTemp_Games_Per_Team = {}
    dictChronologicGames = {}
    
    for year in range(minimum,maximum):
        
        print("######################## Creating JetLag Information in {} #####################".format(year))
        
        #Preparing the datasets to be used
        dictTemp_Games_Per_Team[year] = dict_Games_Per_Team[year][['Game_ID', 'Team', 'Team_against', 'hometeam', 'visteam', 'play_homevisitor']]
        dictTempInfo[year] = dictInfo[year][['Game_ID','site','date']].copy()
        dictTempInfo[year].rename(columns ={'date': 'date_game', 'site': 'site_game'}, inplace=True)

        #Merging the information of site and date in the Games_per_team dataset.
        dictChronologicGames[year] = pd.merge(dictTemp_Games_Per_Team[year], dictTempInfo[year], on = 'Game_ID')
        dictChronologicGames[year] = dictChronologicGames[year].drop_duplicates()
        
        #Sorting the dataset by Team and Date.
        dictChronologicGamesGrouped[year] = dictChronologicGames[year].sort_values(by = ['Team', 'date_game'], ascending=[True, True])
        
        #Creating the shifted columns or site and date. 
        dictChronologicGamesGrouped[year]['site_before'] = dictChronologicGamesGrouped[year]['site_game'].shift(periods= 1).fillna(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[0],'site_game'])
        dictChronologicGamesGrouped[year]['date_travel'] = dictChronologicGamesGrouped[year]['date_game'].shift(periods= 1).fillna(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[0],'date_game'])
        
        #Inserting Elo
        dictChronologicGamesGrouped[year]['Year'] = year
        dictChronologicGamesGrouped[year] = dictChronologicGamesGrouped[year].merge(df_Elo, how='left', on=['Year','Team']).fillna(0)
        
        #Inserting the Jet_Lag Value. 
        dictChronologicGamesGrouped[year] = dictChronologicGamesGrouped[year].join(timesZonesDayLight_site.stack().rename('Jet_Lag').rename_axis(('site_before','site_game')), on=['site_before','site_game'])       
        dictChronologicGamesGrouped[year]['Jet_Lag'] = dictChronologicGamesGrouped[year]['Jet_Lag'].apply(lambda x: 3 if x < -3 else x) 
        dictChronologicGamesGrouped[year]['Jet_Lag'] = dictChronologicGamesGrouped[year]['Jet_Lag'].apply(lambda x: -3 if x > 3 else x) 


        
        #Calculating the compensation value.
        dictChronologicGamesGrouped[year]['date_travel'] =  pd.to_datetime(dictChronologicGamesGrouped[year]['date_travel'], format='%Y/%m/%d')
        dictChronologicGamesGrouped[year]['date_game'] = pd.to_datetime(dictChronologicGamesGrouped[year]['date_game'], format='%Y/%m/%d')
        dictChronologicGamesGrouped[year]['Compensation']  = ((dictChronologicGamesGrouped[year]['date_game'] - dictChronologicGamesGrouped[year]['date_travel']).dt.days)
        
                
        #Inserting the JetLag Numeric Variable. 
        dictChronologicGamesGrouped[year]['Jet_Lag_numeric'] =  dictChronologicGamesGrouped[year]['Jet_Lag'].abs()
        
        dictChronologicGamesGrouped[year] = dictChronologicGamesGrouped[year].drop_duplicates()
        dictChronologicGamesGrouped[year]['Jet_Lag_Compensed'] = 0
        dictChronologicGamesGrouped[year]['Value_Jet_Lag_Compensed'] = 0
        dictChronologicGamesGrouped[year]['Sign'] = 0
        
        
        #Adjusting the initial games of season per team. 
        dictChronologicGamesGrouped[year]['First_Game'] = dictChronologicGamesGrouped[year]['Compensation'].apply(lambda x: 1 if x < 0 else 0)
        dictChronologicGamesGrouped[year]['Jet_Lag'] =  dictChronologicGamesGrouped[year][['First_Game','Jet_Lag']].apply(lambda x: 0 if x['First_Game'] == 1 else x['Jet_Lag'], axis=1)
        dictChronologicGamesGrouped[year]['Jet_Lag_numeric'] =  dictChronologicGamesGrouped[year][['First_Game','Jet_Lag_numeric']].apply(lambda x: 0 if x['First_Game'] == 1 else x['Jet_Lag_numeric'], axis=1)
        dictChronologicGamesGrouped[year]['Compensation'] =  dictChronologicGamesGrouped[year]['Compensation'].apply(lambda x: 0 if x < 0 else x)
        
        
        #Creating the Jet_Lag_Compensed by including the special considerations of first game and jet lag remaining.
        for i in range(1,len(dictChronologicGamesGrouped[year])):
            
            if(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'First_Game'] == 1):
                dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed'] = 0
            
            if(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'First_Game'] != 1):
                dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed'] = dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Jet_Lag'] + dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i-1],'Jet_Lag_Compensed'] 
            
            if(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed'] == 0):
                dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Jet_Lag_Compensed'] = 0
            
            if(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']<0):
                if(abs(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']) - dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Compensation'] < 0):
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Sign'] = 0
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Jet_Lag_Compensed'] = 0
                    
                if(abs(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']) - dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Compensation'] >= 0):
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Sign'] = -1
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Jet_Lag_Compensed'] = (abs(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']) - dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Compensation']) * dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Sign']
            
            if(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']>0):
                if(abs(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']) - dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Compensation'] < 0):
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Sign'] = 0
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Jet_Lag_Compensed'] = 0
                    
                if(abs(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']) - dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Compensation'] >= 0):
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Sign'] = 1
                    dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Jet_Lag_Compensed'] = (abs(dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Value_Jet_Lag_Compensed']) - dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Compensation']) * dictChronologicGamesGrouped[year].loc[dictChronologicGamesGrouped[year].index[i],'Sign']

         #Inserting the Direction value
        def func(x):
            if x > 0:
                return "East"
            elif x < 0:
                return "West"
            else:
                return 'Same' 
        dictChronologicGamesGrouped[year]['Direction'] =  dictChronologicGamesGrouped[year]['Jet_Lag_Compensed'].apply(func)        

        #Modyfing Jet_Lag_boolean to relate it to Jet_Lag_Compensed as in the paper:
        #A value of 0 was assigned if the team had no jet lag (1 h or less), and 1 if the team had jet lag (2 h or more).
        dictChronologicGamesGrouped[year]['Jet_Lag_boolean'] =  dictChronologicGamesGrouped[year]['Jet_Lag_Compensed'].apply(lambda x: 0 if -1 < x < 1 else 1)  
        
        pathChronologicalGamesGrouped = r'.\tables\output\dict_Chronological_Games_Grouped_' + str(year) + '.csv'
        dictChronologicGamesGrouped[year].to_csv(pathChronologicalGamesGrouped)
       
    
    return dictChronologicGamesGrouped

def createStatisticlVariables(dict_Games_Per_Team,  minimum, maximum):
    
    for year in range(minimum,maximum):
        
        print("######################## Creating Final Variables Dictionary in {} #####################".format(year))
        
        dictFinalVariables[year] = dict_Games_Per_Team[year][['Game_ID', 'Team', 'play_homevisitor', 'At_bats', 'Singles', 'Doubles', 'Triples', 'Home_Runs', 'Walks', 'Strikeouts', 'Stolen_bases', 'Caught_Stealing', 'Sacrifice_hits', 'Sacrifice_flies', 'GIDP', 'OPA', 'ERPA', 'OA', 'Winning', 'Runs_scored', 'Runs_allowed', 'Batting_Average_BA', 'On_Base_OBP', 'Slugging_SLG','FIP','BABIP','Errors']].copy()
        dictFinalVariables[year]['play_homevisitor_against'] =  dictFinalVariables[year]['play_homevisitor'].apply(lambda x: 'Away' if x == 1 else 'Home')
        dictFinalVariables[year]['play_homevisitor'] =  dictFinalVariables[year]['play_homevisitor'].apply(lambda x: 'Home' if x == 1 else 'Away')
        
        
        pathFinalVariables = r'.\tables\output\dict_Final_Variables_' + str(year) + '.csv'
        dictFinalVariables[year].to_csv(pathFinalVariables)    

    return dictFinalVariables


def combineOffensiveDefensiveMeasureJetLag(dict_offensive_measures,dict_Chronologic_Games, minimum, maximum):
    
    for year in range(minimum,maximum):
        
        print("######################## Combining Off and Def Stats with Jetlag information in {} #####################".format(year))
              
        #Selecting the relevant columns from both datasets
        dict_offensive_measures[year].index = range(len(dict_offensive_measures[year]))
        dict_Chronologic_Games[year].index = range(len(dict_Chronologic_Games[year]))
        dict_Chronologic_Games[year] = dict_Chronologic_Games[year][['Game_ID','Team','Team_against','Elo','Jet_Lag','Direction','Jet_Lag_numeric','Jet_Lag_boolean', 'Jet_Lag_Compensed']]
        dictOffensiveDefensiveMeasureJetLag[year] = pd.merge(dict_offensive_measures[year], dict_Chronologic_Games[year], on=['Game_ID','Team'])
        
        #Creating the mirror values for the team against.
        dictOffensiveDefensiveMeasureJetLag[year]['downShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Direction'].shift(periods= 1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['upShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Direction'].shift(periods= -1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['Direction_against'] =  dictOffensiveDefensiveMeasureJetLag[year][['play_homevisitor','downShift', 'upShift']].apply(lambda x: x['upShift'] if x['play_homevisitor'] == 'Away' else x['downShift'], axis=1)
        
        dictOffensiveDefensiveMeasureJetLag[year]['downShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_numeric'].shift(periods= 1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['upShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_numeric'].shift(periods= -1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_numeric_against'] =  dictOffensiveDefensiveMeasureJetLag[year][['play_homevisitor','downShift', 'upShift']].apply(lambda x: x['upShift'] if x['play_homevisitor'] == 'Away' else x['downShift'], axis=1)
        
        dictOffensiveDefensiveMeasureJetLag[year]['downShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_boolean'].shift(periods= 1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['upShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_boolean'].shift(periods= -1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_boolean_against'] =  dictOffensiveDefensiveMeasureJetLag[year][['play_homevisitor','downShift', 'upShift']].apply(lambda x: x['upShift'] if x['play_homevisitor'] == 'Away' else x['downShift'], axis=1)

        dictOffensiveDefensiveMeasureJetLag[year]['downShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_Compensed'].shift(periods= 1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['upShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_Compensed'].shift(periods= -1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_Compensed_against'] =  dictOffensiveDefensiveMeasureJetLag[year][['play_homevisitor','downShift', 'upShift']].apply(lambda x: x['upShift'] if x['play_homevisitor'] == 'Away' else x['downShift'], axis=1)
        
        dictOffensiveDefensiveMeasureJetLag[year]['downShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag'].shift(periods= 1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['upShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag'].shift(periods= -1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['Jet_Lag_against'] =  dictOffensiveDefensiveMeasureJetLag[year][['play_homevisitor','downShift', 'upShift']].apply(lambda x: x['upShift'] if x['play_homevisitor'] == 'Away' else x['downShift'], axis=1)

        dictOffensiveDefensiveMeasureJetLag[year]['downShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Elo'].shift(periods= 1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['upShift'] = dictOffensiveDefensiveMeasureJetLag[year]['Elo'].shift(periods= -1).fillna(0)
        dictOffensiveDefensiveMeasureJetLag[year]['Elo_against'] =  dictOffensiveDefensiveMeasureJetLag[year][['play_homevisitor','downShift', 'upShift']].apply(lambda x: x['upShift'] if x['play_homevisitor'] == 'Away' else x['downShift'], axis=1)
        
        dictOffensiveDefensiveMeasureJetLag[year]['Net_Elo'] = dictOffensiveDefensiveMeasureJetLag[year]['Elo'] - dictOffensiveDefensiveMeasureJetLag[year]['Elo_against']
        
        dictOffensiveDefensiveMeasureJetLag[year] = dictOffensiveDefensiveMeasureJetLag[year].drop(['downShift', 'upShift'], axis=1)
        
        pathOffensiveDefensiveMeasureJetLag = r'.\tables\output\dict_Offensive_Defensive_Measure_JetLag_' + str(year) + '.csv'
        dictOffensiveDefensiveMeasureJetLag[year].to_csv(pathOffensiveDefensiveMeasureJetLag)

    
    return dictOffensiveDefensiveMeasureJetLag

def createFinalDataset(df, minimum, maximum):
    
    print("######################## Creating final dataframe #####################")
          
    dfFinalDataset = pd.DataFrame()
    dfFinalDataset = pd.concat(df.values(), ignore_index=True)
    
    pathFinalDataset = r'.\tables\output\df_Final_Dataset_' + str(minimum) + '_to_' + str(maximum - 1) + '.csv'
    dfFinalDataset.to_csv(pathFinalDataset)
    
    return dfFinalDataset
    