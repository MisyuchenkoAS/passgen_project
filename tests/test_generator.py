import unittest
import string
from passgen.generator import generate_password


class TestGenerator(unittest.TestCase):   # Все тесты должны быть методами этого класса
    """Тесты для модуля генерации паролей."""

    def test_generate_password_default_length(self):
        """Тест генерации пароля со стандартной длиной."""
        password = generate_password()   # Вызываем функцию без параметров
        self.assertEqual(len(password), 12)

    def test_generate_password_custom_length(self):
        """Тест генерации пароля с пользовательской длиной."""
        password = generate_password(length=15)
        self.assertEqual(len(password), 15)

    def test_generate_password_only_lowercase(self):
        """Тест генерации пароля только из строчных букв."""
        password = generate_password(
            length=10,
            use_digits=False,
            use_special_chars=False,
            use_uppercase=False
        )
        for char in password:
            self.assertIn(char, string.ascii_lowercase)  # проверяет наличие строки в допустимом наборе

    def test_generate_password_with_digits(self):
        """Тест генерации пароля с цифрами."""
        password = generate_password(
            length=10,
            use_digits=True,
            use_special_chars=False,
            use_uppercase=False
        )
        has_digits = any(char in string.digits for char in password)    # возвращает True если хоть один символ цифрa
        self.assertTrue(has_digits, "Пароль должен содержать цифры")    # проверяет что условие истинно

    def test_generate_password_with_special_chars(self):
        """Тест генерации пароля со спецсимволами."""
        password = generate_password(
            length=10,
            use_digits=False,
            use_special_chars=True,
            use_uppercase=False
        )
        has_special = any(char in string.punctuation for char in password)
        self.assertTrue(has_special, "Пароль должен содержать спецсимволы")

    def test_generate_password_with_uppercase(self):
        """Тест генерации пароля с заглавными буквами."""
        password = generate_password(
            length=10,
            use_digits=False,
            use_special_chars=False,
            use_uppercase=True
        )
        has_uppercase = any(char in string.ascii_uppercase for char in password)
        self.assertTrue(has_uppercase, "Пароль должен содержать заглавные буквы")

    def test_generate_password_all_options(self):
        """Тест генерации пароля со всеми опциями."""
        password = generate_password(
            length=20,
            use_digits=True,
            use_special_chars=True,
            use_uppercase=True
        )
        self.assertEqual(len(password), 20)

        # Проверяем наличие разных типов символов
        has_lower = any(char in string.ascii_lowercase for char in password)
        has_upper = any(char in string.ascii_uppercase for char in password)
        has_digits = any(char in string.digits for char in password)
        has_special = any(char in string.punctuation for char in password)

        self.assertTrue(has_lower, "Должны быть строчные буквы")
        self.assertTrue(has_upper, "Должны быть заглавные буквы")
        self.assertTrue(has_digits, "Должны быть цифры")
        self.assertTrue(has_special, "Должны быть спецсимволы")


if __name__ == '__main__':
    unittest.main()    # запускаем все тесты в файле
