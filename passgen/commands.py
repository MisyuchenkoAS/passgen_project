"""Модуль обработки команд для генератора паролей."""

from .generator import generate_password
from .storage import save_password, find_password
from .utils import validate_password_length


def handle_generate(args):
    """Обрабатывает команду генерации пароля из аргументов командной строки.

    Args:
        args: Объект с аргументами командной строки, содержащий:
            - length (int): Длина пароля
            - digits (bool): Включать цифры
            - special (bool): Включать спецсимволы
            - uppercase (bool): Включать заглавные буквы
            - service (str): Название сервиса для сохранения

    Raises:
        ValueError: Если длина пароля меньше минимально допустимой
    """
    try:
        validate_password_length(args.length)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return

    password = generate_password(
        length=args.length,
        use_digits=args.digits,
        use_special_chars=args.special,
        use_uppercase=args.uppercase
    )

    print(f"Сгенерированный пароль: {password}")

    # Если указан сервис, сохраняем пароль
    if args.service:
        save_password(args.service, password)
        print(f"Пароль для сервиса '{args.service}' сохранён (в хэшированном виде).")


def handle_find(args):
    """Обрабатывает команду поиска пароля по имени сервиса.

    Args:
        args: Объект с аргументами командной строки, содержащий:
            - service (str): Название сервиса для поиска

    Prints:
        Найденный хэш пароля или сообщение об ошибке
    """
    hashed_pw = find_password(args.service)
    if hashed_pw:
        print(f"Найден хэш пароля для сервиса '{args.service}': {hashed_pw}")
        print("ВНИМАНИЕ: Пароль хранится в хэшированном виде и не может быть восстановлен!")
    else:
        print(f"Пароль для сервиса '{args.service}' не найден.")


def interactive_mode():
    """Запускает интерактивный режим работы с генератором паролей.

    Предоставляет пользователю меню с выбором действий:
    - Создание нового пароля
    - Поиск сохраненного пароля
    - Просмотр документации
    - Выход из программы
    """
    print("Добро пожаловать в Генератор паролей!")
    print("=" * 40)

    while True:
        print("\nЧто вы хотите сделать?")
        print("1 - Создать новый пароль")
        print("2 - Найти сохранённый пароль")
        print("3 - Посмотреть документацию")
        print("4 - Выйти из программы")

        choice = input("\nВведите номер действия (1/2/3/4): ").strip()

        if choice == "1":
            create_password_interactive()
        elif choice == "2":
            find_password_interactive()
        elif choice == "3":
            show_documentation_interactive()
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def create_password_interactive():
    """Создает пароль в интерактивном режиме с запросом параметров у пользователя.

    Запрашивает у пользователя:
    - Длину пароля
    - Наличие цифр
    - Наличие спецсимволов
    - Наличие заглавных букв
    - Сохранение для сервиса
    """
    print("\n Создание нового пароля")
    print("-" * 30)

    # Длина пароля
    while True:
        try:
            length = input("Введите длину пароля (по умолчанию 12): ").strip()
            if not length:
                length = 12
                break
            length = int(length)
            validate_password_length(length)
            break
        except ValueError as e:
            print(f" {e}. Попробуйте снова.")

    # Цифры
    digits = input("Добавить цифры? (д/н, по умолчанию д): ").strip().lower()
    use_digits = digits != 'н'

    # Спецсимволы
    special = input("Добавить специальные символы? !@#$% (д/н, по умолчанию д): ").strip().lower()
    use_special = special != 'н'

    # Заглавные буквы
    uppercase = input("Добавить заглавные буквы? (д/н, по умолчанию д): ").strip().lower()
    use_uppercase = uppercase != 'н'

    # Генерация пароля
    print("\n Генерируем пароль...")
    password = generate_password(
        length=length,
        use_digits=use_digits,
        use_special_chars=use_special,
        use_uppercase=use_uppercase
    )

    print(f"✅ Ваш новый пароль: {password}")

    # Сохранение
    save = input("\nХотите сохранить этот пароль для сервиса? (д/н): ").strip().lower()
    if save == 'д':
        service = input("Для какого сервиса сохраняем пароль? (например: gmail, yandex): ").strip()
        if service:
            save_password(service, password)
            print(f"✅ Пароль для '{service}' сохранён (в хэшированном виде)")
        else:
            print("Название сервиса не может быть пустым")


def find_password_interactive():
    """Ищет пароль в интерактивном режиме по названию сервиса."""
    print("\n Поиск пароля")
    print("-" * 20)

    service = input("Для какого сервиса ищем пароль? ").strip()
    if not service:
        print("Название сервиса не может быть пустым")
        return

    hashed_pw = find_password(service)
    if hashed_pw:
        print(f"✅ Найден хэш пароля для '{service}': {hashed_pw}")
        print("ВНИМАНИЕ: Пароль хранится в хэшированном виде и не может быть восстановлен!")
    else:
        print(f"Пароль для сервиса '{service}' не найден")


def show_documentation_interactive():
    """Показывает документацию по модулям и функциям в интерактивном режиме."""
    print("\nДОКУМЕНТАЦИЯ ГЕНЕРАТОРА ПАРОЛЕЙ")
    print("=" * 50)

    # Документация из __init__.py (модуля в целом)
    print("\n О ПРОЕКТЕ PASSGEN:")
    print("-" * 25)
    try:
        import passgen
        if passgen.__doc__:
            print(passgen.__doc__)
        else:
            print("Документация модуля отсутствует")
    except ImportError:
        print("Не удалось загрузить документацию модуля")

    print("\n ФУНКЦИЯ generate_password:")
    print("-" * 30)
    from .generator import generate_password
    if generate_password.__doc__:
        print(generate_password.__doc__)
    else:
        print("Документация отсутствует")

    print("\n ФУНКЦИЯ save_password:")
    print("-" * 25)
    from .storage import save_password
    if save_password.__doc__:
        print(save_password.__doc__)
    else:
        print("Документация отсутствует")

    print("\n ФУНКЦИЯ find_password:")
    print("-" * 25)
    from .storage import find_password
    if find_password.__doc__:
        print(find_password.__doc__)
    else:
        print("Документация отсутствует")

    print("\n Примеры использования:")
    print("-" * 25)
    print("• generate_password(length=12) - пароль из 12 символов")
    print("• generate_password(length=8, use_digits=False) - без цифр")
    print("• save_password('gmail', 'пароль') - сохранить пароль")
    print("• find_password('gmail') - найти хэш пароля")

    input("\nНажмите Enter чтобы продолжить...")
