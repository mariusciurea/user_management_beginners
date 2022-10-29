import sqlite3
from getpass import getpass

def create_user_menu() -> str:
    """
    application menu for creating the account/login/show up
    the details
    :return: the option you chose as a string (1/2/3/E)
    """
    option = input('1. -> create account\n'
                   '2. -> login\n'
                   '3. -> show details\n'
                   'E. -> exit\n'
                   'Enter your choise: '
                   )
    return option


def connect_db() -> (sqlite3.Connection, sqlite3.Cursor):
    """
    create the connection to the db
    :return: connection object -> 'con' and
            the database cursor -> 'cur'
    """
    con = sqlite3.connect("test_users_login.db")
    cur = con.cursor()
    return con, cur


def create_table(command) -> None:
    cur.execute(command)


def execute_command(command, data=None):
    if 'insert' in command or 'INSERT' in command:
        if data:
            cur.execute(command, data)
            con.commit()
        else:
            cur.execute(command)
            con.commit()
        return

    res = cur.execute(command)
    return res.fetchall()


def create_user_data() -> (str, str, str):
    """
    input the user details for account creation
    :return: username, passwd, email
    """
    username = input('Enter the username: ')
    # passwd = getpass()  # if executed from cmd, not pycharm terminal
    passwd = input('Enter the passwd: ')
    email = input('Enter the email: ')

    return username, passwd, email


def login_user_data() -> (str, str):
    """
    input the user details for login
    :return: username, password
    """
    username = input('Enter the username: ')
    passwd = input('Enter the passwd: ')
    return username, passwd


if __name__ == '__main__':
    try:
        con, cur = connect_db()
    except sqlite3.Error as e:
        print(f'An exeception occurred! The connection'
              f'to the database it is not possible')
        exit()

    create_users_table = 'CREATE TABLE IF NOT EXISTS users(\n' \
                         'user_name TEXT NOT NULL,\n' \
                         'password TEXT NOT NULL,\n' \
                         'email TEXT PRIMARY KEY\n' \
                         ');'
    create_table(create_users_table)

    option = create_user_menu()

    while option:
        if option == '1':
            username, passwd, email = create_user_data()
            if username and passwd and email:
                try:
                    users = execute_command('SELECT user_name FROM users')
                except sqlite3.Error as e:
                    print(e)
                    print('enter the data again')
                    option = create_user_menu()
                else:
                    if (username,) not in users: # users = [(user1,), (user2,)...] -
                        # lista cu userii - fiecare element este un tuplu cu cate un user
                        data = (username, passwd, email)
                        execute_command(f"INSERT INTO users VALUES{data}")
                        print('Successfully created the account!')
                    else:
                        print(f'{username} already exists! Try another one!')
                    option = create_user_menu()
            else:
                print('you have to enter all the data')
                option = create_user_menu()

        elif option == '2':
            username, passwd = login_user_data()
            try:
                user_data = execute_command('SELECT user_name, password FROM users')
            except sqlite3.Error as e:
                print(e)
                print('login again')
                username, passwd = login_user_data()
            else:
                if (username, passwd) in user_data:
                    print(f'{username} successfully logged in!')
                else:
                    print(f'user or password is incorrect. Try again to login!')
                    username, passwd = login_user_data()
            option = create_user_menu()

        elif option == '3':
            print('This is going to be implemented')
            option = create_user_menu()

        elif option == 'E' or option == 'e':
            exit()

        else:
            print('Not a valid option. Try again')
            option = create_user_menu()


