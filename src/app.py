import sqlite3  # база данных
from car_dao import select_data, add_user_data, update_color, del_car
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


@app.route('/cars', methods=['GET'])
def get_cars():
    logger.info("Принят запрос на список автомобилей от клиента из базы данных")
    cars = select_data()
    record_count = len(cars)

    if record_count == 0:
        logger.info("Запрос выполнен успешно: база данных пуста.")
    else:
        logger.info("Запрос выполнен успешно: клиенту направлено %d записей из базы данных.", record_count)

    return jsonify(cars)


@app.route('/cars', methods=['POST'])
def post_cars():
    logger.info("Принят запрос от клиента на добавление новой машины в базу данных")
    data = request.get_json()
    new_car = {
        "model": data["model"],
        "color": data["color"]
    }
    add_user_data(new_car)
    logger.info("Запрос на добавление новой машины в базу данных выполнен успешно")
    return "Запись добавлена", 201


@app.route('/cars/<int:car_id>/color', methods=['PUT'])
def update_car(car_id):
    logger.info("Принят запрос от клиента на изменение цвета машины с id = %d", car_id)
    cars = select_data()
    # проверяем, есть ли запись в БД
    flag = False
    for car in cars:
        if car_id in car:
            flag = True
    if flag is False:
        logger.error("Машина с id = %d в базе данных не найдена", car_id)
        return jsonify({"error": "Машина не найдена"}), 404

    # Получаем JSON данные из запроса
    data = request.get_json()

    # Обновляем цвет машины
    new_color = data["color"]
    update_color(car_id, new_color)
    logger.info("Цвет машины обновлен. Новый цвет: %s", new_color)

    return "ок", 200


@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    logger.info("Принят запрос от клиента на удаление машины с id = %d", car_id)
    cars = select_data()
    # проверяем, есть ли запись в БД
    flag = False
    for car in cars:
        if car_id in car:
            flag = True
    if flag is False:
        logger.error("Машина с id = %d в базе данных не найдена", car_id)
        return jsonify({"error": "Машина не найдена"}), 404

    # Удаляем запись из бд
    del_car(car_id)
    record_count = len(select_data())
    logger.info("Машина с id = %d удалена из базы данных. В базе данных осталось %d машин", car_id, record_count)

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
