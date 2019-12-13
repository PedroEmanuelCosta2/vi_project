import sys
import os
from src.armed_conflicts_manager import ArmedConflictManager

sys.path.insert(0, '../')
import settings as st

if __name__ == '__main__':

    armed_conflict = ArmedConflictManager()

    armed_conflict_pickle_path = os.path.join(st.files['armed_conflict_pickle'], "ArmedConflict.pkl")

    armed_conflict_total_path = os.path.join(st.files['armed_conflict'], "armed_conflict.xlsx")
    armed_conflict.df_total = armed_conflict.read_df(armed_conflict_total_path)

    try:
        armed_conflict_pruned_path = os.path.join(st.files['armed_conflict'], "pruned_articles_armed_conflict.xlsx")
        armed_conflict.df_pruned = armed_conflict.read_df(armed_conflict_pruned_path)
    except:
        columns = ['id', 'year', 'type_of_violence', 'conflict_name', 'side_a',
                   'side_b', 'number_of_sources', 'source_article', 'source_office',
                   'source_date', 'source_headline', 'source_original',
                   'where_coordinates', 'latitude', 'longitude', 'country', 'country_id',
                   'region', 'date_start', 'date_end', 'deaths_a', 'deaths_b', 'deaths_civilians']

        armed_conflict.df_pruned = armed_conflict.df_total[columns]
        armed_conflict.df_pruned = armed_conflict.df_pruned.dropna(subset=['source_headline'])

    armed_conflict.armed_conflict_total = armed_conflict.init_armed_conflict(armed_conflict.df_total)
    armed_conflict.armed_conflict_pruned = armed_conflict.init_armed_conflict(armed_conflict.df_pruned)

    armed_conflict.save(armed_conflict_pickle_path)
