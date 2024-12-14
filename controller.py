import sys
from model import busketSave
from model import reg_and_create_id
from model import craftPizza
from model import edit_cost
from view import buy
from view import check
from view import print_menu
from model import beerTypes

busket = []
def user(bornn_year):
    print_menu(bornn_year)

    try:
        print('Что вы хотели бы заказать?')
        user_input = int(input('Введите цифру соответствующую ващему выбору: '))
        if user_input == 8 and 2024-bornn_year>=18:
            user_number = craftPizza()
        elif user_input == 7 and 2024-bornn_year<18:
            user_number = craftPizza()
        elif user_input == 5 and 2024-bornn_year>=18:
            files = beerTypes()
            user_input = files[0]
            user_number = files[2]
        else:
            user_number = int(input('введите количество: '))
        busketSave(busket, user_input, bornn_year, user_number)
        if input('Для продолжения заказа введите 1, иначе любой символ: ')=='1':
            user(bornn_year)
        else:
            check(busket, buy(busket))
            print('♥♥♥Спасибо за заказ!♥♥♥\n   Приходите еще)')
            sys.exit()
    except KeyError:
        print('Такого варианта нет!!!')
        user(bornn_year)
    except ValueError:
        print('Введите число а не букву!!!')
        user(bornn_year)

def admin():
    print('Добро пожаловать в панель администратора пиццерии!')
    print('Доступные функции:\n 1 - вывод логов    \n 2 - чистка логов    \n 3 - вывод данных пользователей    \n 4 - изменение стоимости товаров    \n 5 - просмотр кол-ва продуктов на складе')
    while True:
        func_choise = int(input())

        if func_choise == 1:
            with open('logs.txt', 'r', encoding='utf-8') as file:
                logs = file.read()
            print(logs)
        elif func_choise == 2:
            with open('logs.txt', 'w', encoding='utf-8') as file:
                file.write('')
        elif func_choise == 3:
            with open('users_data.json', 'r', encoding='utf-8') as file:
                users_data = file.read()
            print(users_data)
        elif func_choise == 4:
            with open('cost.json', 'r', encoding='utf-8') as file:
                costs = file.read()
            print(f'Нынешние цены: {costs}')
            edit_cost(input('Продукт: '), int(input('Новая цена: ')))
        elif func_choise == 5:
            with open('products.json', 'r', encoding='utf-8') as file:
                poducts = file.read()
            print(poducts)
def openPizza():
    born_year = reg_and_create_id()

    if born_year == True:
        admin()
        with open('users_data.json', 'a', encoding='utf-8') as file:
                file.write(f'\nПользователь вошёл в админку')
    else:
        user(born_year)


