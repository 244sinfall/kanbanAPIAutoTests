import requests

from delete_records import delete_test_records
from tests.auth_test import TestUser, get_tester_user_authorized_for_other_test
from tests.projects_test import Project, projects_create_project_test, projects_get_all_test

test_board_name_local = 'This is autotest generated board'


class Board:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.project = Project()


def boards_delete_board_test(test_user, test_board) -> bool:
    print('Starting deleting board test...')
    response = {}
    try:
        board_delete_info = requests.delete(f'http://173.212.214.70:3004/boards/delete/{test_board.id}',
                                            headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = board_delete_info.json()
        if 'success' in response:
            if response['success'] is True:
                del test_board
                print('Test board successfully deleted.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Deleting project test FAILED. Error: {e}, {response}')
        return False


def boards_update_board_test(test_user, test_board, new_name: str, new_project: Project) -> bool:
    print('Starting board update test...')
    response = {}
    try:
        board_new_info = requests.put(f'http://173.212.214.70:3004/boards/update/{test_board.id}',
                                      headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)},
                                      data={
                                          'name': new_name,
                                          'projectId': new_project.id
                                      })
        response = board_new_info.json()
        if 'name' in response and 'projectId' in response and '_id' in response:
            if response['name'] == new_name \
                    and response['projectId'] == new_project.id \
                    and response['_id'] == test_board.id:
                test_board.name = response['name']
                test_board.project = new_project
                print('Test board successfully updated.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Updating board test FAILED. Error: {e}, {response}')
        return False


def boards_get_by_id_test(test_user: TestUser, test_board: Board) -> bool:
    print('Starting board get by id test...')
    response = {}
    try:
        board_info = requests.get(f'http://173.212.214.70:3004/boards/{test_board.id}',
                                  headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = board_info.json()
        if 'name' in response and 'projectId' in response and '_id' in response:
            if response['name'] == test_board.name \
                    and response['projectId'] == test_board.project.id \
                    and response['_id'] == test_board.id:
                print('Test board successfully received by ID.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Getting project by id test FAILED. Error: {e}, {response}')
        return False


def boards_create_board_test(test_user: TestUser, test_board: Board) -> bool:
    print('Starting board create test...')
    response = {}
    try:
        new_board_request = requests.post('http://173.212.214.70:3004/boards/create',
                                          data={'name': test_board.name,
                                                'projectId': test_board.project.id,
                                                },
                                          headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = new_board_request.json()
        if 'name' in response and 'projectId' in response and '_id' in response:
            if response['name'] == test_board.name and response['projectId'] == test_board.project.id:
                test_board.id = response['_id']
                print('Test board successfully created.')
                return True
            else:
                raise 'Wrong record created.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Creating project test FAILED. Error: {e}, {response}')
        return False


def boards_get_all_test(test_user: TestUser) -> (bool, int):
    print('Starting all boards receiving test...')
    try:
        boards_request = requests.get('http://173.212.214.70:3004/boards',
                                      headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        boards_list = boards_request.json()
        if isinstance(boards_list, list):
            print(f'Boards list successfully received. Found {len(boards_list)} boards.')
            return True, len(boards_list)
        else:
            print(f'Board list was not received. Here what was: {boards_list.text}')
            return False
    except Exception as e:
        print(f'Get all boards test failed. ERROR: {e}')
        exit()


def check_or_create_test_projects(test_user: TestUser, needed: int) -> ([Project], bool):
    test_projects = []
    is_all_project_got, items = projects_get_all_test(test_user)
    if items < needed:
        print(f'You need at least {needed} projects for test. We are going to create them')
        for times in range(needed):
            new_project = Project()
            new_project.name = f'This is autotest generated project #{times}'
            new_project.description = 'If you see this, please report dimafilin6@icloud.com'
            projects_create_project_test(test_user, new_project)
            test_projects.append(new_project)
        return test_projects, False
    else:
        response = {}
        try:
            print('Fetching two existing projects. If anything will go wrong - run projects test.')
            projects_get = requests.get('http://173.212.214.70:3004/projects',
                                        headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
            response = projects_get.json()
            for times in range(needed):
                new_project = Project()
                new_project.id = response[times]['_id']
                new_project.name = response[times]['name']
                new_project.description = response[times]['description']
                print(f'{times + 1}: {new_project.id}')
                test_projects.append(new_project)
            return test_projects, True
        except BaseException as e:
            print(f'ERROR while fetching projects. Error: {e}, Response: {response}')
            exit()


def run_boards_test():
    print('Running board tests...')
    test_user = get_tester_user_authorized_for_other_test('dimafilin6@icloud.com', '12345678')
    is_all_boards_got, items = boards_get_all_test(test_user)
    if is_all_boards_got is True:
        test_board = Board()
        test_board.name = test_board_name_local
        test_projects, found = check_or_create_test_projects(test_user, 2)
        test_board.project = test_projects[0]
        if boards_create_board_test(test_user, test_board) is True:
            boards_get_by_id_test(test_user, test_board)
            boards_update_board_test(test_user, test_board, new_name=test_board_name_local + ' UPDATED',
                                     new_project=test_projects[1])
            boards_delete_board_test(test_user, test_board)


if __name__ == '__main__':
    print('Running boards test directly.')
    run_boards_test()
    delete_test_records()
