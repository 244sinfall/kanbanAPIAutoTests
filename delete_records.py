import requests

from tests import auth_test


def delete_test_records():
    try:
        # Getting test user
        test_user = auth_test.get_tester_user_authorized_for_other_test('dimafilin6@icloud.com', '12345678')
        print('Log in with tester account success.')
        # Getting users
        categories = ('users', 'projects', 'boards', 'statuses', 'tasks')
        for category in categories:
            request = requests.get(f'http://173.212.214.70:3004/{category}',
                                   headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
            result_list = request.json()
            any_match_deleted = 0
            for match in result_list:
                if 'autotest' in match['name']:
                    requests.delete(f'http://173.212.214.70:3004/{category}/delete/{match["_id"]}',
                                    headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
                    any_match_deleted += 1
            if any_match_deleted == 0:
                print(f'No {category} found to clean.')
            else:
                print(f'Deleted {any_match_deleted} test records from "{category}" list')
    except Exception as e:
        print(f'Clean is not completed! Error: {e}')
