import requests
import time

tester_user_email_local = 'dimafilin6@icloud.com'
tester_user_password_local = '12345678'


class TestUser:
    def __init__(self):
        self.email = 'new_test_user_dont_delete@test.com'
        self.name = 'if you see this, contact dmitry filin'
        self.password = '12345678'
        self.refreshToken = ''
        self.accessToken = ''


def get_tester_user_authorized_for_other_test(tester_user_email: str, tester_user_password: str) -> TestUser:
    print('Authorizing testing user...')
    out_test_user = TestUser()
    out_test_user.email = tester_user_email
    out_test_user.password = tester_user_password
    try:
        login_request = requests.post('http://173.212.214.70:3004/auth/login', data={'email': out_test_user.email,
                                                                                     'password': out_test_user.password})
        response: dict = login_request.json()
        if 'token' in response.keys() and 'refreshToken' in response.keys():
            out_test_user.accessToken = response['token']
            out_test_user.refreshToken = response['refreshToken']
            print('Access & refresh token received successfully')
            return out_test_user
        else:
            print('Something went wrong. Run auth test.')
    except Exception as e:
        print(f'Getting test user authorized FAILED. Error: {e}. Run Auth test.')
        exit()


def auth_log_out_test(test_user: TestUser) -> bool:
    print('Log out test...')
    try:
        # Getting users using test user token
        users_request = requests.get('http://173.212.214.70:3004/users',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        users_list = users_request.json()
        print('Log in instance checked.')
        # Logout
        logout_request = requests.post('http://173.212.214.70:3004/auth/logout', headers= {
            'Authorization': 'Bearer {}'.format(test_user.accessToken) })
        logout_response = logout_request.json()
        if 'success' in logout_response:
            if logout_response['success'] is True:
                print('Log out successfully completed. Checking instance again...')
                # Checking
                users_request = requests.get('http://173.212.214.70:3004/users',
                                             headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
                users_list = users_request.json()
                if isinstance(users_list, list):
                    print('Log out failed. Response received.')
                    return False
                else:
                    print(f'Log out completed! Token burnt out: {users_request.text}')
                    return True
            else:
                raise ValueError
        else:
            raise ValueError
    except Exception as e:
        print(f'Error on logging out test. Error: {e}')
        return False


def auth_refresh_test(test_user: TestUser) -> bool:
    print('Refresh token test... 15 seconds delay started.')
    time.sleep(15)
    try:
        if test_user.refreshToken != '':
            refresh_request = requests.post('http://173.212.214.70:3004/auth/refresh',
                                            data={'refreshToken': test_user.refreshToken})
            refresh_response: dict = refresh_request.json()
            if 'token' in refresh_response.keys() and 'refreshToken' in refresh_response.keys():
                if refresh_response['refreshToken'] == test_user.refreshToken:
                    print('ERROR. Refresh token has remained same!.')
                else:
                    print('Refresh token has changed.')
                if refresh_response['token'] != test_user.accessToken:
                    print('New access token generated successfully.')
                    test_user.accessToken = refresh_response['token']
                    return True
                else:
                    print(f'Refresh token test FAILED! Old token: {test_user.accessToken},'
                          f' New token: {refresh_response["token"]}')
                    return False
    except Exception as e:
        print(f'Refresh token test FAILED. Error: {e}')


def emergency_test_user_delete(test_user: TestUser):
    print('Deleting created test user...')
    try:
        # Getting token
        login_request = requests.post('http://173.212.214.70:3004/auth/login', data={'email': tester_user_email_local,
                                                                                     'password': tester_user_password_local})
        login_response = login_request.json()
        token = login_response['token']
        print('Log in with tester account success.')
        # Getting users
        users_request = requests.get('http://173.212.214.70:3004/users',
                                     headers={'Authorization': 'Bearer {}'.format(token)})
        users_list = users_request.json()
        print('Users list request success.')
        # Search for created user ID
        temp_user_id = ''
        for user in users_list:
            if user['email'] == test_user.email:
                temp_user_id = user['_id']
                print('Test created user found.')
        if temp_user_id == '':
            print('Test user was not found! Make sure it exist, or nothing had broken...')
            return
        # Deleting user
        delete_request = requests.delete(f'http://173.212.214.70:3004/users/delete/{temp_user_id}', headers= {
            'Authorization': 'Bearer {}'.format(token)
        })
        delete_response = delete_request.json()
        if delete_response['success'] is True:
            print('Test user deleted. Test is completed.')
        else:
            print('Found user might not be deleted! Make sure it does not exist.')
    except Exception as e:
        print(f'Test user most likely was not deleted! Error: {e}')


def auth_log_in_test(test_user: TestUser) -> bool:
    print('Starting sign in test...')
    try:
        login_request = requests.post('http://173.212.214.70:3004/auth/login', data={'email': test_user.email,
                                                                                     'password': test_user.password})
        response: dict = login_request.json()
        if 'token' in response.keys() and 'refreshToken' in response.keys():
            test_user.accessToken = response['token']
            test_user.refreshToken = response['refreshToken']
            print('Log in test passed.')
            return True
        else:
            print(f'Log in test FAILED. Response: {response}')
            emergency_test_user_delete()
            return False
    except Exception as e:
        print(f'Log in test FAILED. Error: {e}')
        emergency_test_user_delete()
        return False


def auth_sign_up_test(test_user: TestUser) -> bool:
    print('Starting sign up test...')
    response = {}
    try:
        register_request = requests.post('http://173.212.214.70:3004/auth/signup',
                                         data={'email': test_user.email,
                                                'name': test_user.name,
                                                'password': test_user.password})
        response = register_request.json()
        if response['success'] is True:
            print('Sign up test passed.')
            return True
        else:
            print(f'Sign up test FAILED. Response: {response}')
            return False
    except Exception as e:
        print(f'Sign up test FAILED. Error: {e}, {response}')
        if 'exist' in response['error']:
            print('Seems like user was not deleted after last test. Deleting it...')
            emergency_test_user_delete(test_user)
            run_auth_tests()


def run_auth_tests():
    print('Running auth tests...')
    test_user = TestUser()
    if auth_sign_up_test(test_user) is True:
        if auth_log_in_test(test_user) is True:
            auth_refresh_test(test_user)
            auth_log_out_test(test_user)
            emergency_test_user_delete(test_user)
    # auth_refresh_test()
    # auth_log_out_test()


if __name__ == '__main__':
    run_auth_tests()