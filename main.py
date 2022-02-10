# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import http
import requests

# Press the green button in the gutter to run the script.
from tests.auth_test import run_auth_tests
from tests.boards_test import run_boards_test
from tests.projects_test import run_projects_test
from tests.statuses_test import run_statuses_test
from tests.users_test import run_users_test

if __name__ == '__main__':
    print('This is bunch of autotests for http://173.212.214.70:3004/api-doc\n')
    print('You can test some part of it directly or run all tests in sequence\n')
    print('Select one of options by inputting it number:\n')
    print('1. Authorization\n')
    print('2. Users\n')
    print('3. Projects\n')
    print('4. Boards\n')
    print('5. Statuses\n')
    print('6. Tasks\n')
    print('7. TEST ALL\n')
    print('0. Quit')
    try:
        selected = int(input())
        if 1 <= selected <= 7:
            if selected == 1 or selected == 7:
                print('---------RUNNING AUTHORIZATION TEST---------')
                run_auth_tests()
                print('--------FINISHED AUTHORIZATION TEST---------')
            if selected == 2 or selected == 7:
                print('-------------RUNNING USERS TEST-------------')
                run_users_test()
                print('------------FINISHED USERS TEST-------------')
            if selected == 3 or selected == 7:
                print('------------RUNNING PROJECTS TEST-----------')
                run_projects_test()
                print('-----------FINISHED PROJECTS TEST-----------')
            if selected == 4 or selected == 7:
                print('------------RUNNING BOARDS TEST-------------')
                run_boards_test()
                print('-----------FINISHED BOARDS TEST-------------')
            if selected == 5 or selected == 7:
                print('-----------RUNNING STATUSES TEST------------')
                run_statuses_test()
                print('-----------FINISHED STATUSES TEST-----------')
            if selected == 6 or selected == 7:
                print('-------------RUNNING TASKS TEST-------------')
                # run_tasks_test()
                print('------------FINISHED TASKS TEST-------------')
        else:
            raise ValueError
    except ValueError:
        print('Wrong selection. Program quits.')
        exit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
