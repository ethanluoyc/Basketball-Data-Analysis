import glob
import re
import os
import json

from stats_calculator import *
from Basketball import BasketballGame, add_aid_rows
from StatsNba import get_lineup_data


ALLTEAMS = ['CLE', 'NYK', 'PHI', 'ATL', 'MIN', 'DEN', 'OKC',
            'MIA', 'MEM', 'CHI', 'LAL', 'POR',
            'DET', 'BOS']
DATAPATH = "../../data/%s/%s/%s"
PLAY_BY_PLAY_DIRECTORY = '../../data/play_by_play/2008-2009.regular_season/'  # PATH of the play_by_play data
OUTPUT_PATH = '../../data/output/%s'
STATS_NBA_PATH = '../../data/stats_nba/%s'
REFPATH = '../../data/stats_nba/2008-09_team_lineup/%s.csv'  # PATH where stats.nba.com data is located
ALL_GAME_FILES = [os.path.basename(x) for x in glob.glob(PLAY_BY_PLAY_DIRECTORY + '*.csv')]
ATTRIBUTES = ["interval",
              "FGM", 'FGA', 'FGP',
              'B3M', 'B3A', 'B3P',
              'FTM', 'FTA', 'FTP',
              'OREB', 'DREB', "TRB",
              'TOV', 'STL', 'BLK', 'F',
              'PTD', 'P']
ALLTEAMS   = ['CLE', 'NJN', 'NYK', 'MIL', 'PHI', 'ATL', 'MIN', 'DEN', 'OKC',
            'MIA', 'WAS', 'MEM', 'CHI', 'LAL', 'POR', 'GSW', 'UTA', 'ORL',
            'DET', 'IND', 'TOR', 'HOU', 'SAS', 'BOS', 'LAC', 'PHX', 'SAC']

teamids = [["00", 1610612766, "2004", "2014", "CHA"], ["00", 1610612765, "1948", "2014", "DET"],
           ["00", 1610612764, "1961", "2014", "WAS"], ["00", 1610612763, "1995", "2014", "MEM"],
           ["00", 1610612762, "1974", "2014", "UTA"], ["00", 1610612761, "1995", "2014", "TOR"],
           ["00", 1610612760, "1967", "2014", "OKC"], ["00", 1610612759, "1976", "2014", "SAS"],
           ["00", 1610612758, "1948", "2014", "SAC"], ["00", 1610612757, "1970", "2014", "POR"],
           ["00", 1610612756, "1968", "2014", "PHX"], ["00", 1610612755, "1949", "2014", "PHI"],
           ["00", 1610612754, "1976", "2014", "IND"], ["00", 1610612753, "1989", "2014", "ORL"],
           ["00", 1610612752, "1946", "2014", "NYK"], ["00", 1610612751, "1976", "2014", "BKN"],
           ["00", 1610612750, "1989", "2014", "MIN"], ["00", 1610612749, "1968", "2014", "MIL"],
           ["00", 1610612748, "1988", "2014", "MIA"], ["00", 1610612747, "1948", "2014", "LAL"],
           ["00", 1610612746, "1970", "2014", "LAC"], ["00", 1610612745, "1967", "2014", "HOU"],
           ["00", 1610612744, "1946", "2014", "GSW"], ["00", 1610612743, "1976", "2014", "DEN"],
           ["00", 1610612742, "1980", "2014", "DAL"], ["00", 1610612741, "1966", "2014", "CHI"],
           ["00", 1610612740, "1988", "2014", "NOP"], ["00", 1610612739, "1970", "2014", "CLE"],
           ["00", 1610612738, "1946", "2014", "BOS"], ["00", 1610612737, "1949", "2014", "ATL"],
           ["00", 1610610027, "1949", "1949", "null"], ["00", 1610610024, "1947", "1954", "null"],
           ["00", 1610610036, "1946", "1950", "null"], ["00", 1610610030, "1949", "1952", "null"],
           ["00", 1610610034, "1946", "1949", "null"], ["00", 1610610025, "1946", "1949", "null"],
           ["00", 1610610029, "1948", "1948", "null"], ["00", 1610610032, "1946", "1948", "null"],
           ["00", 1610610035, "1946", "1946", "null"], ["00", 1610610031, "1946", "1946", "null"],
           ["00", 1610610028, "1946", "1946", "null"], ["00", 1610610026, "1946", "1946", "null"],
           ["00", 1610610037, "1949", "1949", "null"], ["00", 1610610023, "1949", "1949", "null"],
           ["00", 1610610033, "1949", "1949", "null"]]


