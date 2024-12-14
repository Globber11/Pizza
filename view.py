import json
import dpath

# Функция для замены кавычек в строке
def swap_quotes(s: str) -> str:
    dict = { '"':"'", "'":'"' }  # Словарь для замены кавычек
    return ''.join(dict.get(c, c) for c in s)  # Создание новой строки с заменёнными кавычками

# Загрузка данных меню и цен из JSON файлов
with open('menu.json', 'r', encoding='utf-8') as file:
    menu = file.read()
    menu = json.loads(menu)  # Декодируем содержимое в формат JSON

with open('menu18.json', 'r', encoding='utf-8') as file:
    menu18 = file.read()
    menu18 = json.loads(menu18)  # Декодируем содержимое в формат JSON

with open('cost.json', 'r', encoding='utf-8') as file:
    cost = file.read()
    cost = json.loads(cost)  # Декодируем содержимое в формат JSON

# Декоратор для оборачивания функции с выводом разделителей
def check_decorator(func):
    def wrapper(*args, **kwargs):
        print("\n" + "="*30)  # Перед выполнением функции печатаем разделитель
        func(*args, **kwargs)  # Вызываем оборачиваемую функцию
        print("="*30 + "\n")  # После выполнения функции печатаем разделитель
    return wrapper

@check_decorator
def check(buskett, listD):
    moreCost = 0  # Инициализируем переменную для расчета стоимости
    print('Ваш чек:')  # Выводим заголовок для чека
    # Обработка элементов в корзине пользователя
    for i in range(0, len(buskett), 3):
        if buskett[i] == 'создать свою пиццу':
            print(f"{buskett[i]}: {buskett[i + 2]} x 1шт")  # Специальный вывод для "создать свою пиццу"
            moreCost += buskett[i + 2]  # Добавляем стоимость
        elif buskett[i] == 'пиво':
            print(f"{buskett[i]}: {buskett[i + 1]} x {buskett[i + 2]}шт")  # Вывод для пива
            moreCost += buskett[i + 2]  # Добавляем количество пива к общей стоимости
        else:
            print(f"{buskett[i]}: {buskett[i + 1]} x {buskett[i + 2]}шт")  # Вывод для других продуктов
            moreCost += buskett[i + 1] * buskett[i + 2]  # Добавляем стоимость продукта

    print(' ')
    # Обработка информации о внесенной сумме
    if listD[0] == 1:  # Если первая часть данных содержит 1
        print(f'Внесено: {listD[1]}')  # Выводим внесенную сумму
        print(f'Оплачено: {moreCost}')  # Выводим общую стоимость
        print(f'Сдача: {listD[1] - moreCost}')  # Вычисляем сдачу
    else:
        print(f'Оплачено: {moreCost}')  # Если не наличные, просто выводим сумму к оплате

    # Чтение номера чека из файла
    with open('check_number.txt', 'r') as file:
        check_number = file.read()

    print(f'Номер чека: {check_number}')  # Вывод номера чека

    # Обновление номера чека в файле
    with open('check_number.txt', 'w') as file:
        file.write(str(int(check_number) + 1))  # Увеличиваем номер чека на 1

    # Логирование покупки
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nВыбор товаров завершён, корзина: {buskett}')
        file.write(f'\nК оплате: {moreCost}, внесено: {listD[1]}, сдача: {int(listD[1]) - moreCost}')
        file.write(f'\nКонец лога')
        file.write(f'\n')

def buy(buskett):
    from model import check_consumption  # Импортируем функцию проверки наличия продуктов
    mostCost = 0  # Переменная для хранения итоговой стоимости
    # Расчет общей стоимости продуктов в корзине
    for i in range(0, len(buskett), 3):
        if buskett[i] == 'создать свою пиццу':
            mostCost += buskett[i + 2]  # Добавляем стоимость создания пиццы
        elif buskett[i] == 'пиво':
            mostCost += buskett[i + 2]  # Добавляем стоимость пива
        else:
            mostCost += buskett[i + 1] * buskett[i + 2]  # Добавляем стоимость других продуктов

    print(f'Итого к оплате: {mostCost}')  # Выводим общую сумму к оплате
    print('Оплата картой или наличными?')
    print('1) Наличные\n2) Карта')  # Предлагаем выбор способа оплаты

    try:
        bought = int(input('Введите цифру соответствующую вашему выбору: '))  # Получаем выбор пользователя
        check_consumption(bought)  # Проверяем возможность покупки
    except ValueError:
        print('Введи числовое значение!!!')  # Обработка ошибки ввода
        buy(buskett)  # Повторный вызов функции

    CardOrNal = 0  # Инициализация переменной для хранения суммы

    if bought == 1:  # Если выбраны наличные
        try:
            CardOrNal = int(input('Внесите сумму в рублях: '))  # Вводим сумму
            if CardOrNal < mostCost:  # Проверка на наличие достаточной суммы
                print('Нехватает денежных средств!!!')
            elif CardOrNal < 0:  # Проверка на отрицательное значение
                print('Долги берут в банке, а не в кафе!!!')
                buy(buskett)  # Повторный вызов функции
        except ValueError:
            print('Введи числовое значение!!!')  # Обработка ошибки ввода
            buy(buskett)  # Повторный вызов функции
    elif bought == 2:
        pass  # Если выбрана оплата картой, пропускаем дополнительные действия
    else:
        print('Такого варианта ответа нет!!!')  # Обработка неверного выбора
        buy(buskett)  # Повторный вызов функции

    return [bought, CardOrNal]  # Возвращаем способ и сумму оплаты

def printMenu():
    # Функция для вывода меню
    print('Меню: ')
    for i in range(1, 8):
        menu_ = str(i)  # Преобразуем индекс в строку
        print(f'   {i}){dpath.get(menu, menu_)}: {dpath.get(cost, dpath.get(menu, menu_))}')  # Выводим меню и цен

def printMenu18():
    # Функция для вывода меню с элементами, доступными только для старше 18 лет
    print('Меню: ')
    for i in range(1, 9):
        menu18_ = str(i)  # Преобразуем индекс в строку
        print(f'   {i}){dpath.get(menu18, menu18_)}: {dpath.get(cost, dpath.get(menu18, menu18_))}')  # Выводим меню и цен

def print_menu(born_year):
    # Функция, определяющая, какое меню выводить в зависимости от возраста
    if 2024 - born_year >= 18:  # Проверка, достаточно ли возраст
        printMenu18()  # Выводим меню для взрослых
    else:
        printMenu()  # Выводим меню для молодежи


