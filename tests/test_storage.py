import unittest
import os
import json
from passgen.storage import save_password, load_all_passwords, find_password
from passgen.utils import hash_password


class TestStorage(unittest.TestCase):
    """Тесты для модуля работы с хранилищем."""

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.test_file = "test_passwords.json"
        # Временно подменяем файл хранилища на тестовый
        import passgen.storage
        self.original_file = passgen.storage.STORAGE_FILE    # Сохраняем оригинальное имя
        passgen.storage.STORAGE_FILE = self.test_file        # Подменяем на тестовое

        # Удаляем тестовый файл, если он существует
        if os.path.exists(self.test_file):     # проверяет существование файла
            os.remove(self.test_file)

    def tearDown(self):
        """Очистка после каждого теста."""
        import passgen.storage
        # Восстанавливаем оригинальный файл
        passgen.storage.STORAGE_FILE = self.original_file

        # Удаляем тестовый файл
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_password_new_service(self):
        """Тест сохранения пароля для нового сервиса."""
        save_password("test_service", "test_password")

        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(self.test_file))

        # Проверяем содержимое файла
        with open(self.test_file, 'r') as f:
            data = json.load(f)    # читает данные из файла в формате JSON и преобразует их в словарь

        expected_hash = hash_password("test_password")
        self.assertEqual(data["test_service"], expected_hash)

    def test_save_password_existing_service(self):
        """Тест обновления пароля для существующего сервиса."""
        # Сохраняем первый пароль
        save_password("test_service", "password1")
        first_hash = hash_password("password1")

        # Сохраняем второй пароль для того же сервиса
        save_password("test_service", "password2")
        second_hash = hash_password("password2")

        # Читаем данные из файла
        with open(self.test_file, 'r') as f:
            data = json.load(f)

        # Должен быть сохранен второй пароль
        self.assertEqual(data["test_service"], second_hash)
        self.assertNotEqual(data["test_service"], first_hash)

    def test_load_all_passwords_empty(self):
        """Тест загрузки паролей из несуществующего файла."""
        data = load_all_passwords()
        self.assertEqual(data, {})

    def test_load_all_passwords_with_data(self):
        """Тест загрузки паролей из существующего файла."""
        # Создаем тестовые данные
        test_data = {
            "service1": hash_password("pass1"),
            "service2": hash_password("pass2")
        }

        with open(self.test_file, 'w') as f:
            json.dump(test_data, f)

        # Загружаем данные
        loaded_data = load_all_passwords()

        self.assertEqual(loaded_data, test_data)

    def test_find_password_existing(self):
        """Тест поиска существующего пароля."""
        test_data = {
            "gmail": hash_password("gmail_pass"),
            "yandex": hash_password("yandex_pass")
        }

        with open(self.test_file, 'w') as f:
            json.dump(test_data, f)

        found_hash = find_password("gmail")
        self.assertEqual(found_hash, hash_password("gmail_pass"))

    def test_find_password_non_existing(self):
        """Тест поиска несуществующего пароля."""
        test_data = {"gmail": hash_password("gmail_pass")}

        with open(self.test_file, 'w') as f:
            json.dump(test_data, f)

        found_hash = find_password("non_existing")
        self.assertIsNone(found_hash)


if __name__ == '__main__':
    unittest.main()
