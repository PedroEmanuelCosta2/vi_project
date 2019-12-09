import pandas as pd
import pickle
import pycountry
from src.armed_conflict import ArmedConflict


class ArmedConflictManager:

    def __init__(self):
        self.df_total = None
        self.df_pruned = None
        self.armed_conflict_total = []
        self.armed_conflict_pruned = []
        self.countries = {}
        self.init()

    def init(self):
        self.init_countries()

    def init_countries(self):
        for country in pycountry.countries:
            country_name = country.name.lower()
            country_code = country.alpha_2

            self.countries[country_name] = country_code

        self.countries['kosovo'] = 'XK'
        self.countries['somaliland'] = 'XS'

    def init_armed_conflict(self, df):

        armed_conflicts = []

        for _, row in df.iterrows():
            country_name = row.country.lower()
            country_code = self.countries[country_name]

            armed_conflicts.append(
                ArmedConflict(row.year, row.conflict_name, row.side_a, row.side_b, row.number_of_sources,
                              row.source_article, row.source_office, row.source_date, row.source_headline,
                              row.source_original, row.where_coordinates, row.latitude, row.longitude,
                              row.country, country_code, row.region, row.date_start, row.date_end,
                              row.deaths_a, row.deaths_b, row.deaths_civilians))

        curr_countries = [a.country for a in armed_conflicts]
        diff_countries = self.diff(list(self.countries.keys()), curr_countries)

        for c in diff_countries:
            armed_conflicts.append(ArmedConflict(country=c, country_code=self.countries[c]))

        return armed_conflicts

    def save(self, path_file):
        pickle.dump(self, open(path_file, "wb"))

    @staticmethod
    def diff(first, second):
        first = set(first)
        second = set(second)
        return [item for item in first if item not in second]

    @staticmethod
    def load(path_file):
        return pickle.load(open(path_file, "rb"))

    @staticmethod
    def read_df(df_path=None):
        if df_path is None:
            df_path = ""
        else:
            df_path = df_path

        return pd.read_excel(df_path)
