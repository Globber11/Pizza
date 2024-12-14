import json
from random import seed, random
import dpath

# Загрузка данных из JSON файлов
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
    # Логируем начало процесса регистрации
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nНачат процесс регистрации/авторизации')

    # Функция для загрузки пользователей из файла
    def load_users():
        try:
            with open('users_data.json', 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():
                    return json.loads(content)  # Если файл не пустой, загружаем данные
                return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Возвращаем пустой список если файла нет или ошибки в декодировании

    # Функция для сохранения пользователей в файл
    def save_users(users_):
        with open('users_data.json', 'w', encoding='utf-8') as file:
            json.dump(users_, file, ensure_ascii=False, indent=4)  # Сохраняем данные в формате JSON

    print('Приветствую тебя в нашей онлайн пиццерии!')
    print('Для того чтобы сделать заказ, зарегистрируйтесь или войдите')
    print('Введите по очереди свои данные:')

    # Вводим данные пользователя
    name = input('Имя:')
    last_name = input('Фамилия:')

    # Проверка на корректность ввода номера телефона
    while True:
        try:
            phone_number = int(input('Номер телефона без + и пробелов:'))
            break
        except ValueError:
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nПользователь ввёл некорректный номер телефона')
            print('Пожалуйста, введите корректный номер телефона')

    global born_year  # Глобальная переменная для года рождения

    # Проверка на корректность ввода года рождения
    while True:
        try:
            born_year = int(input('Год рождения:'))
            if born_year < 1900:
                print(f'Кому ты πздиш, тебе точно не больше ста лет')  # Проверка на возраст
                continue
            break
        except ValueError:
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nПользователь ввёл некорректный год рождения')
            print('Пожалуйста, введите корректный год рождения')

    with open("admin_password.txt", "r", encoding='utf-8') as file:
        admin_password = file.read()
    
    # Проверка на наличие прав администратора
    if name == 'admin' and last_name == admin_password:
        return True

    # Генерация уникального идентификатора пользователя
    seed(name + last_name + str(phone_number) + str(born_year))
    user_id = int(random() * 10 ** 15)

    users = load_users()  # Загружаем пользователей

    # Проверка на уникальность идентификатора пользователя
    for user in users:
        if user['user_id'] == user_id:
            print(f'Пользователь с ID {user_id} уже зарегистрирован.')
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nТакой пользователь уже зареган под ID {user_id}')
            return born_year

    # Сбор данных о пользователе
    user_data = {
        'user_id': user_id,
        'name': name,
        'last_name': last_name,
        'phone_number': phone_number,
        'born_year': born_year
    }

    users.append(user_data)  # Добавление нового пользователя
    save_users(users)  # Сохранение пользователей

    print(f'Регистрация прошла успешно! Ваш ID: {user_id}')  # Уведомление о успешной регистрации
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nРегистрация завершена, данные: {user_data}')
        file.write(f'\n')
        file.write(f'\n')
    return user_data['born_year']  # Возвращаем год рождения пользователя

def busketSave(buskett, userIn, born_year, userNum=1):
    # Загрузка цен на пивные продукты
    with open('pizzaProductsCost.json', 'r', encoding='utf-8') as file:
        beerProductsCost = json.load(file)

    # Проверка на добавление пива в корзину
    if userIn == "пиво 'Балтика 9'" or userIn == "фирменное пиво":
        buskett.append(userIn)
        buskett.append(dpath.get(beerProductsCost, userIn))  # Получаем цену пива
        buskett.append(userNum)
        with open("logs.txt", "a", encoding='utf-8') as file:
            file.write(f'\nДобавлено в корзину {userNum} {userIn}')
    # Проверка на возраст пользователя для алкоголя
    elif 2024 - born_year < 18:
        if dpath.get(menu, str(userIn)) in buskett:
            buskett[buskett.index(dpath.get(menu, str(userIn))) + 2] += userNum
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
            buskett[buskett.index(dpath.get(menu18, str(userIn))) + 2] += userNum
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')
        else:
            buskett.append(dpath.get(menu18, str(userIn)))
            buskett.append(dpath.get(cost, dpath.get(menu18, str(userIn))))
            buskett.append(userNum)
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')

def warehouse(product, quantity):
    # Функция управления складом
    def load():
        try:
            with open('products.json', 'r', encoding='utf-8') as file:
                content = file.read()
                if content.strip():
                    return json.loads(content)  # Если файл не пустой, загружаем данные
                return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # Возвращаем пустой список если файла нет или ошибки в декодировании

    # Функция для изменения количества продукта на складе
    def edit(products_):
        for _ in products_:
            if _ == product:
                products_[product] -= quantity  # Уменьшаем количество продукта
                return products_  # Возвращаем обновленный список
        return False  # Продукта нет на складе

    # Функция для сохранения обновленного списка продуктов
    def save(products_):
        with open('products.json', 'w', encoding='utf-8') as file:
            json.dump(products_, file, ensure_ascii=False, indent=4)

    products = edit(load())  # Пытаемся редактировать

    if products:
        save(products)  # Сохраняем изменения, если редактирование прошло успешно
        return True
    else:
        return False  # Сообщаем, что редактирование не прошло

products = {}  # Инициализация пустого словаря для продуктов

def edit_cost(product, new_cost):
    # Функция изменения стоимости продукта
    def load():
        with open('cost.json', 'r', encoding='utf-8') as file:
            content = file.read()
            if content.strip():
                return json.loads(content)  # Если файл не пустой, загружаем данные
            return []

    # Функция для изменения цены продукта
    def edit(products_):
        for _ in products_:
            if _ == product:
                products_[product] = new_cost  # Изменяем стоимость продукта
                return products_

    # Функция для сохранения обновленного списка цен
    def save(products_):
        with open('cost.json', 'w', encoding='utf-8') as file:
            json.dump(products_, file, ensure_ascii=False, indent=4)

    save(edit(load()))  # Загружаем, редактируем и сохраняем изменения

def check_consumption(number_product):
    # Функция проверки доступности продуктов на складе согласно номеру продукта
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
        return True  # Доступно, если возраст 18+
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
            return False  # Проверка на доступность кальянной таблетки

def beerTypes():
    # Функция для выбора алкогольных напитков
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)
    with open('pizzaProductsCost.json', 'r', encoding='utf-8') as file:
        beerProductsCost = json.load(file)

    print('Выберите алкогольный напиток')
    i = 0
    for product in products:
        i += 1
        if 8 <= i <= 9:  # Показать продукты с 7 по 8
            print(f' {product}')
    # Цикл для выбора пива и его количества
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
            elif warehouse(productName, productQuantity) == False:
                print("Ошибка: на складе не хватает этого продукта")
                continue
            elif productQuantity >= 10:
                print("Ошибка: вы превысили максимальное значение этого продукта")
                continue
        except ValueError:
            print("Ошибка: введите корректное число.")
            continue
        break
    return [productName, beerProductsCost[productName], productQuantity]  # Возвращаем выбранный продукт

