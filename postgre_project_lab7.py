import psycopg2
from config_postgre import host, user, password, db_name

adding_table = {
    "door": "(id двери, название двери, цену, id используемого материала, id характеристики)",
    "material": "(id материала, название, прочность(строка) )",
    "warehouse": "(id склада, адрес, объем, id поставщика, id доставщика)",
    "stored": "(количество, id склада, id двери)"
}


def checkYN(string):
    if string == "Y":
        return True
    return False


def any_symbol_is_alpha(string):
    for i in string:
        if i.isalpha():
            return True


def compile_string(mas):
    finally_string = "("
    for i in range(len(mas)):
        if i != len(mas) - 1 and mas[i] != " ":
            if any_symbol_is_alpha(mas[i]):
                finally_string += f"'{mas[i]}', "
            else:
                finally_string += f"{mas[i]}, "
        else:
            if any_symbol_is_alpha(mas[i]):
                finally_string += f"'{mas[i]}')"
            else:
                finally_string += f"{mas[i]})"

    return finally_string


def choose_table():
    global chosen_table
    table_choose = int(input(f"Выберите действие CRUD:\n1 - Добавить в таблицу {chosen_table}\n2 - Получить данные из таблицы {chosen_table}\n3 - Редактировать данные из таблицы {chosen_table}\n4 - Удалить данные из таблицы {chosen_table}\n"))
    if table_choose == 1:
        adding_info = input(f"Заполните данные через пробел в соответствии с порядком {adding_table[chosen_table]}:\n").replace(",", "").split(" ")
        adding_func(compile_string(adding_info))
    elif table_choose == 2:
        where_question = input("Использовать конструкцию where? (Y/N): ")
        find_func(checkYN(where_question))
    elif table_choose == 3:
        replace_func()
    elif table_choose == 4:
        delete_func()


def adding_func(info):
    global chosen_table
    try:

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"insert into {chosen_table} values{info};"
            )
            connection.commit()
            print("Успешно добавили запись!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nПодключение разорвано!")


def find_func(is_where):
    parameter = input("Введите параметр: ")
    global chosen_table
    try:

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            if is_where:
                where_parameter = input("Введите параметр where: ")
                cursor.execute(
                    f"select {parameter} from {chosen_table} where {where_parameter}"
                )
            else:
                cursor.execute(
                    f"select {parameter} from {chosen_table}"
                )
            print(cursor.fetchall())
            print("Запись успешно просмотрена!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nПодключение разорвано!")


def replace_func():
    set_parameter = input("Введите параметр SET: ")
    where_parameter = input("Введите параметр WHERE: ")
    global chosen_table
    try:

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"update {chosen_table} set {set_parameter} where {where_parameter}"
            )
            connection.commit()
            print("Запись успешно изменена!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nПодключение разорвано!")


def delete_func():
    where_parameter = input("Введите параметр WHERE: ")
    global chosen_table
    try:

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"delete from {chosen_table} where {where_parameter}"
            )
            connection.commit()
            print("Запись успешно удалена!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nПодключение разорвано!")


def choose_analit():
    analyt_question = int(input("Выберете аналитический запрос:\n1 - Показать из какого материала состоит дверь\n2 - Рассчёт суммы стоимостей дверей с определенным материалом\n3 - Вывод адресов и объемов складов по полному или частичному адресу\n"))
    if analyt_question == 1:
        material_from_door()
    elif analyt_question == 2:
        sum_of_door_prices()
    elif analyt_question == 3:
        warehouses_with_address()


def material_from_door():
    door_name = input("Введите название двери, у которой хотите проверить материал: ")
    try:

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"select material_name from material JOIN door ON id_material = fk_id_material WHERE door_name = '{door_name}'"
            )
            print(cursor.fetchall())
            print("Успешно!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nПодключение разорвано!")


def sum_of_door_prices():
    material_name = input("Введите название материала, у которого хотите посчитать сумму: ")
    try:

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"select SUM(price) from door JOIN material ON fk_id_material = id_material WHERE material_name = '{material_name}'"
            )
            print(cursor.fetchall())
            print("Успешно!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nПодключение разорвано!")


def warehouses_with_address():
    warehouse_address = input("Введите частичный либо полный адрес склада: ")
    try:

        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"select address, volume from warehouse where address like '%{warehouse_address}%'"
            )
            print(cursor.fetchall())
            print("Успешно!")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("\nПодключение разорвано!")


main_choose = int(input("Выберите таблицу с которой будете работать:\n1 - Двери\n2 - Материалы\n3 - Склад\n4 - Хранится(Многие ко многим)\n5 - Совершить аналитический запрос\n"))
chosen_table = ""
if main_choose == 1:
    chosen_table = "door"
    choose_table()
elif main_choose == 2:
    chosen_table = "material"
    choose_table()
elif main_choose == 3:
    chosen_table = "warehouse"
    choose_table()
elif main_choose == 4:
    chosen_table = "stored"
    choose_table()
elif main_choose == 5:
    choose_analit()