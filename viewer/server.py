from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.insert(0, '../')
import settings as st
sys.path.insert(0, 'src/')
from armed_conflict import ArmedConflict

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

armed_conflict_path = os.path.join(st.files['armed_conflict'], "pruned_articles_armed_conflict.xlsx")
ARMED_CONFLICT = ArmedConflict(armed_conflict_path)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html')


@app.route('/armed_conflict_position', methods=['POST'])
def post_visualisation():
    json_dict = ARMED_CONFLICT.position
    return jsonify(json_dict)
