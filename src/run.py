from main import *
from Tools import game_file_info, label_win_loss
from Basketball import LineupStats

ALLTEAMS = ['CLE', 'NJN', 'NYK', 'MIL', 'PHI', 'ATL', 'MIN', 'DEN', 'OKC',
            'MIA', 'WAS', 'MEM', 'CHI', 'LAL', 'POR', 'GSW', 'UTA', 'ORL',
            'DET', 'IND', 'TOR', 'HOU', 'SAS', 'BOS', 'LAC', 'PHX', 'SAC']

ATTRIBUTES = ["FGM", "FGA", "FGP", "FG3M", "FG3A", "FG3P", "FTM", "FTA", "FTP",
              "OREB", "DREB", "REB", "TOV", "TOVP",
              "AST", "PF", "STL", "BLK",
              "INTERVAL", "PTS", "PTD"]


def loop_over_games_of_teams(team_list=ALLTEAMS):
    """A decorator which allows the data generation to iterate over games of teams and the teams of the season"""
    def outter_wrapper(f):
        """function layer, used as input for a function that returns the DataFrame from a game"""
        def wrapper():
            output = []
            for team_name in team_list:  # loop over all teams
                for file_name in ALL_GAME_FILES:  # loop over all games of the team
                    result = re.search(team_name, file_name)  # find game_id that includes the team
                    if result:
                        print 'loading from %s' % file_name
                        output.append(label_win_loss(f(team_name, file_name)))
                        # add in DataFame.to_csv() if want to separately save the stats for different teams
            return pd.concat(output, axis=0)

        return wrapper
    return outter_wrapper

@loop_over_games_of_teams
def lineup_data_of_game(team_name, file_name):
    # read the play-by-play data
    df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + file_name)
    team_data = BasketballGame(file_name, df, team_name, 1 if team_name == file_name[9:12] else 2)
    team_info = game_file_info(file_name, team_name)
    game = []
    for linup_no in range(1, int(team_data.data.tail(1).combination_number.item()) + 1):
        lineup_df = team_data.give_nth_combination(linup_no)
        lineup = LineupStats(lineup_df, team_info).generate_row(["FTM", "FTA", "PTS"]).append(pd.Series(team_info))
        game.append(lineup)
    return pd.concat(game, axis=1).T


# print lineup_data_of_game()

@loop_over_games_of_teams
def main(team_name, file_name):
    rows = []
    # NAME_COLUMNS = ["a1", "a2", "a3", "a4", "a5", "h1", "h2", "h3", "h4", "h5"]
    game_info = game_file_info(file_name, team_name)

    # load the play-by-play data from the csv file
    team_df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + file_name)

    # add aid rows that would help split the lineups
    # can have two settings, one is by a team, two is by both teams, i.e. as long as one player is swaped, there is a
    # new lineup
    add_aid_rows(team_df, game_info["teams"])

    # end_lineup_no is the total number of lineups present in the game
    end_lineup_no = int(team_df.tail(1).lineup_no.item())
    for lineup in range(1, end_lineup_no + 1):
        lineup_df = team_df[team_df["lineup_no"] == lineup]
        lineup_data = LineupStats(lineup_df, game_info)
        rows.append(pd.Series(lineup_data.PLAYERS + lineup_data.OPPONENTS + [team_name, file_name]).append(
            lineup_data.generate_row(ATTRIBUTES)))
    return pd.concat(rows, axis=1).T


COLUMNS = ["FGM", 'FGA', 'FGP',
           'B3M', 'B3A', 'B3P',
           'FTM', 'FTA', 'FTP',
           'ORB', 'DRB', "TRB", "ORBP", "DRBP", "TRBP",
           'TOV', 'STL', 'BLK', 'F',
           'PTD', 'P']


def generate_row(df, col=COLUMNS):
    """'used to generate a list from the attributes"""
    row = []
    for attribute in col:
        row.append(getattr(df, attribute))
    return row


@loop_over_games_of_teams
def gamestats_from_actual_play_by_play(team_name, file_name):
    df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + file_name)
    game_info = game_file_info(file_name, team_name)
    team_data = BasketballGame(file_name, df, team_name, 1 if team_name == file_name[9:12] else 2)
    oppteam_data = BasketballGame(file_name, df, game_info["oppteam_name"], game_info["oppteam_no"])
    game = []

    game_stats = pd.Series(generate_row(team_data), index=COLUMNS)
    oppgame_stats = pd.Series(generate_row(oppteam_data), index=['OPP_' + elt for elt in COLUMNS])
    game.append(game_stats)
    game.append
    out = pd.DataFrame(pd.concat([game_stats, oppgame_stats], axis=0)).T
    return out


