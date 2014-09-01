"""This file helps to get lineup stats from scraped data from stats.nba.com"""

__author__ = 'luoyicheng'
import pandas as pd
# Path settings
LINEUP_STATS_PATH = '../../data/stats_nba/2008-09_team_lineup/%s.csv'  # PATH where stats.nba.com data is located
STATS_NBA_PATH = '../../data/stats_nba/%s'

# Retrieved attribute settings
ATTRIBUTES = ["FGM", "FGA", "FGP", "FG3M", "FG3A", "FG3P", "FTM", "FTA", "FTP",
              "OREB", "DREB", "REB", "TOV", "TOVP",
              "AST", "PF", "STL", "BLK",
              ]



def get_lineup_data(team_name, lineup_key, interval=60 * 48, normalize=True, type="median"):
    """This function retrieves to find lineup data from stats.nba.com using name keys"""
    """the normalization uses seconds"""
    try:
        ref = pd.read_csv(LINEUP_STATS_PATH % team_name)
    except:
        print "%s, STAT.NBA.com of the team not AVAILABLE " % team_name
        return pd.Series()

    if type == "mean":
        not_found_reference = ref.mean()
    elif type == "median":
        not_found_reference = ref.median()
    elif type == "none":
        pass

    key = " - ".join(
        sorted([",".join(name.split()[::-1]) for name in lineup_key]))  # form the search key used in statsnba.com data

    mask = ref['GROUP_NAME'] == key
    normalize_coefficient = interval / float(60 * 48)

    if mask.any():
        out = (ref[mask].squeeze()['FGM':]) * normalize_coefficient
        out["TYPE"]="none"
        return out  # /float(2880)
    else:
        print 'Season Team %s,team: %s,lineupkey=%s' % (type, team_name, key)
        if type == "none":
            return pd.Series()
        else:
            df = not_found_reference["FGM":] * normalize_coefficient  # need to redo this part
            df["TYPE"] = type
            df["NON_LINEUP_COUNT"] = 1
            return df

def get_team_seasonal_mean(team_name):
    """Obtain the team seasonal mean data from stats.nba.com"""
    ref = pd.read_csv(STATS_NBA_PATH % "2008-09_team_mean.csv")
    team_seasonal_mean = ref[ref['TEAM_ABBREVIATION'] == team_name].squeeze()
    return team_seasonal_mean[ATTRIBUTES]

