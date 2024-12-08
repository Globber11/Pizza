import json  # Импорт библиотеки для работы с JSON-данными
from random import seed, random  # Импортируем функции для генерации случайных чисел

import dpath  # Импортируем библиотеку dpath для работы с вложенными структурами данных

# Чтение и загрузка меню пиццы из JSON-файлов
with open('menu18.json', 'r', encoding='utf-8') as file:
    menu18 = file.read()  # Считываем содержимое файла
    menu18 = json.loads(menu18)  # Преобразуем JSON-строку в Python-объект

with open('menu.json', 'r', encoding='utf-8') as file:
    menu = file.read()  # Считываем содержимое файла
    menu = json.loads(menu)  # Преобразуем JSON-строку в Python-объект

with open('cost.json', 'r', encoding='utf-8') as file:
    cost = file.read()  # Считываем содержимое файла
    cost = json.loads(cost)  # Преобразуем JSON-строку в Python-объект

# Функция для регистрации пользователя и создания уникального ID
def reg_and_create_id():
    # Запись в лог о начале процесса регистрации/авторизации
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\n')
        file.write(f'\nНачат процесс регистрации/авторизации')

    # Функция загрузки данных пользователей из файла
    def load_users():
        try:
            with open('users_data.json', 'r', encoding='utf-8') as file:  # Открываем файл с данными пользователей
                content = file.read()  # Считываем содержимое
                if content.strip():  # Если файл не пустой
                    return json.loads(content)  # Возвращаем данные в виде Python-объекта
                return []  # Если файл пустой, возвращаем пустой список
        except (FileNotFoundError, json.JSONDecodeError):  # Обработка исключений: файл не найден или ошибка декодирования
            return []  # В случае ошибки возвращаем пустой список

    # Функция сохранения данных пользователей в файл
    def save_users(users_):
        with open('users_data.json', 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump(users_, file, ensure_ascii=False, indent=4)  # Сохраняем данные в формате JSON

    # Приветственное сообщение и запрос данных у пользователя
    print('Приветствую тебя в нашей онлайн пиццерии!')
    print('Для того чтобы сделать заказ, зарегистрируйтесь или войдите')
    print('Введите по очереди свои данные:')

    name = input('Имя:')  # Запрос имени
    last_name = input('Фамилия:')  # Запрос фамилии

    # Цикл для ввода корректного номера телефона
    while True:
        try:
            phone_number = int(input('Номер телефона без + и пробелов:'))  # Запрос номера телефона
            break  # Выход из цикла, если введено корректное значение
        except ValueError:  # Обработка исключения при некорректном вводе
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nПользователь ввёл некорректный номер телефона')  # Запись в лог
            print('Пожалуйста, введите корректный номер телефона')  # Запрос повторного ввода

    global born_year  # Объявление переменной года рождения как глобальной

    # Цикл для ввода корректного года рождения
    while True:
        try:
            born_year = int(input('Год рождения:'))  # Запрос года рождения
            break  # Выход из цикла, если введено корректное значение
        except ValueError:  # Обработка исключения при некорректном вводе
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nПользователь ввёл некорректный год рождения')  # Запись в лог
            print('Пожалуйста, введите корректный год рождения')  # Запрос повторного ввода

    # Проверка на наличие администратора
    if name == 'admin' and last_name == 'BAN':
        return True  # Возвращение True для администратора

    # Инициализация генератора случайных чисел
    seed(name + last_name + str(phone_number) + str(born_year))
    user_id = int(random() * 10 ** 15)  # Генерация уникального ID пользователя

    users = load_users()  # Загрузка данных пользователей

    # Создание словаря с данными нового пользователя
    user_data = {
        'user_id': user_id,
        'name': name,
        'last_name': last_name,
        'phone_number': phone_number,
        'born_year': born_year
    }
    
    # Проверка на уникальность ID пользователя
    for user in users:
        if user['user_id'] == user_id:
            print(f'Пользователь с ID {user_id} уже зарегистрирован.')  # Сообщение о дублировании ID
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nТакой пользователь уже зареган под ID {user_id}')  # Запись в лог
            return user_data['born_year']  # Возвращение года рождения

    users.append(user_data)  # Добавление нового пользователя в список
    save_users(users)  # Сохранение обновленного списка пользователей

    print(f'Регистрация прошла успешно! Ваш ID: {user_id}')  # Сообщение об успешной регистрации
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nРегистрация завершена, данные: {user_data}')  # Запись в лог
        file.write(f'\n')
        file.write(f'\n')
    return user_data['born_year']  # Возвращение года рождения

# Функция для сохранения товара в корзине
def busketSave(buskett, userIn, born_year, userNum=1):
    if 2024 - born_year < 18:  # Проверка на возраст пользователя
        if dpath.get(menu, str(userIn)) in buskett:  # Если товар уже в корзине
            # Увеличение количества товара в корзине
            buskett[buskett.index(dpath.get(menu, str(userIn))) + 2] += userNum
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')  # Запись в лог
        else:  # Если товара нет в корзине
            # Добавление нового товара в корзину
            buskett.append(dpath.get(menu, str(userIn)))
            buskett.append(dpath.get(cost, dpath.get(menu, str(userIn))))
            buskett.append(userNum)
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')  # Запись в лог
    else:  # Если пользователь старше 18 лет
        if dpath.get(menu, str(userIn)) in buskett:  # Если товар уже в корзине
            buskett[buskett.index(dpath.get(menu18, str(userIn))) + 2] += userNum  # Увеличение количества товара
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')  # Запись в лог
        else:  # Если товара нет в корзине
            # Добавление нового товара в корзину
            buskett.append(dpath.get(menu18, str(userIn)))
            buskett.append(dpath.get(cost, dpath.get(menu18, str(userIn))))
            buskett.append(userNum)
            with open("logs.txt", "a", encoding='utf-8') as file:
                file.write(f'\nДобавлено в корзину {userNum} {userIn}')  # Запись в лог

# Функция управления запасами продуктов
def warehouse(product, quantity):
    # Функция загрузки данных о продуктах из файла
    def load():
        try:
            with open('products.json', 'r', encoding='utf-8') as file:  # Открываем файл с данными о продуктах
                content = file.read()  # Считываем содержимое
                if content.strip():  # Если файл не пустой
                    return json.loads(content)  # Возвращаем данные в виде Python-объекта
                return []  # Если файл пустой, возвращаем пустой список
        except (FileNotFoundError, json.JSONDecodeError):  # Обработка исключений: файл не найден или ошибка декодирования
            return []  # В случае ошибки возвращаем пустой список

    # Функция редактирования данных о продуктах
    def edit(products_):
        for _ in products_:  # Проход по всем продуктам
            if _ == product:  # Если продукт совпадает с заданным
                products_[product] -= quantity  # Уменьшаем количество на складе
                return products_  # Возвращаем обновленный список
        return False  # Если продукт не найден, возвращаем False

    # Функция сохранения обновленных данных о продуктах
    def save(products_):
        with open('products.json', 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump(products_, file, ensure_ascii=False, indent=4)  # Сохраняем данные в формате JSON

    products = edit(load())  # Обновляем данные о продуктах

    if products:  # Если данные успешно обновлены
        save(products)  # Сохраняем их в файл
        return True  # Возвращаем True
    else:
        return False  # В случае ошибки возвращаем False

products = {}  # Инициализация пустого словаря для продуктов

# Функция редактирования цены продукта
def edit_cost(product, new_cost):
    # Функция загрузки данных о ценах из файла
    def load():
        with open('cost.json', 'r', encoding='utf-8') as file:  # Открываем файл с данными о ценах
            content = file.read()  # Считываем содержимое
            if content.strip():  # Если файл не пустой
                return json.loads(content)  # Возвращаем данные в виде Python-объекта
            return []  # Если файл пустой, возвращаем пустой список

    # Функция редактирования цен на продукты
    def edit(products_):
        for _ in products_:  # Проход по всем продуктам
            if _ == product:  # Если продукт совпадает с заданным
                products_[product] = new_cost  # Обновляем цену продукта
                return products_  # Возвращаем обновленный список

    # Функция сохранения обновленных данных о ценах
    def save(products_):
        with open('cost.json', 'w', encoding='utf-8') as file:  # Открываем файл для записи
            json.dump(products_, file, ensure_ascii=False, indent=4)  # Сохраняем данные в формате JSON

    save(edit(load()))  # Обновляем и сохраняем данные о ценах

# Функция проверки наличия продуктов для приготовления
def check_consumption(number_product):
    if number_product == 1:  # Проверка для первого продукта
        if not warehouse("тесто", 200):  # Проверка наличия теста
            return False  # Если теста не хватает, возвращаем False
        if not warehouse("пепперони", 20):  # Проверка наличия пепперони
            return False  # Если пепперони не хватает, возвращаем False
        if not warehouse("сыр", 40):  # Проверка наличия сыра
            return False  # Если сыра не хватает, возвращаем False
    elif number_product == 2:  # Проверка для второго продукта
        if not warehouse("тесто", 200):  # Проверка наличия теста
            return False  # Если теста не хватает, возвращаем False
        if not warehouse("томаты", 30):  # Проверка наличия томатов
            return False  # Если томатов не хватает, возвращаем False
        if not warehouse("сыр", 40):  # Проверка наличия сыра
            return False  # Если сыра не хватает, возвращаем False
    elif number_product == 3:  # Проверка для третьего продукта
        if not warehouse("тесто", 200):  # Проверка наличия теста
            return False  # Если теста не хватает, возвращаем False
        if not warehouse("сыр", 100):  # Проверка наличия сыра
            return False  # Если сыра не хватает, возвращаем False
    elif number_product == 4:  # Проверка для четвертого продукта
        if not warehouse("тесто", 200):  # Проверка наличия теста
            return False  # Если теста не хватает, возвращаем False
        if not warehouse("сыр", 40):  # Проверка наличия сыра
            return False  # Если сыра не хватает, возвращаем False
        if not warehouse("ветчина", 30):  # Проверка наличия ветчины
            return False  # Если ветчины не хватает, возвращаем False
        if not warehouse("грибы", 30):  # Проверка наличия грибов
            return False  # Если грибов не хватает, возвращаем False
    elif number_product == 5 and 2024 - born_year >= 18:  # Если продукт 5 и пользователь старше 18 лет
        return True  # Возвращаем True, т.к. все необходимые проверки пройдены
    elif number_product == 5 and 2024 - born_year < 18:  # Если продукт 5 и пользователь младше 18 лет
        if not warehouse("тесто", 90):  # Проверка наличия теста
            return False  # Если теста не хватает, возвращаем False
        if not warehouse("сыр", 30):  # Проверка наличия сыра
            return False  # Если сыра не хватает, возвращаем False
        if not warehouse("грибы", 20):  # Проверка наличия грибов
            return False  # Если грибов не хватает, возвращаем False
        if not warehouse("пепперони", 20):  # Проверка наличия пепперони
            return False  # Если пепперони не хватает, возвращаем False
    elif number_product == 6 and 2024 - born_year >= 18:  # Если продукт 6 и пользователь старше 18 лет
        if not warehouse("кола", 40):  # Проверка наличия колы
            return False  # Если колы не хватает, возвращаем False
        if not warehouse("виски", 30):  # Проверка наличия виски
            return False  # Если виски не хватает, возвращаем False
    elif number_product == 6 and 2024 - born_year < 18:  # Если продукт 6 и пользователь младше 18 лет
        if not warehouse("сок", 70):  # Проверка наличия сока
            return False  # Если сока не хватает, возвращаем False
    elif number_product == 7 and 2024 - born_year >= 18:  # Если продукт 7 и пользователь старше 18 лет
        if not warehouse("кальянная_таблетка", 50):  # Проверка наличия кальянной таблетки
            return False  # Если кальянной таблетки не хватает, возвращаем False

# Функция для выбора алкогольных напитков
def beerTypes():
    with open('products.json', 'r', encoding='utf-8') as file:  # Открываем файл с данными о продуктах
        products = json.load(file)  # Загружаем данные о продуктах
    print('Выберите алкогольный напиток')  # Запрос выбора напитка
    i = 0  # Инициализация счетчика
    for product in products:  # Проход по всем продуктам
        i += 1  # Увеличение счетчика
        if 6 <= i <= 8:  # Показать продукты с 5 по 7
            print(f' {product}')  # Вывод названия продукта
    while True:  # Бесконечный цикл для получения корректного ввода
        productName = input(f'Введите название продукта, который вы хотите добавить: ')  # Запрос на ввод названия продукта
        if productName not in products:  # Проверка на наличие продукта в списке
            print("Ошибка: продукт не найден. Пожалуйста, выберите продукт из списка.")  # Сообщение об ошибке
            continue  # Продолжение цикла для повторного ввода
        try:
            productQuantity = int(input('Введите количество продукта(максимальное количество 10): '))  # Запрос количества продукта
            if productQuantity <= 0:  # Проверка на положительное число
                print("Ошибка: количество должно быть положительным числом.")  # Сообщение об ошибке
                continue  # Продолжение цикла для повторного ввода
            elif warehouse(productName, productQuantity) == False:  # Проверка наличия на складе
                print("Ошибка: на складе не хватает этого продукта")  # Сообщение об ошибке
                continue  # Продолжение цикла для повторного ввода
            elif productQuantity >= 10:  # Проверка на превышение максимального количества
                print("Ошибка: вы превысили максимальное значение этого продукта")  # Сообщение об ошибке
                continue  # Продолжение цикла для повторного ввода
            return productQuantity  # Возвращение количества продукта

        except ValueError:  # Обработка исключения для некорректного ввода
            print("Ошибка: введите корректное число.")  # Сообщение об ошибке
            continue  # Продолжение цикла для повторного ввода


# Функция для приготовления пиццы
def craftPizza():
    # Загрузка продуктов из файла
    with open('maxProductsQuatity.json', 'r', encoding='utf-8') as file:
        maxProductsQuatity = json.load(file)  # Загружаем максимальные количества продуктов
    # Загрузка продуктов из файла
    with open('products.json', 'r', encoding='utf-8') as file:
        products = json.load(file)  # Загружаем доступные продукты
    # Загрузка продуктов из файла
    with open('pizzaProductsCost.json', 'r', encoding='utf-8') as file:
        pizzaProductsCost = json.load(file)  # Загружаем стоимость продуктов для пиццы
    pizzaCost = pizzaProductsCost['тесто']  # Инициализация стоимости пиццы с учетом теста
    print('Выберите то, из чего вы хотите сделать пиццу:')  # Запрос выбора ингредиентов

    # Показать продукты с 2 по 5
    for i, product in enumerate(products, start=1):  # Проход по всем продуктам
        if 1 < i < 8:  # Показать продукты с 2 по 5
            print(f' {product}')  # Вывод названия продукта

    while True:  # Бесконечный цикл для получения корректного ввода
        productName = input('Введите название продукта, который вы хотите добавить: ')  # Запрос на ввод названия продукта

        # Проверка на наличие продукта в списке
        if productName not in products:  # Если продукт не найден
            print("Ошибка: продукт не найден. Пожалуйста, выберите продукт из списка.")  # Сообщение об ошибке
            continue  # Продолжение цикла для повторного ввода

        try:
            # Запрос количества продукта
            productQuantity = int(input(f'Введите количество продукта (максимальное количество {maxProductsQuatity[productName]}): '))  # Запрос количества продукта

            # Проверка на положительное число
            if productQuantity <= 0:  # Если количество отрицательное или равно нулю
                print("Ошибка: количество должно быть положительным числом.")  # Сообщение об ошибке
                continue  # Продолжение цикла для повторного ввода

            # Проверка наличия на складе
            if not warehouse(productName, productQuantity):  # Если на складе не хватает продукта
                print("Ошибка: на складе не хватает этого продукта.")  # Сообщение об ошибке
                continue  # Продолжение цикла для повторного ввода

            # Проверка на превышение максимального количества
            if productQuantity > maxProductsQuatity[productName]:  # Если количество превышает максимальное
                print("Ошибка: вы превысили максимальное значение этого продукта.")  # Сообщение об ошибке
                continue  # Продолжение цикла для повторного ввода

        except ValueError:  # Обработка исключения для некорректного ввода
            print("Ошибка: введите корректное число.")  # Сообщение об ошибке
            continue  # Продолжение цикла для повторного ввода
        except KeyError:  # Обработка исключения для отсутствия ключа в словаре
            print(f"Ошибка: продукт '{productName}' не найден в максимальных количествах.")  # Сообщение об ошибке
            continue  # Продолжение цикла для повторного ввода
        except Exception as e:  # Обработка любых других исключений
            print(f"Произошла непредвиденная ошибка: {e}")  # Сообщение об ошибке
            continue  # Продолжение цикла для повторного ввода

        # Запрос на продолжение добавления ингредиентов
        if input('Если хотите продолжить добавление ингредиентов, введите 1, иначе любой другой символ: ') == '1':
            pizzaCost += pizzaProductsCost[productName] * productQuantity  # Увеличение стоимости пиццы
            continue  # Продолжение цикла для добавления других ингредиентов
        else:
            pizzaCost += pizzaProductsCost[productName] * productQuantity  # Увеличение стоимости пиццы
            return pizzaCost  # Возвращение итоговой стоимости пиццы


