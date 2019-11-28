import os

root_path = os.path.dirname(os.path.abspath(__file__))  # path to this file

files = dict(data_folder=os.path.join(root_path, 'data'))
files.update(
    dict(
        armed_conflict=os.path.join(files['data_folder'], "armed_conflict"),
        armed_conflict_pickle=os.path.join(files['data_folder'], "armed_conflict_pickle")
    )
)
