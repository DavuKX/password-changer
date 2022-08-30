import string
import mysql.connector
from mysql.connector import Error

def start_connection(database: string, user: string, password: string):
    try:
        connection = mysql.connector.Connect(
            host = 'localhost',
            database = database,
            user = user,
            password = password
        )

        if connection.is_connected():
            cursor = connection.cursor(buffered=False)
            return(connection, cursor)

    except Error as e:
        return("Error connecting to MySql", e)

def end_connection(connection, cursor):
    if connection.is_connected():
            cursor.close()
            connection.close()
            return("MySql connection is closed")
    return("The connection is already closed")

def get_random_user(cursor):

    query = (
        '''
        SELECT 
            CONCAT(lgc_users.first_name, ' ', lgc_users.last_name),
            lgc_employees_view.appointment_name,
            lgc_employees_view.department_name,
            lgc_users.username
        FROM lgc_users
        INNER JOIN lgc_employees_view
            ON lgc_users.username = lgc_employees_view.username
        ORDER BY RAND()
        LIMIT 1
        '''
        )

    cursor.execute(query)
    record = cursor.fetchall()[0]
    return record

def change_password_by_username(connection, cursor, username):
    query = (
            f'''
            UPDATE lgc_users 
            SET lgc_users.password = SHA1("{username}") 
            WHERE lgc_users.username = "{username}"
            '''
        )
    cursor.execute(query)
    return connection.commit()

def get_areas(cursor):
    query= ('''
        SELECT *
        FROM lgc_departments
        ORDER BY name
    ''')
    cursor.execute(query)
    records = cursor.fetchall()
    records = dict((id, department) for id, department in records)
    return records

def get_area(cursor, name):
    query = (f'''
        SELECT 
            id,
            name
        FROM 
            lgc_departments
        WHERE 
            lgc_departments.name = "{name}"
        LIMIT 1
    ''')
    
    cursor.execute(query)
    record = cursor.fetchall()
    record = dict((department, id) for id, department in record)
    return record

def get_user_by_area(cursor, area):
    query = (f'''
        SELECT 
            CONCAT(lgc_users.first_name, ' ', lgc_users.last_name),
            lgc_employees_view.appointment_name,
            lgc_employees_view.department_name,
            lgc_users.username
        FROM lgc_users
        INNER JOIN lgc_employees_view
            ON lgc_users.username = lgc_employees_view.username
        WHERE lgc_employees_view.department_id = "{area}"
        ORDER BY RAND()
        LIMIT 1
    ''')

    cursor.execute(query)
    return cursor.fetchone()

if __name__ == '__main__':

    area = input('write the name of the area: ').upper()
    connection, cursor = start_connection('lgc', 'root', 'root')
    # record = get_random_user(cursor)
    # change_password_by_username(connection, cursor, record[3])
    record = get_area(cursor, area)
    employee = get_user_by_area(cursor, record[area])
    print(employee)

    end_connection(connection, cursor)
    

