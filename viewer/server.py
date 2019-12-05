import os
import sys
from math import log2

from flask import Flask, render_template, jsonify
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

from src.armed_conflicts_manager import ArmedConflictManager

sys.path.insert(0, '../')
import settings as st

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

armed_conflict_pickle_path = os.path.join(st.files['armed_conflict_pickle'], "ArmedConflict.pkl")
ARMED_CONFLICT_MANAGER = ArmedConflictManager.load(armed_conflict_pickle_path)

STOP_WORDS = stopwords.words('english')


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html')


@app.route('/armed_conflict_total', methods=['POST'])
def post_armed_conflict_total():
    json_dict = number_of_conflict_per_country(ARMED_CONFLICT_MANAGER.armed_conflict_total)
    return jsonify(json_dict)


@app.route('/armed_conflict_pruned', methods=['POST'])
def post_armed_conflict_pruned():
    json_dict = number_of_conflict_per_country(ARMED_CONFLICT_MANAGER.armed_conflict_pruned)
    return jsonify(json_dict)


@app.route('/headlines_region', methods=['POST'])
def post_headlines_region():
    region_headlines = {}

    for conflict in ARMED_CONFLICT_MANAGER.armed_conflict_pruned:

        region = conflict.region
        number_of_headlines = conflict.number_of_sources

        if region != "" and region != 0:

            if region not in region_headlines.keys():
                region_headlines[region] = 0

            region_headlines[region] += number_of_headlines

    json_dict = region_headlines

    return jsonify(json_dict)


@app.route('/deaths_by_side', methods=['POST'])
def post_deaths_by_side():
    deaths_by_side = {'deaths_a': 0, 'deaths_b': 0, 'deaths_civilians': 0}

    for conflict in ARMED_CONFLICT_MANAGER.armed_conflict_pruned:

        deaths_by_side['deaths_a'] += conflict.deaths_a
        deaths_by_side['deaths_b'] += conflict.deaths_b
        deaths_by_side['deaths_civilians'] += conflict.deaths_civilians

    json_dict = deaths_by_side

    return jsonify(json_dict)


@app.route('/headlines_ratio_armed_conflict', methods=['POST'])
def post_headlines_ratio_armed_conflict():
    number_of_conflict_dict = number_of_conflict_per_country(ARMED_CONFLICT_MANAGER.armed_conflict_pruned)
    number_of_headlines_dict = {}
    headlines_per_conflict = {}

    for conflict in ARMED_CONFLICT_MANAGER.armed_conflict_pruned:
        country_code = conflict.country_code

        if country_code not in number_of_headlines_dict.keys():
            number_of_headlines_dict[country_code] = 0

        number_of_headlines_dict[country_code] += conflict.number_of_sources

    for conflict in ARMED_CONFLICT_MANAGER.armed_conflict_pruned:

        country_code = conflict.country_code
        number_of_conflict = number_of_conflict_dict[country_code]
        number_of_headlines = number_of_headlines_dict[country_code]

        if number_of_conflict > 1:
            headlines_per_conflict[country_code] = round((log2(number_of_headlines / number_of_conflict)), 2)
        else:
            headlines_per_conflict[country_code] = 0

    json_dict = headlines_per_conflict

    return jsonify(json_dict)


@app.route('/headlines_word_map', methods=['POST'])
def post_headlines_word_map():
    word_map = {}

    for conflict in ARMED_CONFLICT_MANAGER.armed_conflict_pruned:

        headlines = conflict.source_headline

        for headline in headlines:
            headline = simple_preprocess(headline, deacc=True)

            for word in headline:
                if word not in STOP_WORDS:
                    if word not in word_map.keys():
                        word_map[word] = 0
                    word_map[word] += 1

    json_dict = word_map

    return jsonify(json_dict)


def number_of_conflict_per_country(armed_conflicts):
    number_of_conflict = {}

    for conflict in armed_conflicts:
        country_code = conflict.country_code

        if country_code not in number_of_conflict.keys():
            number_of_conflict[country_code] = 0

        number_of_conflict[country_code] += 1

    return number_of_conflict
