import unittest
from passgen.utils import hash_password, validate_password_length


class TestUtils(unittest.TestCase):
    """Тесты для вспомогательных функций."""

    def test_hash_password(self):
        """Тест хэширования пароля."""
        password = "test_password"
        hashed = hash_password(password)

        self.assertIsInstance(hashed, str)     # Проверка типа данных
        self.assertEqual(len(hashed), 64)   # Хэш должен иметь длину 64 символа (SHA-256 в hex)
        self.assertEqual(hashed, hash_password(password))  # Один и тот же пароль должен давать одинаковый хэш
        self.assertNotEqual(hashed, hash_password("different_password"))  # Разные пароли должны давать разные хэши

    def test_validate_password_length_valid(self):
        """Тест проверки допустимой длины пароля."""
        # Не должно вызывать исключений
        validate_password_length(4)
        validate_password_length(12)
        validate_password_length(100)

    def test_validate_password_length_invalid(self):
        """Тест проверки недопустимой длины пароля."""
        with self.assertRaises(ValueError):
            validate_password_length(3)

        with self.assertRaises(ValueError):
            validate_password_length(0)

        with self.assertRaises(ValueError):
            validate_password_length(-5)


if __name__ == '__main__':
    unittest.main()
