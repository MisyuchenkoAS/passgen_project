import unittest
from unittest.mock import patch, MagicMock   # изолировать тестируемый код от внешних зависимостей
from io import StringIO                      # класс, который имитирует файл, но работает со строками в памяти
from passgen.commands import handle_generate, handle_find


class TestCommands(unittest.TestCase):
    """Тесты для модуля обработки команд."""

    def test_handle_generate_valid(self):
        """Тест обработки команды generate с правильными параметрами."""
        # Создаем mock-аргументы
        args = MagicMock()
        args.length = 12
        args.digits = True
        args.special = True
        args.uppercase = True
        args.service = "test_service"

        # Mock функции save_password чтобы не создавать реальные файлы
        with patch('passgen.commands.save_password') as mock_save:
            with patch('passgen.commands.generate_password') as mock_gen:
                mock_gen.return_value = "generated_password"    # при вызове ВСЕГДА возвращает "generated_password"

                # Перехватываем вывод
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:   # накапливает строки как файл
                    handle_generate(args)

                    # Проверяем вывод
                    output = mock_stdout.getvalue()  # получает ВСЕ что было "напечатано" в виде строки
                    self.assertIn("Сгенерированный пароль: generated_password", output) # проверяет что строка содержится в другой строке
                    self.assertIn("Пароль для сервиса 'test_service' сохранён", output)

                # Проверяем вызов функции сохранения
                mock_save.assert_called_once_with("test_service", "generated_password")

    def test_handle_generate_invalid_length(self):
        """Тест обработки команды generate с некорректной длиной."""
        args = MagicMock()
        args.length = 2

        # Перехватываем вывод
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:    # накапливает строки как файл
            handle_generate(args)

            output = mock_stdout.getvalue()      # получает ВСЕ что было "напечатано" в виде строки
            self.assertIn("Ошибка: Длина пароля должна быть не менее 4 символов", output) # проверяет что строка содержится в другой строке

    def test_handle_find_existing(self):
        """Тест обработки команды find для существующего сервиса."""
        args = MagicMock()
        args.service = "existing_service"

        with patch('passgen.commands.find_password') as mock_find:
            mock_find.return_value = "hashed_password_123"

            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_find(args)

                output = mock_stdout.getvalue()
                self.assertIn("Найден хэш пароля для сервиса 'existing_service'", output)
                self.assertIn("hashed_password_123", output)
                self.assertIn("ВНИМАНИЕ: Пароль хранится в хэшированном виде", output)

    def test_handle_find_non_existing(self):
        """Тест обработки команды find для несуществующего сервиса."""
        args = MagicMock()
        args.service = "non_existing_service"

        with patch('passgen.commands.find_password') as mock_find:
            mock_find.return_value = None

            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                handle_find(args)

                output = mock_stdout.getvalue()
                self.assertIn("Пароль для сервиса 'non_existing_service' не найден", output)


if __name__ == '__main__':
    unittest.main()
