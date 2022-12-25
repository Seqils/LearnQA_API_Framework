from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def setup_method(self):
        self.url_auth = "/user/"
        self.url_login = "/user/login"

    def test_edit_just_created_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(self.url_auth, data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
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

        response3 = MyRequests.put(self.url_auth + str(user_id),
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   data={'firstName': new_name}
                                   )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(self.url_auth + str(user_id),
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   )

        Assertions.assert_json_value_by_name(response4, 'firstName', new_name, "Wrong first name after edit")

    def test_not_auth_user_data_change(self):
        #REG new
        data = self.prepare_registration_data()
        response = MyRequests.post(self.url_auth, data=data)
        user_id = self.get_json_value(response, "id")

        #Trying to put as not auth
        response2 = MyRequests.put(self.url_auth + str(user_id))
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_content(response2, "Auth token not supplied")

    def test_auth_user_can_change_data(self):
        changing_data = {
            'firstName': 'Guido',
            'lastName': "van Rossum"
        }
        #REG new
        data = self.prepare_registration_data()
        response = MyRequests.post(self.url_auth, data=data)
        user_id = self.get_json_value(response, "id")
        email = data['email']
        password = data['password']
        login_data = {
            'email': email,
            'password': password
        }

        #Login ang get auth_sid and token
        response_log = MyRequests.post(self.url_login, data=login_data)
        Assertions.assert_code_status(response_log, 200)
        auth_sid = self.get_cookie(response_log, "auth_sid")
        token = self.get_headers(response_log, "x-csrf-token")

        #Trying to put as not auth
        response_edit = MyRequests.put(self.url_auth + str(user_id),
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       data=changing_data
                                       )
        Assertions.assert_code_status(response_edit, 200)

        # #check data
        # response_check = MyRequests.get(self.url_auth + str(user_id),
        #                                 headers={'x-csrf-token': token},
        #                                 cookies={'auth_sid': auth_sid},
        #                                 )
        #
        # Assertions.assert_json_value_by_name(
        #     response_check,
        #     'firstName',
        #     changing_data['firstName'],
        #     f"firstName wasn't edited"
        # )
        #
        # Assertions.assert_json_value_by_name(
        #     response_check,
        #     'lastName',
        #     changing_data['lastName'],
        #     f"lastName wasn't edited"
        # )

    def test_auth_user_change_wrong_email(self):
        changing_data = {
            'email': 'wrongemail.lol.com',
        }
        # REG new
        data, user_id = self.create_new_user_and_get_user_id()
        email = data['email']
        password = data['password']
        login_data = {
            'email': email,
            'password': password
        }

        # Login ang get auth_sid and token
        auth_sid, token = self.login_and_get_token_and_cookie(login_data=login_data)

        # Trying to put as not auth
        response_edit = MyRequests.put(self.url_auth + str(user_id),
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       data=changing_data
                                       )
        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_content(response_edit, "Invalid email format")

    def test_auth_user_change_invalid_firstname(self):
        changing_data = {
            'firstName': 'q',
        }
        # REG new
        data, user_id = self.create_new_user_and_get_user_id()
        email = data['email']
        password = data['password']
        login_data = {
            'email': email,
            'password': password
        }

        # Login ang get auth_sid and token
        auth_sid, token = self.login_and_get_token_and_cookie(login_data=login_data)

        # Trying to put as not auth
        response_edit = MyRequests.put(self.url_auth + str(user_id),
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       data=changing_data
                                       )
        Assertions.assert_code_status(response_edit, 400)
        Assertions.assert_json_value_by_name(response_edit,
                                             'error',
                                             'Too short value for field firstName',
                                             'Something went wrong, perhaps firstName was changed'
                                             )
