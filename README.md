# Документация по использованию online-пиццерии
**1) Использование обычным пользователем:**

При запуске программы необходимо ввести свои данные: имя, фамилию, номер телефона и год рождения

На основе этих данных программа сгенерирует ID пользователя

Далее необходимо выбрать товары следуя инструкциям программы

После выбрать метод и произвети её

**2) Использование панели администратора:**

Если при регистрации/авторизации в имя и фамилию ввести логин и пароль администратора то вы попадёте на админ-панель

На ней можно: просматривать и очищать логи, просматривать данные всех польхователей, просматривать сколько продуктов осталось на складе и изменять стоимость товаров

**3) Краткая документация:**

Файл main: он производит запуск всей программы

Файл model: в нём содержится вся логика программы, большая часть функций

Файл view: содержит все функции отвечающие за взаимодействие с пользователем

Файл controller: является главным файлом и связующим model и view
