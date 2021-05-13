import random

import pytest
import requests
from flask import url_for
from loguru import logger

import core
from tests.conftest import fake


@pytest.fixture(autouse=True)
def mock_requests(mocker):
    requests = mocker.patch("app.requests", autospec=True)
    requests.post.return_value.json.return_value = {
        "createdAtIso": "2021-05-13T23:18:13+00:00",
        "id": 2062934,
        "name": "",
        "number": "+32 47998753",
        "user": 1362149
    }
    requests.codes.created = 201
    return requests


def test_post_number(client, mock_requests):
    mock_requests.post.return_value.status_code = requests.codes.created

    json_data = {
        'area_code': '050',
        'number': random.randint(0, 999999),
        'auth_token': fake.md5(),
        'id': fake.md5()
    }

    response = client.post(url_for("post_number_to_user_list"), json=json_data)

    assert response.status_code == 201  # created
    # endpoint returns data from dncm
    assert response.json == mock_requests.post.return_value.json.return_value

    assert mock_requests.post.call_args[1]['headers'] == {'Authorization': f"Bearer {json_data['auth_token']}"}
    assert 'name' in mock_requests.post.call_args[1]['json']
    assert mock_requests.post.call_args[1]['json']['number'] == f"+32{json_data['area_code'][1:]}{json_data['number']:0>6}"
    assert mock_requests.post.call_args[1]['json']['user'] == json_data['id']


def test_post_small_city_number(client, mock_requests):
    json_data = {
        'area_code': random.choice(core.SMALL_CITY_AREA_CODES),
        'number': random.randint(0, 999999),
        'auth_token': fake.md5(),
        'id': fake.md5()
    }

    response = client.post(url_for("post_number_to_user_list"), json=json_data)
    assert mock_requests.post.call_args[1]['json']['number'] == f"+32{json_data['area_code'][1:]}{json_data['number']:0>6}"


def test_post_large_city_number(client, mock_requests):
    json_data = {
        'area_code': random.choice(core.LARGE_CITY_AREA_CODES),
        'number': random.randint(0, 999999),
        'auth_token': fake.md5(),
        'id': fake.md5()
    }

    response = client.post(url_for("post_number_to_user_list"), json=json_data)
    assert mock_requests.post.call_args[1]['json']['number'] == f"+32{json_data['area_code'][1:]}{json_data['number']:0>7}"

def test_post_mobile_number(client, mock_requests):
    json_data = {
        'area_code': random.choice(core.MOBILE_AREA_CODES),
        'number': random.randint(0, 999999),
        'auth_token': fake.md5(),
        'id': fake.md5()
    }

    response = client.post(url_for("post_number_to_user_list"), json=json_data)
    assert mock_requests.post.call_args[1]['json']['number'] == f"+32{json_data['area_code'][1:]}{json_data['number']:0>6}"


def test_number_padding_for_6_digits(client, mock_requests):
    json_data = {
        'area_code': random.choice(core.MOBILE_AREA_CODES + core.SMALL_CITY_AREA_CODES),
        'number': 0,
        'auth_token': fake.md5(),
        'id': fake.md5()
    }

    response = client.post(url_for("post_number_to_user_list"), json=json_data)
    assert mock_requests.post.call_args[1]['json']['number'] == f"+32{json_data['area_code'][1:]}000000"

def test_number_padding_for_7_digits(client, mock_requests):
    json_data = {
        'area_code': random.choice(core.LARGE_CITY_AREA_CODES),
        'number': 0,
        'auth_token': fake.md5(),
        'id': fake.md5()
    }

    response = client.post(url_for("post_number_to_user_list"), json=json_data)
    assert mock_requests.post.call_args[1]['json']['number'] == f"+32{json_data['area_code'][1:]}0000000"
