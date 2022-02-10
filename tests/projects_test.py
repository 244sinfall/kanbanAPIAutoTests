import requests

from tests.auth_test import TestUser, get_tester_user_authorized_for_other_test

test_project_name_local = 'This is autotest generated project'
test_project_description_local = 'If you see this, please report dimafilin6@icloud.com'


class Project:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.description = ''


def projects_delete_project_test(test_user, test_project) -> bool:
    print('Starting deleting project test...')
    response = {}
    try:
        project_delete_info = requests.delete(f'http://173.212.214.70:3004/projects/delete/{test_project.id}',
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = project_delete_info.json()
        if 'success' in response:
            if response['success'] is True:
                del test_project
                print('Test project successfully deleted.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except Exception as e:
        print(f'Deleting project test FAILED. Error: {e}, {response}')
        return False


def projects_update_project_test(test_user, test_project, new_name, new_description) -> bool:
    print('Starting project update test...')
    response = {}
    try:
        project_new_info = requests.put(f'http://173.212.214.70:3004/projects/update/{test_project.id}',
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)},
                                        data={
                                            'name': new_name,
                                            'description': new_description
                                        })
        response = project_new_info.json()
        if 'name' in response and 'description' in response and '_id' in response:
            if response['name'] == new_name \
                    and response['description'] == new_description \
                    and response['_id'] == test_project.id:
                test_project.name = response['name']
                test_project.description = response['description']
                print('Test project successfully updated.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except Exception as e:
        print(f'Updating project test FAILED. Error: {e}, {response}')
        return False


def projects_get_by_id_test(test_user: TestUser, test_project: Project) -> bool:
    print('Starting project get by id test...')
    response = {}
    try:
        project_info = requests.get(f'http://173.212.214.70:3004/projects/{test_project.id}',
                                         headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = project_info.json()
        if 'name' in response and 'description' in response and '_id' in response:
            if response['name'] == test_project.name \
                    and response['description'] == test_project.description \
                    and response['_id'] == test_project.id:
                print('Test project successfully receieved by ID.')
                return True
            else:
                raise 'Wrong record received.'
        else:
            raise 'Wrong response format'
    except Exception as e:
        print(f'Getting project by id test FAILED. Error: {e}, {response}')
        return False


def projects_create_project_test(test_user: TestUser, test_project: Project) -> bool:
    print('Starting project create test...')
    response = {}
    try:
        new_project_request = requests.post('http://173.212.214.70:3004/projects/create',
                                         data={'name': test_project.name,
                                                'description': test_project.description,
                                                },
                                            headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        response = new_project_request.json()
        if 'name' in response and 'description' in response and '_id' in response:
            if response['name'] == test_project.name and response['description'] == test_project.description:
                test_project.id = response['_id']
                print('Test project successfully created.')
                return True
            else:
                raise 'Wrong record created.'
        else:
            raise 'Wrong response format'
    except Exception as e:
        print(f'Creating project test FAILED. Error: {e}, {response}')
        return False


def projects_get_all_test(test_user: TestUser) -> (bool, int):
    print('Starting all project receiving test...')
    try:
        projects_request = requests.get('http://173.212.214.70:3004/projects',
                                     headers={'Authorization': 'Bearer {}'.format(test_user.accessToken)})
        projects_list = projects_request.json()
        if isinstance(projects_list, list):
            print(f'Projects list successfully received. Found {len(projects_list)} projects.')
            return True, len(projects_list)
        else:
            print(f'Project list was not received. Here what was: {projects_request.text}')
            return False
    except Exception as e:
        print(f'Get all projects test failed. ERROR: {e}')
        exit()


def run_projects_test():
    print('Running project tests...')
    test_user = get_tester_user_authorized_for_other_test('dimafilin6@icloud.com', '12345678')
    is_all_project_got, items = projects_get_all_test(test_user)
    if is_all_project_got is True:
        test_project = Project()
        test_project.name = test_project_name_local
        test_project.description = test_project_description_local
        if projects_create_project_test(test_user, test_project) is True:
            projects_get_by_id_test(test_user, test_project)
            projects_update_project_test(test_user, test_project, new_name=test_project_name_local+' UPDATED',
                                         new_description=test_project_description_local+' UPDATED')
            projects_delete_project_test(test_user, test_project)


if __name__ == '__main__':
    run_projects_test()