import pandas as pd
from datetime import datetime
from data_operation import *
import numpy as np
def score_calculate(df):
	df_pt_scored = df[((df['etype']=='shot') & (df['result']=='made'))]
	return df_pt_scored['points'].sum()+len(df[(df['etype']=='free throw') & (df['result']=='made')])
def calculate_FGM(df):
	cond_pt = (df['etype']=='shot') & (df['result']=='made')
	return len(df[cond_pt].index)
def calculate_FGA(df):
	shot_cond= df['etype']=='shot'
	return len(df[shot_cond].index)
def calculate_3M(df):
	cond_3M= (df['etype']=='shot')&(df['type']=='3pt')&(df['result']=='made')
	return len(df[cond_3M].index)
def calculate_3A(df):
	cond_3A = (df['etype']=='shot')&(df['type']=='3pt')
	return len(df[cond_3A].index)
def calculate_FTM(df):
	cond_FTM =(df['etype']=='free throw') & (df['result']=='made')
	return len(df[cond_FTM].index)
def calculate_FTA(df):
	cond_FTA =(df['etype']=='free throw')
	return len(df[cond_FTA].index)
def calculate_playtime(team,teamno,playername):
	nameindex = detect_team(teamno)
	mask = team[nameindex].isin([playername]).any(axis=1)
	team[['a1c','a2c','a3c','a4c','a5c']]=team[nameindex].shift(1)
	mask2 = team[['a1c','a2c','a3c','a4c','a5c']].isin([playername]).any(axis=1)
	co = team[~mask & mask2]['time remaining'].index #time the player is changed out
	ci = team[mask & ~mask2]['time remaining'].index #time the player is changed in
	time_in =0
	for i,o in zip(ci,co):
		time_in = time_in + (team.ix[i,'time remaining']-team.ix[o,'time remaining'])
	if len(ci)>len(co):
		time_in = time_in + int(team.ix[ci].tail(1)['time remaining'])
	return time_in
def calculate_ORB(df):
	cond = (df['etype']=='rebound')&(df['type']=='off')
	return len(df[cond].index)
def calculate_DRB(df):
	cond = 	(df['etype']=='rebound')&(df['type']=='def')
	return len(df[cond].index)
def calculate_TOV(df):
	cond = 	(df['etype']=='turnover')
	return len(df[cond].index)
def calculate_AST(df):
	cond = df['assist'].notnull()
	return len(df[cond].index)
def calculate_STL(df):
	cond = df['steal'].notnull()
	return len(df[cond].index)
def calculate_BLK(df):
	cond = df['block'].notnull()
	return len(df[cond].index)
def calculate_F(df)  :
	# cond1 = (df['reason']=='foul') & (df['etype']=='free throw') & (df['outof']==2)
	# cond2 = (df['reason']=='foul') & (df['etype']=='free throw') & (df['outof']==1)
	# cond3 = (df['reason']=='foul') & (df['etype']!='free throw')
	# print df[cond1|cond2|cond3][['team','player','etype','outof','reason']]
	# return len(df[cond1].index)/2+len(df[cond2].index)+len(df[cond3].index)
	cond = (df['etype']=='foul')&(df['type']!='double technical')&(df['type']!='defense 3 second')
	# cond2 = (df['etype']=='foul')&(
	# 	(df['type']!='offensive') | (df['type']!='shooting') | (df['type']!='looseball') | (df['type']!='personal')
	# )
	return len(df[cond].index)
def detect_team(teamno):
	if (teamno==1):
		nameindex = ['a1','a2','a3','a4','a5']
	else: 
		nameindex = ['h1','h2','h3','h4','h5']

	return nameindex
def nth_combination(BasketballTeam,nth_num):
	nameindex = detect_team(BasketballTeam.teamno)
	comparison=BasketballTeam.shift(1)
	msk = (BasketballTeam[nameindex]==comparison[nameindex]).all(axis=1)
	no_of_combi = len(list(BasketballTeam[~msk].index))
	start = BasketballTeam[~msk].iloc[nth_num-1]
	end = BasketballTeam[~msk].iloc[nth_num] if nth_num != no_of_combi else BasketballTeam.tail(1).index
	return BasketballTeam.ix[start.name:end.name,:]	
def get_player_list(nth_combidata,teamno):
	'''This gives the namelist of the nth team'''
	data = nth_combidata
	nameindex = detect_team(teamno)
	players  = data.ix[data.head(1).index,nameindex].values
	return players[0].tolist()

def opposing_team(BasketballTeam,nth_num):
	data = nth_combination(BasketballTeam,nth_num)
	start = data.head(1).index.item()
	end = data.tail(1).index.item()
	msk = (BasketballTeam['team'] == BasketballTeam.oppteamname)
	# print BasketballTeam[msk]
	return score_calculate(BasketballTeam[msk].ix[start:end])

def gettime(s):
	the_time = s['time'].item()
	present_time = datetime.strptime(the_time,"%M:%S")
	return present_time

def calculate_interval(teamdata,nth_combi):
	'''calculate the interval for the nth team played in a game'''
	combi_data=teamdata.give_nth_combination(nth_combi)
	if nth_combi != teamdata.totalcombi:
				next_interval = teamdata.give_nth_combination(nth_combi+1)
				e = next_interval.head(1)
	else: e = combi_data.tail(1)
	s = combi_data.head(1)
	interval = s['time remaining'].item()-e['time remaining'].item()
	return interval	