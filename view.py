import json  # Импортируем модуль для работы с JSON-форматом
import dpath  # Импортируем модуль для работы с путями в словарях

def swap_quotes(s: str) -> str:
    # Функция для замены кавычек в строке
    dict = { '"':"'", "'":'"' }  # Создаём словарь для замены одинарных и двойных кавычек
    return ''.join(dict.get(c, c) for c in s)  # Возвращаем строку с заменёнными кавычками

# Открываем файл menu.json для чтения и загружаем его содержимое в переменную menu
with open('menu.json', 'r', encoding='utf-8') as file:
    menu = file.read()  # Читаем содержимое файла
    menu = json.loads(menu)  # Загружаем данные из JSON в словарь

# Открываем файл menu18.json для чтения и загружаем его содержимое в переменную menu18
with open('menu18.json', 'r', encoding='utf-8') as file:
    menu18 = file.read()  # Читаем содержимое файла
    menu18 = json.loads(menu18)  # Загружаем данные из JSON в словарь

# Открываем файл cost.json для чтения и загружаем его содержимое в переменную cost
with open('cost.json', 'r', encoding='utf-8') as file:
    cost = file.read()  # Читаем содержимое файла
    cost = json.loads(cost)  # Загружаем данные из JSON в словарь

def check_decorator(func):
    # Декоратор для обрамления функции с выводом разделителей
    def wrapper(*args, **kwargs):
        print("\n" + "="*30)  # Выводим разделитель перед вызовом функции
        func(*args, **kwargs)  # Вызываем оборачиваемую функцию
        print("="*30 + "\n")  # Выводим разделитель после вызова функции
    return wrapper

@check_decorator
def check(buskett, listD):
    # Функция для проверки и вывода чека
    moreCost = 0  # Инициализируем переменную для подсчета общей стоимости
    print('Ваш чек:')  # Выводим заголовок чека
    for i in range(0, len(buskett), 3):
        if buskett[i] == 'создать свою пиццу':
            # Если выбрана опция "создать свою пиццу"
            print(f"{buskett[i]}: {buskett[i + 2]} x 1шт")  # Выводим информацию о пицце
            moreCost += buskett[i + 2]  # Добавляем стоимость пиццы к общей
        else:
            # Для остальных товаров
            print(f"{buskett[i]}: {buskett[i + 1]} x {buskett[i + 2]}шт")  # Выводим информацию о товаре
            moreCost += buskett[i + 1] * buskett[i + 2]  # Добавляем стоимость товара к общей
    print(' ')
    if listD[0] == 1:
        # Если оплата наличными
        print(f'Внесено: {listD[1]}')  # Выводим внесённую сумму
        print(f'Оплачено: {moreCost}')  # Выводим общую стоимость
        print(f'Сдача: {listD[1] - moreCost}')  # Выводим сдачу
    else:
        print(f'Оплачено: {moreCost}')  # Выводим общую стоимость для оплаты картой

    # Читаем номер чека из файла
    with open('check_number.txt', 'r') as file:
        check_number = file.read()  # Получаем текущий номер чека
    print(f'Номер чека: {check_number}')  # Выводим номер чека

    # Записываем новый номер чека в файл
    with open('check_number.txt', 'w') as file:
        file.write(str(int(check_number) + 1))  # Увеличиваем номер чека на 1 и записываем

    # Записываем информацию о покупке в лог-файл
    with open("logs.txt", "a", encoding='utf-8') as file:
        file.write(f'\nВыбор товаров завершён, корзина: {buskett}')  # Логируем содержимое корзины
        file.write(f'\nК оплате: {moreCost}, внесено: {listD[1]}, сдача: {int(listD[1])-moreCost}')  # Логируем информацию о платеже
        file.write(f'\nКонец лога')  # Логируем конец записи

def buy(buskett):
    # Функция для обработки покупки
    from model import check_consumption  # Импортируем функцию проверки потребления
    mostCost = 0  # Переменная для подсчета общей стоимости
    for i in range(0, len(buskett), 3):
        if buskett[i] == 'создать свою пиццу':
            mostCost += buskett[i + 2]  # Добавляем стоимость пиццы
        else:
            mostCost += buskett[i + 1] * buskett[i + 2]  # Добавляем стоимость других товаров
    print(f'Итого к оплате: {mostCost}')  # Выводим общую стоимость
    print('Оплата картой или наличными?')  # Запрашиваем способ оплаты
    print('1)Наличные\n2)Карта')  # Выводим варианты оплаты
    try:
        bought = int(input('Введите цифру соответствующую вашему выбору: '))  # Считываем выбор пользователя
        check_consumption(bought)  # Проверяем допустимость выбора
    except ValueError:
        print('Введи числовое значение!!!')  # Обработка ошибки ввода
        buy(buskett)  # Повторный вызов функции

    CardOrNal = 0  # Переменная для хранения суммы, внесённой при оплате наличными
    if bought == 1:
        try:
            CardOrNal = int(input('Внесите сумму в рублях: '))  # Считываем сумму
            if CardOrNal < mostCost:
                print('Нехватает денежных средств!!!')  # Проверка на недостаток средств
            elif CardOrNal < 0:
                print('Долги берут в банке а не в кафе!!!')  # Проверка на отрицательное значение
                buy(buskett)  # Повторный вызов функции
        except ValueError:
            print('Введи числовое значение!!!')  # Обработка ошибки ввода
            buy(buskett)  # Повторный вызов функции
    elif bought == 2:
        pass  # Если выбрана оплата картой, ничего не делаем
    else:
        print('Такого варианта ответа нет!!!')  # Обработка некорректного выбора
        buy(buskett)  # Повторный вызов функции
    return [bought, CardOrNal]  # Возвращаем метод оплаты и сумму

def printMenu():
    # Функция для вывода меню
    print('Меню: ')  # Заголовок меню
    for i in range(1, 8):
        menu_ = str(i)  # Превращаем номер в строку
        print(f'   {i}){dpath.get(menu, menu_)}: {dpath.get(cost, dpath.get(menu, menu_))}')  # Выводим наименование и стоимость

def printMenu18():
    # Функция для вывода меню для людей старше 18 лет
    print('Меню: ')  # Заголовок меню
    for i in range(1, 9):
        menu18_ = str(i)  # Превращаем номер в строку
        print(f'   {i}){dpath.get(menu18, menu18_)}: {dpath.get(cost, dpath.get(menu18, menu18_))}')  # Выводим наименование и стоимость

def print_menu(born_year):
    # Функция для выбора меню в зависимости от возраста
    if 2024 - born_year >= 18:
        printMenu18()  # Если клиенту 18 лет и больше, выводим меню для взрослых
    else:
        printMenu()  # В противном случае выводим стандартное меню