def _generate_row(df, col):
    """'used to generate a list from the attributes"""
    row = []
    for attribute in col:
        row.append(getattr(df, attribute))
    return row


def generate_game_data(filename, teamno, folderpath=PLAY_BY_PLAY_DIRECTORY):
    '''This funciton generates game data from lineup retrieved from stats.nba.com'''
    df = pd.read_csv(folderpath + filename)
    # add_aid_rows(df,)
    teamname = filename[9:12] if teamno == 1 else filename[12:15]
    team = BasketballGame(filename, df, teamname, teamno)

    gamestats = []
    # reads in data of the season's mean
    ref = pd.read_csv(STATS_NBA_PATH % "2008-09_team_mean.csv")  # reads the mean data of teams of the season
    opponent_team_mean = ref[ref['TEAM_ABBREVIATION'] == team.oppteamname].squeeze()

    opponent_team_mean.index = ['OPP_%s' % elt for elt in opponent_team_mean.index]

    for lineup_no in range(1, team.totalcombi + 1):  # Loop over lineups in the game
        lineup = team.give_nth_combination(lineup_no)

        player_names = get_player_list(lineup, team.teamno)

        interval = calculate_interval(team, lineup_no)

        lineup_data = get_lineup_data(teamname, player_names, interval, type="none")
        if lineup_data.empty:
            return pd.Series()
        # print lineup_data
        row_s = lineup_data  # This transforms the columns name used by stats.nba.com to the convention
        # I used throughout the project
        # row_s.rename(index={
        #     'PLUS_MINUS': 'PTD',
        #     'PTS': 'P',
        #     'FT_PCT': 'FTP',
        #     'FG_PCT': 'FGP',
        #     'OREB': 'ORB',
        #     'DREB': 'DRB',
        #     'REB': 'TRB',
        #     'FG3_PCT': 'B3P',
        #     'PF': 'F'
        # }, inplace=True)
        # row_s.drop("PFD", inplace=True)  # drop Personal Foul Drawn since not used in our study
        row_s.name = lineup_no
        row_s["interval"] = interval
        # if row_s.TYPE == ("median" or "mean"):
        #     pass
        # else:
        gamestats.append(row_s.T)
            # print gamestats
    game_agg = pd.DataFrame(gamestats).sum()  # sum up a games all scores
    # this PTD is still the actual PTD of the game, it is only the
    # stats that have been replaced.
    # game_agg.PTD = team.PTD
    game_agg["Actual PTS"] = team.P
    game_agg["Actual PTS scaled"] = team.P * game_agg.interval / float(team.interval)
    game_agg["Actual PTD scaled"] = team.PTD * game_agg.interval / float(team.interval)
    game_agg["Actual PTD"] = team.PTD
    game_agg = game_agg.append(opponent_team_mean["OPP_FGM":])
    # print game_agg
    return game_agg