def craftPizza():
    # Функция для создания пиццы
    # Загрузка максимальных количеств продуктов
    with open('maxProductsQuatity.json', 'r', encoding='utf-8') as file:
        maxProductsQuatity = json.load(file)
    # Загрузка доступных продуктов
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)
    # Загрузка цен на пиццу
    with open('pizzaProductsCost.json', 'r', encoding='utf-8') as file:
        pizzaProductsCost = json.load(file)
    
    pizzaCost = pizzaProductsCost['тесто']  # Начальная цена пиццы
    print('Выберите то, из чего вы хотите сделать пиццу:')

    # Показать продукты с 2 по 5 для выбора
    for i, product in enumerate(products, start=1):
        if 1 < i < 8:
            print(f' {product}')

    # Цикл для выбора ингредиентов пиццы
    while True:
        productName = input('Введите название продукта, который вы хотите добавить: ')

        # Проверка на наличие продукта в списке
        if productName not in products:
            print("Ошибка: продукт не найден. Пожалуйста, выберите продукт из списка.")
            continue

        try:
            # Запрос количества продукта
            productQuantity = int(input(f'Введите количество продукта (максимальное количество {maxProductsQuatity[productName]}): '))

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
            pizzaCost += pizzaProductsCost[productName] * productQuantity
            continue
        else:
            pizzaCost += pizzaProductsCost[productName] * productQuantity
            return pizzaCost  # Возвращаем общую стоимость пиццы
