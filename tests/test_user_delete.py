from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def setup_method(self):
        self.url_auth = "/user"
        self.url_login = "/user/login"

    def test_delete_user_with_id2(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        id = "2"
        #login and user
        auth_sid, token = self.login_and_get_token_and_cookie(login_data=login_data)

        response_del = MyRequests.delete(self.url_auth + id,
                                         cookies={'auth_sid': auth_sid},
                                         headers={'x-csrf-token': token}
                                        )

        Assertions.assert_code_status(response_del, 404)
        print(response_del.content)
