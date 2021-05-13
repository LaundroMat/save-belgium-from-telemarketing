import requests
from flask import Flask, request

import core

app = Flask(__name__)


@app.route('/')
def main():
    return {}


@app.route('/account/new')
def create_new_user_account():
    return core.create_account()._asdict()


@app.route('/numbers/generate')
def get_list_of_phone_numbers(range_start: int = 0, range_end: int = None):
    MAX_BLOCK_SIZE = 10000
    try:
        selected_area_code = request.args['area_code']
        assert selected_area_code in core.SMALL_CITY_AREA_CODES + core.LARGE_CITY_AREA_CODES + core.MOBILE_AREA_CODES
    except (KeyError, AssertionError):
        return {'error': 'Please set a valid area code.'}
    range_start = int(request.args.get('range_start', 0))
    range_end = int(request.args.get('range_end', 0))

    # TODO: add limit to number of phone numbers to generate
    try:
        if selected_area_code in core.LARGE_CITY_AREA_CODES + core.MOBILE_AREA_CODES:
            if range_end > 0:
                assert (range_end - range_start) < MAX_BLOCK_SIZE
            else:
                range_end = min(range_start + MAX_BLOCK_SIZE, 9999999)

        if selected_area_code in core.SMALL_CITY_AREA_CODES:
            if range_end > 0:
                assert (range_end - range_start) < MAX_BLOCK_SIZE
            else:
                range_end = min(range_start + MAX_BLOCK_SIZE, 999999)
    except AssertionError:
        return {'error': f'Range is too broad, max block size is {MAX_BLOCK_SIZE} numbers.'}

    # something like (len(selected_area_codes) * (range_end - range_start)) < 10.000
    return {'numbers': [pn for pn in core.generate_phone_numbers([selected_area_code], range_start, range_end if range_end > 0 else None)]}


@app.route('/number/add-to-list', methods=['POST', 'GET'])
def post_number_to_user_list():
    if request.method == 'GET':
        return {"message": "POST number:+32(x)xx(x)xxxxxx, auth_token:str and id:int (the user's id) to add a number to the do not call list."}

    post_data = request.get_json(force=True)  # Skip request content type "application/json" requirement

    try:
        data = {
            "name": f"{core.fake.first_name()} {core.fake.last_name()}",
            "number": post_data['phone_number'],
            "user": post_data['id']
        }
    except KeyError:
        return {"error": "POST data must contain phone_number, auth_token:str and id:int (the user's id) to add a number to the do not call list."}

    try:
        response = requests.post(
            "https://www.dncm.be/wp-json/app/v1/number",
            headers={
                "Authorization": f"Bearer {post_data['auth_token']}"
            },
            json=data
        )
    except KeyError:
        return {"error": "POST data must contain phone_number, auth_token:str and id:int (the user's id) to add a number to the do not call list."}

    try:
        assert response.status_code == requests.codes.created
    except AssertionError:
        return {'error': response.json()}

    return response.json()