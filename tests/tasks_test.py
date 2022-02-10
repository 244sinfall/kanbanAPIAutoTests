import requests

from delete_records import delete_test_records
from tests.auth_test import TestUser, get_tester_user_authorized_for_other_test

from tests.projects_test import Project
from tests.statuses_test import check_or_create_test_boards, Status, statuses_create_status_test, statuses_get_all_test
from tests.users_test import User, users_get_all_test, users_create_user_test

test_status_name_local = 'This is autotest generated status'
test_project = Project()


class Task:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.description = ''
        self.assignedTo = ''
        self.boardID = ''
        self.statusID = ''


def tasks_delete_task_test(test_user, test_task: Task) -> bool:
    print('Starting deleting task test...')
    response = {}
    try:
        task_delete_info = requests.delete(f'http://173.212.214.70:3004/tasks/delete/{test_task.id}',
                                           headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = task_delete_info.json()
        if 'success' in response:
            if response['success'] is True:
                del test_task
                print('Test task successfully deleted.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Deleting task test FAILED. Error: {e}, {response}')
        return False


def tasks_update_task_test(test_user: TestUser, test_task: Task, new_name, new_description,
                           new_board_id, new_status_id, new_assigned_to) -> bool:
    print('Starting task update test...')
    response = {}
    try:
        task_new_info = requests.put(f'http://173.212.214.70:3004/tasks/update/{test_task.id}',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)},
                                     data={
                                         'name': new_name,
                                         'description': new_description,
                                         'boardId': new_board_id,
                                         'statusId': new_status_id,
                                         'assignedTo': new_assigned_to
                                     })
        response = task_new_info.json()
        if 'name' in response and 'description' and 'assignedTo' in response and 'boardId' in response \
                and 'statusId' in response and '_id' in response:
            if response['name'] == new_name \
                    and response['description'] == new_description \
                    and response['assignedTo'] == new_assigned_to \
                    and response['boardId'] == new_board_id \
                    and response['statusId'] == new_status_id:
                test_task.name = response['name']
                test_task.description = response['description']
                test_task.assignedTo = response['assignedTo']
                test_task.boardID = response['boardId']
                test_task.statusID = response['statusId']
                print('Test task successfully updated.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Updating status test FAILED. Error: {e}, {response}')
        return False


