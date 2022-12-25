import allure
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests

@allure.epic('User registration cases')
class TestUserRegister(BaseCase):

    exclude_data = {
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    }

    def setup_method(self):
        self.url = "/user/"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description('Test if user can register successfully')
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_json_has_key(response, "id")
        Assertions.assert_code_status(response, 200)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description('Test if user can register with existing mail')
    def test_create_user_with_exc_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected content [{response.content}]"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description('Test if user can create user with wrong mail')
    def test_create_user_with_wrong_email(self):
        email = 'nikita.donkov.fancymail.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)

    @allure.severity(allure.severity_level.MINOR)
    @allure.description('Tests if user can register with no fields')
    @pytest.mark.parametrize('condition', exclude_data)
    def test_create_user_with_no_field(self, condition):
        data = self.prepare_registration_data()
        self.delete_field_in_data(data, condition)

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected content [{response.content}]"

    @allure.severity(allure.severity_level.MINOR)
    @allure.description('Test if user can register with 1 char username')
    def test_create_user_with_onechar_username(self):
        data = self.prepare_registration_data()
        data['username'] = 'q'

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"The value of 'username' field is too short")

    @allure.severity(allure.severity_level.MINOR)
    @allure.description('Test if user can register with too long username')
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data['username'] = self.generate_string(255)

        response = MyRequests.post(self.url, data=data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_content(response, f"The value of 'username' field is too long")
