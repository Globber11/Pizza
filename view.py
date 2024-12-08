import json
import dpath
def swap_quotes(s: str) -> str:
  dict = { '"':"'", "'":'"' }
  return ''.join(dict.get(c, c) for c in s)
with open('menu.json', 'r', encoding='utf-8') as file:
    menu = file.read()
    menu = json.loads(menu)
with open('menu18.json', 'r', encoding='utf-8') as file:
    menu18 = file.read()
    menu18 = json.loads(menu18)
with open('cost.json', 'r', encoding='utf-8') as file:
    cost = file.read()
    cost = json.loads(cost)
def check_decorator(func):
    def wrapper(*args, **kwargs):
        print("\n" + "="*30)
        func(*args, **kwargs)
        print("="*30 + "\n")
    return wrapper

@check_decorator
def check(buskett, listD):
    moreCost = 0
    print('Ваш чек:')
    for i in range(0,len(buskett),3):
        if buskett[i] == 'создать свою пиццу':
            print(f"{buskett[i]}: {buskett[i + 2]} x 1шт")
            moreCost += buskett[i + 2]
        else:
            print(f"{buskett[i]}: {buskett[i+1]} x {buskett[i+2]}шт")
            moreCost+=buskett[i+1]*buskett[i+2]
    print(' ')
    if listD[0]==1:
        print(f'Внесено: {listD[1]}')
        print(f'Оплачено: {moreCost}')
        print(f'Сдача: {listD[1]-moreCost}')
    else:
        print(f'Оплачено: {moreCost}')
    with open('check_number.txt', 'r') as file:
        check_number = file.read()
    print(f'Номер чека: {check_number}')
    with open('check_number.txt', 'w') as file:
        file.write(str(int(check_number) + 1))
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nВыбор товаров завершён, корзина: {buskett}')
        file.write(f'\nК оплате: {moreCost}, внесено: {listD[1]}, сдача: {int(listD[1])-moreCost}')
        file.write(f'\nКонец лога')
        file.write(f'\n')


def buy(buskett):
    from model import check_consumption
    mostCost = 0
    for i in range(0,len(buskett),3):
        if buskett[i] == 'создать свою пиццу':
            mostCost += buskett[i + 2]
        else:
            mostCost+=buskett[i+1]*buskett[i+2]
    print(f'Итого к оплате: {mostCost}')
    print('Оплата картой или наличными?')
    print('1)Наличные\n2)Карта')
    try:
        bought = int(input('Введите цифру соответствующую ващему выбору: '))
        check_consumption(bought)
    except ValueError:
        print('Введи числовое значение!!!')
        buy(buskett)
    CardOrNal = 0
    if bought==1:
        try:
            CardOrNal = int(input('Внесите сумму в рублях: '))
            if CardOrNal<mostCost:
                print('Нехватает денежных средств!!!')
            elif CardOrNal<0:
                print('Долги берут в банке а не в кафе!!!')
                buy(buskett)
        except ValueError:
            print('Введи числовое значение!!!')
            buy(buskett)
    elif bought==2:
        pass
    else:
        print('Такого варианта ответа нет!!!')
        buy(buskett)
    return [bought, CardOrNal]
def printMenu():
    print('Меню: ')
    for i in range(1, 8):
        menu_ = str(i)
        print(f'   {i}){dpath.get(menu, menu_)}: {dpath.get(cost, dpath.get(menu, menu_))}')
def printMenu18():
    print('Меню: ')
    for i in range(1, 9):
        menu18_ = str(i)
        print(f'   {i}){dpath.get(menu18, menu18_)}: {dpath.get(cost, dpath.get(menu18, menu18_))}')
def print_menu(born_year):
    if 2024-born_year>=18:
        printMenu18()
    else:
        printMenu()
