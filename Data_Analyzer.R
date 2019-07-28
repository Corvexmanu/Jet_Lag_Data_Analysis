library(tidyverse)
library(goftest)
library(broom)
library(ggalt)
library(GGally)
library(dplyr)
library(tidyr)
library(forcats)

################################################IMPORTING DATA########################################################
data_importer_df <- function (){
  df<- read_csv('./tables/output/df_Final_Dataset_1975_to_2018.csv') %>%
    mutate(Venue_Team = paste(play_homevisitor, Team, sep = ""),
           Venue_Team_Against = paste(play_homevisitor_against, Team_against, sep = ""),
           Venue_DirectionJetlag_Team = paste(play_homevisitor, Direction, sep = ""),
           Venue_DirectionJetlag_Against = paste(play_homevisitor_against, Direction_against, sep = ""),
           Venue = play_homevisitor) %>%
    select (-c(play_homevisitor, play_homevisitor_against,Direction_against))
  
  df <- as.data.frame(unclass(df))
  
  df <- df %>%
    mutate(Jet_Lag_boolean = as.factor(df$Jet_Lag_boolean),
           Jet_Lag_boolean_against = as.factor(df$Jet_Lag_boolean_against),
           Winning = as.factor(df$Winning),
           Jet_Lag = as.factor(df$Jet_Lag),
           Jet_Lag = as.factor(df$Jet_Lag),
           Jet_Lag_against = as.factor(df$Jet_Lag_against),
           Jet_Lag_numeric = as.factor(df$Jet_Lag_numeric),
           Jet_Lag_numeric_against = as.factor(df$Jet_Lag_numeric_against),
           Jet_Lag_Compensed = as.factor(df$Jet_Lag_Compensed),
           Jet_Lag_Compensed_against = as.factor(df$Jet_Lag_Compensed_against),
           Venue_DirectionJetlag_Against = as.factor(df$Venue_DirectionJetlag_Against),
           Venue_DirectionJetlag_Team = as.factor(df$Venue_DirectionJetlag_Team),
           Venue_Team = as.factor(df$Venue_Team))
  return(df)
}

data_importer_df_bg <- function(){
  df_bg<- read_csv('./tables/output/df_Final_Dataset_1975_to_2018.csv') %>%
    mutate(Venue_Team = paste(play_homevisitor, Team, sep = ""),
           Venue_Team_Against = paste(play_homevisitor_against, Team_against, sep = ""),
           Venue_DirectionJetlag_Team = paste(play_homevisitor, Direction, sep = ""),
           Venue_DirectionJetlag_Against = paste(play_homevisitor_against, Direction_against, sep = ""),
           Venue = play_homevisitor) %>%
    filter(Jet_Lag_boolean == 1) %>%
    filter(Jet_Lag_Compensed < 4) %>%
    select (-c(play_homevisitor, play_homevisitor_against,Direction_against))
  
  df_bg <- as.data.frame(unclass(df_bg))
  df_bg <- df_bg %>%
    mutate(Jet_Lag_boolean = as.factor(df_bg$Jet_Lag_boolean),
           Jet_Lag_boolean_against = as.factor(df_bg$Jet_Lag_boolean_against),
           Winning = as.factor(df_bg$Winning),
           Jet_Lag = as.factor(df_bg$Jet_Lag),
           Jet_Lag = as.factor(df_bg$Jet_Lag),
           Jet_Lag_against = as.factor(df_bg$Jet_Lag_against),
           Jet_Lag_numeric = as.factor(df_bg$Jet_Lag_numeric),
           Jet_Lag_numeric_against = as.factor(df_bg$Jet_Lag_numeric_against),
           Jet_Lag_Compensed = as.factor(df_bg$Jet_Lag_Compensed),
           Jet_Lag_Compensed_against = as.factor(df_bg$Jet_Lag_Compensed_against),
           Venue_DirectionJetlag_Against = as.factor(df_bg$Venue_DirectionJetlag_Against),
           Venue_DirectionJetlag_Team = as.factor(df_bg$Venue_DirectionJetlag_Team),
           Venue_Team = as.factor(df_bg$Venue_Team))
  return(df_bg)
}

df <- data_importer_df()
df_bg <- data_importer_df_bg()

