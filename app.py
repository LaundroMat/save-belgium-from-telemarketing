from flask import Flask

import core

app = Flask(__name__)


@app.route('/')
def create_new_user_account():
    return {}


@app.route('/account/new')
def create_new_user_account():
    return core.create_account()


@app.route('/numbers')
def get_list_of_phone_numbers(selected_area_codes: list = None, range_start: int = 0, range_end: int = None):
    return [pn for pn in core.generate_phone_numbers(selected_area_codes, range_start, range_end)]
