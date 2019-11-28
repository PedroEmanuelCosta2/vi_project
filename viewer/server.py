import sys
import os
from math import log2, log10
from enum import Enum
from nltk.corpus import stopwords
from flask import Flask, render_template, request, jsonify
from src.armed_conflict import ArmedConflict
from gensim.utils import simple_preprocess

sys.path.insert(0, '../')
import settings as st

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

armed_conflict_pickle_path = os.path.join(st.files['armed_conflict_pickle'], "ArmedConflict.pkl")
ARMED_CONFLICT = ArmedConflict.load(armed_conflict_pickle_path)

STOP_WORDS = stopwords.words('english')


class ArmedConflictParam(Enum):
    NUMBER_OF_CONFLICT = 1
    NUMBER_OF_HEADLINES = 2
    HEADLINES = 3


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html')


@app.route('/armed_conflict_total', methods=['POST'])
def post_armed_conflict_total():
    json_dict = sub_dict(ARMED_CONFLICT.armed_conflict_total, ArmedConflictParam.NUMBER_OF_CONFLICT.value)
    return jsonify(json_dict)


@app.route('/armed_conflict_pruned', methods=['POST'])
def post_armed_conflict_pruned():
    json_dict = sub_dict(ARMED_CONFLICT.armed_conflict_pruned, ArmedConflictParam.NUMBER_OF_CONFLICT.value)
    return jsonify(json_dict)


@app.route('/headlines_ratio_armed_conflict', methods=['POST'])
def post_headlines_ratio_armed_conflict():
    json_dict = {}

    armed_conflict_pruned = ARMED_CONFLICT.armed_conflict_pruned

    for country_code in armed_conflict_pruned.keys():

        number_of_conflict = armed_conflict_pruned[country_code][ArmedConflictParam.NUMBER_OF_CONFLICT.value]
        number_of_headlines = armed_conflict_pruned[country_code][ArmedConflictParam.NUMBER_OF_HEADLINES.value]

        if number_of_conflict > 1:
            json_dict[country_code] = round((log2(number_of_headlines / number_of_conflict)), 2)
        else:
            json_dict[country_code] = 0

    return jsonify(json_dict)


@app.route('/headlines_word_map', methods=['POST'])
def post_headlines_word_map():
    word_map = {}

    armed_conflict_pruned = ARMED_CONFLICT.armed_conflict_pruned

    for country_code in armed_conflict_pruned.keys():
        headlines = armed_conflict_pruned[country_code][ArmedConflictParam.HEADLINES.value]

        for headline in headlines:
            headline = simple_preprocess(headline, deacc=True)

            for word in headline:
                if word not in STOP_WORDS:
                    if word not in word_map.keys():
                        word_map[word] = 0
                    word_map[word] += 1

    json_dict = word_map

    return jsonify(json_dict)


def sub_dict(my_dict, armed_conflict_parm):
    my_sub_dict = {}

    for key in my_dict.keys():
        my_sub_dict[key] = my_dict[key][armed_conflict_parm]

    return my_sub_dict
