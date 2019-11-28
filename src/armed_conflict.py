import pandas as pd
import pickle
import pycountry


class ArmedConflict:

    def __init__(self):
        self.df_total = None
        self.df_pruned = None
        self.armed_conflict_total = {}
        self.armed_conflict_pruned = {}
        self.countries = {}
        self.init()

    def init(self):
        self.init_countries()

    def init_countries(self):
        for country in pycountry.countries:
            country_name = country.name.lower()
            country_code = country.alpha_2

            self.countries[country_name] = country_code

    def init_armed_conflict(self, df):
        # (country name, number of conflict, number of headlines, headlines)
        armed_conflict = {'XS': ["", 0, 0, []]}

        for country_name in self.countries.keys():
            country_code = self.countries[country_name]
            armed_conflict[country_code] = [country_name, 0, 0, []]

        for _, row in df.iterrows():
            country = row.country.lower()
            code = self.countries[country]
            number_of_headlines = 0 if row.number_of_sources < 0 else row.number_of_sources

            try:
                headlines = row.source_headline.split(';')
            except:
                headlines = []

            armed_conflict[code][1] += 1  # Number of conflict
            armed_conflict[code][2] += number_of_headlines  # Number of headlines per country
            armed_conflict[code][3] += headlines  # All headlines per country

        return armed_conflict

    def save(self, path_file):
        pickle.dump(self, open(path_file, "wb"))

    @staticmethod
    def load(path_file):
        return pickle.load(open(path_file, "rb"))

    @staticmethod
    def init_position(df):
        position = {}

        for _, row in df.iterrows():
            zone = row.where_coordinates
            latitude = row.latitude
            longitude = row.longitude
            position[zone] = (latitude, longitude)

        return position

    @staticmethod
    def read_df(df_path=None):
        if df_path is None:
            df_path = ""
        else:
            df_path = df_path

        return pd.read_excel(df_path)
