import sys
import os
from src.armed_conflicts_manager import ArmedConflictManager

sys.path.insert(0, '../')
import settings as st

if __name__ == '__main__':

    armed_conflict = ArmedConflictManager()

    armed_conflict_pickle_path = os.path.join(st.files['armed_conflict_pickle'], "ArmedConflict.pkl")

    # armed_conflict = ArmedConflict.load(armed_conflict_pickle_path)
    # print(armed_conflict.armed_conflict_total['CH'][1])

    armed_conflict_total_path = os.path.join(st.files['armed_conflict'], "armed_conflict.xlsx")
    armed_conflict_pruned_path = os.path.join(st.files['armed_conflict'], "pruned_articles_armed_conflict.xlsx")

    armed_conflict.df_total = armed_conflict.read_df(armed_conflict_total_path)
    armed_conflict.df_pruned = armed_conflict.read_df(armed_conflict_pruned_path)

    armed_conflict.armed_conflict_total = armed_conflict.init_armed_conflict(armed_conflict.df_total)
    armed_conflict.armed_conflict_pruned = armed_conflict.init_armed_conflict(armed_conflict.df_pruned)

    armed_conflict.save(armed_conflict_pickle_path)
