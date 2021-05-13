import collections
import random

import requests
from faker import Faker
from loguru import logger

UserRecord = collections.namedtuple('UserRecord', ['id', 'auth_token', 'email'])


def get_fake_user_data():
    login = fake.ascii_safe_email()
    return {
        "login": login,
        "email": login,
        "pass": fake.password(),  # Yes, "pass" ¯\_(ツ)_/¯
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "language": random.choice(["nl", "fr", "de", "en"]),
        "gender": random.choice(["M", "F"])
    }


def create_account() -> UserRecord:
    # login must be email adress
    user_data = get_fake_user_data()

    # Create user
    response = requests.post("https://www.dncm.be/wp-json/app/v1/consumerregistration", json=user_data)
    try:
        assert response.status_code == requests.codes.created
    except AssertionError:
        if response.status_code == requests.codes.internal_server_error:
            logger.warning(f"User {user_data['email']} already exists; retrying")
            if response.json()['code'] == "existing_user_login":
                create_account()
        raise Exception(f"Something went wrong when creating new user: f{response.status_code}: f{response.json()}")

    response = requests.post("https://www.dncm.be/wp-json/jwt-auth/v1/token", json={
        "username": user_data["email"],
        "password": user_data["pass"]
    })

    new_user_data = response.json()
    logger.debug(new_user_data)
    logger.info(f"Created new user {new_user_data['user']['email']} with password {user_data['pass']}")
    return UserRecord(
        id=new_user_data['user']['id'],
        auth_token=new_user_data['token'],
        email=new_user_data['user']['email']
    )


fake = Faker(locale="nl-BE")


def generate_phone_numbers(selected_area_codes: list = None, range_start: int = 0, range_end: int = None):
    # Source: https://en.wikipedia.org/wiki/Telephone_numbers_in_Belgium

    large_city_area_codes = ["02", "03", "04", "09"]
    small_city_area_codes = ["010", "011", "012", "013", "014", "015", "016", "019", "050", "051", "052", "053", "054", "055", "056", "057", "058", "059", "060", "061", "063", "064", "065", "067", "068", "069", "071", "080", "081", "082",
                             "083", "084", "085", "086", "087", "089"]

    mobile_area_codes = ['0455', '0456', '0457', '0458', '0459', '0460', '04610', '04611', '04612', '04613', '04614', '04615', '04616', '04617', '04618', '04619', '04620', '04621', '04622', '04623', '04624', '04625', '04626', '04627',
                         '04628', '04629', '04630', '04631', '04632', '04633', '04634', '04635', '04636', '04637', '04638', '04639', '04640', '04641', '04642', '04643', '04644', '04645', '04646', '04647', '04648', '04649', '04650', '04651',
                         '04652', '04653', '04654', '04655', '04656', '04657', '04658', '04659', '04660', '04661', '04662', '04663', '04664', '04665', '04666', '04667', '04668', '04669', '04670', '04671', '04672', '04673', '04674', '04675',
                         '04676', '04677', '04678', '04679', '04680', '04681', '04682', '04683', '04684', '04685', '04686', '04687', '04688', '04689', '0469', '0470', '0471', '0472', '0473', '0474', '0475', '0476', '0477', '0478', '0479',
                         '04800', '04801', '04802', '04803', '04804', '04805', '04806', '04807', '04808', '04809', '0481', '0482', '0483', '0484', '0485', '0486', '0487', '0488', '0489', '0490', '0491', '0492', '0493', '0494', '0495',
                         '0496', '0497', '0498', '0499']

    for area_code in [ac for ac in large_city_area_codes if selected_area_codes is None or ac in selected_area_codes]:
        phone_number = range_start
        while phone_number <= (range_end or 9999999):
            yield f"{area_code[1:]}{phone_number:0>7}"
            phone_number += 1

    for area_code in [ac for ac in small_city_area_codes if selected_area_codes is None or ac in selected_area_codes]:
        phone_number = range_start
        while phone_number <= (range_end or 999999):
            yield f"{area_code[1:]}{phone_number:0>6}"
            phone_number += 1

    for area_code in [ac for ac in mobile_area_codes if selected_area_codes is None or ac in selected_area_codes]:
        phone_number = range_start
        while phone_number <= (range_end or 999999):
            yield f"{area_code[1:]}{phone_number:0>7}"
            phone_number += 1
