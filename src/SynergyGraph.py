import pandas as pd
import time
import os

PLAYERCOLUMNS = ["P1", "P2", "P3", "P4", "P5"]
DATA_PATH = "../../data/synergy/%s"

SYNERGY_PATH = "../../synergy graph/Synergy Graph/data/%s/"


class SynergyGraphData():
    def __init__(self, csv_path):
        df = pd.read_csv(DATA_PATH %csv_path)
        self.players = set(df[PLAYERCOLUMNS].values.ravel().tolist())
        self.data = df

    def write_players(self):
        return self.players

    def write_data(self, attribute):
        return self.data[PLAYERCOLUMNS+[attribute]]
    def write_dataset(self, folder_name, comments="NO"):

        date =  time.strftime("_%d_%m_%Y")
        folder = folder_name + date
        outputpath = SYNERGY_PATH % folder + "/"
        os.makedirs(outputpath)
        with open(outputpath + "players.txt", "w") as players_file:
            [players_file.write(player+",") for player in self.players]
        with open(outputpath + "notes.txt", "w") as notes_file:
            notes_file.write(comments)
        self.data.to_csv(outputpath + "data.csv", index=False)


data = SynergyGraphData("CLE_REB.csv")
data.write_dataset("trial")