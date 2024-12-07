import json
from random import seed, random
import dpath

with open('menu18.json', 'r', encoding='utf-8') as file:
    menu18 = file.read()
    menu18 = json.loads(menu18)
with open('menu.json', 'r', encoding='utf-8') as file:
    menu = file.read()
    menu = json.loads(menu)
with open('cost.json', 'r', encoding='utf-8') as file:
    cost = file.read()
    cost = json.loads(cost)

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
            if born_year < 1900:
                print(f'Кому ты πздиш, тебе точно не больше ста лет')
                continue
            break
        except ValueError:
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nПользователь ввёл некорректный год рождения')
            print('Пожалуйста, введите корректный год рождения')

    if name == 'admin' and last_name == 'BAN':
        return True

    seed(name + last_name + str(phone_number) + str(born_year))

    user_id = int(random() * 10 ** 15)

    users = load_users()

    for user in users:
        if user['user_id'] == user_id:
            print(f'Пользователь с ID {user_id} уже зарегистрирован.')
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nТакой пользователь уже зареган под ID {user_id}')
            return born_year

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
        if dpath.get(menu, str(userIn)) in buskett:
            buskett[buskett.index(dpath.get(menu, str(userIn)))+2]+=userNum
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')
        else:
            buskett.append(dpath.get(menu, str(userIn)))
            buskett.append(dpath.get(cost, dpath.get(menu, str(userIn))))
            buskett.append(userNum)
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')
    else:
        if dpath.get(menu18, str(userIn)) in buskett:
            buskett[buskett.index(dpath.get(menu18, str(userIn)))+2]+=userNum
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')
        else:
            buskett.append(dpath.get(menu18, str(userIn)))
            buskett.append(dpath.get(cost, dpath.get(menu18, str(userIn))))
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

def edit_cost(product, new_cost):
    def load():
        with open('cost.json', 'r', encoding='utf-8') as file:
            content = file.read()
            if content.strip():
                return json.loads(content)
            return []

    def edit(products_):
        for _ in products_:
            if _ == product:
                products_[product] = new_cost
                return products_

    def save(products_):
        with open('cost.json', 'w', encoding='utf-8') as file:
            json.dump(products_, file, ensure_ascii=False, indent=4)

    save(edit(load()))

def check_consumption(number_product):
    if number_product == 1:
        if warehouse("тесто", 200) == False:
            return False
        if warehouse("пепперони", 20) == False:
            return False
        if warehouse("сыр", 40) == False:
            return False
    elif number_product == 2:
        if warehouse("тесто", 200) == False:
            return False
        if warehouse("томаты", 30) == False:
            return False
        if warehouse("сыр", 40) == False:
            return False
    elif number_product == 3:
        if warehouse("тесто", 200) == False:
            return False
        if warehouse("сыр", 100) == False:
            return False
    elif number_product == 4:
        if warehouse("тесто", 200) == False:
            return False
        if warehouse("сыр", 40) == False:
            return False
        if warehouse("ветчина", 30) == False:
            return False
        if warehouse("грибы", 30) == False:
            return False
    elif number_product == 5 and 2024 - born_year >= 18:
        return True
    elif number_product == 5 and 2024 - born_year < 18:
        if warehouse("тесто", 90) == False:
            return False
        if warehouse("сыр", 30) == False:
            return False
        if warehouse("грибы", 20) == False:
            return False
        if warehouse("пепперони", 20) == False:
            return False
    elif number_product == 6 and 2024 - born_year >= 18:
        if warehouse("кола", 40) == False:
            return False
        if warehouse("виски", 30) == False:
            return False
    elif number_product == 6 and 2024 - born_year < 18:
        if warehouse("сок", 70) == False:
            return False
    elif number_product == 7 and 2024 - born_year >= 18:
        if warehouse("кальянная_таблетка", 50) == False:
            return False
def beerTypes():
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)
    print('Выберите алкогольный напиток')
    i = 0
    for product in products:
        i += 1
        if 6 <= i <= 8:  # Показать продукты с 5 по 7
            print(f' {product}')
    while True:
        productName = input(f'Введите название продукта, который вы хотите добавить: ')
        if productName not in products:
            print("Ошибка: продукт не найден. Пожалуйста, выберите продукт из списка.")
            continue
        try:
            productQuantity = int(input('Введите количество продукта(максимальное количество 10): '))
            if productQuantity <= 0:
                print("Ошибка: количество должно быть положительным числом.")
                continue
            elif warehouse(productName, productQuantity)==False:
                print("Ошибка: на складе не хватает этого продукта")
                continue
            elif productQuantity>=10:
                print("Ошибка: вы превысили максимальное значение этого продукта")
                continue
            return productQuantity
        except ValueError:
            print("Ошибка: введите корректное число.")
            continue


def craftPizza():
    # Загрузка продуктов из файла
    with open('maxProductsQuatity.json', 'r', encoding='utf-8') as file:
        maxProductsQuatity = json.load(file)
    # Загрузка продуктов из файла
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)
    # Загрузка продуктов из файла
    with open('pizzaProductsCost.json', 'r', encoding='utf-8') as file:
        pizzaProductsCost = json.load(file)
    pizzaCost = pizzaProductsCost['тесто']
    print('Выберите то, из чего вы хотите сделать пиццу:')

    # Показать продукты с 2 по 5
    for i, product in enumerate(products, start=1):
        if 1 < i < 8:
            print(f' {product}')

    while True:
        productName = input('Введите название продукта, который вы хотите добавить: ')

        # Проверка на наличие продукта в списке
        if productName not in products:
            print("Ошибка: продукт не найден. Пожалуйста, выберите продукт из списка.")
            continue

        try:
            # Запрос количества продукта
            productQuantity = int(
                input(f'Введите количество продукта (максимальное количество {maxProductsQuatity[productName]}): '))

            # Проверка на положительное число
            if productQuantity <= 0:
                print("Ошибка: количество должно быть положительным числом.")
                continue

            # Проверка наличия на складе
            if not warehouse(productName, productQuantity):
                print("Ошибка: на складе не хватает этого продукта.")
                continue

            # Проверка на превышение максимального количества
            if productQuantity > maxProductsQuatity[productName]:
                print("Ошибка: вы превысили максимальное значение этого продукта.")
                continue

        except ValueError:
            print("Ошибка: введите корректное число.")
            continue
        except KeyError:
            print(f"Ошибка: продукт '{productName}' не найден в максимальных количествах.")
            continue
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            continue
        # Запрос на продолжение добавления ингредиентов
        if input('Если хотите продолжить добавление ингредиентов, введите 1, иначе любой другой символ: ') == '1':
            pizzaCost += pizzaProductsCost[productName]*productQuantity
            continue
        else:
            pizzaCost += pizzaProductsCost[productName] * productQuantity
            return pizzaCost


