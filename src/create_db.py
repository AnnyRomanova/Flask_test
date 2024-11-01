import sqlite3  # база данных
from logging import getLogger, basicConfig, DEBUG  # для логирования

# настраиваем логирование
logger = getLogger(__name__)  # создаем логера с таким же именем как у файла
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # формат вывода время-название файла-уровень-сообщение
basicConfig(level=DEBUG, format=FORMAT)  # устанавливаем самый низкий уровень логирования, куда и в каком виде сохраняем логи


with sqlite3.connect('cars.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()
logger.info("Подключение к базе данных")


def create_db():
    logger.info("Запрос на создание базы данных")
    cursor.execute("""CREATE TABLE cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT,
        color TEXT
        )""")
    logger.info("База данных с пустыми полями создана")


# Добавляем данные в таблицу
def fill_the_table():
    logger.info("Запрос на заполнение базы данных")
    query_list = [
        ('volkswagen', 'синий'),
        ('Lamborghini', 'красный'),
        ('Toyota', 'серебристый')
     ]
    query = """ INSERT INTO cars (model, color) VALUES(?,?); """

    cursor.executemany(query, query_list)

    connection.commit()  # обновляем бд
    logger.info("Таблица в базе данных заполнена. Количество записей: %d", len(query_list))


# Создаем бд
create_db()

# Заполняем БД
fill_the_table()



