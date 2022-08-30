from db_conexion import *

USER = 'root'
PASSWORD = 'root'

def main_page():

    options = [1, 2, 3, 4]

    print('''
    Select what you want to do:
    1. Get a random employee
    2. Get a employee by area
    3. see the areas
    4. exit
    ''')

    selection = int(input('write the number of the action: '))
    
    while selection not in options:
        selection = int(input('write a proper selection: '))

    return selection

def get_random_employee():

    connection, cursor = start_connection('lgc', USER, PASSWORD)
    employee = get_random_user(cursor)
    change_password_by_username(connection, cursor, employee[-1])
    end_connection(connection, cursor)

    return(f'''
    Nombre: {employee[0]}
    Cargo: {employee[1]}
    Departamento: {employee[2]}
    Usuario: {employee[3]}
    Contraseña: {employee[3]}
    ''')

def get_employee_by_area():    
    
    area = input('Write the area: ').upper()
    connection, cursor = start_connection('lgc', USER, PASSWORD)
    area_info = get_area(cursor, area)
    employee = get_user_by_area(cursor, area_info[area])

    change_password_by_username(connection, cursor, employee[-1])
    end_connection(connection, cursor)
    
    return(f'''
    Nombre: {employee[0]}
    Cargo: {employee[1]}
    Departamento: {employee[2]}
    Usuario: {employee[3]}
    Contraseña: {employee[3]}
    ''')

def get_departments():
    connection, cursor = start_connection('lgc', USER, PASSWORD)
    areas = get_areas(cursor)
    end_connection(connection, cursor)
    return areas

def exit():
    return ("Ciao...")

if __name__ == '__main__':
    selection = main_page()
    if selection == 1:
        print(get_random_employee())
    elif selection == 2:
        print(get_employee_by_area())
    elif selection == 3:
        departments = get_departments()
        for department in departments:
            print(department, ":", departments[department])
    elif selection == 4:
        print(exit())
