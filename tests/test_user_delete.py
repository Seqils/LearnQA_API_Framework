import time
import allure
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic('User delete cases')
class TestUserDelete(BaseCase):
    def setup_method(self):
        self.url_auth = "/user"
        self.url_auth_id2 = "/user/2"
        self.url_login = "/user/login"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description('Test if user with id = 2 can delete himself')
    def test_delete_user_with_id2(self):
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        #login and user
        auth_sid, token = self.login_and_get_token_and_cookie(login_data=login_data)
        #delete data
        response_del = MyRequests.delete(self.url_auth_id2,
                                         cookies={'auth_sid': auth_sid},
                                         headers={'x-csrf-token': token},
                                         data={'id': '2'}
                                         )

        Assertions.assert_code_status(response_del, 400)
        Assertions.assert_content(response_del,
                                  'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description('Test if authorized user can delete himself')
    def test_auth_user_can_delete_himself(self):
        #reg
        data, user_id = self.create_new_user_and_get_user_id()
        email = data['email']
        password = data['password']
        login_data = {
            'email': email,
            'password': password
        }
        #login
        auth_sid, token = self.login_and_get_token_and_cookie(login_data=login_data)

        #delete data
        response_del = MyRequests.delete(self.url_auth + '/' + str(user_id),
                                         cookies={'auth_sid': auth_sid},
                                         headers={'x-csrf-token': token},
                                         data={'id': user_id}
                                         )

        Assertions.assert_code_status(response_del, 200)

        #check user by id
        response_del2 = MyRequests.get(self.url_auth + '/' + str(user_id),
                                       cookies={'auth_sid': auth_sid},
                                       headers={'x-csrf-token': token},
                                       )

        Assertions.assert_code_status(response_del2, 404)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description('Test if authorized user cant delete another user data')
    @pytest.mark.xfail
    def test_auth_user_cant_delete_another(self):
        # reg 1st user
        data, user_id = self.create_new_user_and_get_user_id()
        email = data['email']
        password = data['password']
        login_data = {
            'email': email,
            'password': password
        }
        time.sleep(1)
        # reg 2nd user
        data_sec, user_id_sec = self.create_new_user_and_get_user_id()

        # login as 1st
        auth_sid, token = self.login_and_get_token_and_cookie(login_data=login_data)

        #try to delete another user
        response_del = MyRequests.delete(self.url_auth + '/' + str(user_id_sec),
                                         cookies={'auth_sid': auth_sid},
                                         headers={'x-csrf-token': token},
                                         )

        Assertions.assert_code_status(response_del, 400)

        #check if user exist
        response_check = MyRequests.get(self.url_auth + '/' + str(user_id_sec),
                                        cookies={'auth_sid': auth_sid},
                                        headers={'x-csrf-token': token},
                                        )

        Assertions.assert_code_status(response_del, 400)


