from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):
    def setup_method(self):
        self.id = 2
        self.url_not_auth = f"/user/{self.id}"
        self.url_login = "/user/login/"
        self.url_auth = "/user/"

    def test_get_user_details_not_auth(self):
        response = MyRequests.get(self.url_not_auth)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post(self.url_login, data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")
        response2 = MyRequests.get(self.url_auth + str(user_id_from_auth),
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response2, expected_fields)
