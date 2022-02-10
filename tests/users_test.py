import requests

from delete_records import delete_test_records
from tests.auth_test import TestUser, get_tester_user_authorized_for_other_test
from tests.boards_test import Board, check_or_create_test_projects
from tests.projects_test import Project
from tests.statuses_test import check_or_create_test_boards

test_user_email_local = 'automated@test.com'
test_user_name_local = 'This is autotest generated user'
test_user_password_local = '12345678'


class User:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.email = ''
        self.password = ''
        self.avatar_link = ''
        self.projects = [Project(), Project(), Project()]
        self.boards = [Board(), Board(), Board()]


def users_delete_user_test(test_user, new_user: User) -> bool:
    print('Starting deleting user test...')
    response = {}
    try:
        user_delete_info = requests.delete(f'http://173.212.214.70:3004/users/delete/{new_user.id}',
                                           headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = user_delete_info.json()
        if 'success' in response:
            if response['success'] is True:
                del new_user
                print('Test user successfully deleted.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Deleting user test FAILED. Error: {e}, {response}')
        return False


def users_update_user_test(test_user, new_user: User, new_name: str, new_password: str, new_email: str,
                           new_project_ids, new_board_ids) -> bool:
    print('Starting user update test...')
    response = {}
    try:
        user_new_info = requests.put(f'http://173.212.214.70:3004/users/update/{new_user.id}',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)},
                                     data={
                                            'name': new_name,
                                            'email': new_email,
                                            'password': new_password,
                                            'projectIds': new_project_ids,
                                            'boardIds': new_board_ids
                                          })
        response = user_new_info.json()
        if 'name' in response and 'email' in response and 'projectIds' in response \
                and 'boardIds' in response and '_id' in response:
            if response['name'] == new_name \
                    and response['email'] == new_password \
                    and response['_id'] == new_user.id \
                    and response['projectIds'] == new_project_ids \
                    and response['boardIds'] == new_board_ids:
                new_user.name = new_name
                new_user.email = new_email
                new_user.password = new_password
                for project in new_project_ids:
                    new_project = Project()
                    new_project.id = project
                    new_user.projects.append(new_project)
                for board in new_board_ids:
                    new_board = Board()
                    new_board.id = board
                    new_user.boards.append(new_board)
                print('Test user successfully updated.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Updating user test FAILED. Error: {e}, {response}')
        return False


def users_get_by_id_test(test_user: TestUser, new_user: User) -> bool:
    print('Starting user get by id test...')
    project_ids = []
    board_ids = []
    for project in new_user.projects:
        project_ids.append(project.id)
    for board in new_user.boards:
        board_ids.append(board.id)
    response = {}
    try:
        user_info = requests.get(f'http://173.212.214.70:3004/users/{new_user.id}',
                                 headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = user_info.json()
        if 'name' in response and 'email' in response and '_id' in response \
                and 'projectIds' in response and 'boardIds' in response:
            if response['name'] == new_user.name \
                    and response['email'] == new_user.email \
                    and response['_id'] == new_user.id \
                    and response['projectIds'] == project_ids \
                    and response['boardIds'] == board_ids:
                print('Test user successfully received by ID.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Getting user by id test FAILED. Error: {e}, {response}')
        return False


def users_create_user_test(test_user: TestUser, new_user: User) -> bool:
    print('Starting user create test...')
    project_ids = []
    board_ids = []
    for project in new_user.projects:
        project_ids.append(project.id)
    for board in new_user.boards:
        board_ids.append(board.id)
    response = {}
    try:
        new_user_request = requests.post('http://173.212.214.70:3004/users/create',
                                         data={'name': new_user.name,
                                               'password': new_user.password,
                                               'email': new_user.email,
                                               'projectIds': project_ids,
                                               'boardIds': board_ids
                                               },
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = new_user_request.json()
        if 'name' in response and 'email' in response and '_id' in response \
                and 'projectIds' in response and 'boardIds' in response:
            if response['name'] == new_user.name and response['email'] == new_user.email \
                    and response['projectIds'] == project_ids and response['boardIds'] == board_ids:
                new_user.id = response['_id']
                print('Test user successfully created.')
                return True
            else:
                raise 'Wrong record created.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Creating user test FAILED. Error: {e}, {response}')
        return False


def users_get_all_test(test_user: TestUser) -> (bool, int):
    print('Starting all users receiving test...')
    try:
        users_request = requests.get('http://173.212.214.70:3004/users',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        users_list = users_request.json()
        if isinstance(users_list, list):
            print(f'Users list successfully received. Found {len(users_list)} users.')
            return True, len(users_list)
        else:
            print(f'Users list was not received. Here what was: {users_list.text}')
            return False
    except Exception as e:
        print(f'Get all users test failed. ERROR: {e}')
        exit()


def run_users_test():
    print('Running users tests...')
    test_user = get_tester_user_authorized_for_other_test('dimafilin6@icloud.com', '12345678')
    projects_list, projects_fetched = check_or_create_test_projects(test_user, 3)
    boards_list, boards_fetched = check_or_create_test_boards(test_user, 3)
    new_user = User()
    new_user.name = test_user_name_local
    new_user.email = test_user_email_local
    new_user.password = test_user_password_local
    new_user.projects = [projects_list[0], projects_list[1]]
    new_user.boards = [boards_list[0], boards_list[1]]

    if users_create_user_test(test_user, new_user) is True:
        users_get_by_id_test(test_user, new_user)
        users_update_user_test(test_user, new_user, new_user.name + ' UPDATED', new_password=new_user.password+'1',
                               new_email=new_user.email+'m', new_project_ids=[projects_list[1], projects_list[2]],
                               new_board_ids=[boards_list[1], boards_list[2]])
        users_delete_user_test(test_user, new_user)


if __name__ == '__main__':
    print('Running users test directly.')
    run_users_test()
    delete_test_records()