df_summary <- select(df_bg, c(OPA,OA,Runs_scored,Batting_Average_BA,On_Base_OBP,Slugging_SLG,Net_Elo)) %>%
  gather(Offensive_Statistic, Measure, OPA:Net_Elo)%>%
  group_by(Offensive_Statistic)%>%
  summarise_all(funs(mean,median,min,max))

kable(df_summary, format = 'markdown', digits = 2, align = 'c')

#Data for our linear analysis:
df_bg_lm <- select(df_bg, c(OPA,ERPA,OA,Winning,Runs_scored,Runs_allowed,Batting_Average_BA,On_Base_OBP,Slugging_SLG,
                            Net_Elo,
                            Venue_Team, Venue_Team_Against, 
                            Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                            Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))

###################################################VISUALIZATION ANALYSIS###############################################

df_off_plots <- select(df, c(Jet_Lag,Jet_Lag_boolean, Venue,Venue_DirectionJetlag_Team,Jet_Lag_Compensed,OPA,OA,Runs_scored,Batting_Average_BA,On_Base_OBP,Slugging_SLG,Net_Elo)) %>%
  filter(Jet_Lag_Compensed != '4') %>%
  gather(Offensive_Statistic, Measure, OPA:Slugging_SLG)

df_bg_plots <- mutate(df_bg, Venue_DirectionJetlag_Value_Team = paste(Venue_DirectionJetlag_Team,Jet_Lag_Compensed,sep = ""),
                      Venue_DirectionJetlag_Value_Team = as.factor(Venue_DirectionJetlag_Value_Team))
df_bg_plots <- mutate(df_bg_plots, Venue_DirectionJetlag_Value_Team = fct_relevel(Venue_DirectionJetlag_Value_Team,
                                                                                  "HomeWest-2", "HomeWest-1",
                                                                                  "HomeEast1","HomeEast2",
                                                                                  "AwayWest-2", "AwayWest-1",
                                                                                  "AwayEast1","AwayEast2"))

ggplot(data = df, aes(Jet_Lag_boolean)) +
  geom_bar(color="black", fill="lightskyblue") +
  xlab("Presence of Jet Lag")+
  scale_x_discrete(labels = c("Jet Lag","No Jet Lag"))+
  ylab("Frequency of Games per Team") +
  theme_bw()

ggplot(data = df_bg, aes(Direction)) +
  geom_bar(color="black", fill="lightskyblue") +
  xlab("DIrection of Jet Lag")+
  scale_x_discrete(labels = c("Eastward","Westward"))+
  ylab("Frequency of Games per Team") +
  theme_bw()


ggplot(data = df_bg, aes(Venue)) +
  geom_bar(color="black", fill="lightskyblue") +
  xlab("Venue principal team")+
  #scale_x_discrete(labels = c("Eastward","Westward"))+
  ylab("Frequency of Games per Team") +
  theme_bw()

#General Analysis:

ggplot(data = df_off_plots ,aes(x=Net_Elo))+
  geom_histogram(aes(y=..density..),color="black", fill="lightskyblue")+
  stat_function(fun = "dnorm",
                args = list(mean(df_bg$Net_Elo),
                            sd = sd(df_bg$Net_Elo)), size = 1)+
  ylab('Density of frequencies')+
  facet_wrap(~Offensive_Statistic)+
  xlab('Net difference of Relative Skills \namong baseball teams')+
  theme_bw()

ggplot(data = df_off_plots ,aes(x=Measure))+
  geom_histogram(color="black", fill="lightskyblue")+
  #stat_function(fun = "dnorm", args = list(mean(df_bg$Net_Elo), sd = sd(df_bg$Net_Elo)), size = 1)+
  ylab('Frequency values')+
  facet_wrap(~Offensive_Statistic, scales="free")+
  xlab('Offensive statistic measurement scale' )+
  theme_bw()

normFunc <- function(x){(x-mean(x, na.rm = T))/sd(x, na.rm = T)}

df_off_plots_scale <- select(df, c(Jet_Lag,Jet_Lag_boolean,Venue_DirectionJetlag_Team,Jet_Lag_Compensed,OPA,OA,Runs_scored,Batting_Average_BA,On_Base_OBP,Slugging_SLG,Net_Elo)) %>%
  mutate(Runs_scored = normFunc(df$Runs_scored))%>%
  filter(Jet_Lag_Compensed != '4') %>%
  gather(Offensive_Statistic, Measure, OPA:Slugging_SLG)

