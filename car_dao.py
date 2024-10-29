import sqlite3  # база данных
from logging import getLogger, basicConfig, DEBUG  # для логирования

# настраиваем логирование
logger = getLogger()  # создание своего логера
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # формат вывода время-название файла-уровень-сообщение
basicConfig(level=DEBUG, format=FORMAT)  # устанавливаем самый низкий уровень логирования, куда и в каком виде сохраняем логи


with sqlite3.connect('cars.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()
logger.info("Подключение к базе данных")


#  кладем данные из бд в список
def select_data():
    cursor.execute("SELECT * FROM cars")
    cars_list = cursor.fetchall()
    logger.info("Получены данные из базы данных")
    return cars_list


# метод добавляет новые данные в бд
def add_user_data(data):
    data_list = []
    for value in data.values():
        data_list.append(value)
    query = " INSERT INTO cars (model, color, transmission, quantity) VALUES(?,?,?,?); "
    cursor.execute(query, tuple(data_list))
    connection.commit()
    logger.debug("Добавлены новые данные в БД")