from stats_calculator import *
from pandas import DataFrame
# basketball is a subclass of DataFrame

def add_aid_rows(df, team_names):
    [_set_dummies(df, team) for team in team_names]
    namecolumns = ['a1', 'a2', 'a3', 'a4', 'a5', 'h1', 'h2', 'h3', 'h4', 'h5']

    # this add all the aid rows

    df['timeleft'] = 0
    end_period = df.tail(1).period.item()

    df.ix[:, 'time'] = pd.to_datetime(df.time, format='%M:%S')
    df.ix[(df.period <= 4), 'timeleft'] = (end_period - 4) * 5 * 60

    if end_period > 4:
        df.ix[(df.period > 4), 'timeleft'] = (end_period - df.period) * 5 * 60
        df.ix[(df.period <= 4), 'timeleft'] += (end_period - 4) * 5 * 60
    df.ix[df.period <= 4, 'timeleft'] += (4 - df.period) * 12 * 60
    df.ix[:, 'timeleft'] = df.ix[:, 'timeleft'] + pd.DatetimeIndex(df.time).minute * 60 + pd.DatetimeIndex(
        df.time).second  # add current time to overtime

    namecolumns = ['a1', 'a2', 'a3', 'a4', 'a5', 'h1', 'h2', 'h3', 'h4', 'h5'] if len(team_names) == 2 else ['a1', 'a2', 'a3', 'a4', 'a5']
    # this part handles gives a lineup number for each row.

    msk = (df.ix[:, namecolumns] != df.ix[:, namecolumns].shift(1)).any(axis=1)  # the two adjacent rows differ in name
    msk2 = (df['etype'].shift(-1) != 'sub')  # for multiple substitution, only consider the last sub
    counter = 0
    for index in df[(msk & msk2)].index:
        counter += 1
        df.ix[index:, 'lineup_no'] = counter





class BasketballGame(DataFrame):
    def __init__(self, sourcefilename, sourceDataFrame, teamname, teamno):

        DataFrame.__init__(self, sourceDataFrame)
        self.SN = sourcefilename[0:15]
        self.data = sourceDataFrame
        self.teamname = teamname
        self.teamno = teamno
        self.home = 0 if self.teamno == 1 else 1
        self.oppteamname = sourcefilename[9:12] if self.teamno == 2 else sourcefilename[12:15]
        self.oppteamno = 2 if self.teamno == 1 else 1

        selector = sourceDataFrame[sourceDataFrame['team'] == teamname]
        self.FGM = calculate_FGM(selector)
        self.FGA = calculate_FGA(selector)
        self.FGP = float(self.FGM) / self.FGA if self.FGA != 0 else 0
        self.B3M = calculate_3M(selector)
        self.B3A = calculate_3A(selector)
        self.B3P = float(self.B3M) / self.B3A if self.B3A != 0 else 0
        self.FTM = calculate_FTM(selector)
        self.FTA = calculate_FTA(selector)
        self.FTP = float(self.FTM) / self.FTA if self.FTA != 0 else 0
        self.P = int(score_calculate(selector))
        self.ORB = calculate_ORB(selector)
        self.DRB = calculate_DRB(selector)
        self.TRB = self.ORB + self.DRB
        self.TOV = calculate_TOV(selector)
        self.TOVP = self.TOV / (self.FGA + self.FTA * 0.44 + self.TOV) if (
             self.FGA + self.FTA * 0.44 + self.TOV) != 0 else 0
        self.AST = calculate_AST(selector)
        self.F = calculate_F(selector)

        '''-------------the code here will be used to produce rows that will aid the calculation of time interval-------------'''
        _set_dummies(self, self.teamname)

        combination_starter = self._combinaiton_reference()
        self.totalcombi = combination_starter.etype.count()

        '''-------------this calculates for every row what the combination number is------------------ '''
        counter = 0
        combinations = combination_starter.index
        for identifier in combinations:
            counter += 1
            self.data.ix[identifier:, 'combination_number'] = counter

        '''this is to calculate the time remaining of each row, notice that overtime is considered here'''

        self['time remaining'] = 0
        end_period = self.data.tail(1).period.item()
        self.data.ix[(self.data.period <= 4), 'time remaining'] = (end_period - 4) * 5 * 60
        if end_period > 4:
            self.data.ix[(self.data.period > 4), 'time remaining'] = (end_period - self.data.period) * 5 * 60
        self.data.ix[self.data.period <= 4, 'time remaining'] += (4 - self.data.period) * 12 * 60
        self.data.ix[:, 'time'] = pd.to_datetime(self.data.time, format='%M:%S')
        self.data.ix[:, 'time remaining'] = self.data.ix[:, 'time remaining'] + pd.DatetimeIndex(
            self.data.time).minute * 60 + pd.DatetimeIndex(self.data.time).second

        self.MP = self.data.head(1).ix[:, 'time remaining'].item() / 60

        oppselector = sourceDataFrame[sourceDataFrame['team'] == self.oppteamname]
        self.ORBP = float(self.ORB) / (self.ORB + calculate_DRB(oppselector))
        self.DRBP = float(self.DRB) / (self.DRB + calculate_ORB(oppselector))
        self.TRBP = float(self.TRB) / (self.TRB + calculate_DRB(oppselector) + calculate_ORB(oppselector))
        self.PTD = int(self.P - score_calculate(oppselector))
        self.STL = calculate_STL(oppselector)
        self.BLK = calculate_BLK(oppselector)
        self.interval = self.data.head(1).ix[:, 'time remaining'].item()
        nameindex = detect_team(self.teamno)
        self.players = pd.Series(self.data[nameindex].values.ravel()).unique()

    def give_nth_combination(self, no):
        df = self.data.ix[self.data['combination_number'] == no]
        return df

    def _combinaiton_reference(self):
        df = self.data[(self.data['team'] == self.teamname) | (self.data['team'] == 'OFF')]
        nameindex = detect_team(self.teamno)
        msk1 = (df.ix[:, nameindex] == df.ix[:, nameindex].shift(1)).all(axis=1)
        msk2 = (df['etype'].shift(-1) != 'sub')
        return df.ix[((~msk1) & msk2)]


