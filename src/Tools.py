__author__ = 'luoyicheng'


def label_win_loss(df):
    """Apply this funcion to a Series to determine whether it is win or loss"""
    idx = "PTD"
    df["WL"] = "NA"
    def win_or_lose(row):
        if row[idx] > 0:
            return "WIN"
        elif row[idx]==0:
            return "DRAW"
        else:
            return "LOSE"
    df["WL"] = df.apply(win_or_lose,axis=1)
    return df

def game_file_info(filename, teamname):
    dict = {}
    dict["game_id"] = filename
    dict["teams"] = [filename[9:12], filename[12:15]]
    dict["team_no"] = 1 if teamname == dict["teams"][0] else 2
    dict["oppteam_no"] = 2 if dict["team_no"] == 1 else 1
    dict["team_name"] = teamname
    dict["oppteam_name"] = dict["teams"][0] if dict["teams"][0] != teamname else dict["teams"][1]
    return dict