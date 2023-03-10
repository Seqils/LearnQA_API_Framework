import json
from datetime import datetime
import random
import string
from requests import Response

from lib.assertions import Assertions
from lib.my_requests import MyRequests


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot file cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_headers(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot file cookie with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email,
        }

    def delete_field_in_data(self, data: dict, key: str):
        if key in data:
            del data[key]
        else:
            raise Exception(f"No such key [{key}] in data!")

        return data

    def generate_string(self, length: int):
        gen_string = ''.join(random.choices(string.ascii_lowercase, k=length))
        return gen_string

    def create_new_user_and_get_user_id(self):
        data = self.prepare_registration_data()
        response = MyRequests.post('/user', data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')
        user_id = self.get_json_value(response, 'id')
        return data, user_id

    def login_and_get_token_and_cookie(self, login_data: dict):
        response = MyRequests.post('/user/login', data=login_data)
        Assertions.assert_code_status(response, 200)
        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_headers(response, 'x-csrf-token')
        return auth_sid, token
