from calc import *
from pandas import DataFrame
import datetime
#basketball is a subclass of DataFrame

'''
parameters  :
	sourcefilename  : the filename
	sourceDataFrame : ATTENTION, the input here is variable 
			when used to generate the overall stats of the team, the DataFrame from the actual play-by-play data
			is involved.
			However, when used to calculate nth_combi, the selected time scope is used
			Also, when used to generate player stats, the DataFrame input will only involve those rows that concern ths 
			player.
	teamname: the name of the team
	teamno  : the number of the team as indicated from the csv file
			  notice that eg: CLE*** the teamno=1
			  			      ***CLE the teamno=2

Attributes  :
	SN      :
	sourcefile:
	source  :
	selector: it automatically select the contectual DataFrame
	teamname: the name of the team
	teamno  : make reference to the input 
	opp_teamname/no : the info of the opposite
	FGM     : field goal made
	FGA     : field goal attempted
	FGP     : field goal %
	B3M     : 3Pointers made
	B3A     : 3Pointers attempted
	B3P     : 3Pointers  %
	FTM     : Free Throw made
	FTA     : Free Throw attempted 
	FTP     : Free Throw 
	p	    : Points scored 
'''
class BasketballGame(DataFrame):
	def __init__(self,sourcefilename,sourceDataFrame,teamname,teamno):

		DataFrame.__init__(self,sourceDataFrame)
		self.SN = sourcefilename[0:15]
		self.data = sourceDataFrame
		self.teamname = teamname
		self.teamno   = teamno
		self.home     = 0 if self.teamno == 1 else 1
		self.oppteamname = sourcefilename[9:12] if self.teamno==2 else sourcefilename[12:15]
		self.oppteamno = 2 if self.teamno==1 else 1

		selector = sourceDataFrame[sourceDataFrame['team']==teamname]
		self.FGM = calculate_FGM(selector)
		self.FGA = calculate_FGA(selector)
		self.FGP = float(self.FGM) / self.FGA if self.FGA!=0 else 0
		self.B3M  = calculate_3M(selector)
		self.B3A  = calculate_3A(selector)
		self.B3P  = float(self.B3M) / self.B3A if self.B3A!=0 else 0
		self.FTM = calculate_FTM(selector)
		self.FTA = calculate_FTA(selector)
		self.FTP = float(self.FTM) / self.FTA if self.FTA!=0 else 0
		self.P = int(score_calculate(selector))
		self.ORB = calculate_ORB(selector)
		self.DRB = calculate_DRB(selector)
		self.TRB = self.ORB+self.DRB
		self.TOV = calculate_TOV(selector)
		self.TOVP  = self.TOV/(self.FGA+self.FTA*0.44+self.TOV) if (self.FGA+self.FTA*0.44+self.TOV)!=0 else 0
		self.AST = calculate_AST(selector)
		self.F    = calculate_F(selector)

		'''-------------the code here will be used to produce rows that will aid the calculation of time interval-------------
		'''
		self._set_dummies()

		combination_starter =self._combinaiton_reference()
		self.totalcombi=combination_starter.etype.count()

		'''-------------this calculates for every row what the combination number is------------------ '''
		counter =0
		combinations = combination_starter.index
		for identifier in combinations:
			counter +=1
			self.data.ix[identifier:,'combination_number']=counter
		
		'''this is to calculate the time remaining of each row, notice that overtime is considered here'''
		
		self['time remaining']=0
		end_period = self.data.tail(1).period.item()
		self.data.ix[(self.data.period<=4),'time remaining']= (end_period-4)*5*60
		if end_period>4:
			self.data.ix[(self.data.period>4),'time remaining']=(end_period -self.data.period)*5*60
		self.data.ix[self.data.period<=4,'time remaining']+=(4-self.data.period)*12*60
		self.data.ix[:,'time']=pd.to_datetime(self.data.time, format='%M:%S')
		self.data.ix[:,'time remaining'] = self.data.ix[:,'time remaining']+pd.DatetimeIndex(self.data.time).minute*60+pd.DatetimeIndex(self.data.time).second

		self.MP = self.data.head(1).ix[:,'time remaining'].item()/60

		oppselector = sourceDataFrame[sourceDataFrame['team']==self.oppteamname]
		self.ORBP = float(self.ORB)/(self.ORB+calculate_DRB(oppselector))
		self.DRBP = float(self.DRB)/(self.DRB+calculate_ORB(oppselector))
		self.TRBP = float(self.TRB)/(self.TRB+calculate_DRB(oppselector)+calculate_ORB(oppselector))
		self.PTD  = int(self.P - score_calculate(oppselector))
		self.STL  = calculate_STL(oppselector)
		self.BLK  = calculate_BLK(oppselector)
		self.interval = self.data.head(1).ix[:,'time remaining'].item()
		nameindex = detect_team(self.teamno)
		self.players = pd.Series(self.data[nameindex].values.ravel()).unique()

	def give_nth_combination(self,no):
		df = self.data.ix[self.data['combination_number']==no]
		return df
	def _combinaiton_reference(self):
		df = self.data[(self.data['team']==self.teamname)|(self.data['team']=='OFF')]
		nameindex = detect_team(self.teamno)
		msk1 = (df.ix[:,nameindex]==df.ix[:,nameindex].shift(1)).all(axis=1)
		msk2 = (df['etype'].shift(-1) != 'sub')
		return df.ix[((~msk1) & msk2)]
	def _set_dummies(self):
		tp = self.data.tail(1).period.item() 
		for period in range(1,tp+1):
			msk = self.data.period==period

			df=  self.data.ix[msk]
			h = df.head(1).index.item()
			dummy = df.xs(h)
			dummy.team = self.teamname
			dummy.time = '12:00' if period<=4 else '5:00'
			dummy.etype= 'dummy'
			self.data = pd.concat([self.data[:h],
				pd.DataFrame(dummy).T,
				self.data[h:]],axis=0).reset_index(drop=True)

			df= self.data[self.data.period==period]
			t = df.tail(1).index.item()
			dummy = df.xs(t)
			dummy.team = self.teamname
			dummy.time = '00:00'
			dummy.etype= 'dummy'
			self.data = pd.concat([self.data.ix[:t,:],
				pd.DataFrame(dummy).T,
				self.data.ix[t+1:,:]],axis=0).reset_index(drop=True)	
	
	def give_lineup_agg(self,lineup_no):
		df = BasketballLineup(give_nth_combination(lineup_no),self.teamname,self.oppteamname,self.teamno)
		df.interval = df.data.head(1).ix['time remaining'].item()
		
		return df

