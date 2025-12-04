"""Модуль работы с хранилищем паролей в базе данных."""

from .database_postgres import PasswordDB

# Создаем базу ОДИН РАЗ при запуске программы
db = PasswordDB()


def save_password(service, password):
    """Сохраняет хэш пароля для указанного сервиса в базу данных.

    Args:
        service (str): Название сервиса (например: 'gmail', 'yandex')
        password (str): Пароль в открытом виде
    """
    db.save_password(service, password)


def find_password(service):
    """Находит хэш пароля для указанного сервиса в базе данных.

    Args:
        service: Название сервиса

    Returns:
        str or None: Хэш пароля или None если не найден
    """
    return db.find_password(service)


def get_all_passwords():
    """Возвращает все сохраненные пароли.

    Returns:
        list: Список кортежей (сервис, хэш_пароля)
    """
    return db.get_all_passwords()


def delete_password(service):
    """Удаляет пароль для указанного сервиса.

    Args:
        service: Название сервиса

    Returns:
        bool: True если удалено, False если не найдено
    """
    return db.delete_password(service)
