import sqlite3  # база данных
from logging import getLogger, basicConfig, DEBUG  # для логирования
from flask import Flask, jsonify, request


# настраиваем логирование
logger = getLogger()  # создание своего логера
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # формат вывода время-название файла-уровень-сообщение
basicConfig(level=DEBUG, format=FORMAT)  # устанавливаем самый низкий уровень логирования, куда и в каком виде сохраняем логи


with sqlite3.connect('cars.sqlite', check_same_thread=False) as connection:
    cursor = connection.cursor()
logger.info("Подключение к базе данных")


app = Flask(__name__)


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


@app.route('/cars', methods=['GET'])
def get_cars():
    cars = select_data()
    logger.info(cars)
    return jsonify(cars)


@app.route('/cars', methods=['POST'])
def post_cars():
    data = request.get_json()
    new_car = {
        "model": data["model"],
        "color": data["color"],
        "transmission": data["transmission"],
        "quantity": data["quantity"]
    }

    add_user_data(data)
    # Возвращаем ответ с кодом 201 (Created) и новыми данными
    return jsonify(new_car), 201


if __name__ == "__main__":
    app.run(debug=True)
