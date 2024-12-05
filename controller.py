import sys
from view import print_menu
from model import busketSave
from model import reg_and_create_id
from view import buy
from view import check
from model import craftPizza

busket = []
def zakaz(bornn_year):
    print_menu(bornn_year)

    try:
        print('Что вы хотели бы заказать?')
        user_input = int(input('Введите цифру соответствующую ващему выбору: '))
        if user_input == 8 and 2024-bornn_year>=18:
            craftPizza()
        elif user_input == 7 and 2024-bornn_year<18:
            craftPizza()
        else:
            user_number = int(input('введите количество: '))
        busketSave(busket, user_input, bornn_year, user_number)
        if input('Для продолжения заказа введите 1, иначе любой символ: ')=='1':
            zakaz(bornn_year)
        else:
            check(busket, buy(busket))
            print('♥♥♥Спасибо за заказ!♥♥♥\n   Приходите еще)')
            sys.exit()
    except KeyError:
        print('Такого варианта нет!!!')
        zakaz(bornn_year)
    except ValueError:
        print('Введите число а не букву!!!')
        zakaz(bornn_year)
def openPizza():
    born_year = reg_and_create_id()
    zakaz(born_year)