@loop_over_games_of_teams
def gamestats_from_statsnba_mean(team_name, file_name):
    """read the two opposing teams, then replace game stats with seasonal mean from stats.nba.com"""
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

    game_info = game_file_info(file_name, team_name)
    ref = pd.read_csv(STATS_NBA_PATH % ("2008-09_team_mean.csv"))
    df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + file_name)

    team_name = game_info["team_name"]
    oppteam_name = game_info["oppteam_name"]
    team_df = BasketballGame(file_name, df, team_name, game_info["team_no"])
    oppteam_df = BasketballGame(file_name, df, oppteam_name, game_info["oppteam_no"])

    team_seasonal_mean = ref[ref['TEAM_ABBREVIATION'] == team_name].squeeze()
    team_seasonal_mean = team_seasonal_mean.append(pd.Series([team_df.PTD, team_df.P], index=["PTD", "POINTS"]))
    oppteam_seasonal_mean = ref[ref['TEAM_ABBREVIATION'] == oppteam_name].squeeze()
    oppteam_seasonal_mean = oppteam_seasonal_mean.append(
        pd.Series([oppteam_df.PTD, oppteam_df.P], index=["PTD", "POINTS"]))
    oppteam_seasonal_mean.index = ['OPP_' + elt for elt in oppteam_seasonal_mean.index]

    return label_win_loss(pd.DataFrame(pd.concat([team_seasonal_mean, oppteam_seasonal_mean], axis=0)).T)


@loop_over_games_of_teams
def gamestats_from_play_by_play_opponent_mean(team_name, file_name):
    df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + file_name)
    game_info = game_file_info(file_name, team_name)
    team_data = BasketballGame(file_name, df, team_name, 1 if team_name == file_name[9:12] else 2)

    ref = pd.read_csv(STATS_NBA_PATH % ("2008-09_team_mean.csv"))

    opp_seasonal_mean = ref[ref['TEAM_ABBREVIATION'] == game_info["oppteam_name"]].squeeze()
    game_stats = pd.Series(generate_row(team_data), index=COLUMNS)

    out = pd.DataFrame(pd.concat([game_stats, opp_seasonal_mean], axis=0)).T
    return out


@loop_over_games_of_teams(ALLTEAMS)
def lineupstats_splitbytwoteams(team_name, file_name):
    rows = []
    # NAME_COLUMNS = ["a1", "a2", "a3", "a4", "a5", "h1", "h2", "h3", "h4", "h5"]
    game_info = game_file_info(file_name, team_name)

    # load the play-by-play data from the csv file
    team_df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + file_name)

    # add aid rows that would help split the lineups
    # can have two settings,  
    # one is by a team, 
    #two is by both teams, i.e. as long as one player is swaped, there is a
    # new lineup
    add_aid_rows(team_df, game_info["teams"])

    # end_lineup_no is the total number of lineups present in the game
    end_lineup_no = int(team_df.tail(1).lineup_no.item())
    # iterate through all lineups in the team
    for lineup in range(1, end_lineup_no + 1):
        lineup_df = team_df[team_df["lineup_no"] == lineup]

        # generate stats for the interval played by this particular lineup
        lineup_data = LineupStats(lineup_df, game_info)
        lineup_row = pd.Series(
                                lineup_data.PLAYERS +
                                lineup_data.OPPONENTS +
                                [team_name, file_name]).append(
                                lineup_data.generate_row(ATTRIBUTES)
        )

        if (lineup_row.INTERVAL != 0 ):
            rows.append(lineup_row)

    # concatenate the lineups of the game into a DataFrame
    return pd.concat(rows, axis=1).T


@loop_over_games_of_teams(ALLTEAMS)
def gamestats_from_weighted_sum_lineups(team_name, file_name):
    game_info = game_file_info(file_name, team_name)
    rows = []
    
    # load the play-by-play data from the csv file
    team_df = pd.read_csv(PLAY_BY_PLAY_DIRECTORY + file_name)

    # add aid rows that would help split the lineups
    # can have two settings, one is by a team, two is by both teams, i.e. as long as one player is swaped, there is a
    # new lineup
    add_aid_rows(team_df, game_info["teams"])

    # end_lineup_no is the total number of lineups present in the game
    end_lineup_no = int(team_df.tail(1).lineup_no.item())
    # iterate through all lineups in the team
    for lineup in range(1, end_lineup_no + 1):
        lineup_df = team_df[team_df["lineup_no"] == lineup]
        lineup_data = LineupStats(lineup_df, game_info)
        lineup_row = get_lineup_data(game_info["team_name"], lineup_data.PLAYERS,
                                      interval=lineup_data.INTERVAL,
                                      type="median")

        rows.append(lineup_row)
    game_data = pd.concat(rows, axis=1).T

    # calculate weighted sum,this will generate a row
    out_df = game_data.sum()

    out_df["game_id"] = file_name

    #append the game's PTD to the Series of entry
    df = team_df
    out_df["PTD"] = score_calculate(df[df["team"]==game_info["team_name"]])- \
                    score_calculate(df[df["team"]==game_info["oppteam_name"]])

    # concatenate the lineups of the game into a DataFrame
    return pd.DataFrame(out_df).T



df = lineupstats_splitbytwoteams()
df.to_csv(OUTPUT_PATH % "lineupstats_splitbytwoteams.csv", index=False)




