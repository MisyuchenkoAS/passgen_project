"""Модуль генерации случайных паролей."""

import random
import string


def generate_password(length=12, use_digits=True, use_special_chars=True, use_uppercase=True):
    """Генерирует случайный пароль заданной длины и сложности.

    Args:
        length: Длина пароля (по умолчанию 12)
        use_digits: Включать цифры (по умолчанию True)
        use_special_chars: Включать спецсимволы (по умолчанию True)
        use_uppercase: Включать заглавные буквы (по умолчанию True)

    Returns:
        str: Сгенерированный пароль

    Raises:
        ValueError: Если невозможно сгенерировать пароль (пустой набор символов)
    """
    # Базовый набор символов (строчные буквы)
    characters = string.ascii_lowercase

    # Расширяем набор в зависимости от флагов
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    if use_uppercase:
        characters += string.ascii_uppercase

    # Проверяем, что есть хотя бы один символ для генерации
    if not characters:
        raise ValueError("Нельзя сгенерировать пароль без символов!")

    # Генерируем пароль
    password = ''.join(random.choice(characters) for _ in range(length))  # выбор случ. символа/объеденение
    return password
