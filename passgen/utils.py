"""Модуль вспомогательных функций."""

import hashlib    # модуль для хэширования


def hash_password(password):
    """Создает SHA-256 хэш пароля.

       Args:
           password: Пароль в открытом виде

       Returns:
           str: Хэш пароля в hex-формате
       """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_password_length(length):
    """Проверяет минимальную длину пароля.

        Args:
            length: Длина пароля для проверки

        Raises:
            ValueError: Если длина меньше 4 символов
        """
    if length < 4:
        raise ValueError("Длина пароля должна быть не менее 4 символов")