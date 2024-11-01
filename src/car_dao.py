import sqlite3  # база данных
from logging import getLogger, basicConfig, DEBUG  # для логирования

# настраиваем логирование
logger = getLogger(__name__)  # создаем логера с таким же именем как у файла
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # формат вывода время-название файла-уровень-сообщение
basicConfig(level=DEBUG, format=FORMAT)  # устанавливаем самый низкий уровень логирования, куда и в каком виде сохраняем логи


with sqlite3.connect('cars.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()
logger.info("Подключение к базе данных")


#  кладем данные из бд в список
def select_data():
    logger.info("В базу данных отправлен запрос на получение списка всех записей")
    cursor.execute("SELECT * FROM cars")
    cars_list = cursor.fetchall()
    logger.info("Список автомобилей получен. Элементов в списке - %d", len(cars_list))
    return cars_list


# метод добавляет новые данные в бд
def add_user_data(data):
    logger.info("В базу данных отправлен запрос на добавление новой записи")
    data_list = []
    for value in data.values():
        data_list.append(value)
    query = " INSERT INTO cars (model, color) VALUES(?,?); "
    cursor.execute(query, tuple(data_list))
    connection.commit()
    logger.info("Новая запись добавлена в базу данных")


# метод обновляет данные в бд (цвет автомобиля)
def update_color(car_id, new_color):
    logger.info("В базу данных отправлен запрос на изменение записи с id = %d", car_id)
    query = " UPDATE cars SET color = ? WHERE id = ? "
    cursor.execute(query, (new_color, car_id))
    connection.commit()
    logger.info("Запись с id = %d успешно изменена", car_id)


# метод удаляет запись из бд
def del_car(car_id):
    logger.info("В базу данных отправлен запрос на удаление записи с id = %d", car_id)
    query = "DELETE FROM cars WHERE id = ?"
    cursor.execute(query, (car_id,))
    connection.commit()
    logger.info("Запись с id = %d успешно удалена", car_id)
