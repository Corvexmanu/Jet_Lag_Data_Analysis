library(tidyverse)

#Importing data
df_bg <- read_csv('./tables/output/df_Final_Dataset_1992_to_2011.csv')

#Adjusting classes
df_bg <- as.data.frame(unclass(df_bg))
lapply(df_bg, class)

df_bg <- filter(df_bg, df_bg$Jet_Lag_Compensed < 4)

count_games <- as.data.frame(table(df_bg$Game_ID)) %>%
  filter(Freq != 2)

#Exploring the data visually. 


#Creating data control group Home
df_bg_cg_h <- filter(df_bg, df_bg$Jet_Lag_Compensed == 0) %>%
  filter(play_homevisitor == 'Home') %>%
  select(Game_ID, Team, Runs_scored, Batting_Average_BA, On_Base_OBP, Slugging_SLG, FIP, BABIP, Errors)

#Creating data control group Home
df_bg_cg_v <- filter(df_bg, df_bg$Jet_Lag_Compensed == 0) %>%
  filter(play_homevisitor == 'Visitor') %>%
  select(Game_ID, Team, Runs_scored, Batting_Average_BA, On_Base_OBP, Slugging_SLG, FIP, BABIP, Errors)


#Creating data experiment h.1 = Jetlag !+ 0, Home + West Jetlag
df_bg_eh.1 <- filter(df_bg, Jet_Lag_Compensed != 0) %>%
  filter(play_homevisitor == 'Home') %>%
  filter(Direction == 'West') %>%
  select(Game_ID, Team, Runs_scored, Batting_Average_BA, On_Base_OBP, Slugging_SLG, FIP, BABIP, Errors)

#Creating data experiment h.2 = Jetlag !+ 0, Home + East Jetlag
df_bg_eh.2 <- filter(df_bg, Jet_Lag_Compensed != 0) %>%
  filter(play_homevisitor == 'Home') %>%
  filter(Direction == 'East') %>%
  select(Game_ID, Team, Runs_scored, Batting_Average_BA, On_Base_OBP, Slugging_SLG, FIP, BABIP, Errors)

#Creating data experiment v.1 = Jetlag !+ 0, Visitor + West Jetlag
df_bg_ev.1 <- filter(df_bg, Jet_Lag_Compensed != 0) %>%
  filter(play_homevisitor == 'Visitor') %>%
  filter(Direction == 'West') %>%
  select(Game_ID, Team, Runs_scored, Batting_Average_BA, On_Base_OBP, Slugging_SLG, FIP, BABIP, Errors)

#Creating data experiment v.2 = Jetlag !+ 0, Visitor + East Jetlag
df_bg_ev.2 <- filter(df_bg, Jet_Lag_Compensed != 0) %>%
  filter(play_homevisitor == 'Visitor') %>%
  filter(Direction == 'East') %>%
  select(Game_ID, Team, Runs_scored, Batting_Average_BA, On_Base_OBP, Slugging_SLG, FIP, BABIP, Errors)


mean(df_bg_cg$Slugging_SLG)

mean(df_bg_e1.1$Slugging_SLG)
mean(df_bg_e1.2$Slugging_SLG)
mean(df_bg_e1.3$Slugging_SLG)
mean(df_bg_e1.4$Slugging_SLG)

