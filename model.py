import json
from random import seed, random
from view import menu
from view import menu18
from view import cost
from view import cost18
def reg_and_create_id():
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nНачат процесс регистрации/авторизации')
    def load_users():
        try:
            with open('users_data.json', 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():
                    return json.loads(content)
                return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_users(users_):
        with open('users_data.json', 'w', encoding='utf-8') as file:
            json.dump(users_, file, ensure_ascii=False, indent=4)

    print('Приветствую тебя в нашей онлайн пиццерии!')
    print('Для того чтобы сделать заказ, зарегистрируйтесь или войдите')
    print('Введите по очереди свои данные:')

    name = input('Имя:')
    last_name = input('Фамилия:')

    while True:
        try:
            phone_number = int(input('Номер телефона без + и пробелов:'))
            break
        except ValueError:
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nПользователь ввёл некорректный номер телефона')
            print('Пожалуйста, введите корректный номер телефона')

    global born_year

    while True:
        try:
            born_year = int(input('Год рождения:'))
            break
        except ValueError:
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nПользователь ввёл некорректный год рождения')
            print('Пожалуйста, введите корректный год рождения')

    seed(name + last_name + str(phone_number) + str(born_year))

    user_id = int(random() * 10 ** 15)

    users = load_users()

    for user in users:
        if user['user_id'] == user_id:
            print(f'Пользователь с ID {user_id} уже зарегистрирован.')
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nТакой пользователь уже зареган под ID {user_id}')
            return

    user_data = {
        'user_id': user_id,
        'name': name,
        'last_name': last_name,
        'phone_number': phone_number,
        'born_year': born_year
    }

    users.append(user_data)
    save_users(users)

    print(f'Регистрация прошла успешно! Ваш ID: {user_id}')
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nРегистрация завершена, данные: {user_data}')
        file.write(f'\n')
        file.write(f'\n')
    return user_data['born_year']

def busketSave(buskett, userIn, born_year, userNum=1):
    if 2024-born_year<18:
        if menu(userIn) in buskett:
            buskett[buskett.index(menu(userIn))+2]+=userNum
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')
        else:
            buskett.append(menu(userIn))
            buskett.append(cost(menu(userIn)))
            buskett.append(userNum)
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')
    else:
        if menu(userIn) in buskett:
            buskett[buskett.index(menu18(userIn))+2]+=userNum
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')
        else:
            buskett.append(menu18(userIn))
            buskett.append(cost18(menu18(userIn)))
            buskett.append(userNum)
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')

def warehouse(product, quantity):
    def load():
        try:
            with open('products.json', 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():
                    return json.loads(content)
                return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def edit(products_):
        for _ in products_:
            if _ == product:
                products_[product] -= quantity
                return products_
        return False

    def save(products_):
        with open('products.json', 'w', encoding='utf-8') as file:
            json.dump(products_, file, ensure_ascii=False, indent=4)

    products = edit(load())

    if products:
        save(products)
        return True
    else:
        return False
products = {}
maxProductsQuatity = {
    'пепперони': 20,
    'томаты': 30,
    'сыр': 50,
    'бекон': 25
}

def craftPizza():
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)
    print('Выберите то из чего вы хотите сделать пиццу')
    i = 0
    for product in products:
        i += 1
        if 1 < i < 6:  # Показать продукты с 2 по 5
            print(f' {product}')

    while True:
        productName = input(f'Введите название продукта, который вы хотите добавить: ')
        if productName not in products:
            print("Ошибка: продукт не найден. Пожалуйста, выберите продукт из списка.")
            continue
        try:
            productQuantity = int(input(f'Введите количество продукта(максимальное количество {maxProductsQuatity[productName]}): '))
            if productQuantity <= 0:
                print("Ошибка: количество должно быть положительным числом.")
                continue
            elif warehouse(productName, productQuantity)==False:
                print("Ошибка: на складе не хватает этого продукта")
                continue
            elif productQuantity>=maxProductsQuatity[productName]:
                print("Ошибка: вы превысили максимальное значение этого продукта")
                continue
        except ValueError:
            print("Ошибка: введите корректное число.")
        if input('Если хотите продолжить добавление ингредиентов введите 1, иначе любой другой символ:')=='1':
            continue
        else:
            break
