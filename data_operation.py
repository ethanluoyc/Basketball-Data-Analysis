import pandas as pd



def separating_opp_team(fpstring='20081028.CLEBOS.csv'):
	complete_fpstring = 'data_test/' + fpstring
	time_of_game = fpstring[0:8]
	team1 = fpstring[9:12]
	team2 = fpstring[12:15]
	#this block loads the csv data from the raw play by play data file
	df = pd.read_csv(complete_fpstring)

	df_team1 = df[df['team'] == team1]
	df_team1 = df_team1.drop(['a1','a2','a3','a4','a5'],1) # is this a or h? figur out
	team1_output_path = 'data_test_output/'+time_of_game+str(team1)+'.csv'

	f1 = open(team1_output_path,'w')
	df_team1.to_csv(team1_output_path)
	f1.close
	

	df_team2 = df[df['team'] == team2]
	df_team2 = df_team2.drop(['h1','h2','h3','h4','h5'],1)
	team2_output_path = 'data_test_output/'+time_of_game+str(team2)+'.csv'
	f2 = open(team2_output_path,'w')
	df_team2.to_csv(team2_output_path)
	f2.close

def score_calculate(teamcsvfile):
	df = pd.read_csv(teamcsvfile)
	df_pt_scored = df[((df['etype']=='shot') & (df['result']=='made'))]
	df_ft_scored = df[((df['etype']=='free throw') & (df['result']=='made'))]
	return df_pt_scored['points'].sum()+len(df_ft_scored.index)
	#print df_pt_scored['points'].sum()+len(df_ft_scored.index)



separating_opp_team()
print int(score_calculate('data_test_output/20081028BOS.csv'))
print int(score_calculate('data_test_output/20081028CLE.csv'))
	#this block of code separates the first team 