def tasks_get_by_id_test(test_user: TestUser, test_task: Task) -> bool:
    print('Starting task get by id test...')
    response = {}
    try:
        task_info = requests.get(f'http://173.212.214.70:3004/tasks/{test_task.id}',
                                 headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = task_info.json()
        if 'name' in response and 'description' and 'assignedTo' in response and 'boardId' in response \
                and 'statusId' in response and '_id' in response:
            if response['name'] == test_task.name \
                    and response['description'] == test_task.description \
                    and response['assignedTo'] == test_task.assignedTo \
                    and response['boardId'] == test_task.boardID \
                    and response['statusId'] == test_task.statusID:
                print('Test task successfully received by ID.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Getting task by id test FAILED. Error: {e}, {response}')
        return False


def tasks_create_task_test(test_user: TestUser, test_task: Task) -> bool:
    print('Starting task create test...')
    response = {}
    try:
        new_task_request = requests.post('http://173.212.214.70:3004/tasks/create',
                                         data={'name': test_task.name,
                                               'description': test_task.description,
                                               'assignedTo': test_task.assignedTo,
                                               'boardId': test_task.boardID,
                                               'statusId': test_task.statusID,
                                               },
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = new_task_request.json()
        if 'name' in response and 'description' and 'assignedTo' in response and 'boardId' in response \
                and 'statusId' in response and '_id' in response:
            if response['name'] == test_task.name \
                    and response['description'] == test_task.description \
                    and response['assignedTo'] == test_task.assignedTo \
                    and response['boardId'] == test_task.boardID \
                    and response['statusId'] == test_task.statusID:
                test_task.id = response['_id']
                print('Test task successfully created.')
                return True
            else:
                raise 'Wrong record created.'
        else:
            raise 'Wrong response format'
    except BaseException as e:
        print(f'Creating task test FAILED. Error: {e}, {response}')
        return False


def tasks_get_all_test(test_user: TestUser) -> (bool, int):
    print('Starting all tasks receiving test...')
    try:
        tasks_request = requests.get('http://173.212.214.70:3004/tasks',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        tasks_list = tasks_request.json()
        if isinstance(tasks_list, list):
            print(f'Tasks list successfully received. Found {len(tasks_list)} tasks.')
            return True, len(tasks_list)
        else:
            print(f'Tasks list was not received. Here what was: {tasks_list.text}')
            return False
    except Exception as e:
        print(f'Get all tasks test failed. ERROR: {e}')
        exit()


def check_or_create_test_users(test_user: TestUser, needed: int) -> ([User], bool):
    test_users = []
    is_all_users_got, items = users_get_all_test(test_user)
    if items < needed:
        print(f'You need at least {needed} users for test. We are going to create them')
        for times in range(needed):
            new_user = User()
            new_user.name = f'This is autotest generated user #{times}'
            new_user.password = '12345678'
            new_user.email = 'autotestemail@email.com'
            users_create_user_test(test_user, new_user)
            test_users.append(new_user)
        return test_users, False
    else:
        response = {}
        try:
            print('Fetching existing users. If anything will go wrong - run users test.')
            users_get = requests.get('http://173.212.214.70:3004/users',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
            response = users_get.json()
            for times in range(needed):
                new_user = User()
                new_user.id = response[times]['_id']
                new_user.name = response[times]['name']
                new_user.email = response[times]['email']
                print(f'{times + 1}: {new_user.id}')
                test_users.append(new_user)
            return test_users, True
        except BaseException as e:
            print(f'ERROR while fetching users. Error: {e}, Response: {response}')
            exit()


def check_or_create_test_statuses(test_user: TestUser, needed: int) -> ([Status], bool):
    test_statuses = []
    is_all_statuses_got, items = statuses_get_all_test(test_user)
    if items < needed:
        print(f'You need at least {needed} statuses for test. We are going to create them')
        for times in range(needed):
            new_status = Status()
            new_status.name = f'This is autotest generated user #{times}'
            statuses_create_status_test(test_user, new_status)
            test_statuses.append(new_status)
        return test_statuses, False
    else:
        response = {}
        try:
            print('Fetching three existing statuses. If anything will go wrong - run statuses test.')
            status_get = requests.get('http://173.212.214.70:3004/statuses',
                                      headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
            response = status_get.json()
            for times in range(needed):
                new_status = Status()
                new_status.id = response[times]['_id']
                new_status.name = response[times]['name']
                print(f'{times + 1}: {new_status.id}')
                test_statuses.append(new_status)
            return test_statuses, True
        except BaseException as e:
            print(f'ERROR while fetching boards. Error: {e}, Response: {response}')
            exit()


def run_tasks_test():
    print('Running tasks tests...')
    test_user = get_tester_user_authorized_for_other_test('dimafilin6@icloud.com', '12345678')
    is_all_tasks_get, items = tasks_get_all_test(test_user)
    if is_all_tasks_get is True:
        users_list, users_fetched = check_or_create_test_users(test_user, 2)
        boards_list, boards_fetched = check_or_create_test_boards(test_user, 2)
        statuses_list, statuses_fetched = check_or_create_test_statuses(test_user, 2)
        new_task = Task()
        new_task.name = 'Autotest generated task'
        new_task.description = 'If you see this, contact dimafilin6@icloud.com'
        new_task.boardID = boards_list[0].id
        new_task.statusID = statuses_list[0].id
        new_task.assignedTo = users_list[0].id

        if tasks_create_task_test(test_user, new_task) is True:
            tasks_get_by_id_test(test_user, new_task)
            tasks_update_task_test(test_user, new_task, new_task.name + ' UPDATED',
                                   new_description=new_task.description + ' UPDATED',
                                   new_board_id=boards_list[1].id, new_status_id=statuses_list[1].id,
                                   new_assigned_to=users_list[1].id)
            tasks_delete_task_test(test_user, new_task)


if __name__ == '__main__':
    print('Running tasks test directly.')
    run_tasks_test()
    delete_test_records()
