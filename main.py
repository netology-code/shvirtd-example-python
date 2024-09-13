from flask import Flask, request, jsonify
import os
import mysql.connector
from datetime import datetime
import logging
import time

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение данных для подключения к базе данных из переменных окружения
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_NAME')

if not all([db_host, db_user, db_password, db_database]):
    logging.error("Необходимо задать все переменные окружения: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME.")
    raise EnvironmentError("Отсутствуют необходимые переменные окружения для подключения к базе данных.")

def get_db_connection():
    """Подключение к базе данных с обработкой ошибок и ожиданием первичной инициализации"""
    retries = 5  # Количество попыток подключения
    delay = 5  # Задержка между попытками в секундах

    while retries > 0:
        try:
            connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_database,
                autocommit=True
            )
            return connection
        except mysql.connector.Error as err:
            logging.warning(f"Не удалось подключиться к базе данных: {err}. Это первичный запуск? Ждем инициализации MYSQL. Повторная попытка через {delay} секунд...")
            retries -= 1
            time.sleep(delay)

    # Если после всех попыток подключение не удалось
    logging.error("Невозможно подключиться к базе данных после 5 попыток.")
    raise mysql.connector.Error("Не удалось подключиться к базе данных.")

def create_table():
    """Создание таблицы при запуске приложения"""
    try:
        db = get_db_connection()
        cursor = db.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {db_database}.requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            request_date DATETIME,
            request_ip VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
        logging.error(f"Ошибка создания таблицы: {err}")
        raise

# Создание таблицы при старте приложения
create_table()

@app.route('/')
def index():
    try:
        # Получение IP-адреса пользователя только из заголовка X-Forwarded-For
        ip_address = request.headers.get('X-Forwarded-For')

        if not ip_address:
            return jsonify({'error': 'IP-адрес не найден в заголовке X-Forwarded-For'}), 400

        # Запись в базу данных
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO requests (request_date, request_ip) VALUES (%s, %s)"
        values = (current_time, ip_address)

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(query, values)
        cursor.close()
        db.close()

        return jsonify({'time': current_time, 'ip': ip_address})
    except mysql.connector.Error as err:
        logging.error(f"Ошибка записи в базу данных: {err}")
        return jsonify({'error': 'Ошибка работы с базой данных'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
