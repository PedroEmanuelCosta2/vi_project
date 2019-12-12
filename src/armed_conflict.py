from datetime import date


class ArmedConflict:

    def __init__(self, year=None, conflict_name=None, side_a=None, side_b=None, number_of_sources=None,
                 source_article=None, source_office=None, source_date=None, source_headline=None, source_original=None,
                 where_coordinates=None, latitude=None, longitude=None, country=None, country_code=None, region=None,
                 date_start=None, date_end=None, deaths_a=None, deaths_b=None, deaths_civilians=None):

        self.year = 0 if year is None else int(year)
        self.conflict_name = "" if conflict_name is None else conflict_name.lower()
        self.side_a = "" if side_a is None else side_a.lower()
        self.side_b = "" if side_b is None else side_b.lower()
        self.number_of_sources = 0 if number_of_sources is None else number_of_sources
        self.source_article = [] if source_article is None else self.split_text(source_article, ';')
        self.source_office = [] if source_office is None else self.split_text(source_office, ';')

        try:
            self.source_date = [] if source_date is None else [self.date_format(d) for d in source_date.split(';')]
        except:
            self.source_date = []

        self.source_headline = [] if source_headline is None else self.split_text(source_headline, ';')
        self.source_original = [] if source_original is None else self.split_text(source_original, ';')
        self.where_coordinates = "" if where_coordinates is None else where_coordinates.lower()
        self.latitude = 0 if latitude is None else float(latitude)
        self.longitude = 0 if longitude is None else float(longitude)
        self.country = "" if country is None else country.lower()
        self.country_code = "" if country_code is None else country_code
        self.region = "" if region is None else region.lower()
        self.date_start = date(1970, 1, 1) if date_start is None else date_start
        self.date_end = date(1970, 1, 1) if date_end is None else date_end
        self.deaths_a = 0 if deaths_a is None else int(deaths_a)
        self.deaths_b = 0 if deaths_b is None else int(deaths_b)
        self.deaths_civilians = 0 if deaths_civilians is None else int(deaths_civilians)

    @staticmethod
    def date_format(d):
        return date(int(d[0:4]), int(d[5:7]), int(d[8:10]))

    @staticmethod
    def split_text(text, sep):

        try:
            return [t.lower() for t in text.split(sep)]
        except:
            return []
