"""Модуль для работы с PostgreSQL базой данных паролей."""
import psycopg2
from .utils import hash_password


class PasswordDB:
    """Класс для работы с PostgreSQL базой данных паролей."""

    def __init__(self):
        """Инициализация подключения к PostgreSQL базе данных."""
        self.init_database()  # Инициализация базы данных

    def get_connection(self, dbname="passwords_db"):
        """Создает и возвращает соединение с PostgreSQL базой данных."""
        return psycopg2.connect(
            dbname=dbname,
            user="anna",
            password="12345",
            host="localhost",  # хост (ищем программу на этом же компьютере)
            port="5432"  # порт (по умолчанию для PostgreSQL)
        )

    def init_database(self):
        """Создает базу данных и таблицу, если они не существуют."""
        try:
            # Сначала подключаемся к стандартной базе postgres
            conn = psycopg2.connect(
                dbname="postgres",
                user="anna",
                password="12345",
                host="localhost",
                port="5432"
            )
            conn.autocommit = True  # Для создания базы данных (автоматическое подтверждение изменений)

            cursor = conn.cursor()  # создаем объект курсора(выполняет SQL-запросы к базе данных)

            # проверка существования базы данных в PostgreSQL
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'passwords_db'")
            exists = cursor.fetchone()  # результат запроса в виде списка кортежей

            if not exists:
                cursor.execute('CREATE DATABASE passwords_db')
                print("✅ База данных passwords_db создана")

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"❌ Ошибка при создании базы данных: {e}")
            return

        # Теперь подключаемся к нашей базе и создаем таблицу
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS passwords (
                        id SERIAL PRIMARY KEY,                       
                        service TEXT NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')    # Автоматически увеличивающееся целое число (первичный ключ)
                conn.commit()
                print("✅ Таблица passwords создана в PostgreSQL")
        except Exception as e:
            print(f"❌ Ошибка при создании таблицы: {e}")

    def save_password(self, service, password):
        """Сохраняет хэш пароля в PostgreSQL базу данных.

        Args:
            service: Название сервиса
            password: Пароль в открытом виде
        """
        hashed_pw = hash_password(password)

        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Проверяем, существует ли уже запись для этого сервиса
            cursor.execute('SELECT id FROM passwords WHERE service = %s', (service,))
            existing = cursor.fetchone()

            if existing:
                # Обновляем существующую запись
                cursor.execute(
                    'UPDATE passwords SET password_hash = %s WHERE service = %s',
                    (hashed_pw, service)
                )
                print(f"✅ Пароль для '{service}' обновлен в PostgreSQL")
            else:
                # Создаем новую запись (указываем таблицу для вставки)
                cursor.execute(
                    'INSERT INTO passwords (service, password_hash) VALUES (%s, %s)',
                    (service, hashed_pw)
                )
                print(f"✅ Пароль для '{service}' сохранен в PostgreSQL")

            conn.commit()

    def find_password(self, service):
        """Находит хэш пароля по названию сервиса в PostgreSQL.

        Args:
            service: Название сервиса

        Returns:
            str or None: Хэш пароля или None если не найден
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT password_hash FROM passwords WHERE service = %s',
                (service,)
            )
            result = cursor.fetchone()
            return result[0] if result else None

    def get_all_passwords(self):
        """Возвращает все сохраненные пароли из PostgreSQL.

        Returns:
            list: Список кортежей (сервис, хэш_пароля)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT service, password_hash FROM passwords ORDER BY service')
            return cursor.fetchall()

    def delete_password(self, service):
        """Удаляет пароль для указанного сервиса из PostgreSQL.

        Args:
            service: Название сервиса

        Returns:
            bool: True если удалено, False если не найдено
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM passwords WHERE service = %s', (service,))
            conn.commit()
            return cursor.rowcount > 0  # количество затронутых строк
