"""
Главный модуль для запуска генератора паролей.

Обрабатывает аргументы командной строки и запускает соответствующие команды.
"""

import argparse   # обработка аргументов командной строки
from passgen.commands import handle_generate, handle_find, handle_list, handle_delete, interactive_mode


def main():
    """Точка входа в программу - обработка аргументов командной строки."""

    parser = argparse.ArgumentParser(description="Генератор безопасных паролей")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Парсер для команды generate
    parser_generate = subparsers.add_parser("generate", help="Сгенерировать новый пароль")
    parser_generate.add_argument("-l", "--length", type=int, default=12,
                                 help="Длина пароля (по умолчанию: 12)")
    parser_generate.add_argument("-d", "--digits", action="store_true",
                                 help="Включать цифры")
    parser_generate.add_argument("-s", "--special", action="store_true",
                                 help="Включать спецсимволы")
    parser_generate.add_argument("-u", "--uppercase", action="store_true",
                                 help="Включать заглавные буквы")
    parser_generate.add_argument("--service", type=str,
                                 help="Название сервиса для сохранения пароля")

    # Парсер для команды find
    parser_find = subparsers.add_parser("find", help="Найти пароль по имени сервиса")
    parser_find.add_argument("service", type=str, help="Название сервиса")

    # Парсер для команды list (НОВАЯ КОМАНДА)
    subparsers.add_parser("list", help="Показать все сохраненные пароли")

    # Парсер для команды delete (НОВАЯ КОМАНДА)
    parser_delete = subparsers.add_parser("delete", help="Удалить пароль по имени сервиса")
    parser_delete.add_argument("service", type=str, help="Название сервиса")

    # Парсер для интерактивного режима
    subparsers.add_parser("interactive", help="Интерактивный режим (удобный)")

    args = parser.parse_args()

    # Вызов соответствующей функции в зависимости от команды
    if args.command == "generate":
        handle_generate(args)
    elif args.command == "find":
        handle_find(args)
    elif args.command == "list":
        handle_list(args)
    elif args.command == "delete":
        handle_delete(args)
    elif args.command == "interactive":
        interactive_mode()
    else:
        # Если не указана команда - запускаем интерактивный режим
        interactive_mode()


if __name__ == "__main__":
    main()