def _set_dummies(df,team_name):
    total_period = df.tail(1).period.item() + 1
    for period in range(1, total_period):
        msk = df.period == period
        df_one_period = df.ix[msk]
        h = df_one_period.head(1).index.item()
        dummy = df_one_period.xs(h)
        dummy.team = team_name
        dummy.time = '12:00' if period <= 4 else '5:00'
        dummy.etype = 'dummy'
        df = pd.concat([df[:h],
                        pd.DataFrame(dummy).T,
                        df[h:]], axis=0).reset_index(drop=True)

        df_one_period = df[df.period == period]
        t = df_one_period.tail(1).index.item()
        dummy = df_one_period.xs(t)
        dummy.team = team_name
        dummy.time = '00:00'
        dummy.etype = 'dummy'
        df = pd.concat([df.ix[:t, :],
                        pd.DataFrame(dummy).T,
                        df.ix[t + 1:, :]], axis=0).reset_index(drop=True)


class LineupStats():
    def __init__(self, lineup_df, game_info):
        team_name = game_info["team_name"]
        oppteam_name = game_info["oppteam_name"]
        team_msk = lineup_df["team"]==team_name
        oppteam_msk = lineup_df["team"]==oppteam_name
        player_index = detect_team(game_info["team_no"])

        self.PLAYERS = lineup_df.head(1)[player_index].values.tolist()[0]
        self.OPPONENTS = lineup_df.head(1)[detect_team(game_info["oppteam_no"])].values.tolist()[0]

        self.FGM = calculate_FGM(lineup_df[team_msk])
        self.FGA = calculate_FGA(lineup_df[team_msk])
        self.FGP = float(self.FGM) / self.FGA if self.FGA != 0 else 0
        self.FG3M = calculate_3M(lineup_df[team_msk])
        self.FG3A = calculate_3A(lineup_df[team_msk])
        self.FG3P = float(self.FG3M) / self.FG3A if self.FG3A != 0 else 0
        self.FTM = calculate_FTM(lineup_df[team_msk])
        self.FTA = calculate_FTA(lineup_df[team_msk])
        self.FTP = float(self.FTM) / self.FTA if self.FTA != 0 else 0
        self.OREB = calculate_ORB(lineup_df[team_msk])
        self.DREB = calculate_DRB(lineup_df[team_msk])
        self.REB = self.OREB + self.DREB
        self.TOV = calculate_TOV(lineup_df[team_msk])
        self.TOVP = self.TOV / (self.FGA + self.FTA * 0.44 + self.TOV) if (self.FGA + self.FTA * 0.44 + self.TOV) != 0 else 0
        self.AST = calculate_AST(lineup_df[team_msk])
        self.PF = calculate_F(lineup_df[team_msk])
        self.PTS = int(score_calculate(lineup_df[team_msk]))
        self.PTD = int(self.PTS - score_calculate(lineup_df[oppteam_msk]))
        self.STL = calculate_STL(lineup_df[oppteam_msk])
        self.BLK = calculate_BLK(lineup_df[oppteam_msk])
        self.INTERVAL = lineup_df.head(1).timeleft.item() - lineup_df.tail(1).timeleft.item()

    def generate_row(self, col):
        """parameter : col (list) : the attributes that wants to be extracted
           return    : a Series that contain all desired attributes
        """
        row = []
        [row.append(getattr(self, attribute)) for attribute in col]
        return pd.Series(row, index=col)
