import sys  # Импортируем модуль sys для использования функции exit
from model import busketSave  # Импортируем функцию для сохранения заказа в корзину
from model import reg_and_create_id  # Импортируем функцию регистрации и создания ID
from model import craftPizza  # Импортируем функцию для создания пиццы
from model import edit_cost  # Импортируем функцию изменения стоимости продуктов
from view import buy  # Импортируем функцию для обработки покупки
from view import check  # Импортируем функцию для проверки заказа
from view import print_menu  # Импортируем функцию для вывода меню
from model import beerTypes  # Импортируем функцию для выбора пива

busket = []  # Инициализация пустого списка для хранения заказов

def user(bornn_year):
    print_menu(bornn_year)  # Выводим меню в зависимости от года рождения пользователя

    try:
        print('Что вы хотели бы заказать?')  # Запрос на выбор продукта
        user_input = int(input('Введите цифру соответствующую вашему выбору: '))  # Ввод выбора пользователя
        # Проверяем условия для создания пиццы и выбора пива
        if user_input == 8 and 2024 - bornn_year >= 18:
            user_number = craftPizza()  # Создание пиццы для взрослых
        elif user_input == 7 and 2024 - bornn_year < 18:
            user_number = craftPizza()  # Создание пиццы для молодежи
        elif user_input == 5 and 2024 - bornn_year >= 18:
            files = beerTypes()  # Выбор пива, если пользователь взрослый
            user_input = files[0]  # Получаем название пива
            user_number = files[2]  # Получаем количество пива
        else:
            user_number = int(input('Введите количество: '))  # Запрос количества товара

        # Вызываем функцию для сохранения заказа в корзину
        busketSave(busket, user_input, bornn_year, user_number)

        # Запрос на продолжение заказа
        if input('Для продолжения заказа введите 1, иначе любой символ: ') == '1':
            user(bornn_year)  # Рекурсивный вызов для продолжения заказа
        else:
            check(busket, buy(busket))  # Проверка и завершение заказа
            print('♥♥♥Спасибо за заказ!♥♥♥\n   Приходите еще)')  # Сообщение об успешном заказе
            sys.exit()  # Завершаем программу
    except KeyError:  # Обработка ошибки, если выбран несуществующий продукт
        print('Такого варианта нет!!!')
        user(bornn_year)  # Рекурсивный вызов для повторного ввода
    except ValueError:  # Обработка ошибки, если введено не числовое значение
        print('Введите число а не букву!!!')
        user(bornn_year)  # Рекурсивный вызов для повторного ввода

def admin():
    print('Добро пожаловать в панель администратора пиццерии!')  # Приветствие админа
    print('Доступные функции:\n 1 - вывод логов    \n 2 - чистка логов    \n 3 - вывод данных пользователей    \n 4 - изменение стоимости товаров    \n 5 - просмотр кол-ва продуктов на складе')
    while True:
        func_choise = int(input())  # Ввод выбора функции администратором

        if func_choise == 1:  # Вывод логов
            with open('logs.txt', 'r', encoding='utf-8') as file:
                logs = file.read()  # Чтение логов из файла
            print(logs)  # Вывод логов
        elif func_choise == 2:  # Чистка логов
            with open('logs.txt', 'w', encoding='utf-8') as file:
                file.write('')  # Очищаем содержимое лога
        elif func_choise == 3:  # Вывод данных пользователей
            with open('users_data.json', 'r', encoding='utf-8') as file:
                users_data = file.read()  # Чтение данных пользователей из файла
            print(users_data)  # Вывод данных пользователей
        elif func_choise == 4:  # Изменение стоимости товаров
            with open('cost.json', 'r', encoding='utf-8') as file:
                costs = file.read()  # Чтение текущих цен из файла
            print(f'Нынешние цены: {costs}')  # Вывод текущих цен
            edit_cost(input('Продукт: '), int(input('Новая цена: ')))  # Запрос на изменение цены
        elif func_choise == 5:  # Просмотр количества продуктов на складе
            with open('products.json', 'r', encoding='utf-8') as file:
                poducts = file.read()  # Чтение данных о продуктах из файла
            print(poducts)  # Вывод данных о продуктах

def openPizza():
    born_year = reg_and_create_id()  # Регистрация пользователя и получение года рождения

    if born_year == True:  # Проверка на наличие доступа к админке
        admin()  # Переход в админку
        with open('users_data.json', 'a', encoding='utf-8') as file:
            file.write(f'\nПользователь вошёл в админку')  # Логируем вход в админку
    else:
        user(born_year)  # Переход к пользовательскому интерфейсу


