from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def setup_method(self):
        self.url_reg = "/user/"
        self.url_login = "/user/login"

    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(self.url_reg, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post(self.url_login, data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_headers(response2, 'x-csrf-token')

        # EDIT
        new_name = "Changed name"

        response3 = MyRequests.put(self.url_reg + str(user_id),
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(self.url_reg + str(user_id),
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   )

        Assertions.assert_json_value_by_name(response4, 'firstName', new_name, "Wrong first name after edit")
