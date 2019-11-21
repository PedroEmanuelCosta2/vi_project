import pandas as pd


class ArmedConflict:

    def __init__(self, df_path=None):
        if df_path is None:
            self.df_path = ""
        else:
            self.df_path = df_path

        self.df = pd.read_excel(self.df_path)

        self.position = {}

        self.init()

    def init(self):
        self.init_position()

    def init_position(self):
        for _, row in self.df.iterrows():
            zone = row.where_coordinates
            latitude = row.latitude
            longitude = row.longitude

            self.position[zone] = (latitude, longitude)