ggplot(data = df_off_plots_scale ,aes(x=Measure))+
  geom_histogram(color="black", fill="lightskyblue")+
  #stat_function(fun = "dnorm", args = list(mean(df_bg$Net_Elo), sd = sd(df_bg$Net_Elo)), size = 1)+
  ylab('Frequency values')+
  facet_wrap(~Offensive_Statistic, scales="free")+
  xlab('Offensive statistic measurement scale ')+
  theme_bw()

ggplot(data=df, aes(x=Jet_Lag, y=OPA)) + geom_boxplot() +
  xlab("Number of Time Zones Crossed")+
  theme_bw() + ylab("Offensive Performance Average") + coord_flip()

ggplot(data=df, aes(x=Jet_Lag_boolean, y=OPA)) + geom_boxplot() +
  xlab("Existence of Time Zones Crossed")+
  theme_bw() + ylab("Offensive Performance Average") + coord_flip()

df_off_plots_2 <- filter(df_off_plots, Venue_DirectionJetlag_Team != 'HomeSame')%>%
  filter(Venue_DirectionJetlag_Team != 'AwaySame')

ggplot(data=df_off_plots_2, aes(y= Measure, x=Venue_DirectionJetlag_Team)) + geom_boxplot(color="black", fill="lightskyblue") +
  xlab("Jet lag Boolean\nMeasurement levels")+
  facet_wrap( ~ Offensive_Statistic, scales="free_y")+
  #scale_x_discrete(labels=c("No Jetlag", "Jetlag"))+
  theme_bw() + ylab("Offensive statistic values")

df_off_plots_level <- select(df_bg, c(Jet_Lag,Jet_Lag_boolean, Venue,Venue_DirectionJetlag_Team,Jet_Lag_Compensed,OPA,OA,Runs_scored,Batting_Average_BA,On_Base_OBP,Slugging_SLG,Net_Elo)) %>%
  filter(Jet_Lag_Compensed != '4') %>%
  #select(-c(Runs_scored))%>%
  gather(Offensive_Statistic, Measure, OPA:Slugging_SLG)

ggplot(data=df_off_plots_level, aes(y= Measure, x=Jet_Lag_Compensed)) +
  geom_boxplot(color="black", fill="lightskyblue") +
  xlab("JetLag Level")+
  facet_grid(Offensive_Statistic ~ Venue, scales="free_y")+
  theme_bw() + ylab("Measurement Value")


#Boolean Analysis:

ggplot(data=df_bg, aes(x=Venue_DirectionJetlag_Team, y=OPA)) + geom_boxplot() +
  xlab("Presence of JetLag Compensed\nBy Direction and Venue")+
  facet_wrap( ~ Venue, scales="free_x")+
  theme_bw() + ylab("Offensive Performance Average")

ggplot(data=df_bg, aes(x=Venue_DirectionJetlag_Team, y=OPA)) + geom_boxplot() +
  xlab("Presence of JetLag Compensed\nBy Direction and Venue")+
  facet_wrap( ~ Direction, scales="free_x")+
  theme_bw() + ylab("Offensive Performance Average")


#Numeric Analysis:
ggplot(data=df_bg_plots, aes(x=Venue_DirectionJetlag_Value_Team, y=OPA)) + geom_boxplot() +
  xlab("Level of JetLag Compensed\nBy Direction and Venue")+
  theme_bw() + ylab("Offensive Performance Average")   + coord_flip()

ggplot(data=df_bg_plots, aes(x=Venue_DirectionJetlag_Value_Team, y=OPA)) + geom_boxplot() +
  xlab("Level of JetLag Compensed\nBy Venue")+
  facet_wrap( ~ Venue, scales="free_x")+
  theme_bw() + ylab("Offensive Performance Average")

ggplot(data=df_bg_plots, aes(x=Venue_DirectionJetlag_Value_Team, y=OPA)) + geom_boxplot() +
  xlab("Level of JetLag Compensed\nBy Direction")+
  facet_wrap( ~ Direction, scales="free_x")+
  theme_bw() + ylab("Offensive Performance Average")


