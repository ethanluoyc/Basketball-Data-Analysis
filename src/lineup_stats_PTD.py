__author__ = 'luoyicheng'

import pandas as pd
import StatsNba as nba

# df = pd.read_csv("../../lineup_from_playbplay_allteams_9 Aug 2.0.csv")

df = pd.concat([pd.read_csv("../testing.csv"),pd.read_csv("../training.csv")],axis=0)
def get_lineup_stats(row, key=["P1", "P2", "P3", "P4", "P5"]):
    data = nba.som_get_lineup_data(row[key])
    row_o = row[key].append(data)
    return pd.DataFrame(row_o)


table = []

for i, row in df.iterrows():
    # if i == 20: break
    team_data = get_lineup_stats(row)
    opp_team_data = get_lineup_stats(row, ["O1", "O2", "O3", "O4", "O5"])
    opp_team_data.index = ["OPP_"+ col for col in opp_team_data.index]
    table.append(pd.concat([team_data, opp_team_data,pd.Series(row["PTD"],index=["PTD"])],axis=0).T)
    # print pd.concat([team_data, opp_team_data],axis=0).T
df = pd.concat(table, axis=0)

df.to_csv("../som_lineup_nba_stats_playby_play.csv", index=False, float_format="%.1f")







