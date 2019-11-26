from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.insert(0, '../')
import settings as st
sys.path.insert(0, 'src/')
from armed_conflict import ArmedConflict

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

armed_conflict_total_path = os.path.join(st.files['armed_conflict'], "armed_conflict.xlsx")
armed_conflict_pruned_path = os.path.join(st.files['armed_conflict'], "pruned_articles_armed_conflict.xlsx")
ARMED_CONFLICT_TOTAL = ArmedConflict(armed_conflict_total_path)
ARMED_CONFLICT_PRUNED = ArmedConflict(armed_conflict_pruned_path)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html')


@app.route('/armed_conflict_number', methods=['POST'])
def post_armed_conflict_number():
    pruned = request.form['pruned']

    if pruned == "false":
        number_of_armed_conflict = ARMED_CONFLICT_TOTAL.number_of_armed_conflict
    else:
        number_of_armed_conflict = ARMED_CONFLICT_PRUNED.number_of_armed_conflict

    json_dict = number_of_armed_conflict

    return jsonify(json_dict)