###############################################OFENSIVE BOOLEAN MODEL#########################################


##Creating Datasets to analyze each stat##

df_bg_bol_lm <- select(df_bg_lm, c(Venue_Team, Venue_Team_Against, 
                                Venue_DirectionJetlag_Team, Venue_DirectionJetlag_Against))

df_bg_bol_lm <-   rownames_to_column(df_bg_bol_lm,'rn') %>%
  gather(key, val, Venue_Team:Venue_DirectionJetlag_Against) %>% 
  count(rn, val) %>%
  spread(val, n, fill = 0)  %>%
  select(-rn) %>%
  mutate_all(as.factor) %>%
  mutate(Net_Elo = df_bg_lm$Net_Elo)%>%
  select(-c(HomeSame,AwaySame))

#OPA#
df_bg_bol_lm_OPA <- mutate(df_bg_bol_lm,
                           OPA = df_bg_lm$OPA)

#ERPA#
df_bg_bol_lm_ERPA <- mutate(df_bg_bol_lm,
                            ERPA = df_bg_lm$ERPA)

#OA#
df_bg_bol_lm_OA <- mutate(df_bg_bol_lm,
                          OA = df_bg_lm$OA )

#Winning#
df_bg_bol_lm_Winning <- mutate(df_bg_bol_lm,
                               Winning = df_bg_lm$Winning)

#Runs_scored#
df_bg_bol_lm_Runs_scored <- mutate(df_bg_bol_lm,
                                   Runs_scored = df_bg_lm$Runs_scored)

#Batting_Average_BA#
df_bg_bol_lm_Batting_Average_BA <- mutate(df_bg_bol_lm,
                                          Batting_Average_BA = df_bg_lm$Batting_Average_BA)

#On_Base_OBP#
df_bg_bol_lm_On_Base_OBP <- mutate(df_bg_bol_lm,
                                   On_Base_OBP = df_bg_lm$On_Base_OBP)

#Slugging_SLG#
df_bg_bol_lm_Slugging_SLG <- mutate(df_bg_bol_lm,
                                    Slugging_SLG = df_bg_lm$Slugging_SLG)

##Creating Linear Model for each stat##
bg_bol_OPA_lm <- lm(OPA~., data=df_bg_bol_lm_OPA)
bg_bol_ERPA_lm <- lm(ERPA~., data=df_bg_bol_lm_ERPA)
bg_bol_OA_lm <- lm(OA~., data=df_bg_bol_lm_OA)
bg_bol_Winning_lm <- lm(Winning~., data=df_bg_bol_lm_Winning)
bg_bol_Runs_Scored_lm <- lm(Runs_scored~., data=df_bg_bol_lm_Runs_scored)
bg_bol_Batting_Average_BA_lm <- lm(Batting_Average_BA~., data=df_bg_bol_lm_Batting_Average_BA)
bg_bol_OBP_lm <- lm(On_Base_OBP~., data=df_bg_bol_lm_On_Base_OBP)
bg_bol_SLG_lm <- lm(Slugging_SLG~., data=df_bg_bol_lm_Slugging_SLG)


