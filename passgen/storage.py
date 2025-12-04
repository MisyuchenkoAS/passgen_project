"""Модуль работы с хранилищем паролей."""

import json
import os     # файловая система
from .utils import hash_password

STORAGE_FILE = "passwords.json"


def save_password(service, password):
    """Сохраняет хэш пароля для указанного сервиса.

    Args:
        service (str): Название сервиса (например: 'gmail', 'yandex')
        password (str): Пароль в открытом виде
    """
    hashed_pw = hash_password(password)

    # Загружаем существующие пароли
    data = load_all_passwords()

    # Добавляем или обновляем запись
    data[service] = hashed_pw

    # Обратобка исключений для записи / Сохраняем обратно в файл
    try:
        with open(STORAGE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Ошибка записи в файл: {e}")


def load_all_passwords():
    """Загружает все сохранённые пароли из файла.

    Returns:
        dict: Словарь {сервис: хэш} или пустой словарь если файл не существует
    """
    if not os.path.exists(STORAGE_FILE):   # существует ли файл
        return {}

    try:
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Ошибка чтения файла: {e}")
        return {}


def find_password(service):
    """Находит хэш пароля для указанного сервиса.

    Args:
        service: Название сервиса

    Returns:
        str or None: Хэш пароля или None если не найден
    """
    data = load_all_passwords()  # загружаем все данные из файла
    return data.get(service)     # поиск по ключу