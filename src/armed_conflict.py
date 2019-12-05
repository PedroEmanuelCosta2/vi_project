from datetime import date


class ArmedConflict:

    def __init__(self, year, conflict_name, side_a, side_b, number_of_sources, source_article, source_office,
                 source_date, source_headline, source_original, where_coordinates, latitude, longitude,
                 country, country_code, region, date_start, date_end, deaths_a, deaths_b, deaths_civilians):

        self.year = int(year)
        self.conflict_name = conflict_name.lower()
        self.side_a = side_a.lower()
        self.side_b = side_b.lower()
        self.number_of_sources = 0 if number_of_sources < 0 else number_of_sources
        self.source_article = self.split_text(source_article, ';')
        self.source_office = self.split_text(source_office, ';')

        try:
            self.source_date = [date(int(d[0:4]), int(d[5:7]), int(d[8:10])) for d in source_date.split(';')]
        except:
            self.source_date = []

        self.source_headline = self.split_text(source_headline, ';')
        self.source_original = self.split_text(source_original, ';')
        self.where_coordinates = where_coordinates.lower()
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.country = country.lower()
        self.country_code = country_code
        self.region = region.lower()
        self.date_start = date_start
        self.date_end = date_end
        self.deaths_a = int(deaths_a)
        self.deaths_b = int(deaths_b)
        self.deaths_civilians = int(deaths_civilians)

    @staticmethod
    def split_text(text, sep):

        try:
            return [t.lower() for t in text.split(sep)]
        except:
            return []
