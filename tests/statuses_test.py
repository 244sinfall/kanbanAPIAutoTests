import requests

from tests.auth_test import TestUser, get_tester_user_authorized_for_other_test
from tests.boards_test import Board, boards_get_all_test, boards_delete_board_test, boards_create_board_test
from tests.projects_test import Project, projects_create_project_test, projects_get_all_test, \
    projects_delete_project_test

test_status_name_local = 'This is autotest generated status'
test_project = Project()


class Status:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.boards = [Board()]


def statuses_delete_status_test(test_user, test_status: Status) -> bool:
    print('Starting deleting status test...')
    response = {}
    try:
        status_delete_info = requests.delete(f'http://173.212.214.70:3004/boards/delete/{test_status.id}',
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = status_delete_info.json()
        if 'success' in response:
            if response['success'] is True:
                del test_status
                print('Test status successfully deleted.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Deleting status test FAILED. Error: {e}, {response}')
        return False


def statuses_update_status_test(test_user, test_status, new_name: str, new_boards: [Board]) -> bool:
    print('Starting status update test...')
    response = {}
    try:
        ids_list = []
        for boards in test_status.boards:
            ids_list.append(boards.id)
        status_new_info = requests.put(f'http://173.212.214.70:3004/statuses/update/{test_status.id}',
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)},
                                        data={
                                            'name': new_name,
                                            'boardIds': ids_list
                                        })
        response = status_new_info.json()
        if 'name' in response and 'boardIds' in response and '_id' in response:
            if response['name'] == new_name \
                    and response['boardIds'] == ids_list \
                    and response['_id'] == test_status.id:
                test_status.name = response['name']
                test_status.boards = new_boards
                print('Test status successfully updated.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Updating status test FAILED. Error: {e}, {response}')
        return False


def statuses_get_by_id_test(test_user: TestUser, test_status: Status) -> bool:
    print('Starting status get by id test...')
    response = {}
    try:
        ids_list = []
        for boards in test_status.boards:
            ids_list.append(boards.id)
        status_info = requests.get(f'http://173.212.214.70:3004/statuses/{test_status.id}',
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = status_info.json()
        if 'name' in response and 'boardIds' in response and '_id' in response:
            if response['name'] == test_status.name \
                    and response['boardIds'] == ids_list \
                    and response['_id'] == test_status.id:
                print('Test status successfully receieved by ID.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Getting status by id test FAILED. Error: {e}, {response}')
        return False


def statuses_create_status_test(test_user: TestUser, test_status: Status) -> bool:
    print('Starting status create test...')
    response = {}
    try:
        ids_list = []
        for boards in test_status.boards:
            ids_list.append(boards.id)
        new_status_request = requests.post('http://173.212.214.70:3004/statuses/create',
                                         data={'name': test_status.name,
                                                'boardIds': ids_list,
                                                },
                                            headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = new_status_request.json()
        if 'name' in response and 'boardIds' in response and '_id' in response:
            if response['name'] == test_status.name and response['boardIds'] == ids_list:
                test_status.id = response['_id']
                print('Test statuses successfully created.')
                return True
            else:
                raise 'Wrong record created.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Creating status test FAILED. Error: {e}, {response}')
        return False


def statuses_get_all_test(test_user: TestUser) -> (bool, int):
    print('Starting all statuses receiving test...')
    try:
        statuses_request = requests.get('http://173.212.214.70:3004/statuses',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        statuses_list = statuses_request.json()
        if isinstance(statuses_list, list):
            print(f'Statuses list successfully received. Found {len(statuses_list)} statuses.')
            return True, len(statuses_list)
        else:
            print(f'Statuses list was not received. Here what was: {statuses_list.text}')
            return False
    except Exception as e:
        print(f'Get all statuses test failed. ERROR: {e}')
        exit()


def check_or_create_test_boards(test_user: TestUser) -> ([Board], bool):
    test_boards = []
    is_all_boards_got, items = boards_get_all_test(test_user)
    if items < 3:
        print('You need at least 3 boards to test statuses. We are going to create them')
        print('Creating project for the future test. If anything will go wrong - run project test.')
        test_project.name = 'This is statuses autotest generated project.'
        test_project.description = 'It should be removed asap, if not, contact: dimafilin6@icloud.com'
        projects_create_project_test(test_user, test_project)
        for times in range(3):
            new_board = Board()
            new_board.name = f'This is autotest generated project #{times}'
            new_board.project = test_project
            boards_create_board_test(test_user, new_board)
            test_boards.append(new_board)
        return test_boards, False
    else:
        response = {}
        try:
            print('Fetching three existing boards. If anything will go wrong - run boards test.')
            boards_get = requests.get('http://173.212.214.70:3004/boards',
                                        headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
            response = boards_get.json()
            for times in range(3):
                new_board = Board()
                new_board.id = response[times]['_id']
                new_board.name = response[times]['name']
                new_board.project = Project()
                new_board.project.id = response[times]['projectId']
                print(f'{times + 1}: {new_board.id}')
                test_boards.append(new_board)
            return test_boards, True
        except BaseException as e:
            print(f'ERROR while fetching boards. Error: {e}, Response: {response}')
            exit()


def run_statuses_test():
    print('Running statuses tests...')
    test_user = get_tester_user_authorized_for_other_test('dimafilin6@icloud.com', '12345678')
    is_all_statuses_got, items = statuses_get_all_test(test_user)
    if is_all_statuses_got is True:
        test_status = Status()
        test_status.name = test_status_name_local
        test_boards, found = check_or_create_test_boards(test_user)
        test_status.boards = [test_boards[0], test_boards[1]]
        if statuses_create_status_test(test_user, test_status) is True:
            statuses_get_by_id_test(test_user, test_status)
            statuses_update_status_test(test_user, test_status, new_name=test_status_name_local+' UPDATED',
                                        new_boards=[test_boards[1], test_boards[2]])
            statuses_delete_status_test(test_user, test_status)
        if found is False:
            for board in test_boards:
                boards_delete_board_test(test_user, board)
        if test_project.id != '':
            projects_delete_project_test(test_user, test_project)


if __name__ == '__main__':
    print('Running statuses test directly.')
    run_statuses_test()