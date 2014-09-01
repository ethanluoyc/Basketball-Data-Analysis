import pandas as pd
pd.options.mode.chained_assignment = None # set warning to NOne

# def separating_opp_team(df,teamname,teamno=1):
# 	#this block loads the csv data from the raw play by play data file
# 	#TO TAKE NOTE
# 	if teamno==1:
# 		df_team1 = df[df['team'] == teamname]                 #team1='CLE',away team, thus drop home
# 		df_team1 = df_team1.drop(['h1','h2','h3','h4','h5'],1)
# 		df_team1 = df_team1.rename(columns=
# 								{'a1':'p1',
# 								 'a2':'p2',
# 								 'a3':'p3',
# 								 'a4':'p4',
# 								 'a5':'p5'
# 								}) # this match happens at BOS so BOS = hOME
# 		return df_team1

# 	elif teamno==2:
# 		df_team2 = df[df['team'] == teamname]
# 		# global tm2
# 		# tm2 = df_team2
# 		df_team2 = df_team2.drop(['a1','a2','a3','a4','a5'],1)
# 		df_team2 = df_team2.rename(columns=
# 								{'h1':'p1',
# 								 'h2':'p2',
# 								 'h3':'p3',
# 								 'h4':'p4',
# 								 'h5':'p5'
# 								})
# 		return df_team2

#this function is to help tp slice the players into the combinations
# def combi_mark(df):
# 	#df = pd.read_csv(teamcsvfile)
# 	#df['markers'] = Fase
# 		# if end_of_p[] !=  :
# 		# 	df = df[df['period']==period+1].head(1).markers = True
	
# 	df_to_mark = df[df["etype"]=='sub']
# 	df_to_mark['markers'] = True
# 	refno = list(df_to_mark.index)
# 	for i in range(len(refno)-2):
# 		mid = i+1
# 		last = mid+1
# 		if (((refno[i]+1 == refno[mid]) and (refno[mid]+1 == refno[last]))&
# 			(mid < len(refno)-1)): 
# 			df_to_mark[(df_to_mark.index==refno[mid])]=False
	

# 	#print df_to_mark['markers']
# 	df_to_mark = df_to_mark[df_to_mark['markers']==True]#set the markers to point at those that has True for markers, exclude inbetween data
# 	refno = list(df_to_mark.index) #refresh refino since we have deleted the False markers

		
# 	for period in range(1,5):
# 		e = df[df['period']==period].tail(1)
# 		s = df[df['period']==period +1].head(1)
# 		mask = (
# 			   (s['p1'].str==e['p1'].str) &
# 			   (s['p2'].str==e['p2'].str) &
# 			   (s['p3'].str==e['p3'].str) &
# 			   (s['p4'].str==e['p4'].str) &
# 			   (s['p5'].str==e['p5'].str)
# 			   )
# 		if mask:pass 
# 		else:
# 			refno=refno + list(s.index)
# 			refno.sort()
	#to list all the combination of players
	#the codes below are all for diaplay of results
'''
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
			combi_init = row
	
'''
	# df.ix[refno,'markers']=True
	# df_out = df
	# return df_out





#return the name of the team in the name strinng
def team1_name(fpstring):
	team1 = fpstring[9:12]
	return team1
#return the name of the team in the name string
def team2_name(fpstring):
	team2 = fpstring[12:15]
	return team2

def select_opp_team(team,opp_team_all):
	head = int(team.head(1).index)
	tail = int(team.tail(1).index)
	return opp_team_all.ix[head:tail]



