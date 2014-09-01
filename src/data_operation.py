import pandas as pd
pd.options.mode.chained_assignment = None # set warning to NOne

def separating_opp_team(fpstring):
	complete_fpstring = 'data_test/' + fpstring
	time_of_game = fpstring[0:8]
	team1 = fpstring[9:12]
	team2 = fpstring[12:15]
	#this block loads the csv data from the raw play by play data file
	df = pd.read_csv(complete_fpstring)
	#TO TAKE NOTE
	df_team1 = df[df['team'] == team1] 
	df_team1.iloc[0:0]='Ref'         
	# global tm1
	# tm1 = df_team1         #team1='CLE',away team, thus drop home
	df_team1 = df_team1.drop(['h1','h2','h3','h4','h5'],1) # this match happens at BOS so BOS = hOME
	team1_output_path = 'data_test_output/'+time_of_game+str(team1)+'.csv'

	f1 = open(team1_output_path,'w')
	df_team1.to_csv(team1_output_path,index=False)
	f1.close
	

	df_team2 = df[df['team'] == team2]
	# global tm2
	# tm2 = df_team2
	df_team2 = df_team2.drop(['a1','a2','a3','a4','a5'],1)
	team2_output_path = 'data_test_output/'+time_of_game+str(team2)+'.csv'
	f2 = open(team2_output_path,'w')
	df_team2.to_csv(team2_output_path,index=False)
	f2.close
	#end of a code block :)
	#sreturn [df_team1,df_team2]

def score_calculate(df):
	#df = pd.read_csv(teamcsvfile)
	df_pt_scored = df[((df['etype']=='shot') & (df['result']=='made'))]
	df_ft_scored = df[((df['etype']=='free throw') & (df['result']=='made'))]
	return df_pt_scored['points'].sum()+len(df_ft_scored.index)
	#print df_pt_scored['points'].sum()+len(df_ft_scored.index)

#this function is to help tp slice the players into the combinations
def combi_mark(df):
	#df = pd.read_csv(teamcsvfile)
	#df['markers'] = False
	df_to_mark = df[df["etype"]=='sub']
	df_to_mark['markers'] = True
	refno = list(df_to_mark.index)
	for i in range(len(refno)-2):
		mid = i+1
		last = mid+1
		if (((refno[i]+1 == refno[mid]) and (refno[mid]+1 == refno[last]))&
			(mid < len(refno)-1)): 
			df_to_mark[(df_to_mark.index==refno[mid])]=False
	
	#print df_to_mark['markers']
	df_to_mark = df_to_mark[df_to_mark['markers']==True]#set the markers to point at those that has True for markers, exclude inbetween data
	refno = list(df_to_mark.index) #refresh refino since we have deleted the False markers

	#to list all the combination of players
	combi_init = int(df_to_mark.head(1).index) #set the starter of the iteration
	for row in refno:
		if (row-1-combi_init > 2): #the twos are not marked as False even though there are not displayed in this output. stiil can use marker==true to do relevant search
			print ('players from',str(combi_init),'to',str(row-1))
		if row == int(refno[-1]):
			print ('players from',row,'to',str(int(df.tail(1).index)))
		combi_init = row 
	#end of this block

	combi_init = int(df_to_mark.head(1).index) #set the starter of the iteration
	for row in refno:
		if (row-1-combi_init > 2)&(row!=combi_init): #the twos are not marked as False even though there are not displayed in this output. stiil can use marker==true to do relevant search
			#print ('players from',combi_init,'to',row-1)
			#print row #add more code such that it returns the namelist :)
			combi_init = row
	df.ix[refno,'markers']=True
	return df

#return the name of the team in the name strinng
def team1_name(fpstring):
	team1 = fpstring[9:12]
	return team1
#return the name of the team in the name string
def team2_name(fpstring):
	team2 = fpstring[12:15]
	return team2

#main programme
name= '20081028.CLEBOS.csv'
filepath='data_test/'+name
df=pd.read_csv(filepath)
# tm1=pd.DataFrame()
# tm2=pd.DataFrame()
separating_opp_team(name)

time_of_game = name[0:8]
tm1name = team1_name(name)
tm2name = team2_name(name)


tm1=pd.read_csv('data_test_output/'+time_of_game+tm1name+'.csv')
tm2=pd.read_csv('data_test_output/'+time_of_game+tm2name+'.csv')

print int(score_calculate(tm1))
print int(score_calculate(tm2))
marked=combi_mark(tm1)
marked.to_csv('data_test_output/try_output.csv',index=True)
#this block of code separates the first team 