class BasketballLineup():
	def __init__(self,lineup_df,teamname,oppteamname,teamno):
		# DataFrame.__init__(BasketballGamePart)
		# teamname = Basketball.teamname
		# oppteamname = Basketball.oppteamname
		# part = Basketball.give_nth_combination(nth_combination)
		part = lineup_df
		selector = part[part['team']==teamname]
		self.lineup_names = get_player_list(lineup_df,teamno)
		self.FGM = calculate_FGM(selector)
		self.FGA = calculate_FGA(selector)
		self.FGP = float(self.FGM) / self.FGA if self.FGA!=0 else 0
		self.B3M  = calculate_3M(selector)
		self.B3A  = calculate_3A(selector)
		self.B3P  = float(self.B3M) / self.B3A if self.B3A!=0 else 0
		self.FTM = calculate_FTM(selector)
		self.FTA = calculate_FTA(selector)
		self.FTP = float(self.FTM) / self.FTA if self.FTA!=0 else 0
		self.ORB = calculate_ORB(selector)
		self.DRB = calculate_DRB(selector)
		self.TRB   = self.ORB+self.DRB
		self.TOV   = calculate_TOV(selector)
		self.TOVP  = self.TOV/(self.FGA+self.FTA*0.44+self.TOV) if (self.FGA+self.FTA*0.44+self.TOV)!=0 else 0
		self.AST   = calculate_AST(selector)
		self.F     = calculate_F(selector)
		self.P     = int(score_calculate(selector))
		# self.MP = self.head(1).ix[:,'time remaining'].item()/60

		oppselector = part[part['team']==oppteamname]
		self.ORBP = float(self.ORB)/(self.ORB+calculate_DRB(oppselector)) if (self.ORB+calculate_DRB(oppselector)) !=0 else 0
		self.DRBP = float(self.DRB)/(self.DRB+calculate_ORB(oppselector)) if (self.DRB+calculate_ORB(oppselector)) !=0 else 0
		self.TRBP = float(self.TRB)/(self.TRB+calculate_DRB(oppselector)+calculate_ORB(oppselector)) if (self.TRB+calculate_DRB(oppselector)+calculate_ORB(oppselector))!=0 else 0
		self.PTD  = int(self.P - score_calculate(oppselector))
		self.STL  = calculate_STL(oppselector)
		self.BLK  = calculate_BLK(oppselector)
		# self.interval = calculate_interval(Basketball, nth_combination)
