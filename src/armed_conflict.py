import pandas as pd
import pycountry


class ArmedConflict:

    def __init__(self, df_path=None):
        self.df = self.read_df(df_path)
        self.position = {}
        self.countries = {}
        self.number_of_armed_conflict = {}

        self.init()

    def init(self):
        self.init_countries()
        self.init_number_of_armed_conflict(self.df)

    def init_countries(self):
        for country in pycountry.countries:
            country_name = country.name.lower()
            country_code = country.alpha_2

            self.countries[country_name] = country_code
            self.number_of_armed_conflict[country_code] = 0
            self.number_of_armed_conflict['XS'] = 0

    def init_number_of_armed_conflict(self, df):
        # for code in self.number_of_armed_conflict.keys():
        #     self.number_of_armed_conflict[code] = 0

        for _, row in df.iterrows():
            country = row.country.lower()
            code = self.countries[country]

            self.number_of_armed_conflict[code] += 1

    def init_position(self, df):
        for _, row in df.iterrows():
            zone = row.where_coordinates
            latitude = row.latitude
            longitude = row.longitude

            self.position[zone] = (latitude, longitude)

    @staticmethod
    def read_df(df_path=None):
        if df_path is None:
            df_path = ""
        else:
            df_path = df_path

        return pd.read_excel(df_path)
