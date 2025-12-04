import unittest
from unittest.mock import patch, MagicMock
from passgen.storage import save_password, find_password, get_all_passwords, delete_password


class TestStorage(unittest.TestCase):
    """Тесты для модуля работы с хранилищем (PostgreSQL версия)."""

    def setUp(self):
        """Подготовка перед каждым тестом."""
        # Создаем заглушку для объекта БД (имитация без реальной БД)
        self.db_mock = MagicMock()

        # Временно заменяем реальную БД на заглушку в модуле storage
        self.db_patcher = patch("passgen.storage.db", self.db_mock)
        self.db_patcher.start()  # включаем замену

    def tearDown(self):
        """Очистка после каждого теста."""
        self.db_patcher.stop()  # отключаем замену, возвращаем оригинал

    def test_save_password_new_service(self):
        """Тест сохранения пароля для нового сервиса."""
        save_password("test_service", "test_password")

        # Проверяем что метод save_password БД вызван с правильными аргументами
        self.db_mock.save_password.assert_called_once_with("test_service", "test_password")

    def test_save_password_existing_service(self):
        """Тест обновления пароля для существующего сервиса."""
        save_password("test_service", "password1")
        save_password("test_service", "password2")

        # Должно быть два вызова
        self.assertEqual(self.db_mock.save_password.call_count, 2)

    def test_find_password_existing(self):
        """Тест поиска существующего пароля."""
        # Настраиваем заглушку возвращать тестовый хэш
        self.db_mock.find_password.return_value = "hashed_password_123"

        result = find_password("test_service")

        self.assertEqual(result, "hashed_password_123")  # проверяем результат
        self.db_mock.find_password.assert_called_once_with("test_service")  # проверяем вызов

    def test_find_password_non_existing(self):
        """Тест поиска несуществующего пароля."""
        # Настраиваем заглушку возвращать None
        self.db_mock.find_password.return_value = None

        result = find_password("non_existing")

        self.assertIsNone(result)  # должен быть None
        self.db_mock.find_password.assert_called_once_with("non_existing")

    def test_get_all_passwords(self):
        """Тест получения всех паролей."""
        # Тестовые данные
        expected_data = [("gmail", "hash1"), ("yandex", "hash2")]
        self.db_mock.get_all_passwords.return_value = expected_data

        result = get_all_passwords()

        self.assertEqual(result, expected_data)  # проверяем совпадение данных
        self.db_mock.get_all_passwords.assert_called_once()  # проверяем вызов

    def test_delete_password_existing(self):
        """Тест удаления существующего пароля."""
        # Настраиваем заглушку возвращать True (успешное удаление)
        self.db_mock.delete_password.return_value = True

        result = delete_password("test_service")

        self.assertTrue(result)  # должен быть True
        self.db_mock.delete_password.assert_called_once_with("test_service")

    def test_delete_password_non_existing(self):
        """Тест удаления несуществующего пароля."""
        # Настраиваем заглушку возвращать False (не найдено)
        self.db_mock.delete_password.return_value = False

        result = delete_password("non_existing")

        self.assertFalse(result)  # должен быть False
        self.db_mock.delete_password.assert_called_once_with("non_existing")


if __name__ == '__main__':
    unittest.main()