##Creating confidence Intervals##
tidy_bg_bol_OPA_lm <- tidy(bg_bol_OPA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_bol_ERPA_lm <- tidy(bg_bol_ERPA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_bol_OA_lm <- tidy(bg_bol_OA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_bol_Winning_lm <- tidy(bg_bol_Winning_lm, conf.int = T, conf.level = 0.95)
tidy_bg_bol_Runs_Scored_lm <- tidy(bg_bol_Runs_Scored_lm, conf.int = T, conf.level = 0.95)
tidy_bg_bol_Batting_Average_BA_lm <- tidy(bg_bol_Batting_Average_BA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_bol_OBP_lm <- tidy(bg_bol_OBP_lm, conf.int = T, conf.level = 0.95)
tidy_bg_bol_SLG_lm <- tidy(bg_bol_SLG_lm, conf.int = T, conf.level = 0.95)


##Getting Results##
bg_bol_OPA_sum <- summary(bg_bol_OPA_lm)


summary(bg_bol_ERPA_lm)
summary(bg_bol_OA_lm)
summary(bg_bol_Winning_lm)
summary(bg_bol_Runs_Scored_lm)
summary(bg_bol_Batting_Average_BA_lm)
summary(bg_bol_OBP_lm)
summary(bg_bol_SLG_lm)


################################################ANALYSIS OF BOOLEAN MODEL#######################################

#Extracting Parameters
r_OPA_bol <- filter(tidy_bg_bol_OPA_lm, 
                  term == 'HomeWest1' |term == 'HomeEast1' | term == 'AwayWest1' |term == 'AwayEast1' | term == 'Net_Elo')
r_ERPA_bol <- filter(tidy_bg_bol_ERPA_lm, 
                  term == 'HomeWest1' |term == 'HomeEast1' | term == 'AwayWest1' |term == 'AwayEast1' | term == 'Net_Elo')
r_OA_bol <- filter(tidy_bg_bol_OA_lm, 
                   term == 'HomeWest1' |term == 'HomeEast1' | term == 'AwayWest1' |term == 'AwayEast1' | term == 'Net_Elo')
r_Runs_Scored_bol <- filter(tidy_bg_bol_Runs_Scored_lm,
                          term == 'HomeWest1' |term == 'HomeEast1' | term == 'AwayWest1' |term == 'AwayEast1' | term == 'Net_Elo')
r_Batting_Average_BA_bol <- filter(tidy_bg_bol_Batting_Average_BA_lm,
                                 term == 'HomeWest1' |term == 'HomeEast1' | term == 'AwayWest1' |term == 'AwayEast1' | term == 'Net_Elo')
r_Batting_OBP_bol <- filter(tidy_bg_bol_OBP_lm, 
                                 term == 'HomeWest1' |term == 'HomeEast1' | term == 'AwayWest1' |term == 'AwayEast1' | term == 'Net_Elo')
r_Batting_SLG_bol <- filter(tidy_bg_bol_SLG_lm, 
                                 term == 'HomeWest1' |term == 'HomeEast1' | term == 'AwayWest1' |term == 'AwayEast1' | term == 'Net_Elo')


#Analisis OPA Statistic#

#Correlation#
df_bg_bol_lm_OPA.pairs <- ggpairs(df_bg_lm, columns = c("OPA","OA","Slugging_SLG",'Runs_scored', 'Batting_Average_BA', 'On_Base_OBP',"Net_Elo"),
                     lower=list(continuous="smooth"),
                     diag=list(continuous="densityDiag"))
df_bg_bol_lm_OPA.pairs

#Normality of residuals#
fortify_bol_lm_OPA <- fortify(bg_bol_OPA_lm)
fortify_bol_lm_OPA$Venue_DirectionJetlag_Team <- df_bg_lm$Venue_DirectionJetlag_Team

ggplot(data = fortify_bol_lm_OPA, aes(x=.resid))+
  geom_histogram(colour = "black", fill = "lightskyblue", aes(y=..density..))+
  stat_function(fun = "dnorm",
                args = list(mean(fortify_bol_lm_OPA$.resid),
                            sd = sd(fortify_bol_lm_OPA$.resid)), size = 1)+
  theme_bw()+
  xlab("Error Residuals")+
  facet_wrap(~Venue_DirectionJetlag_Team)+
  ylab("Distribution of Residuals")

ggplot(data=fortify_bol_lm_OPA, aes(x=.fitted, y=.resid)) +
  geom_point() + theme_bw() + xlab("Fitted values") +
  #facet_wrap(~Venue_DirectionJetlag_Team)+
  ylab("Residuals") + geom_smooth()

ggplot(data=fortify_bol_lm_OPA, aes(x=.fitted, y=.resid)) +
  geom_point() + theme_bw() + xlab("Fitted values") +
  facet_wrap(~Venue_DirectionJetlag_Team)+
  geom_encircle(color=NA, fill="lightskyblue", alpha=0.25, s_shape = 1 , expand=0) +
  ylab("Residuals")

ggplot(data=fortify_bol_lm_OPA, aes(sample=.stdresid)) +
  stat_qq(geom="point") + geom_abline() +
  xlab("Theoretical (Z ~ N(0,1))") +
  facet_wrap(~Venue_DirectionJetlag_Team)+
  ylab("Sample") + coord_equal() + theme_bw()

ad.test(fortify_bol_lm_OPA$.stdresid, null = "pnorm", mean = 0, sd = 1)

#Intercepts to create the equation# (Why I have two values with NA?)
bg_bol_OPA_lm

#Goodness of fit = 0.0210 -> explains the 2.1%
glance(bg_bol_OPA_lm)

#Information about our fitted model: 
#9946 degrees of freedom as we started with 10016 observations and estimated 70 parameters. R tells us this in the summary output we have evidence to reject H0 for 
#3  parameters as their p values are less than 0.05 -> Intercept + Net_Elo + AwayWest
summary(bg_bol_OPA_lm)

#Here we specifed 95% confidence. So we've detected an effect of 
#Intercept 0.4496703936(0.4027465378,0.4965942495)
#Net_Elo 0.0004310896(0.0003614059,0.0005007733)
#AwayWest 0.0117774970(0.0009316292,0.0226233647)
#At a significance level of 0.05
tidy_bg_bol_OPA_lm <- tidy(bg_bol_OPA_lm, conf.int = T, conf.level = 0.95)
select(tidy_bg_bol_OPA_lm, term, estimate, conf.low, conf.high)

###########################################OFENSIVE CATEGORICAL MODELS###################################

#Function to include numeric jetlag as a value in the dummy variables#
create.ds.categorical <- function(df1){
  
  df2 <- rownames_to_column(df1, 'rn') %>%
    gather(key, val, matches("^Venue_"))%>%
    group_by(rn, val) %>% 
    mutate(n = case_when(key == "Venue_DirectionJetlag_Team" ~ Jet_Lag_Compensed, 
                         key == "Venue_DirectionJetlag_Against" ~ Jet_Lag_Compensed_against,
                         TRUE ~ as.factor(n()))) %>% 
    select(-Jet_Lag_Compensed, -Jet_Lag_Compensed_against, -key)%>% 
    spread(val, n, fill = 0) %>%  
    ungroup%>% 
    mutate_if(is.factor, funs(factor(replace(as.character(.), is.na(.), "0")))) %>%
    select(-rn, -AwaySame, -HomeSame)
  
  return(df2)
}

##Creating Datasets to analyze each stat##

#OPA#
df_bg_cat_lm_OPA <- select(df_bg_lm, c(OPA,Net_Elo,
                                   Venue_Team, Venue_Team_Against, 
                                   Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                   Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))

df_bg_cat_lm_OPA <- create.ds.categorical(df_bg_cat_lm_OPA)

#ERPA#
df_bg_cat_lm_ERPA <- select(df_bg_lm, c(ERPA,Net_Elo,
                                   Venue_Team, Venue_Team_Against, 
                                   Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                   Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))

df_bg_cat_lm_ERPA <- create.ds.categorical(df_bg_cat_lm_ERPA)

#OA#
df_bg_cat_lm_OA <- select(df_bg_lm, c(OA,Net_Elo,
                                    Venue_Team, Venue_Team_Against, 
                                    Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                    Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))

df_bg_cat_lm_OA <- create.ds.categorical(df_bg_cat_lm_OA)

#Winning#
df_bg_cat_lm_Winning <- select(df_bg_lm, c(Winning,Net_Elo,
                                  Venue_Team, Venue_Team_Against, 
                                  Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                  Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))


df_bg_cat_lm_Winning <- create.ds.categorical(df_bg_cat_lm_Winning)

#Runs_scored#
df_bg_cat_lm_Runs_scored <- select(df_bg_lm, c(Runs_scored,Net_Elo,
                                           Venue_Team, Venue_Team_Against, 
                                           Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                           Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))

df_bg_cat_lm_Runs_scored <- df_bg_cat_lm_Runs_scored[1:10000,]
df_bg_cat_lm_Runs_scored <- create.ds.categorical(df_bg_cat_lm_Runs_scored)

#Batting_Average_BA#
df_bg_cat_lm_Batting_Average_BA <- select(df_bg_lm, c(Batting_Average_BA,Net_Elo,
                                               Venue_Team, Venue_Team_Against, 
                                               Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                               Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))

df_bg_cat_lm_Batting_Average_BA <- create.ds.categorical(df_bg_cat_lm_Batting_Average_BA)

#On_Base_OBP#
df_bg_cat_lm_On_Base_OBP <- select(df_bg_lm, c(On_Base_OBP,Net_Elo,
                                                      Venue_Team, Venue_Team_Against, 
                                                      Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                                      Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))

df_bg_cat_lm_On_Base_OBP <- create.ds.categorical(df_bg_cat_lm_On_Base_OBP)

#Slugging_SLG#
df_bg_cat_lm_Slugging_SLG <- select(df_bg_lm, c(Slugging_SLG,Net_Elo,
                                               Venue_Team, Venue_Team_Against, 
                                               Venue_DirectionJetlag_Team, Jet_Lag_Compensed,
                                               Venue_DirectionJetlag_Against, Jet_Lag_Compensed_against))


df_bg_cat_lm_Slugging_SLG <- create.ds.categorical(df_bg_cat_lm_Slugging_SLG)

##Creating Linear Model for each stat##
bg_cat_OPA_lm <- lm(OPA~., data=df_bg_cat_lm_OPA)
bg_cat_ERPA_lm <- lm(ERPA~., data=df_bg_cat_lm_ERPA)
bg_cat_OA_lm <- lm(OA~., data=df_bg_cat_lm_OA)
bg_cat_Winning_lm <- lm(Winning~., data=df_bg_cat_lm_Winning)
bg_cat_Runs_Scored_lm <- lm(Runs_scored~., data=df_bg_cat_lm_Runs_scored)
bg_cat_Batting_Average_BA_lm <- lm(Batting_Average_BA~., data=df_bg_cat_lm_Batting_Average_BA)
bg_cat_OBP_lm <- lm(On_Base_OBP~., data=df_bg_cat_lm_On_Base_OBP)
bg_cat_SLG_lm <- lm(Slugging_SLG~., data=df_bg_cat_lm_Slugging_SLG)


##Creating confidence Intervals##
tidy_bg_cat_OPA_lm <- tidy(bg_cat_OPA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_cat_ERPA_lm <- tidy(bg_cat_ERPA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_cat_OA_lm <- tidy(bg_cat_OA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_cat_Winning_lm <- tidy(bg_cat_Winning_lm, conf.int = T, conf.level = 0.95)
tidy_bg_cat_Runs_Scored_lm <- tidy(bg_cat_Runs_Scored_lm, conf.int = T, conf.level = 0.95)
tidy_bg_cat_Batting_Average_BA_lm <- tidy(bg_cat_Batting_Average_BA_lm, conf.int = T, conf.level = 0.95)
tidy_bg_cat_OBP_lm <- tidy(bg_cat_OBP_lm, conf.int = T, conf.level = 0.95)
tidy_bg_cat_SLG_lm <- tidy(bg_cat_SLG_lm, conf.int = T, conf.level = 0.95)


##Getting Results##
bg_cat_OPA_sum <- summary(bg_cat_OPA_lm)
pt(-abs(coef(bg_cat_OPA_sum)[, 3]), bg_cat_OPA_lm$df,  lower = TRUE)
summary(bg_cat_ERPA_lm)
summary(bg_cat_OA_lm)
summary(bg_cat_Winning_lm)
summary(bg_cat_Runs_Scored_lm)
summary(bg_cat_Batting_Average_BA_lm)
summary(bg_cat_OBP_lm)
summary(bg_cat_SLG_lm)

################################################ANALYSIS OF CATEGORICAL MODEL#######################################
#Extracting Parameters
q_OPA_cat <- filter(tidy_bg_cat_OPA_lm, 
                    str_detect(term, "West") == TRUE | str_detect(term, "East") == TRUE | str_detect(term, "Elo") == TRUE) 

q_ERPA_cat <- filter(tidy_bg_cat_ERPA_lm, 
                     str_detect(term, "West") == TRUE | str_detect(term, "East") == TRUE | str_detect(term, "Elo") == TRUE)

q_OA_cat <- filter(tidy_bg_cat_OA_lm, 
                   str_detect(term, "West") == TRUE | str_detect(term, "East") == TRUE | str_detect(term, "Elo") == TRUE)

q_Runs_Scored_cat <- filter(tidy_bg_cat_Runs_Scored_lm, 
                            str_detect(term, "West") == TRUE | str_detect(term, "East") == TRUE | str_detect(term, "Elo") == TRUE)

q_Batting_Average_BA_cat <- filter(tidy_bg_cat_Batting_Average_BA_lm, 
                                   str_detect(term, "West") == TRUE | str_detect(term, "East") == TRUE | str_detect(term, "Elo") == TRUE)

q_Batting_OBP_cat <- filter(tidy_bg_cat_OBP_lm, 
                             str_detect(term, "West") == TRUE | str_detect(term, "East") == TRUE | str_detect(term, "Elo") == TRUE)

q_Batting_SLG_cat <- filter(tidy_bg_cat_SLG_lm, 
                              str_detect(term, "West") == TRUE | str_detect(term, "East") == TRUE | str_detect(term, "Elo") == TRUE)

#Analisis OPA Statistic#

#Correlation#
df_bg_cat_lm_OPA.pairs <- ggpairs(df_bg_cat_lm_OPA, columns = vars_small,
                           lower=list(continuous="smooth"),
                           diag=list(continuous="densityDiag"))
df_bg_cat_lm_OPA.pairs

#Normality of residuals#
fortify_cat_lm_OPA <- fortify(bg_cat_OPA_lm)
fortify_cat_lm_OPA$Jet_Lag_Compensed <- df_bg_lm$Jet_Lag_Compensed


ggplot(data = fortify_cat_lm_OPA, aes(x=.resid))+
  geom_histogram(colour = "black", fill = "lightskyblue", aes(y=..density..))+
  stat_function(fun = "dnorm",
                args = list(mean(fortify_cat_lm_OPA$.resid),
                            sd = sd(fortify_cat_lm_OPA$.resid)), size = 1)+
  theme_bw()+
  xlab("Error Residuals")+
  facet_wrap(~Jet_Lag_Compensed)+
  ylab("Distribution of Residuals")

ggplot(data=fortify_cat_lm_OPA, aes(x=.fitted, y=.resid)) +
  geom_point() + theme_bw() + xlab("Fitted values") +
  #facet_wrap(~Jet_Lag_Compensed)+
  ylab("Residuals") + geom_smooth()

ggplot(data=fortify_cat_lm_OPA, aes(x=.fitted, y=.resid)) +
  geom_point() + theme_bw() + xlab("Fitted values") +
  facet_wrap(~Jet_Lag_Compensed)+
  geom_encircle(color=NA, fill="lightskyblue", alpha=0.25, s_shape = 1 , expand=0) +
  ylab("Residuals")

ggplot(data=fortify_cat_lm_OPA, aes(sample=.stdresid)) +
  stat_qq(geom="point") + geom_abline() +
  xlab("Theoretical (Z ~ N(0,1))") +
  facet_wrap(~Jet_Lag_Compensed)+
  ylab("Sample") + coord_equal() + theme_bw()

ad_forti <- fortify_cat_lm_OPA%>%
  filter(Jet_Lag_Compensed == '-2')

ad.test(ad_forti$.stdresid, null = "pnorm", mean = 0, sd = 1)

#Intercepts to create the equation# (Why I have two values with NA?)
bg_cat_OPA_lm

#Goodness of fit = 0.0362 -> explains the 3.62%
glance(bg_cat_OPA_lm)

#Information about our fitted model: 
#9942 degrees of freedom as we started with 10016 observations and estimated 74 parameters. R tells us this in the summary output we have evidence to reject H0 for 
#9  parameters as their p values are less than 0.05. However just 4 are considered -> Intercept + Net_Elo + HomeEast1 + HomeEast2 
summary(bg_cat_OPA_lm)

#Here we specifed 95% confidence. So we've detected an effect of 
#Intercept 4.129520e-01(0.3631316510, 0.4627723351)
#Net_Elo 4.273890e-04(0.0003578602,0.0004969178)
#HomeEast1 1.540657e-02(0.0039646285,0.0268485133)
#HomeEast2 3.709290e-02(0.0089563574,0.0652294356)
#At a significance level of 0.05

tidy_bg_cat_OPA_lm <- tidy(bg_cat_OPA_lm, conf.int = T, conf.level = 0.95)
select(tidy_bg_cat_OPA_lm, term, estimate, conf.low, conf.high)
view(tidy_bg_cat_OPA_lm)
