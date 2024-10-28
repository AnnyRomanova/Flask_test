import sqlite3  # база данных
from logging import getLogger, basicConfig, DEBUG  # для логирования

# настраиваем логирование
logger = getLogger()  # создание своего логера
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # формат вывода время-название файла-уровень-сообщение
basicConfig(level=DEBUG, format=FORMAT)  # устанавливаем самый низкий уровень логирования, куда и в каком виде сохраняем логи


with sqlite3.connect('cars.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()
logger.info("Подключение к базе данных")


def create_db():
    cursor.execute("""CREATE TABLE cars (
        model text,
        color text,
        transmission text,
        quantity text
        )""")
    logger.info("База данных с полями создана")


# Добавляем данные в таблицу
def fill_the_table():
    query_list = [
        ('volkswagen', 'синий', 'автомат', "5"),
        ('Lamborghini', 'красный', 'автомат', "3"),
        ('Toyota', 'серебристый', 'механика', "10")
     ]
    query = """ INSERT INTO cars (model, color, transmission, quantity) VALUES(?,?,?,?); """

    cursor.executemany(query, query_list)

    connection.commit()  # обновляем бд
    logger.info("Таблица в базе данных заполнена")


# Создаем бд
create_db()

# Заполняем БД
fill_the_table()



