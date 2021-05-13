from flask import Flask

import core

app = Flask(__name__)


@app.route('/')
def main():
    return {}


@app.route('/account/new')
def create_new_user_account():
    return core.create_account()


@app.route('/numbers')
def get_list_of_phone_numbers(selected_area_code: str, range_start: int = 0, range_end: int = None):
    if selected_area_code not in core.generate_phone_numbers()

    # TODO: add limit to number of phone numbers to generate
    # something like (len(selected_area_codes) * (range_end - range_start)) < 10.000
    return [pn for pn in core.generate_phone_numbers(selected_area_codes, range_start, range_end)]