def generate_games_from_team_season_mean():
    """use mean data throughout the season, combine with actual PTS and PTD"""

    a = []
    ref = pd.read_csv(STATS_NBA_PATH % ("2008-09_team_mean.csv"))
    MEANATTR = [
        'TEAM_ABBREVIATION',
        'FGM', 'FGA', 'FG_PCT',
        'FG3M', 'FG3A', 'FG3_PCT',
        'FTM', 'FTA', 'FT_PCT',
        'OREB',
        'DREB', 'REB',
        'AST',
        'TOV',
        'STL', 'BLK', 'PFD',
        'PLUS_MINUS', 'PTS']
    for team in ALLTEAMS:
        print "preparing stats from " + team
        for gamename in ALL_GAME_FILES:
            result = re.search(team, gamename)
            if result:
                print 'loading %s' % gamename
                team1name = gamename[9:12]
                team1_ref = ref[ref['TEAM_ABBREVIATION'] == team1name].squeeze()
                team2name = gamename[12:15]
                team1 = BasketballGame(gamename, pd.read_csv(PLAY_BY_PLAY_DIRECTORY + gamename), team1name, 1)
                team2 = BasketballGame(gamename, pd.read_csv(PLAY_BY_PLAY_DIRECTORY + gamename), team2name, 2)
                team2_ref = ref[ref['TEAM_ABBREVIATION'] == team2name].squeeze()

                team1row = _generate_row(team1_ref, MEANATTR)
                team1row[18] = team1.PTD
                team1row[19] = team1.P

                team2row = _generate_row(team2_ref, MEANATTR)
                team2row[18] = team2.PTD
                team2row[19] = team2.P
                # this extends opponent data to the row
                team1_temp = team1row[:]
                team1row.extend(team2row)
                # print len(team1_temp)
                team2row.extend(team1_temp)

                a.append(team1row)
                a.append(team2row)
    meanattr = MEANATTR
    # COL.extend(elt for elt in ['opp_'+elt for elt in OPPCOL])
    df = pd.DataFrame(a, columns=meanattr + ['OPP_' + elt for elt in meanattr])
    return df.copy()


def main():
    # this runs for all the 30 teams

    # total_stats = []
    for team in ALLTEAMS:  # LOOP over all the teams
        if not os.path.exists(('../../data/%s/%s' % ('game_lineup_json', team)) + '/'):
            os.makedirs(('../../data/%s/%s' % ('game_lineup_json', team)) + '/')
            print 'creating directory for %s' % team
        print "preparing stats from " + team
        for gamename in ALL_GAME_FILES:  #loopover all games of the team
            result = re.search(team, gamename)
            if result:
                print 'loading from %s' % gamename
                teamno = 1 if result.start() == 9 else 2
                # total_stats.append(generate_game_data(gamename,teamno))
                game_json = generate_json_lineup_data(gamename, teamno)
                with open(DATAPATH % ('game_lineup_json', team, gamename[0:15] + '.json'), 'w') as f:
                    f.write(json.dumps(game_json))
                    # total_stats = pd.DataFrame(total_stats)
                    # print total_stats


def opplineup(filename):
    # namecolumns = ['a1', 'a2', 'a3', 'a4', 'a5', 'h1', 'h2', 'h3', 'h4', 'h5']
    DATA_FOR_NOT_FOUND = "median"
    out = []
    df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + filename)
    team_name = filename[9:12]
    opp_team_name = filename[12:15]
    if (opp_team_name not in ALLTEAMS) and (team_name not in ALLTEAMS):
        print '%s, one of the team not available, skip!' % filename
        return pd.DataFrame()
    else:
        add_aid_rows(df, [team_name, opp_team_name])
        total_lineup = df.head(1).lineup_no.item() + 1
        for lineup_no in range(1, int(total_lineup)):  # go through all the lineups in the game
            lineup_df = df[df.lineup_no == lineup_no]  #
            interval = lineup_df.head(1).timeleft.item() - lineup_df.tail(1).timeleft.item()  # calculate the
            # interval of this lineup

            # print 'This is lineup: %s, the interval is %s' %(lineup_no,interval)
            team1 = lineup_df[lineup_df.team == team_name]
            team2 = lineup_df[lineup_df.team == opp_team_name]
            for team_no, (team_name, team_data), in enumerate(zip([team_name, opp_team_name], [team1, team2])):
                if team_data.empty:  # check that the lineup contains this data of this team
                    print '%s, %s, %s, team not in this lineup data' % (filename, lineup_no, team_name)
                else:
                    team_players = get_player_list(team_data, team_no + 1)
                    lineup_data = get_lineup_data(team_name, team_players, type="none")  # retrieve data from stats.nba
                    if lineup_data.empty is False:
                        team_points = score_calculate(team_data)
                        lineup_data['interval'] = interval  # calculate the interval of this lineup
                        lineup_data['PPM'] = float(team_points) / interval * 60  # calculate PPM(POINTS PER MINUTE)
                        # print lineup_data
                        out.append(lineup_data)  # append a line to the lineup data
            # print  pd.concat(out, axis=1).T
            if out != []:
                return pd.concat(out, axis=1).T  # concatenate all lineup data of one game
            else:
                return pd.Series()





