import sys  # Импортируем модуль sys для работы с системными функциями
from model import busketSave  # Импортируем функцию для сохранения заказов в корзину
from model import reg_and_create_id  # Импортируем функцию для регистрации и создания ID пользователя
from model import craftPizza  # Импортируем функцию для создания пиццы
from model import edit_cost  # Импортируем функцию для изменения стоимости товаров
from view import buy  # Импортируем функцию для обработки покупки
from view import check  # Импортируем функцию для проверки заказа
from view import print_menu  # Импортируем функцию для отображения меню

# Инициализация пустого списка для хранения заказов
busket = []

def user(bornn_year):
    # Отображаем меню для пользователя
    print_menu(bornn_year)

    try:
        print('Что вы хотели бы заказать?')  # Запрашиваем у пользователя заказ
        user_input = int(input('Введите цифру соответствующую вашему выбору: '))  # Получаем выбор пользователя
        # Проверяем условия для создания пиццы в зависимости от возраста
        if user_input == 8 and 2024 - bornn_year >= 18:
            craftPizza()  # Создаем пиццу, если пользователь совершеннолетний
        elif user_input == 7 and 2024 - bornn_year < 18:
            craftPizza()  # Создаем пиццу, если пользователь несовершеннолетний
        else:
            user_number = int(input('Введите количество: '))  # Запрашиваем количество товара
        # Сохраняем заказ в корзину
        busketSave(busket, user_input, bornn_year, user_number)
        # Запрашиваем, хочет ли пользователь продолжить заказ
        if input('Для продолжения заказа введите 1, иначе любой символ: ') == '1':
            user(bornn_year)  # Рекурсивный вызов функции для продолжения заказа
        else:
            # Проверяем заказ и завершаем, выводим благодарность
            check(busket, buy(busket))
            print('♥♥♥Спасибо за заказ!♥♥♥\n   Приходите еще)')
            sys.exit()  # Выход из программы
    except KeyError:
        print('Такого варианта нет!!!')  # Обработка ошибки, если выбран неправильный вариант
        user(bornn_year)  # Повторный вызов функции для нового выбора
    except ValueError:
        print('Введите число, а не букву!!!')  # Обработка ошибки, если введено нечисловое значение
        user(bornn_year)  # Повторный вызов функции для нового выбора

def admin():
    print('Добро пожаловать в панель администратора пиццерии!')  # Приветствие для администратора
    print('Доступные функции:\n 1 - вывод логов    \n 2 - чистка логов    \n 3 - вывод данных пользователей    \n 4 - изменение стоимости товаров    \n 5 - просмотр кол-ва продуктов на складе')
    while True:  # Бесконечный цикл для работы в админ-панели
        func_choise = int(input())  # Получаем выбор функции от администратора

        # Обработка выбора администратора
        if func_choise == 1:
            # Вывод логов
            with open('logs.txt', 'r', encoding='utf-8') as file:
                logs = file.read()
            print(logs)
        elif func_choise == 2:
            # Чистка логов
            with open('logs.txt', 'w', encoding='utf-8') as file:
                file.write('')  # Очищаем содержимое файла
        elif func_choise == 3:
            # Вывод данных пользователей
            with open('users_data.json', 'r', encoding='utf-8') as file:
                users_data = file.read()
            print(users_data)
        elif func_choise == 4:
            # Изменение стоимости товаров
            with open('cost.json', 'r', encoding='utf-8') as file:
                costs = file.read()
            print(f'Нынешние цены: {costs}')  # Вывод текущих цен
            edit_cost(input('Продукт: '), int(input('Новая цена: ')))  # Запрос нового значения цены
        elif func_choise == 5:
            # Просмотр количества продуктов на складе
            with open('products.json', 'r', encoding='utf-8') as file:
                poducts = file.read()
            print(poducts)

def openPizza():
    # Регистрация и создание ID пользователя
    born_year = reg_and_create_id()

    # Проверка, успешно ли прошла регистрация
    if born_year == True:
        admin()  # Если да, то переходим в админку
        with open("logs.txt", "a", encoding='utf-8') as file:
            file.write(f'\nВыполнен вход в панель администратора')  # Записываем вход в логи
    else:
        user(born_year)  # Если нет, то переходим в режим пользователя

